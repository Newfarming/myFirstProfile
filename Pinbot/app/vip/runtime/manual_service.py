# coding: utf-8

import datetime

from django.db import transaction
from pin_utils.django_utils import (
    get_object_or_none,
    get_oid
)
from app.vip.models import (
    UserManualService,
)
from pin_utils.django_utils import (
    get_after_month
)
from app.vip.runtime.service import (
    BaseService
)
from app.vip.runtime.self_service import (
    SelfService,
    SelfServiceUtils,
)
from feed.models import (
    Feed,
    Feed2,
    UserFeed,
    UserFeed2
)
from transaction.models import (
    UserChargePackage
)


class ManualService(BaseService):

    service_name = 'self_service'

    def __init__(self, **data):
        super(ManualService, self).__init__(**data)

    def process(self, **data):
        return self.do_str_to_fun()

    @transaction.atomic
    def create_service(self, **kwargs):
        # 添加人工服务
        manual_service = self.add_service_record(
            user=self.user,
            item=self.product,
            is_insurance=self.is_insurance
        )
        if not manual_service:
            return False

        # 添加自助服务
        self_service = SelfService()
        self_service.add_user_vip_record(
            user=self.user,
            with_manual=True
        )

        self.service_id = manual_service.id
        self.change_service_status(
            status='applying'
        )

        return manual_service

    @transaction.atomic
    def active_service(self, service_id=None, user=None):
        now = datetime.datetime.now()
        if service_id and user:
            service_id = service_id
            user = user
        else:
            service_id = self.service_id
            user = self.user

        manual_service = get_object_or_none(UserManualService, id=service_id)

        expire_time = get_after_month(
            months=manual_service.item.service_month
        )

        manual_service.is_active = True
        manual_service.status = 'success'
        manual_service.active_time = now
        manual_service.expire_time = expire_time
        manual_service.save()

        user_vip = SelfServiceUtils.set_experience_user(self.user)
        user_vip.custom_feed = 5
        user_vip.custom_point = 200
        user_vip.active_time = now
        user_vip.expire_time = expire_time
        user_vip.save()

        self_srv = SelfService()
        self_srv.update_vip_pkg(user_vip)
        self_srv.update_vip_point(user_vip)

        return True

    def deactive_self_service(self):
        has_active_services = UserManualService.objects.filter(
            user=self.user,
            is_active=True,
            expire_time__gt=datetime.datetime.now(),
        ).exists()

        if not has_active_services:
            SelfServiceUtils.set_experience_user(self.user)

        return None

    def deactive_manual_service(self, status):
        manual_service = get_object_or_none(UserManualService, id=self.service_id)
        manual_service.is_active = False
        manual_service.status = status
        manual_service.save()
        self.user = manual_service.user
        return True

    def invalid_service(self, status=None):
        if status:
            service_status = status
        else:
            service_status = 'refunded'

        self.deactive_manual_service(
            status=service_status
        )

        # 失效自助服务
        user_vip = self.deactive_self_service()

        if user_vip:
            # 失效定制服务
            self.deactive_feed(
                user_vip=user_vip
            )

        return True

    def deactive_feed(self, user_vip):
        now = datetime.datetime.now()
        user_charge_pack = get_object_or_none(
            UserChargePackage,
            user=user_vip.user,
            package_type=2,
            feed_package__name='会员定制',
            pkg_source=1,
        )

        user_charge_pack.extra_feed_num = user_vip.item.feed_count
        user_charge_pack.rest_feed = user_vip.item.feed_count
        user_charge_pack.save()

        user_feeds = UserFeed.objects.select_related('feed').filter(
            user_charge_pkg=user_charge_pack,
            is_deleted=False
        )
        feed_ids = [user_feed.feed.id for user_feed in user_feeds]
        feed_obj_ids = [get_oid(user_feed.feed.feed_obj_id) for user_feed in user_feeds]
        user_feeds.update(
            expire_time=now
        )
        Feed.objects.filter(
            id__in=feed_ids
        ).update(
            expire_time=now
        )

        Feed2.objects.filter(
            id__in=feed_obj_ids
        ).update(
            set__expire_time=now
        )

        UserFeed2.objects.filter(
            feed__in=feed_obj_ids
        ).update(
            set__expire_time=now
        )
        return True

    def has_active_service(self, user):
        now = datetime.datetime.now()
        has_active_service = UserManualService.objects.filter(
            user=user,
            is_active=True,
            expire_time__gt=now,
        ).exists()

        return has_active_service

    def get_service_list(self, user, status):
        search_dict = {}
        search_dict['user'] = user

        if status:
            search_dict['status'] = status

        manual_service_list = UserManualService.objects.filter(
            **search_dict
        )
        return manual_service_list

    def add_service_record(self, user, item, is_insurance):
        ums = UserManualService(
            user=user,
            item=item,
            is_insurance=is_insurance,
            order_price=self.order_price
        )
        ums.save()
        return ums

    def refund_service(self):
        if self.get_service_status() != 'success':
            return False

        return self.change_service_status(
            status='refund'
        )

    def cancel_refund_service(self):
        if self.get_service_status() != 'refund':
            return False

        return self.change_service_status(
            status='success'
        )

    def delete_service(self):
        pass

    def close_service(self):
        return self.change_service_status(
            status='closed'
        )

    def cancel_service(self):
        if self.get_service_status() != 'applying':
            return False

        return self.change_service_status(
            status='canceled'
        )

    def finish_service(self):
        return self.invalid_service(
            status='finished'
        )

    def get_service_info(self, service_id):
        return get_object_or_none(UserManualService, id=service_id)
