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
        ret_list = ['pub_feeds', 'statistic', 'feed_result', 'resumes', 'down_resumes', 'send_cards', 'fav_resumes', 'all_data_user_mark_logs', 'first_data_staffs']
        self.db_builder = DataBuilder(
            start_query_time,
            end_query_time,
            ret_list=ret_list
        )
        self.db_builder.build_data()
        self.origin_data = self.db_builder.origin_data

    def get_staff_list(self):
        return self.origin_data.get('first_data_staffs').values_list('username', flat=True)

    def get_new_recommend_count(self):

        ret = self.origin_data.get('feed_result')
        return len(ret)
        #return sum(len(data['resumes']) for data in self.origin_data.get('pub_feeds').as_pymongo())

    def get_new_view_count(self):
        staffs = self.get_staff_list()
        user_log = self.origin_data.get('statistic')

        user_log = user_log.filter(
            page_id='40',
        ).values_list('username', 'access_url')

        u_count = {}
        for u in user_log:
            key = '{0},{1}'.format(u[0], u[1])
            u_count[key] = 1

        return len(u_count)

    def get_new_view_proportion(self):
        return get_proportion(self.get_new_view_count(), self.get_new_recommend_count())

    def get_new_fav_count(self):
        user_log = self.origin_data.get('statistic')

        user_log = user_log.filter(
            page_id='50',
        )
        return len(user_log)
        #return self.origin_data.get('fav_resumes').count()

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
