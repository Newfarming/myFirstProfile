# coding: utf-8
import datetime
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'
from pin_utils.django_utils import (
    get_today
)
from Pinbot.settings import (
    settings
)

REPORT_SCHEMA = {

    'wexin_daily_report': {
        'crontab_time': (0, 18),
        'dash_date': {
            'first_time': datetime.datetime(2010, 01, 01),
            'all_time': datetime.datetime(2015, 03, 28),
            'start_query_time': get_today() - datetime.timedelta(days=1),
            'end_query_time': get_today()
        },
        'report_date': get_today() - datetime.timedelta(days=1),
        'report_table_name': 'WeixinDailyReportData',
        'schema': {
            'new_bind_count': {
                'data_type': 'db',
                'table': 'WeixinUser',
                'fields': [
                                {
                                    'is_bind': True,
                                    'create_time__gt': 'user__date_joined'
                                }

                           ],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_reg_count': {
                'data_type': 'db',
                'table': 'WeixinUser',
                'fields': [
                                {
                                    'is_bind': True,
                                    'create_time__lte': 'user__date_joined'
                                }

                           ],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'total_bin_count': {
                'all_data':True,
                'data_type': 'db',
                'table': 'WeixinUser',
                'fields': [{'is_bind': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'lively_member_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'weixin_member_count',
                'count_field_list': 'user_name',
                'distinct': True,
            },
             'lively_user_count':{
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'count',
                'count_field_list': 'user_name',
                'distinct': True,
             },
            'feed_notify_send_count': {
                'data_type': 'db',
                'table': 'WeixinUser',
                'fields': [{'subscribe': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_feed_count': {
                'data_type': 'db',
                'table': 'WeixinUser',
                'fields': [{'subscribe': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'feed_notify_view_count': {
                'data_type': 'db',
                'table': 'WeixinUser',
                'fields': [{'subscribe': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_feed_favours_count': {
                'data_type': 'db',
                'table': 'WeixinUser',
                'fields': [{'subscribe': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
        }
    },

    'feed_daily_report': {
        'crontab_time': (0, 18),
        'dash_date': {
            'first_time': datetime.datetime(2010, 01, 01),
            'all_time': datetime.datetime(2015, 03, 28),
            'start_query_time': get_today() - datetime.timedelta(days=1),
            'end_query_time': get_today()
        },
        'report_date': get_today() - datetime.timedelta(days=1),
        'report_table_name': 'FeedDailyReportData',
        'schema': {
            'lively_feed_count': {
                'data_type': 'db',
                'table': 'Feed',
                'fields': [{'deleted': False}],
                'time_start_end': ['add_time', 'add_time'],
                'query_method': 'count'
            },
           'new_feed_count': {
                'data_type': 'db',
                'table': 'Feed',
                'time_start_end': ['add_time', 'add_time'],
                'query_method': 'count'
            },
           'lively_feed_user_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'count_field_list': [{'access_url': '/special_feed/feed_list/'}],
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'find_count'
            },
           'lively_feed_member_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'count_field_list': [{'access_url': '/special_feed/feed_list/'}],
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'member_count'
            },
        }
    },

    'core_daily_report': {
        'crontab_time': (0, 18),
        'dash_date': {
            'first_time': datetime.datetime(2010, 01, 01),
            'all_time': datetime.datetime(2015, 03, 28),
            'start_query_time': get_today() - datetime.timedelta(days=1),
            'end_query_time': get_today()
        },
        'report_date': get_today() - datetime.timedelta(days=1),
        'report_table_name': 'CoreDailyReportData',
        'schema': {
            'active_user_count': {
                'data_type': 'db',
                'table': 'UserProfile',
                'fields': [{'user__is_active': True}],
                'time_start_end': ['user__date_joined', 'user__date_joined'],
                'query_method': 'count'
            },
            'member_count': {
                'data_type': 'db',
                'table': 'UserProfile',
                'fields': [{'user__is_active': True}],
                'time_start_end': ['user__date_joined', 'user__date_joined'],
                'query_method': 'member_count'
            },
            'entered_count': {
                'data_type': 'db',
                'select_related': 'ResumeMarkSetting',
                'table': 'DownloadResumeMark',
                'time_start_end': ['mark_time', 'mark_time'],
                'fields': [
                    {
                        'current_mark__code_name__in': [
                           'send_offer',
                           'entry',
                           'reject_offer'
                        ]
                    }
                ],
                'query_method': 'count',
            },
            'lively_user_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'count',
                'count_field_list': 'user_name',
                'distinct': True,
            },
            'lively_member_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'member_count',
                'count_field_list': 'user_name',
                'distinct': True,
            },
            'repeat_visit_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'value_count',
                'count_field_list': 'user_name',
                'limit': 2,
            },
        }
    },
    'user_daily_report': {
        'crontab_time': (0, 18),
        'dash_date': {
            'first_time': datetime.datetime(2010, 01, 01),
            'all_time': datetime.datetime(2015, 03, 28),
            'start_query_time': get_today() - datetime.timedelta(days=1),
            'end_query_time': get_today()
        },
        'report_date': get_today() - datetime.timedelta(days=1),
        'report_table_name': 'UserDailyReportData',
        'schema': {
            'new_register_user_count': {
                'data_type': 'db',
                'table': 'UserProfile',
                'time_start_end': ['user__date_joined', 'user__date_joined'],
                'query_method': 'count'
            },
            'new_active_user_count': {
                'data_type': 'db',
                'table': 'UserProfile',
                'fields': [{'user__is_active': True}],
                'time_start_end': ['user__date_joined', 'user__date_joined'],
                'query_method': 'count'
            },
            'new_experience_user_count': {
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'experience_user'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_self_member_count': {
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [
                            {
                                'vip_role__code_name__in':
                                [
                                   'self_a',
                                   'self_b',
                                   'self_c',
                                ]
                            },
                            {'is_active': True}
                           ],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_self_member_a_count': {
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'self_a'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_self_member_b_count': {
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'self_b'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_self_member_c_count': {
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'self_c'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'new_manual_member_count': {
                'data_type': 'db',
                'table': 'UserManualService',
                'fields': [{'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },

            'all_total_active_user_count': {
                'first_time': True,
                'data_type': 'db',
                'table': 'UserProfile',
                'fields': [{'user__is_active': True}],
                'time_start_end': ['user__date_joined', 'user__date_joined'],
                'query_method': 'count'
            },
            'total_register_user_count': {
                'all_data': True,
                'data_type': 'db',
                'table': 'UserProfile',
                'time_start_end': ['user__date_joined', 'user__date_joined'],
                'query_method': 'count'
            },
            'total_experience_user_count': {
                'all_data':True,
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'experience_user'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'total_self_member_count': {
                'all_data':True,
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [
                            {
                                'vip_role__code_name__in':
                                [
                                   'self_a',
                                   'self_b',
                                   'self_c',
                                ]
                            },
                           {'is_active': True}
                           ],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'total_self_member_a_count': {
                'all_data':True,
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'self_a'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'total_self_member_b_count': {
                'all_data':True,
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'self_b'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'total_self_member_c_count': {
                'all_data':True,
                'data_type': 'db',
                'table': 'UserVip',
                'select_related': 'user,vip',
                'fields': [{'vip_role__code_name': 'self_c'}, {'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'total_manual_member_count': {
                'all_data':True,
                'data_type': 'db',
                'table': 'UserManualService',
                'fields': [{'is_active': True}],
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'lively_user_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'count',
                'count_field_list': 'user_name',
                'distinct': True,
            },
            'repeat_visit_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'value_count',
                'count_field_list': 'user_name',
                'limit': 2,
            },
            'week_lively_user_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'count',
                'count_field_list': 'user_name',
                'distinct': True,
            },
            'month_lively_user_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'count',
                'count_field_list': 'user_name',
                'distinct': True,
            }
        }
    },

    'resume_daily_report': {
        'crontab_time': (0, 18),
        'report_table_name': 'ResumeDailyReportData',
        'dash_date': {
            'first_time': datetime.datetime(2010, 01, 01),
            'all_time': datetime.datetime(2015, 03, 28),
            'start_query_time': get_today() - datetime.timedelta(days=1),
            'end_query_time': get_today()
        },
        'report_date': get_today() - datetime.timedelta(days=1),
        'schema': {
            'resume_commends_count': {
                'data_type': 'mongo',
                'table': 'PubFeedData',
                'count_field_list': 'resumes',
                'time_start_end': ['pub_time', 'pub_time'],
                'query_method': 'sum_count',
            },
            'resume_view_count': {
                'data_type': 'mongo',
                'table': 'UserAccessLog',
                'count_field_list': [{'access_url': '/resumes/display/'}],
                'time_start_end': ['access_time', 'access_time'],
                'query_method': 'find_count'
            },
            'resume_down_count': {
                'data_type': 'db',
                'table': 'ResumeBuyRecord',
                'time_start_end': ['op_time', 'op_time'],
                'query_method': 'count',
            },
            'interviewed_count': {
                'data_type': 'db',
                'select_related': 'ResumeMarkSetting',
                'table': 'DownloadResumeMark',
                'time_start_end': ['mark_time', 'mark_time'],
                'fields': [
                    {
                        'current_mark__code_name__in': [
                           'invite_interview',
                           'join_interview',
                           'next_interview',
                           'lower_ability',
                           'invite_no_interest',
                           'break_invite'
                        ]
                    }
                ],
                'query_method': 'count',
            },
            'entered_count': {
                'data_type': 'db',
                'select_related': 'ResumeMarkSetting',
                'table': 'DownloadResumeMark',
                'time_start_end': ['mark_time', 'mark_time'],
                'fields': [
                    {
                        'current_mark__code_name__in': [
                           'send_offer',
                           'entry',
                           'reject_offer'
                        ]
                    }
                ],
                'query_method': 'count',
            },
            'company_card_send_count': {
                'data_type': 'db',
                'table': 'SendCompanyCard',
                'time_start_end': ['send_time', 'send_time'],
                'query_method': 'count',
            }
        }
    },

    'partner_daily_report': {
        'crontab_time': (23, 23),
        'dash_date': {
            'first_time': datetime.datetime(2010, 01, 01),
            'all_time': datetime.datetime(2015, 03, 28),
            'start_query_time': get_today(),
            'end_query_time': get_today() + datetime.timedelta(days=1),

        },
        'report_date': get_today(),
        'report_table_name': 'PartnerDailyReportData',
        'schema': {
            'accept_task_user_count': {
                'data_type': 'db',
                'table': 'UserAcceptTask',
                'time_start_end': ['update_time', 'update_time'],
                'distinct': 'user__username',
                'query_method': 'count',
            },
            'accept_task_user_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'UserAcceptTask',
                'time_start_end': ['update_time', 'update_time'],
                'distinct': 'user__username',
                'query_method': 'count',
            },
            'task_total_count': {
                'data_type': 'http_request',
                'url': '%s%s' % (settings.API_SEARCH_JOB,'?query_feed_result=True&start=0&feed_type=1&need_company=True&time_field_gte=feed_expire_time%3A-7'),
                'field': 'total',
                'query_method': 'count',
            },
            'task_viewed_count': {
                'data_type': 'cache',
                'field': 'PARTNER_TASK_CHECK_COUNT',
                'query_method': 'get_value'
            },
            'task_accedpted_count': {
                'data_type': 'db',
                'table': 'UserAcceptTask',
                'time_start_end': ['update_time', 'update_time'],
                'query_method': 'count'
            },
            'task_accedpted_count_contrast': {
                'data_type': 'inter_calc',
                'fields': ['task_accedpted_count', 'task_viewed_count']
            },
            'task_accedpted_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'UserAcceptTask',
                'time_start_end': ['update_time', 'update_time'],
                'query_method': 'count'
            },
            'upload_resume_count': {
                'data_type': 'db',
                'table': 'UploadResume',
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'upload_resume_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'UploadResume',
                'time_start_end': ['create_time', 'create_time'],
                'query_method': 'count'
            },
            'do_task_count': {
                'data_type': 'db',
                'table': 'UserTaskResume',
                'time_start_end': ['upload_time', 'upload_time'],
                'query_method': 'count'
            },
            'do_task_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'UserTaskResume',
                'time_start_end': ['upload_time', 'upload_time'],
                'query_method': 'count'
            },
            'resume_viewed_count': {
                'data_type': 'db',
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'check'}],
                'query_method': 'count'
            },
            'resume_viewed_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'check'}],
                'query_method': 'count'
            },
            'resume_download_count': {
                'data_type': 'db',
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'download'}],
                'query_method': 'count'
            },
            'resume_download_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'download'}],
                'query_method': 'count'
            },
            'interviewed_count': {
                'data_type': 'db',
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'interview'}],
                'query_method': 'count'
            },
            'interviewed_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'interview'}],
                'query_method': 'count'
            },
            'entered_count': {
                'data_type': 'db',
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'taking_work'}],
                'query_method': 'count'
            },
            'entered_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'taking_work'}],
                'query_method': 'count'
            },
            'accusation_count': {
                'data_type': 'db',
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'accusation'}],
                'query_method': 'count'
            },
            'accusation_total_count': {
                'data_type': 'db',
                'all_data': True,
                'table': 'TaskCoinRecord',
                'time_start_end': ['record_time', 'record_time'],
                'fields': [{'record_type': 'accusation'}],
                'query_method': 'count'
            },
            'today_commend_and_check_count': {
                'data_type': 'raw_sql',
                'table': 'TaskCoinRecord',
                'sql_str': """select count(*) from partner_taskcoinrecord , partner_usertaskresume  where
                                partner_taskcoinrecord.record_type = 'check' and
                                partner_taskcoinrecord.task_id = partner_usertaskresume.task_id and
                                partner_taskcoinrecord.upload_resume_id = partner_usertaskresume.resume_id and
                                date_format(partner_taskcoinrecord.record_time,"%Y-%m-%d") = date_format(partner_usertaskresume.upload_time,"%Y-%m-%d") and
                                partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                                """.format(
                    get_today(),
                    get_today() + datetime.timedelta(days=1))
            },
            'today_commend_and_download_count': {
                'data_type': 'raw_sql',
                'table': 'TaskCoinRecord',
                'sql_str': """select count(*) from partner_taskcoinrecord , partner_usertaskresume  where
                                partner_taskcoinrecord.record_type = 'download' and
                                partner_taskcoinrecord.task_id = partner_usertaskresume.task_id and
                                partner_taskcoinrecord.upload_resume_id = partner_usertaskresume.resume_id and
                                date_format(partner_taskcoinrecord.record_time,"%Y-%m-%d") = date_format(partner_usertaskresume.upload_time,"%Y-%m-%d") and
                                partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                                """.format(
                                get_today(),
                                get_today() + datetime.timedelta(days=1))
            },
            'today_reward_coin_count': {
                'data_type': 'raw_sql',
                'table': 'TaskCoinRecord',
                'sql_str': """select sum(coin) from partner_taskcoinrecord where
                             partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                            """.format(
                            get_today(),
                            get_today() + datetime.timedelta(days=1))
            },
            'all_reward_coin_count':{
                'data_type': 'raw_sql',
                'table': 'TaskCoinRecord',
                'sql_str': """select sum(coin) from partner_taskcoinrecord where
                             partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}";
                            """.format(
                            '2015-06-01',
                            get_today() + datetime.timedelta(days=1))

            },
            'today_extra_reward_coin_count':{
                'data_type': 'raw_sql',
                'table': 'TaskCoinRecord',
                'sql_str': """select sum(coin) from partner_taskcoinrecord where
                             partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}" and
                             record_type = 'extra_taking_work' or record_type = 'extra_interview' or record_type = 'extra_download';
                            """.format(
                            get_today(),
                            get_today() + datetime.timedelta(days=1))
            },
            'all_extra_reward_coin_count':{
                'data_type': 'raw_sql',
                'table': 'TaskCoinRecord',
                'sql_str': """select sum(coin) from partner_taskcoinrecord where
                             partner_taskcoinrecord.record_time BETWEEN "{0}" AND "{1}" and
                             record_type = 'extra_taking_work' or record_type = 'extra_interview' or record_type = 'extra_download';
                            """.format(
                            '2015-06-01',
                            get_today() + datetime.timedelta(days=1))
            }
        }
    }
}
