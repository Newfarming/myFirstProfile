# coding: utf-8

import mongoengine

from . import models


class FeedParser(mongoengine.Document):
    extend_titles = mongoengine.DictField()
    extend_keywords = mongoengine.DictField()


class FeedResultFilter(mongoengine.Document):
    """
    记录用户对定制的筛选行为
    """
    add_time = mongoengine.DateTimeField(verbose_name='添加时间')
    feed = mongoengine.ReferenceField(models.Feed2, verbose_name='定制')
    filters = mongoengine.DictField(verbose_name='筛选条件')
    username = mongoengine.StringField(verbose_name='用户名')

    meta = {
        'index_background': True,
        'indexes': [
            'add_time',
            'username',
            'feed',
        ]
    }
