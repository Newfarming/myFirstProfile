# coding: utf-8

import datetime

import mongoengine


class UserAccessLog(mongoengine.Document):
    """用户访问日志"""

    user_name = mongoengine.StringField(default='')
    app_name = mongoengine.StringField(default='')
    ip = mongoengine.StringField(default='')
    access_time = mongoengine.DateTimeField(default=datetime.datetime.now())
    refer_url = mongoengine.StringField(default='')
    access_url = mongoengine.StringField(default='')
    user_agent = mongoengine.StringField(default='')

    meta = {
        'collection': 'user_access_log',
        'indexes': [
            'user_name',
            'access_time',
            'access_url'
        ],
    }
