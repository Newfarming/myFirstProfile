# coding: utf-8

import datetime

from pin_tools.dash.builder import (
    DataBuilder
)
from pin_utils.django_utils import (
    get_today,
    get_proportion
)


class ResumeDataDriver(object):

    def __init__(self, **kwargs):

        start_query_time = kwargs.get('start_query_time', get_today() - datetime.timedelta(days=1))
        end_query_time = kwargs.get('end_query_time', get_today())
        ret_list = ['pub_feeds', 'user_access_log', 'resumes', 'down_resumes', 'send_cards', 'fav_resumes', 'all_data_user_mark_logs']
        self.db_builder = DataBuilder(
            start_query_time,
            end_query_time,
            ret_list=ret_list
        )
        self.db_builder.build_data()
        self.origin_data = self.db_builder.origin_data

    def get_new_recommend_count(self):
        return sum(len(data['resumes']) for data in self.origin_data.get('pub_feeds').as_pymongo())

    def get_new_view_count(self):
        user_log = self.origin_data.get('user_access_log')

        user_list = user_log.filter(
            access_url__contains='/resumes/display/',
        )

        return len(user_list)

    def get_new_view_proportion(self):
        return get_proportion(self.get_new_view_count(), self.get_new_recommend_count())

    def get_new_fav_count(self):
        return self.origin_data.get('fav_resumes').count()

    def get_new_down_count(self):
        return self.origin_data.get('resumes').count()

    def get_new_down_proportion(self):
        return get_proportion(self.get_new_down_count(), self.get_new_view_count())

    def get_new_send_card_count(self):
        return self.origin_data.get('send_cards').count()

    def get_new_interview_count(self):

        condition = [
            'invite_interview',
            'join_interview',
            'break_invite',
            'send_offer',
            'reject_offer'
        ]
        mark_ids = self.origin_data.get('down_resumes').select_related('ResumeMarkSetting').filter(
            current_mark__code_name__in=condition
        ).values_list('buy_record', flat=True)

        all_user_mark_logs = self.origin_data.get('all_data_user_mark_logs').select_related('ResumeMarkSetting').filter(
            mark__code_name__in=condition,
            mark_time__lte=get_today() - datetime.timedelta(days=1)
        ).values_list('resume_mark', flat=True)

        return len([val for val in mark_ids if val not in all_user_mark_logs])

    def get_new_entered_count(self):
        ret = self.origin_data.get('down_resumes').select_related('ResumeMarkSetting').filter(
            current_mark__code_name__in=[
                'entry'
            ]
        )
        return ret.count()