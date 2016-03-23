# coding: utf-8

import datetime

from django.core.cache import cache

from feed.models import (
    FeedResult,
    Feed,
    Feed2,
)
from feed.documents import (
    FeedParser,
)

from transaction.models import UserChargePackage

from pin_utils.django_utils import (
    get_oid,
    get_today,
    get_tomommow,
)

from app.task_system.task_finished_judge import (
    resume_read_finished,
    continue_read_resume,
)


class FeedUtils(object):

    @classmethod
    @resume_read_finished
    @continue_read_resume
    def read_feed(cls, request, feed_sid, resume_id, read_user=None):
        feed_oid = get_oid(feed_sid)
        resume_oid = get_oid(resume_id)
        if read_user is None:
            read_user = request.GET.get('user', '')

        if not feed_oid or not resume_oid or read_user not in ('admin', 'user'):
            return False

        upload_read_meta = {
            'admin': {'set__admin_read_status': 'read'},
            'user': {'set__user_read_status': 'read', 'inc__click_count': 1, 'set__user_read_time': datetime.datetime.now()},
        }

        FeedResult.objects(
            feed=feed_oid,
            resume=resume_oid,
            user_read_status='read'
        ).update(
            inc__click_count=1
        )
        FeedResult.objects(
            feed=feed_oid,
            resume=resume_oid,
            user_read_status='unread',
        ).update(
            **upload_read_meta[read_user]
        )
        return True

    @classmethod
    def has_use_feed(cls, user):
        has_feed = Feed.objects.filter(
            user=user,
            feed_type=1,
        )
        return True if has_feed else False

    @classmethod
    def is_user_feed(cls, user, feed_id):
        feed_oid = get_oid(feed_id)
        if not feed_oid:
            return False

        feed = Feed.objects.filter(
            user=user,
            feed_obj_id=feed_oid,
        ).first()
        return feed

    @classmethod
    def is_send_resume(cls, user, resume_id):
        username = user.username
        resume_oid = get_oid(resume_id)
        feed_id_list = [
            i.id
            for i in list(
                Feed2.objects.filter(
                    deleted=False,
                    username=username,
                ).only(
                    'id',
                    'username'
                )
            )
        ]
        has_send = FeedResult.objects.filter(
            feed__in=feed_id_list,
            resume=resume_oid,
            feed_source='brick',
        )
        return True if has_send else False

    @classmethod
    def get_feed_result(cls, feed_id, resume_id):
        feed_oid = get_oid(feed_id)
        resume_oid = get_oid(resume_id)
        if not feed_oid or not resume_oid:
            return False
        feed_result = FeedResult.objects.filter(
            feed=feed_oid,
            resume=resume_oid,
        ).first()
        return feed_result

    @classmethod
    def add_feed_result(cls, feed_id, resume_id, source='pinbot', admin=''):
        now = datetime.datetime.now()
        feed_oid = get_oid(feed_id)
        resume_oid = get_oid(resume_id)

        if not feed_oid or not resume_oid:
            return False

        feed_result = FeedResult.objects.filter(
            feed=feed_oid,
            resume=resume_oid,
        ).first()

        if feed_result:
            feed_result.published = True
            feed_result.is_recommended = True
            feed_result.display_time = now
            feed_result.feed_source = source
            feed_result.pub_time = now
            feed_result.score['cls_score'] = 100
            if feed_result.resume_source:
                feed_result.resume_source = 'accept' + feed_result.resume_source
            if admin:
                feed_result.admin = admin
            feed_result.save()
            return feed_result

        feed_result = FeedResult(
            feed=feed_oid,
            resume=resume_oid,
            is_recommended=True,
            published=True,
            display_time=now,
            pub_time=now,
            admin=admin,
            feed_source=source,
        )
        feed_result.score['cls_score'] = 100
        feed_result.save()
        return feed_result

    @classmethod
    def feed_result_watch(cls, resume_id, feed_id, watch_type):
        feed_result = cls.get_feed_result(feed_id, resume_id)
        if not feed_result:
            return False
        feed_result.watch = True if watch_type else False
        feed_result.save()
        return feed_result

    @classmethod
    def feed_result_download(cls, resume_id, feed_id):
        feed_result = cls.get_feed_result(feed_id, resume_id)
        if not feed_result:
            return False
        feed_result.download = True
        feed_result.save()
        return feed_result


class FeedCacheUtils(object):
    update_cache_key = 'SPECIAL_FEED_UPDATE_FEED_ID_LIST'

    @classmethod
    def add_feed_id_update_cache(cls, feed_sid):
        feed_id = str(feed_sid)
        update_cache_value = cache.get(cls.update_cache_key) or []

        if feed_id not in update_cache_value:
            update_cache_value.append(feed_id)
            cache.set(cls.update_cache_key, update_cache_value, timeout=0)
        return True

    @classmethod
    def get_today_cache(cls, feed_id):
        feed_sid = str(feed_id)
        today_cache_key = feed_sid + '_today_cache'
        today_cache_value = cache.get(today_cache_key, [])
        return today_cache_value

    @classmethod
    def get_today_expire_sec(cls):
        now = datetime.datetime.now()
        tomorrow = get_tomommow()
        expire_time = tomorrow - now
        expire_sec = expire_time.total_seconds()
        return expire_sec

    @classmethod
    def set_cache_expire(cls, feed_id):
        feed_sid = str(feed_id)
        today_click_key = feed_sid + '_today_click'
        today_click_value = cache.get(today_click_key)

        if not today_click_value:
            today_expire_sec = cls.get_today_expire_sec()
            today_cache_key = feed_sid + '_today_cache'
            today_cache_value = cache.get(today_cache_key, [])
            cache.set(today_cache_key, today_cache_value, today_expire_sec)
            cache.set(today_click_key, 1, today_expire_sec)
        return True

    @classmethod
    def update_today_cache(cls):
        update_feed_id_list = cache.get(cls.update_cache_key, [])
        today = get_today()
        tomorrow = get_tomommow()

        has_update_feed_list = []

        for feed_id in update_feed_id_list:
            feed_oid = get_oid(feed_id)
            today_cache_key = feed_id + '_today_cache'
            today_cache_value = cache.get(today_cache_key, [])

            feed_results = FeedResult.objects(
                feed=feed_oid,
                display_time__gte=today,
                display_time__lt=tomorrow,
            )
            resume_ids = [str(fr.resume.id) for fr in feed_results]
            if resume_ids:
                today_cache_value = list(
                    set(today_cache_value) | set(resume_ids)
                )
                cache.set(today_cache_key, today_cache_value, timeout=0)
                has_update_feed_list.append(feed_id)

        not_update_feed_list = list(
            set(update_feed_id_list) - set(has_update_feed_list)
        )
        cache.set(cls.update_cache_key, not_update_feed_list, timeout=0)


class CheckFeedExpire(object):

    def feed_has_expire(self, feed):
        now_time = datetime.datetime.now()
        return True if feed.expire_time and feed.expire_time < now_time else False

    def feed_expire_status(self, feed):
        today = get_tomommow()
        return True if (feed.feed_expire_time and feed.feed_expire_time < today and not self.feed_has_expire(feed)) else False


class CheckRestFeed(object):

    def has_rest_feed(self):
        user = self.request.user
        now = datetime.datetime.now()
        # 所有有效订阅量
        user_charges_pkgs = UserChargePackage.objects.filter(
            user=user,
            feed_end_time__gte=now,
            pay_status='finished',
            pkg_source=1,
        )

        # 计算总共有的有效订阅数量
        total_valid_feed_num = 0
        for user_charges_pkg in user_charges_pkgs:
            total_valid_feed_num += user_charges_pkg.extra_feed_num

        # 计算用户实际已经使用的数量
        user_feed_count = Feed2.objects.filter(
            username=user.username,
            deleted=False,
            expire_time__gte=now,
            feed_type=1,
        ).count()
        return total_valid_feed_num - user_feed_count > 0


class FeedParserUtils(object):

    @classmethod
    def add_field_value(cls, fields_dict, change_fields, default_value):
        for field in change_fields:
            value = fields_dict.get(field, 0)
            if value > 0:
                fields_dict[field] += default_value
            else:
                fields_dict[field] = default_value
        return fields_dict

    @classmethod
    def get_fields_dict(cls, fields_dict, extend_fields, block_fields):
        extend_fields = [i.strip().replace('.', '').replace('$', '') for i in extend_fields if i.strip()]
        block_fields = [i.strip().replace('.', '').replace('$', '') for i in block_fields if i.strip()]

        origin_extend_fields = [k for k, v in fields_dict.items() if v > 0]
        origin_block_fields = [k for k, v in fields_dict.items() if v < 0]
        fields_has_change = (
            set(extend_fields) != set(origin_extend_fields)
            or set(block_fields) != set(origin_block_fields)
        )
        if not fields_has_change:
            return fields_dict

        fields_dict = cls.add_field_value(fields_dict, extend_fields, 1)
        fields_dict = cls.add_field_value(fields_dict, block_fields, -1)
        return fields_dict

    @classmethod
    def save_feed_parser(
            cls,
            feed_id,
            extend_keywords,
            block_keywords,
            extend_titles,
            block_titles):

        feed_oid = get_oid(feed_id)
        if not feed_oid:
            return False

        for i in (extend_keywords, block_keywords, extend_titles, block_titles):
            if not isinstance(i, list):
                return False

        feed_parser = FeedParser.objects.filter(id=feed_oid).first()
        parser_keywords = feed_parser.extend_keywords if feed_parser else {}
        parser_titles = feed_parser.extend_titles if feed_parser else {}

        extend_keywords_dict = cls.get_fields_dict(
            parser_keywords,
            extend_keywords,
            block_keywords,
        )
        extend_titles_dict = cls.get_fields_dict(
            parser_titles,
            extend_titles,
            block_titles,
        )

        if feed_parser:
            feed_parser.extend_keywords = extend_keywords_dict
            feed_parser.extend_titles = extend_titles_dict
        else:
            feed_parser = FeedParser(
                id=feed_oid,
                extend_keywords=extend_keywords_dict,
                extend_titles=extend_titles_dict,
            )

        feed_parser.save()
        return feed_parser
