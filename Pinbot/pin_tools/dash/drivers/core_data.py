# coding: utf-8

import datetime

from pin_tools.dash.builder import (
    DataBuilder
)
from pin_utils.django_utils import (
    get_today
)


class CoreDataDriver(object):

    def __init__(self, **kwargs):

        start_query_time = kwargs.get('start_query_time', get_today() - datetime.timedelta(days=1))
        end_query_time = kwargs.get('end_query_time', get_today())

        ret_list = [
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
        self.get_member_list()

    def get_member_list(self):

        self_member_list = self.origin_data.get('all_data_self_members')
        manual_service_member_list = self.origin_data.get('all_data_manual_service_members')

        self.member_list = []
        self.member_list.extend(self_member_list.values_list('user__username', flat=True))
        self.member_list.extend(manual_service_member_list.values_list('user__username', flat=True))
        self.member_list = set(self.member_list)

    def get_new_register_user_count(self):
        return self.origin_data.get('users').count()

    def get_active_user_count(self):
        ret = self.origin_data.get('users')
        return ret.filter(
            user__is_active=True
        ).count()

    def get_member_count(self):
        ret = self.origin_data.get('members')
        return len(ret)

    def get_lively_user_count(self):
        ret = self.origin_data.get('user_access_log')
        return len(ret.values_list('user_name').distinct('user_name'))

    def get_week_lively_user_count(self):
        return self.get_lively_user_count()

    def get_month_lively_user_count(self):
        return self.get_lively_user_count()

    def get_lively_member_count(self):

        user_list = self.origin_data.get('user_access_log').values_list('user_name').distinct('user_name')
        return len([val for val in user_list if val in self.member_list])

    def get_week_lively_member_count(self):
        return self.get_lively_member_count()

    def get_month_lively_member_count(self):
        return self.get_lively_member_count()

    def get_repeat_visit_count(self):
        result = {}
        user_list = list(self.origin_data.get('user_access_log').values_list('user_name'))
        for key in user_list:

            if user_list.count(key) > 1:
                result[key] = 2
        return len(result)

    def get_week_repeat_visit_user_count(self):
        return self.get_repeat_visit_count()

    def get_week_repeat_visit_member_count(self):

        result = {}
        user_list = list(self.origin_data.get('user_access_log').values_list('user_name'))

        user_list = [val for val in user_list if val in self.member_list]

        for key in user_list:

            if user_list.count(key) > 1:
                result[key] = 2
        return len(result)

    def get_month_repeat_visit_user_count(self):
        return self.get_repeat_visit_count()

    def get_month_repeat_visit_member_count(self):

        result = {}
        user_list = list(self.origin_data.get('user_access_log').values_list('user_name'))

        user_list = [val for val in user_list if val in self.member_list]
        for key in user_list:

            if user_list.count(key) > 1:
                result[key] = 2
        return len(result)