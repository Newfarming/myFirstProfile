# coding: utf-8

import datetime

from pin_tools.dash.builder import (
    DataBuilder
)
from pin_utils.django_utils import (
    get_today
)


class FeedDataDriver(object):

    def __init__(self, **kwargs):

        start_query_time = kwargs.get('start_query_time', get_today() - datetime.timedelta(days=1))
        end_query_time = kwargs.get('end_query_time', get_today())
        ret_list = [
            'feeds',
            'users',
            'members',
            'self_members',
            'all_data_self_members',
            'manual_service_members',
            'all_data_manual_service_members',
            'user_access_log'
        ]
        self.db_builder = DataBuilder(
            start_query_time,
            end_query_time,
            ret_list=ret_list
        )
        self.db_builder.build_data()
        self.origin_data = self.db_builder.origin_data

    def get_lively_feed_count(self):
        ret = self.origin_data.get('feeds').filter(
            deleted=False,
            feed_expire_time__gt=datetime.datetime.now(),
            feed_type=1
        )
        return ret.count()

    def get_new_feed(self):
        return self.origin_data.get('feeds').filter(
            add_time__gte=get_today() - datetime.timedelta(days=1),
            add_time__lt=datetime.datetime.now()
        ).count()

    def get_lively_feed_user_count(self):
        user_log = self.origin_data.get('user_access_log')

        user_list = user_log.filter(
            access_url='/special_feed/page/',
        ).distinct('user_name')

        return len(user_list)

    def get_lively_feed_member_count(self):

        self_member_list = self.origin_data.get('all_data_self_members')
        manual_service_member_list = self.origin_data.get('all_data_manual_service_members')

        member_list = []
        member_list.extend(self_member_list.values_list('user__username', flat=True))
        member_list.extend(manual_service_member_list.values_list('user__username', flat=True))

        user_log = self.origin_data.get('user_access_log')

        user_list = user_log.filter(
            access_url__contains='/special_feed/feed_list/',
        ).distinct('user_name')

        return len([val for val in user_list if val in member_list])
