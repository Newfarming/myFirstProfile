# coding: utf-8

import datetime

from pin_tools.dash.builder import (
    DataBuilder
)
from pin_utils.django_utils import (
    get_today
)


class UserDataDriver(object):

    def __init__(self, **kwargs):

        start_query_time = kwargs.get('start_query_time', get_today() - datetime.timedelta(days=1))
        end_query_time = kwargs.get('end_query_time', get_today())
        ret_list = [
            'users',
            'all_data_users',
            'first_data_users',
            'experience_users',
            'all_data_experience_users',
            'members',
            'all_data_members',
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

    def get_new_register_user_count(self):
        return self.origin_data.get('users').count()

    def get_new_experience_user_count(self):
        return self.origin_data.get('experience_users').count()

    def get_new_member_user_count(self):
        return len(self.origin_data.get('members'))

    def get_new_self_member_user_count(self):
        return self.origin_data.get('self_members').count()

    def get_new_manual_member_user_count(self):
        return self.origin_data.get('manual_service_members').count()

    def get_all_active_user_count(self):
        ret = self.origin_data.get('first_data_users').filter(
            user__is_active=True
        )
        return ret.count()

    def get_all_register_user_count(self):
        return self.origin_data.get('all_data_users').count()

    def get_all_experience_user_count(self):
        return self.origin_data.get('all_data_experience_users').count()

    def get_all_member_user_count(self):
        return len(self.origin_data.get('all_data_members'))

    def get_all_self_member_user_count(self):
        return self.origin_data.get('all_data_self_members').count()

    def get_all_manual_member_user_count(self):
        return self.origin_data.get('all_data_manual_service_members').count()
