# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from mongoengine import connect

from Pinbot.settings import OTHER_DATABASE
from feed.models import Feed,Feed2,UserFeed,UserFeed2
from bson import ObjectId
from django.template.loader import render_to_string

from users.models import User
import time


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

def mysql_to_mongo():
    i = 0
    user_feeds = UserFeed.objects.all().order_by("-add_time")[:10]
    for user_feed in user_feeds:
        print i
        i += 1
        if user_feed.user_charge_pkg:
            if not user_feed.is_deleted:
                object_id = user_feed.feed.feed_obj_id
                feed_mysql = user_feed.feed
                feed_mysql.expire_time = user_feed.expire_time
                feed_mysql.save()

                feed_mongo = Feed2.objects.get(pk=ObjectId(object_id))
                feed_mongo.expire_time = user_feed.expire_time
                feed_mongo.save()

                user_feed_mongos = UserFeed2.objects.filter(feed=ObjectId(object_id))
                for user_feed_mongo in user_feed_mongos:
                    user_feed_mongo.expire_time = user_feed.expire_time
                    user_feed_mongo.save()

# def send_notify_email(request):
#     from users.views import send_email
#     from Pinbot.settings import STATIC_URL
#     from Pinbot.settings import DEFAULT_FROM_EMAIL
#     from feed.models import Feed2
#     subject = render_to_string('email-template/7days-subject.txt')
#     message = render_to_string('email-template/7days.html',locals())
#     print message
#     subject = ''.join(subject.splitlines())
#     usernames = Feed2.objects.filter(is_active=True).distinct('username')
#     for username in usernames:
#         email = 'mf1032025@sina.com'
#         result,info = send_email(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, email=email)
#         time.sleep(10)
#     data = {'status':'ok','msg':''}


def update_mongo():
    feeds = Feed2.objects.filter(feed_expire_time=None)
    print len(feeds)
    for feed in feeds:
        add_time = feed.add_time
        feed_expire_time = add_time + datetime.timedelta(days=8)
        feed.feed_expire_time = feed_expire_time
        feed.save()

def delete_collect_resume():
    i = 0
    from resumes.models import CollectedResume
    for runitem in range(2,200):
        resumes = CollectedResume.objects.filter(status='processed').skip(runitem*5000).limit(10000)
        url_set = set()
        for resume in resumes:
            if resume.url:
                url_set.add(resume.url)
        print len(url_set)
        for url in url_set:
            dup_resumes = CollectedResume.objects.filter(url=url, status='processed').order_by('-createtime')
            if len(dup_resumes) > 1:
                print url
                dup_resumes=dup_resumes[1:]
                for resume in dup_resumes:
                    print i
                    resume.delete()
                    i += 1

#     j = 0
#     resumes = CollectedResume.objects.filter()
#     for resume in resumes:
#         url = resume.url
#         dup_resumes = CollectedResume.objects.filter(url=url, status='processed').order_by('-createtime')
#         print len(dup_resumes)
#         if len(dup_resumes) >= 3:
#             dup_resumes = dup_resumes[0:len(dup_resumes) - 2]
#             for dup_resume in dup_resumes:
#                 j += 1
#                 dup_resume.delete()


if __name__ == '__main__':
    update_mongo()
#     delete_collect_resume()
