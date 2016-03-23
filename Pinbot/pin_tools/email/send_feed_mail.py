# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import base64
import datetime

from django.contrib.auth.models import User
from django.template.loader import render_to_string

from users.models import (
    UserProfile,
)

from feed.models import (
    EmailFeedData,
    Feed2,
    EmailSendInfo,
    FeedResult,
)
from app.partner.models import (
    UserTaskResume,
)

from pin_utils.django_utils import (
    get_tomommow,
    get_today,
    get_yesterday,
)
from pin_utils.email.send_mail import (
    asyn_bat_mail,
)


def get_display_resumes(feed_id, resumes):
    feed_results = FeedResult.objects(
        feed=feed_id,
        resume__in=resumes,
        published=True,
    ).order_by('-job_related').select_related()[:3]

    display_resumes = [fr.resume for fr in feed_results]
    return display_resumes


def get_email_token(username, feed_id):
    token = username + "&&&" + str(feed_id)
    token = base64.b64encode(token)
    return token


def get_email_data(pub_feed):
    after_tomorrow = get_tomommow() + datetime.timedelta(days=1)

    username = pub_feed.email
    last_send_info = EmailSendInfo.objects(username=username).first()

    if last_send_info:
        send_frequency = last_send_info.sendFrequency
        last_send_date = last_send_info.lastSendDate
        need_send = (
            send_frequency
            and last_send_date + datetime.timedelta(days=send_frequency) <= after_tomorrow
        )
    else:
        user = User.objects.filter(username=username)[0]
        last_send_info = EmailSendInfo(
            user=user.id,
            username=username,
        )
        need_send = True

    if not need_send:
        return False

    user_pub_feeds = EmailFeedData.objects(
        email=username,
        is_send=False,
    ).select_related()

    if not user_pub_feeds:
        return False

    feed_info_list = []
    total_num = 0
    keyword_list = []

    for pub_feed in user_pub_feeds:
        feed_id = pub_feed.feed.id
        feed = Feed2.objects(id=feed_id, deleted=False).first()
        if not feed:
            continue
        keywords = feed.title if feed.title else feed.keywords
        keyword_list.append(keywords.replace(u'，', ','))
        resume_num = len(pub_feed.resumes)

        feed.feed_resumes = get_display_resumes(feed_id, pub_feed.resumes)
        feed.feed_result_num = resume_num
        feed.token = get_email_token(username, feed_id)

        total_num += resume_num
        feed_info_list.append(feed)

    keyword_list = ','.join(keyword_list).split(',')
    if len(keyword_list) > 5:
        keyword_list[4] = '...'
    keywords = ','.join(keyword_list[:5])
    subject = u'聘宝为你推荐人才－%s' % keywords

    return {
        'username': username,
        'subject': subject,
        'feed_info_list': feed_info_list,
        'total_num': total_num,
        'email_send_info': last_send_info,
    }


def get_partner_resume(username):
    today = get_today()
    yesterday = get_yesterday()
    user_task_resume = UserTaskResume.objects.select_related(
        'task',
        'task__feed',
        'resume',
    ).filter(
        task__feed__user__username=username,
        upload_time__gte=yesterday,
        upload_time__lt=today,
    ).exclude(
        resume_status=5,
    ).order_by('-id')[:2]

    count = user_task_resume.count()
    display_task_resume = user_task_resume[:2]

    for tr in display_task_resume:
        last_work_query = tr.resume.resume_works.all().order_by('-start_time')[:1]
        if last_work_query:
            tr.resume.last_work = last_work_query[0]

        last_edu_query = tr.resume.resume_educations.all().order_by('-start_time')[:1]
        if last_edu_query:
            tr.resume.last_edu = last_edu_query[0]

    return {
        'partner_resumes': display_task_resume,
        'partner_resumes_count': count,
    }


def get_receive_email(email):
    user_profile_query = UserProfile.objects.select_related(
        'user',
    ).filter(
        user__username=email,
    )
    if not user_profile_query:
        return email

    user_profile = user_profile_query[0]
    notify_email = user_profile.notify_email
    return notify_email if notify_email else email


def send_feed_mail():
    pub_feeds = EmailFeedData.objects(is_send=False)

    for pub_feed in pub_feeds:
        email = pub_feed['email']
        now = datetime.datetime.now()

        email_data = get_email_data(pub_feed)
        if not email_data:
            continue

        partner_resume = get_partner_resume(email)
        email_data.update(partner_resume)

        subject = email_data['subject']
        message = render_to_string('reco_feed_email.html', email_data)
        email_send_info = email_data['email_send_info']
        receive_email = get_receive_email(email)

        result = asyn_bat_mail(
            receive_email,
            subject,
            message,
        )

        if result.get('status') == 'success':
            EmailFeedData.objects(email=email, is_send=False).update(
                set__is_send=True,
            )
            email_send_info.lastSendDate = now
            email_send_info.save()
            print '%s send email success' % email
        else:
            print '%s send email error, result %s' % (email, result)

if __name__ == '__main__':
    send_feed_mail()
