# coding: utf-8

import datetime
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from mongoengine import connect

from Pinbot.settings import OTHER_DATABASE
from feed.models import (
    FeedResult,
    Feed2,
)
from app.special_feed.feed_utils import FeedCacheUtils

from pin_utils.django_utils import (
    get_tomommow,
    get_today,
)

Mongo_setting = OTHER_DATABASE['mongo']
host = Mongo_setting.get('host', '')
username = Mongo_setting.get('user', '')
password = Mongo_setting.get('password', '')

print host, username, password

CONVERT_CACU_TIME = datetime.datetime.strptime(
    '2014-09-09 14',
    '%Y-%m-%d %H'
)

connect(
    'recruiting',
    host=host,
    username=username,
    password=password,
)


def add_update_cache(feed):
    tomorrow = get_tomommow()
    today = get_today()
    feed_id = feed.id

    feed_results = FeedResult.objects(
        feed=feed_id,
        display_time__gte=today,
        display_time__lt=tomorrow,
    )
    resume_sids = [str(fr.resume.id) for fr in feed_results]
    FeedCacheUtils.add_update_cache(feed_id, resume_sids)


def main():
    feeds = Feed2.objects()

    for feed in feeds:
        add_update_cache(feed)


if __name__ == '__main__':
    main()
