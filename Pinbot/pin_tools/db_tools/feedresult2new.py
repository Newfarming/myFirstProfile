# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from mongoengine import connect

from Pinbot.settings import OTHER_DATABASE
from feed.models import FeedResult
from feed.models import UserReadResume

from pin_utils.django_utils import (
    get_today,
    get_tomommow,
)


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


def get_read_status(feed_result):
    feed_id = str(feed_result.feed.id)
    resume_id = str(feed_result.resume.id)

    user_resume_read = UserReadResume.objects.filter(
        feed_id=feed_id,
        resume_id=resume_id,
    )

    return 'read' if user_resume_read else 'unread'


def main():
    old_feed_results = FeedResult.objects(
        published=True,
        display_time=None,
    ).order_by('-calc_time')

    today = get_today()
    tomorrow = get_tomommow()

    caculate_time = today + datetime.timedelta(hours=14)

    for feed_result in old_feed_results:
        calc_time = feed_result.calc_time
        if calc_time < caculate_time:
            feed_result.display_time = today
        else:
            feed_result.display_time = tomorrow
        feed_result.user_read_status = get_read_status(feed_result)
        feed_result.save()
        print feed_result.id, calc_time, feed_result.user_read_status, feed_result.display_time

def notexistedresume():
    from bson import DBRef
    i = 20000
    j = 0
    item = 4
    for runitem in range(1,35):
        feed_results = FeedResult.objects.filter(published=True).skip(item*5000).limit(5000)
        item += 1

        for feed_result in feed_results:
            print i
            i += 1
            if isinstance(feed_result.resume, DBRef):
                j += 1
                print str(feed_result.resume)
    print 'total: '+j

def fix_read_status():
    unread_feed_results = FeedResult.objects(
        display_time__ne=None,
    ).order_by('-calc_time')

    print 'unread_feed_read_status_count', unread_feed_results.count()

    for fr in unread_feed_results:
        read_status = get_read_status(fr)
        fr.user_read_status = read_status
        fr.save()
        print fr.feed.id, read_status


if __name__ == '__main__':
    fix_read_status()
