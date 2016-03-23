# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime
import requests

from django.conf import settings
from django.core.cache import cache
from django.db import connection

from pin_tools.dash.builder import (
    DataBuilder
)
from pin_utils.django_utils import (
    get_today,
    get_proportion
)


class PartnerDataDriver(object):

    def __init__(self, **kwargs):

        start_query_time = kwargs.get('start_query_time', get_today() - datetime.timedelta(days=1))
        end_query_time = kwargs.get('end_query_time', get_today())
        ret_list = [
            'tasks',
            'all_data_tasks',
            'upload_resumes',
            'all_data_upload_resumes',
            'task_coin_records',
            'all_data_task_coin_records',
            'do_tasks',
            'all_data_do_tasks'
        ]
        self.db_builder = DataBuilder(
            start_query_time,
            end_query_time,
            ret_list=ret_list
        )
        self.db_builder.build_data()
        self.origin_data = self.db_builder.origin_data

    def do_sql(self, sql_str):
        cursor = connection.cursor()
        cursor.execute(sql_str)
        ret = cursor.fetchone()
        if ret:
            ret = ret[0]
        else:
            ret = 0
        if ret is None:
            ret = 0

        return ret

    def get_accept_task_user_count(self):
        return self.origin_data.get('tasks').values("user__username").distinct().count()

    def get_all_accept_task_user_count(self):
        return self.origin_data.get('all_data_tasks').values("user__username").distinct().count()

    def get_task_total_count(self):
        try:
            url = '{url}{para}'.format(
                url=settings.API_SEARCH_JOB,
                para='?query_feed_result=True&start=0&feed_type=1&need_company=True&time_field_gte=feed_expire_time%3A-7'
            )
            r = requests.get(url=url).json()
            return r.get('total')
        except Exception:
            return 0

    def get_task_viewed_count(self):
        return cache.get('PARTNER_TASK_CHECK_COUNT', 0)

    def get_task_accedpted_count(self):
        return self.origin_data.get('tasks').count()

    def get_task_accedpted_count_contrast(self):
        return get_proportion(self.get_task_accedpted_count(), self.get_task_viewed_count())

    def get_all_task_accedpted_total_count(self):
        return self.origin_data.get('all_data_tasks').count()

    def get_upload_resume_count(self):
        return self.origin_data.get('upload_resumes').count()

    def get_all_upload_resume_count(self):
        return self.origin_data.get('all_data_upload_resumes').count()

    def get_do_task_count(self):
        return self.origin_data.get('do_tasks').count()

    def get_all_do_task_count(self):
        return self.origin_data.get('all_data_do_tasks').count()

    def get_resume_viewed_count(self):
        return self.origin_data.get('task_coin_records').filter(
            record_type='check'
        ).count()

    def get_all_resume_viewed_count(self):
        return self.origin_data.get('all_data_task_coin_records').filter(
            record_type='check'
        ).count()

    def get_resume_download_count(self):
        return self.origin_data.get('task_coin_records').filter(
            record_type='download'
        ).count()

    def get_resume_all_download_count(self):
        return self.origin_data.get('all_data_task_coin_records').filter(
            record_type='download'
        ).count()

    def get_interviewed_count(self):
        return self.origin_data.get('task_coin_records').filter(
            record_type='interview'
        ).count()

    def get_all_interviewed_count(self):
        return self.origin_data.get('all_data_task_coin_records').filter(
            record_type='interview'
        ).count()

    def get_entered_count(self):
        return self.origin_data.get('task_coin_records').filter(
            record_type='taking_work'
        ).count()

    def get_all_entered_count(self):
        return self.origin_data.get('all_data_task_coin_records').filter(
            record_type='taking_work'
        ).count()

    def get_accusation_count(self):
        return self.origin_data.get('task_coin_records').filter(
            record_type='accusation'
        ).count()

    def get_all_accusation_count(self):
        return self.origin_data.get('all_data_task_coin_records').filter(
            record_type='accusation'
        ).count()

    def get_today_commend_and_check_count(self):
        sql_str = """select count(*) from partner_taskcoinrecord , partner_usertaskresume  where
                        partner_taskcoinrecord.record_type = 'check' and
                        partner_taskcoinrecord.task_id = partner_usertaskresume.task_id and
                        partner_taskcoinrecord.upload_resume_id = partner_usertaskresume.resume_id and
                        date_format(partner_taskcoinrecord.record_time,"%Y-%m-%d") = date_format(partner_usertaskresume.upload_time,"%Y-%m-%d") and
                        partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                        """.format(
            get_today(),
            get_today() + datetime.timedelta(days=1))

        return self.do_sql(sql_str)

    def get_today_commend_and_download_count(self):
        sql_str = """select count(*) from partner_taskcoinrecord , partner_usertaskresume  where
                        partner_taskcoinrecord.record_type = 'download' and
                        partner_taskcoinrecord.task_id = partner_usertaskresume.task_id and
                        partner_taskcoinrecord.upload_resume_id = partner_usertaskresume.resume_id and
                        date_format(partner_taskcoinrecord.record_time,"%Y-%m-%d") = date_format(partner_usertaskresume.upload_time,"%Y-%m-%d") and
                        partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                        """.format(
            get_today(),
            get_today() + datetime.timedelta(days=1))

        return self.do_sql(sql_str)

    def get_today_reward_coin_count(self):
        sql_str = """select sum(coin) from partner_taskcoinrecord where
                      partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                        """.format(
            get_today(),
            get_today() + datetime.timedelta(days=1))

        return self.do_sql(sql_str)

    def get_all_reward_coin_count(self):
        sql_str = """select sum(coin) from partner_taskcoinrecord where
                      partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                        """.format(
            '2015-06-01',
            get_today() + datetime.timedelta(days=1))

        return self.do_sql(sql_str)

    def get_today_extra_reward_coin_count(self):
        sql_str = """select sum(coin) from partner_taskcoinrecord where
                         (record_type = 'extra_taking_work' or record_type = 'extra_interview' or record_type = 'extra_download') and
                         partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                        """.format(
            get_today(),
            get_today() + datetime.timedelta(days=1))
        return self.do_sql(sql_str)

    def get_all_extra_reward_coin_count(self):
        sql_str = """select sum(coin) from partner_taskcoinrecord where
                         (record_type = 'extra_taking_work' or record_type = 'extra_interview' or record_type = 'extra_download') and
                         partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                        """.format(
            '2015-06-01',
            get_today() + datetime.timedelta(days=1))
        return self.do_sql(sql_str)
