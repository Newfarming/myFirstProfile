# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from django.template.loader import render_to_string

from feed.models import (
    UserFeed2,
    Feed2,
)

from pin_utils.django_utils import (
    get_today,
    get_tomommow,
)
from pin_utils.email.send_mail import (
    asyn_bat_mail,
)

EMAIL_SUBJECT = u'［待激活］你的定制需求%s已使用满7天请激活'


def get_email_subject(feed):
    keyword_list = feed.keywords.replace(u'，', ',').split(',')

    if len(keyword_list) > 3:
        keyword_list[3] = '...'
    keyword = u'、'.join(keyword_list[:4])
    subject = EMAIL_SUBJECT % keyword
    return subject


def is_deleted_feed(feed):
    feed_has_deleted = UserFeed2.objects(
        is_deleted=True,
        feed=feed.id,
    )
    return True if feed_has_deleted else False


def main():
    today = get_today()
    tomorrow = get_tomommow()

    expire_feeds = Feed2.objects(
        feed_expire_time__gte=today,
        feed_expire_time__lt=tomorrow,
        feed_type=1,
    )

    for feed in expire_feeds:
        if is_deleted_feed(feed):
            continue

        email = feed.username
        subject = get_email_subject(feed)
        message = render_to_string(
            'email-template/activate_tips.html',
            {'feed': feed}
        )

        result = asyn_bat_mail(
            email,
            subject,
            message,
        )
        if result.get('status') == 'success':
            print '%s send email success' % email
        else:
            print '%s send email error, result %s' % (email, result)


if __name__ == '__main__':
    main()
