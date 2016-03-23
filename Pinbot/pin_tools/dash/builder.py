# coding: utf-8

import sys
import types
import datetime
from django.contrib.auth.models import User
from app.task_system.models import (
    TaskFinishedStatus
)
from transaction.models import (
    DownloadResumeMark,
    ResumeBuyRecord,
    UserMarkLog
)
from resumes.models import (
    UserWatchResume
)
from jobs.models import (
    SendCompanyCard
)
from feed.models import (
    Feed,
    PubFeedData,
    FeedResult
)
from app.vip.models import (
    UserVip,
    UserManualService
)
from users.models import (
    UserProfile
)
from app.weixin.models import (
    WeixinUser,
    MsgSendLog
)
from app.dash.document import (
    UserAccessLog
)
from app.partner.models import (
    UserAcceptTask,
    UserTaskResume,
    TaskCoinRecord,
    UploadResume
)
from statistics.models import (
    StatisticsModel
)

all_data_start_time = datetime.datetime(2015, 03, 28)
first_data_start_time = datetime.datetime(2010, 01, 01)

today_origin_data_template = {
    'users': {
        'source_type': 'db',
        'model': UserProfile,
        'query_fields': {

        },
        'time_field': 'user__date_joined'
    },
    'weixin_users': {
        'source_type': 'db',
        'model': WeixinUser,
        'query_fields': {

        },
        'time_field': 'create_time'
    },
    'members': {
        'source_type': 'calc_add',
        'models': ['self_members', 'manual_service_members']
    },
    'experience_users': {
        'source_type': 'db',
        'model': UserVip,
        'query_fields': {
            'user__is_active': True,
            'vip_role__code_name': 'experience_user'
        },
        'time_field': 'create_time'
    },
    'self_members': {
        'source_type': 'db',
        'model': UserVip,
        'query_fields': {
            'is_active': True,
            'vip_role__level__gte': 3
        },
        'time_field': 'create_time'
    },
    'manual_service_members': {
        'source_type': 'db',
        'model': UserManualService,
        'query_fields': {
            'user__is_active': True
        },
        'time_field': 'create_time'
    },
    'feeds': {
        'source_type': 'db',
        'model': Feed,
        'query_fields': {

        },
    },
    'resumes': {
        'source_type': 'db',
        'model': ResumeBuyRecord,
        'query_fields': {

        },
        'time_field': 'op_time'
    },
    'user_access_log': {
        'source_type': 'db',
        'model': UserAccessLog,
        'query_fields': {

        },
        'time_field': 'access_time'
    },
    'statistic': {
        'source_type': 'db',
        'model': StatisticsModel,
        'query_fields': {

        },
        'time_field': 'access_time'
    },
    'feed_result': {
        'source_type': 'db',
        'model': FeedResult,
        'query_fields': {
            'is_recommended': True
        },
        'time_field': 'calc_time'
    },
    'tasks': {
        'source_type': 'db',
        'model': UserAcceptTask,
        'query_fields': {

        },
        'time_field': 'update_time'
    },
    'upload_resumes': {
        'source_type': 'db',
        'model': UploadResume,
        'query_fields': {

        },
        'time_field': 'create_time'
    },
    'do_tasks': {
        'source_type': 'db',
        'model': UserTaskResume,
        'query_fields': {

        },
        'time_field': 'upload_time'
    },
    'task_coin_records': {
        'source_type': 'db',
        'model': TaskCoinRecord,
        'query_fields': {

        },
        'time_field': 'record_time'
    },
    'down_resumes': {
        'source_type': 'db',
        'model': DownloadResumeMark,
        'query_fields': {

        },
        'time_field': 'mark_time'
    },
    'pub_feeds': {
        'source_type': 'db',
        'model': PubFeedData,
        'query_fields': {

        },
        'time_field': 'pub_time'
    },
    'send_cards': {
        'source_type': 'db',
        'model': SendCompanyCard,
        'query_fields': {

        },
        'time_field': 'send_time'
    },
    'fav_resumes': {
        'source_type': 'db',
        'model': UserWatchResume,
        'query_fields': {
            'type': 1
        },
        'time_field': 'add_time'
    },
    'weixin_msgs': {
        'source_type': 'db',
        'model': MsgSendLog,
        'query_fields': {

        },
        'time_field': 'add_time'
    },
    'user_mark_logs': {
        'source_type': 'db',
        'model': UserMarkLog,
        'query_fields': {

        },
        'time_field': 'mark_time'
    },
    'task_system': {
        'source_type': 'db',
        'model': TaskFinishedStatus,
        'query_fields': {
            'finished_status': 2
        },
        'time_field': 'finished_time'
    },
    'staff': {
        'source_type': 'db',
        'model': User,
        'query_fields': {
            'is_staff': True
        },
        'time_field': 'date_joined'
    }
}


def str_to_class(field):
    try:
        identifier = getattr(sys.modules[__name__], field)
    except AttributeError:
        raise NameError("%s doesn't exist." % field)
    if isinstance(identifier, (types.ClassType, types.TypeType)):
        return identifier
    raise TypeError("%s is not a class." % field)


class DataBuilder(object):

    def __init__(self, start_time, end_time, ret_list):
        self.start_time = start_time
        self.end_time = end_time
        self.origin_data = {}
        self.make_data_struct(ret_list=ret_list)

    def make_data_struct(self, ret_list):
        for key in ret_list:
            self.origin_data[key] = key

    def query_data(self, model, **kwargs):

        return model.objects.filter(
            **kwargs
        )

    def make_query_condition(self, key, time_field, query_fields):
        start_time = self.start_time
        end_time = self.end_time
        if 'all_data' in key:
            start_time = all_data_start_time
        if 'first_data' in key:
            start_time = first_data_start_time

        condition = {}
        if time_field:
            condition.update(
                {
                    "{0}__gte".format(time_field): start_time,
                    "{0}__lt".format(time_field): end_time,
                }
            )
        condition.update(query_fields)

        return condition

    def build_data(self):
        for key in self.origin_data:

            if 'all_data' in key:
                origin_data_template = today_origin_data_template[key[9:]]
            elif 'first_data' in key:
                origin_data_template = today_origin_data_template[key[11:]]
            else:
                origin_data_template = today_origin_data_template[key]

            source_type = origin_data_template.get('source_type')
            if source_type == 'db':
                time_field = origin_data_template.get('time_field')
                query_fields = origin_data_template.get('query_fields')
                model = origin_data_template.get('model')
                condition = self.make_query_condition(
                    key=key,
                    time_field=time_field,
                    query_fields=query_fields
                )

                origin_data = self.query_data(
                    model=model,
                    **condition
                )
                self.origin_data[key] = origin_data

        for key in self.origin_data:

            if 'all_data' in key:
                origin_data_template = today_origin_data_template[key[9:]]
            elif 'first_data' in key:
                origin_data_template = today_origin_data_template[key[11:]]
            else:
                origin_data_template = today_origin_data_template[key]

            source_type = origin_data_template.get('source_type')
            if source_type == 'calc_add':
                models = origin_data_template.get('models')
                tmp_list = []
                [tmp_list.extend(self.origin_data[model_key]) for model_key in models]
                self.origin_data[key] = tmp_list
