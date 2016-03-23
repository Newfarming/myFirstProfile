# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from pin_utils.django_utils import (
    get_today,
    get_pre_week,
    get_pre_month
)
from app.dash.models import (
    UserDailyReportData,
    ResumeDailyReportData,
    ResumeWhitoutStaffDailyReportData,
    PartnerDailyReportData,
    CoreDailyReportData,
    FeedDailyReportData,
    WeixinDailyReportData,
    TaskSystemDailyReportData,
    WeekReportData,
    MonthReportData
)
from pin_tools.dash.drivers.core_data import (
    CoreDataDriver
)
from pin_tools.dash.drivers.feed_data import (
    FeedDataDriver
)
from pin_tools.dash.drivers.partner_data import (
    PartnerDataDriver
)
from pin_tools.dash.drivers.resume_data import (
    ResumeDataDriver
)
from pin_tools.dash.drivers.resume_data_without_staff import (
    ResumeDataDriver as ResumeDataDriver_Without_Staff
)
from pin_tools.dash.drivers.user_data import (
    UserDataDriver
)
from pin_tools.dash.drivers.weixin_data import (
    WeixinDataDriver
)
from pin_tools.dash.drivers.task_data import (
    TaskDailyDataDriver
)


TASK_MAP = {
    'week_data': {
        'driver_class': CoreDataDriver,
        'model_class': WeekReportData,
        'fun_list': {
            'get_week_lively_user_count': 'week_lively_user_count',
            'get_week_lively_member_count': 'week_lively_member_count',
            'get_week_repeat_visit_user_count': 'week_repeat_visit_user_count',
            'get_week_repeat_visit_member_count': 'week_repeat_visit_member_count'
        },
        'crontab_time': (0, 18),
    },

    'month_data': {
        'driver_class': CoreDataDriver,
        'model_class': MonthReportData,
        'fun_list': {
            'get_month_lively_user_count': 'month_lively_user_count',
            'get_month_lively_member_count': 'month_lively_member_count',
            'get_month_repeat_visit_user_count': 'month_repeat_visit_user_count',
            'get_month_repeat_visit_member_count': 'month_repeat_visit_member_count'
        },
        'crontab_time': (0, 18),
    },
    'core_data': {
        'driver_class': CoreDataDriver,
        'model_class': CoreDailyReportData,
        'fun_list': {
            'get_new_register_user_count': 'register_user_count',
            'get_active_user_count': 'active_user_count',
            'get_member_count': 'member_count',
            'get_lively_user_count': 'lively_user_count',
            'get_lively_member_count': 'lively_member_count',
            'get_repeat_visit_count': 'repeat_visit_count'
        },
        'crontab_time': (0, 18),
    },
    'feed_data': {
        'driver_class': FeedDataDriver,
        'model_class': FeedDailyReportData,
        'fun_list': {
            'get_lively_feed_count': 'lively_feed_count',
            'get_new_feed': 'new_feed_count',
            'get_lively_feed_user_count': 'lively_feed_user_count',
            'get_lively_feed_member_count': 'lively_feed_member_count'
        },
        'crontab_time': (0, 18),
    },
    'partner': {
        'driver_class': PartnerDataDriver,
        'model_class': PartnerDailyReportData,
        'fun_list': {
            'get_accept_task_user_count': 'accept_task_user_count',
            'get_all_accept_task_user_count': 'accept_task_user_total_count',
            'get_task_total_count': 'task_total_count',
            'get_task_viewed_count': 'task_viewed_count',
            'get_task_accedpted_count': 'task_accedpted_count',
            'get_task_accedpted_count_contrast': 'task_accedpted_count_contrast',
            'get_all_task_accedpted_total_count': 'task_accedpted_total_count',
            'get_upload_resume_count': 'upload_resume_count',
            'get_all_upload_resume_count': 'upload_resume_total_count',
            'get_do_task_count': 'do_task_count',
            'get_all_do_task_count': 'do_task_total_count',
            'get_resume_viewed_count': 'resume_viewed_count',
            'get_all_resume_viewed_count': 'resume_viewed_total_count',
            'get_resume_download_count': 'resume_download_count',
            'get_resume_all_download_count': 'resume_download_total_count',
            'get_interviewed_count': 'interviewed_count',
            'get_all_interviewed_count': 'interviewed_total_count',
            'get_entered_count': 'entered_count',
            'get_all_entered_count': 'entered_total_count',
            'get_accusation_count': 'accusation_count',
            'get_all_accusation_count': 'accusation_total_count',
            'get_today_commend_and_check_count': 'today_commend_and_check_count',
            'get_today_commend_and_download_count': 'today_commend_and_download_count',
            'get_today_reward_coin_count': 'today_reward_coin_count',
            'get_all_reward_coin_count': 'all_reward_coin_count',
            'get_today_extra_reward_coin_count': 'today_extra_reward_coin_count',
            'get_all_extra_reward_coin_count': 'all_extra_reward_coin_count'
        },
        'crontab_time': (23, 23),
    },
    'resume_data': {
        'driver_class': ResumeDataDriver,
        'model_class': ResumeDailyReportData,
        'fun_list': {
            'get_new_recommend_count': 'resume_commends_count',
            'get_new_view_count': 'resume_view_count',
            'get_new_view_proportion': 'resume_view_proportion',
            'get_new_fav_count': 'resume_fav_count',
            'get_new_down_count': 'resume_down_count',
            'get_new_down_proportion': 'resume_down_proportion',
            'get_new_send_card_count': 'company_card_send_count',
            'get_new_interview_count': 'interviewed_count',
            'get_new_entered_count': 'entered_count'
        },
        'crontab_time': (0, 18),
    },
    'resume_data_without_staff': {
        'driver_class': ResumeDataDriver_Without_Staff,
        'model_class': ResumeWhitoutStaffDailyReportData,
        'fun_list': {
            'get_new_recommend_count': 'resume_commends_count',
            'get_new_view_count': 'resume_view_count',
            'get_new_view_proportion': 'resume_view_proportion',
            'get_new_fav_count': 'resume_fav_count',
            'get_new_down_count': 'resume_down_count',
            'get_new_down_proportion': 'resume_down_proportion',
            'get_new_send_card_count': 'company_card_send_count',
            'get_new_interview_count': 'interviewed_count',
            'get_new_entered_count': 'entered_count'
        },
        'crontab_time': (0, 18),
    },

    'user_data': {
        'driver_class': UserDataDriver,
        'model_class': UserDailyReportData,
        'fun_list': {
            'get_new_register_user_count': 'new_register_user_count',
            'get_new_experience_user_count': 'new_experience_user_count',
            'get_new_self_member_user_count': 'new_self_member_count',
            'get_new_manual_member_user_count': 'new_manual_member_count',
            'get_new_member_user_count': 'new_member_count',
            'get_all_member_user_count': 'total_member_count',
            'get_all_active_user_count': 'all_total_active_user_count',
            'get_all_register_user_count': 'total_register_user_count',
            'get_all_experience_user_count': 'total_experience_user_count',
            'get_all_self_member_user_count': 'total_self_member_count',
            'get_all_manual_member_user_count': 'total_manual_member_count'
        },
        'crontab_time': (0, 18),
    },
    'weixin_data': {
        'driver_class': WeixinDataDriver,
        'model_class': WeixinDailyReportData,
        'fun_list': {
            'get_new_bind_weixin_user_count': 'new_bind_count',
            'get_new_reg_weixin_user_count': 'new_reg_count',
            'get_all_new_bind_weixin_user_count': 'total_bind_count',
            'get_lively_member_count': 'lively_member_count',
            'get_lively_user_count': 'lively_user_count',
            'get_send_msg_count': 'feed_notify_send_count',
            'get_click_msg_count': 'feed_notify_view_count',
            'get_submit_feed_count': 'new_feed_count',
            'get_add_watch_count': 'new_feed_favours_count'
        },
        'crontab_time': (0, 18),
    },
    'task_syatem_data': {
        'driver_class': TaskDailyDataDriver,
        'model_class': TaskSystemDailyReportData,
        'fun_list': {
            'get_task_A1_count': 'task_A1_count',
            'get_task_A2_count': 'task_A2_count',
            'get_task_A3_count': 'task_A3_count',
            'get_task_A4_count': 'task_A4_count',
            'get_task_A5_count': 'task_A5_count',
            'get_task_A6_count': 'task_A6_count',
            'get_task_A6_R1_count': 'task_A6_R1_count',
            'get_task_A6_R2_count': 'task_A6_R2_count',
            'get_task_A6_L1_count': 'task_A6_L1_count',
            'get_task_A7_count': 'task_A7_count',
            'get_task_A7_R1_count': 'task_A7_R1_count',
            'get_task_A7_R2_count': 'task_A7_R2_count',
            'get_task_A7_R3_count': 'task_A7_R3_count',
            'get_task_A8_count': 'task_A8_count',
            'get_task_A8_R1_count': 'task_A8_R1_count',
            'get_task_A8_R2_count': 'task_A8_R2_count',
            'get_task_A8_R3_count': 'task_A8_R3_count',
            'get_task_A9_count': 'task_A9_count',
            'get_task_A9_R1_count': 'task_A9_R1_count',
            'get_task_A9_R2_count': 'task_A9_R2_count',
            'get_task_A9_R3_count': 'task_A9_R3_count',
            'get_task_A10_count': 'task_A10_count',
            'get_task_A10_R1_count': 'task_A10_R1_count',
            'get_task_A11_count': 'task_A11_count',
            'get_task_A12_count': 'task_A12_count',
            'get_task_A13_count': 'task_A13_count',
            'get_task_A14_L1_count': 'task_A14_L1_count',
            'get_task_A15_count': 'task_A15_count',
            'get_task_A15_R1_count': 'task_A15_R1_count',
            'get_task_A15_R2_count': 'task_A15_R2_count',
            'get_task_A16_count': 'task_A16_count',
            'get_task_A17_count': 'task_A17_count',
            'get_task_A18_R1_count': 'task_A18_R1_count',
            'get_task_A18_R2_count': 'task_A18_R2_count',
        },
        'crontab_time': (0, 18),
    },

}


class DriversTask(object):

    task_type_date_range_map = {
        'today': {
            'start_query_time': get_today() - datetime.timedelta(days=1),
            'end_query_time': get_today()
        },
        'week': {
            'start_query_time': get_pre_week()[6],
            'end_query_time': get_pre_week()[0]
        },
        'month': {
            'start_query_time': get_pre_month()[0],
            'end_query_time': get_pre_month()[1]
        }
    }

    def __init__(self):

        self.report_date = get_today() - datetime.timedelta(days=1)
        self.task_type = self.get_task_type()
        self.task_doc = TASK_MAP

    def set_report_date(self, report_date):
        self.report_date = report_date

        self.task_type_date_range_map.get('today')['start_query_time'] = report_date
        self.task_type_date_range_map.get('today')['end_query_time'] = report_date + datetime.timedelta(days=1)

    def set_task_type(self, task_type):
        self.task_type = [task_type]

    def set_task_name(self, task_name):
        self.task_doc = {}
        self.task_doc[task_name] = TASK_MAP.get(task_name)

    def make_data(self):

        for task_type in self.task_type:
            task_doc = self.task_doc.copy()
            start_query_time = self.task_type_date_range_map.get(task_type)['start_query_time']
            end_query_time = self.task_type_date_range_map.get(task_type)['end_query_time']

            if task_type == 'today':
                task_doc.pop('month_data', '')
                task_doc.pop('week_data', '')
            if task_type == 'week':
                task_doc.pop('month_data', '')
                task_doc.pop('weixin_data', '')
                task_doc.pop('user_data', '')
                task_doc.pop('resume_data', '')
                task_doc.pop('resume_data_without_staff', '')
                task_doc.pop('partner', '')
                task_doc.pop('feed_data', '')
                task_doc.pop('core_data', '')

            if task_type == 'month':
                task_doc.pop('week_data', '')
                task_doc.pop('weixin_data', '')
                task_doc.pop('user_data', '')
                task_doc.pop('resume_data', '')
                task_doc.pop('resume_data_without_staff', '')
                task_doc.pop('partner', '')
                task_doc.pop('feed_data', '')
                task_doc.pop('core_data', '')

            print task_type, start_query_time, end_query_time

            for key, val in task_doc.items():

                hour = datetime.datetime.now().hour
                # 判断时间段该报表是否应该统计)
                if not (hour >= TASK_MAP[key].get('crontab_time')[0] and hour <= TASK_MAP[key].get('crontab_time')[1]):
                    continue

                self.model_class = TASK_MAP[key].get('model_class')

                driver_class = TASK_MAP[key].get('driver_class')(
                    start_query_time=start_query_time,
                    end_query_time=end_query_time
                )

                self.db_result = {
                    'report_date': self.report_date
                }

                for fun_key, fun_field in TASK_MAP[key].get('fun_list').items():

                    build_fun = getattr(driver_class, fun_key)
                    ret = build_fun()
                    self.db_result.update(
                        {
                            fun_field: ret
                        }
                    )

                print 'model_class={0} task={1}, key={2}'.format(self.model_class, task_type, key)
                print self.db_result
                self.save_db()

    def save_db(self):

        today_report = self.model_class.objects.filter(
            report_date=self.report_date,
        )

        if today_report:
            today_report.update(
                **self.db_result
            )
        else:

            report = self.model_class(
                **self.db_result
            )

            report.save()

    def get_task_type(self):

        """获取所有task类型"""
        task_type = []
        task_type.append('today')
        today = get_today()

        """判断当天是否为星期一"""
        if today == today + datetime.timedelta(days=-today.weekday()):
            task_type.append('week')

        """判断当天是否为月初"""
        if today == datetime.datetime(today.year, today.month, 1):
            task_type.append('month')

        return task_type

if __name__ == '__main__':
    task = DriversTask()
    task.make_data()
