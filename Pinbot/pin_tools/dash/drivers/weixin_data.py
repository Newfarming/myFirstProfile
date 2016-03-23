# coding: utf-8

import datetime
import re

from pin_tools.dash.builder import (
    DataBuilder
)
from pin_utils.django_utils import (
    get_today
)


class WeixinDataDriver(object):

    def __init__(self, **kwargs):

        start_query_time = kwargs.get('start_query_time', get_today() - datetime.timedelta(days=1))
        end_query_time = kwargs.get('end_query_time', get_today())

        ret_list = [
            'users',
            'weixin_users',
            'weixin_msgs',
            'all_data_self_members',
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

    def get_new_bind_weixin_user_count(self):
        return self.origin_data.get('weixin_users').filter(
            user__date_joined__lte=get_today() - datetime.timedelta(days=1)
        ).count()

    def get_new_reg_weixin_user_count(self):
        return self.origin_data.get('weixin_users').filter(
            user__date_joined__gte=get_today() - datetime.timedelta(days=1)
        ).count()

    def get_all_new_bind_weixin_user_count(self):
        return self.origin_data.get('weixin_users').count()

    def get_lively_member_count(self):
        user_log_list = self.origin_data.get('user_access_log').filter(
            user_agent__contains='MicroMessenger',
        ).distinct('user_name')

        self_member_list = self.origin_data.get('all_data_self_members')
        manual_service_member_list = self.origin_data.get('all_data_manual_service_members')
        member_list = []
        member_list.extend(self_member_list.values_list('user__username', flat=True))
        member_list.extend(manual_service_member_list.values_list('user__username', flat=True))
        member_list = set(member_list)

        return len([val for val in user_log_list if val in member_list])

    def get_lively_user_count(self):
        user_log_list = self.origin_data.get('user_access_log').filter(
            user_agent__contains='MicroMessenger',
        ).distinct('user_name')
        return len(user_log_list)

    def get_send_msg_count(self):
        return self.origin_data.get('weixin_msgs').count()

    def get_click_msg_count(self):

        user_access_urls = self.origin_data.get('user_access_log').filter(
            access_url__contains='/feed_list/'
        ).values_list('access_url')
        user_access_feed_ids = [re.findall(r'/feed_list/(\w*)', url)[0] for url in user_access_urls]

        send_msg_log_urls = self.origin_data.get('weixin_msgs').values_list('url', flat=True)
        msg_feed_ids = [re.findall(r'/list/(\w*)', url)[0] for url in send_msg_log_urls]

        return len([val for val in msg_feed_ids if val in user_access_feed_ids])

    def get_submit_feed_count(self):
        user_log_list = self.origin_data.get('user_access_log').filter(
            user_agent__contains='MicroMessenger',
            access_url__contains='/submit_feed/'
        )
        return len(user_log_list)

    def get_add_watch_count(self):
        user_log_list = self.origin_data.get('user_access_log').filter(
            user_agent__contains='MicroMessenger',
            access_url__contains='/add_watch/'
        )
        return len(user_log_list)
