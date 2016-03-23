# coding: utf-8

import datetime

from django.db.models import Sum

from pinbot_package.models import (
    ResumePackge,
    FeedService,
)
from transaction.models import (
    UserChargePackage,
)
from feed.models import (
    UserFeed,
    UserFeed2,
    Feed2,
    Feed,
)

from django_utils import (
    get_object_or_none,
    get_oid,
    get_today,
)


class PackageUtils(object):

    @classmethod
    def has_package(cls, user, package_name):
        has_pkg = UserChargePackage.objects.filter(
            package_type=1,
            user=user,
            resume_package__name=package_name,
        )
        return has_pkg[0] if has_pkg else False

    @classmethod
    def has_base_pkg(cls, user):
        now = datetime.datetime.now()
        has_base_pkg = UserChargePackage.objects.filter(
            user=user,
            package_type=1,
            resume_end_time__gt=now,
            pay_status='finished',
        )
        return has_base_pkg[0] if has_base_pkg else False

    @classmethod
    def has_pkg(cls, user):
        has_pkg_query = UserChargePackage.objects.filter(
            user=user,
            pay_status='finished',
        )
        return has_pkg_query[0] if has_pkg_query else False

    @classmethod
    def add_package(cls, user, package_name):
        package = get_object_or_none(
            ResumePackge,
            name=package_name
        )
        now = datetime.datetime.now()
        resume_end_time = now + datetime.timedelta(days=package.valid_days)
        feed_end_time = now + datetime.timedelta(days=package.feed_service.valid_days)

        user_pkg = UserChargePackage(
            user=user,
            package_type=1,
            resume_package=package,
            extra_feed_num=package.feed_service_num,
            start_time=now,
            resume_end_time=resume_end_time,
            actual_cost=0,
            rest_feed=package.feed_service_num,
            rest_points=package.total_points,
            feed_end_time=feed_end_time,
            pay_status='finished',
        )
        user_pkg.save()
        return user_pkg

    @classmethod
    def add_feed(cls, user, feed_name, pay_status='finished'):
        feed = get_object_or_none(
            FeedService,
            name=feed_name,
        )
        now = datetime.datetime.now()
        feed_end_time = now + datetime.timedelta(days=feed.valid_days)
        feed_package = UserChargePackage(
            user=user,
            package_type=2,
            feed_package=feed,
            actual_cost=feed.price,
            rest_feed=feed.feed_num,
            extra_feed_num=feed.feed_num,
            feed_end_time=feed_end_time,
            pay_status=pay_status,
        )
        feed_package.save()
        return feed_package

    @classmethod
    def get_vip_feed_pkg(cls, user):
        feed_name = '会员定制'
        has_pkg = UserChargePackage.objects.filter(
            package_type=2,
            user=user,
            feed_package__name=feed_name,
        )
        if not has_pkg:
            feed = cls.add_feed(user, feed_name, pay_status='Start')
        else:
            feed = has_pkg[0]
        return feed

    @classmethod
    def add_partner_feed(cls, user, feed_name):
        now = datetime.datetime.now()
        feed_package = get_object_or_none(
            UserChargePackage,
            user=user,
            feed_package__name=feed_name,
            feed_end_time__gt=now,
        )
        if feed_package:
            return False

        feed_package = cls.add_feed(user, feed_name)
        return feed_package

    @classmethod
    def make_mongo_feed_expire(cls, feed, expire_time):
        feed_oid = get_oid(feed.feed_obj_id)
        mongo_feed = Feed2.objects(id=feed_oid).first()
        mongo_feed.expire_time = expire_time
        UserFeed2.objects.filter(
            feed=mongo_feed,
        ).update(
            set__expire_time=expire_time
        )
        mongo_feed.save()
        return True

    @classmethod
    def make_partner_feed_expire(cls, user, package_name):
        expire_time = datetime.datetime.now()
        user_pkg = UserChargePackage.objects.select_related(
            'userfeed',
        ).filter(
            user=user,
            feed_package__name=package_name,
            feed_end_time__gt=expire_time,
        )
        if not user_pkg:
            return False

        pkg = user_pkg[0]
        pkg.feed_end_time = expire_time

        user_feed = get_object_or_none(
            UserFeed,
            user_charge_pkg=user_pkg
        )

        if user_feed:
            user_feed.expire_time = expire_time
            feed = user_feed.feed
            feed.expire_time = expire_time
            cls.make_mongo_feed_expire(feed, expire_time)
            feed.save()
            user_feed.save()

        pkg.save()
        return True

    @classmethod
    def rest_feed_count(cls, user):
        now = datetime.datetime.now()
        user_feeds = UserChargePackage.objects.filter(
            user=user,
            pay_status='finished',
            rest_feed__gt=0,
            feed_end_time__gt=now,
            pkg_source=1,
        ).aggregate(Sum('rest_feed'))
        return user_feeds.get('rest_feed__sum', 0) or 0

    @classmethod
    def set_package_expire_time(cls, user, expire_time):
        '''
        更新user_vip的定制套餐过期时间
        需要更新
           UserChargePackage
           Feed
           Feed2
           UserFeed
           UserFeed2
        '''
        user_charge_pack = get_object_or_none(
            UserChargePackage,
            user=user,
            package_type=2,
            feed_package__name='会员定制',
            pkg_source=1,
        )

        if not user_charge_pack:
            return False

        user_charge_pack.feed_end_time = expire_time
        user_charge_pack.save()

        user_feeds = UserFeed.objects.select_related('feed').filter(
            user_charge_pkg=user_charge_pack,
            is_deleted=False
        )
        feed_ids = [user_feed.feed.id for user_feed in user_feeds]
        feed_obj_ids = [get_oid(user_feed.feed.feed_obj_id) for user_feed in user_feeds]
        user_feeds.update(
            expire_time=expire_time
        )
        Feed.objects.filter(
            id__in=feed_ids
        ).update(
            expire_time=expire_time
        )

        Feed2.objects.filter(
            id__in=feed_obj_ids
        ).update(
            set__expire_time=expire_time
        )

        UserFeed2.objects.filter(
            feed__in=feed_obj_ids
        ).update(
            set__expire_time=expire_time
        )
        return True

    @classmethod
    def update_uservip_package(cls, user_vip):
        user = user_vip.user
        expire_time = user_vip.expire_time
        result = cls.set_package_expire_time(user, expire_time)
        return result

    @classmethod
    def expire_uservip_package(cls, user):
        expire_time = get_today()
        result = cls.set_package_expire_time(user, expire_time)
        return result

    @classmethod
    def set_uservip_pkg_feed(cls, user_vip):
        user = user_vip.user
        feed_count = user_vip.vip_role.feed_count

        user_charge_pack = get_object_or_none(
            UserChargePackage,
            user=user,
            package_type=2,
            feed_package__name='会员定制',
            pkg_source=1,
        )

        if not user_charge_pack:
            return None

        expire_time = user_vip.expire_time
        user_charge_pack.feed_end_time = expire_time
        user_charge_pack.rest_feed = feed_count
        user_charge_pack.extra_feed_num = feed_count
        user_charge_pack.save()

        return user_charge_pack
