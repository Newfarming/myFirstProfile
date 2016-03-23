# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from mongoengine import connect

from Pinbot.settings import OTHER_DATABASE
from feed.models import (
    FeedResult,
    Feed2,
    EmailFeedData,
)

from app.special_feed.feed_utils import FeedCacheUtils

Mongo_setting = OTHER_DATABASE['mongo']
host = Mongo_setting.get('host', '')
username = Mongo_setting.get('user', '')
password = Mongo_setting.get('password', '')

print host, username, password

connect(
    'recruiting',
    host=host,
    username=username,
    password=password,
)
CONVERT_CACU_TIME = datetime.datetime.strptime(
    '2014-09-09 14',
    '%Y-%m-%d %H'
)


def convert2pub_data(feed):
    username = feed.username
    feed_oid = feed.id

    feed_results = FeedResult.objects(
        feed=feed_oid,
        calc_time__gte=CONVERT_CACU_TIME,
        published=True,
    )

    if not feed_results:
        return False

    FeedCacheUtils.add_feed_id_update_cache(feed_oid)

    pub_admin = 'runforever@163.com'
    resumes = [fr.resume.id for fr in feed_results]

    email_feed = EmailFeedData.objects(
        feed=feed_oid,
        is_send=False,
    ).first()

    if email_feed:
        EmailFeedData.objects(
            feed=feed_oid,
            is_send=False,
        ).update(
            set__pub_admin=pub_admin,
            add_to_set__resumes=resumes,
        )
    else:
        email_feed = EmailFeedData(
            email=username,
            pub_admin=pub_admin,
            feed=feed_oid,
            resumes=resumes,
        )
    email_feed.save()


def main():
    feeds = Feed2.objects(deleted=False)

    for feed in feeds:
        convert2pub_data(feed)

if __name__ == '__main__':
    main()
