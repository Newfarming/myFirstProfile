# coding: utf-8

'''
author: runforever@163.com

module: send email utils

function:
    MailUtils.send_mail()
    MailUtils.send_bat_mail()

    async_send_mail() # celery send mail
    async_send_bat_mail() # celery send mail
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import requests
import datetime

from pin_celery.celery_app import app
from pin_utils.retry import retry

TIMEOUT_EXCEPTION = requests.exceptions.ConnectionError


class MailUtils(object):
    '''
    send mail utils
    function:
        send_mail
        send_bat_mail

    param:
    BAT_API_USER  sendcloud api user for send bat email
    TRIGGER_API_USER sendcloud api user for send trigger user
    API_KEY sendcloud api key
    REPLY_TO email reply user
    EMAIL_FROM email from user
    FROM_NAME email from name
    '''
    url = 'http://sendcloud.sohu.com/webapi/mail.send.json'
    BAT_API_USER = "bat_pinbot_mail"
    TRIGGER_API_USER = "mail_pinbot_me"
    API_KEY = "NxBZG7vOdwGtXD2i"
    REPLY_TO = "team@pinbot.me"
    EMAIL_FROM = "team@mail.pinbot.me"
    FROM_NAME = 'Pinbot'
    create_label_url = 'http://sendcloud.sohu.com/webapi/label.create.json?api_user=%s&api_key=%s&labelName=' % (
        BAT_API_USER,
        API_KEY
    )
    delete_label_url = 'http://sendcloud.sohu.com/webapi/label.delete.json?api_user=%s&api_key=%s&labelId=' % (
        BAT_API_USER,
        API_KEY
    )
    BOUNCES_EMAIL_API = 'http://sendcloud.sohu.com/webapi/bounces.get.json'
    UNSUBSCRIBES_EMAIL_API = 'http://sendcloud.sohu.com/webapi/unsubscribes.get.json'
    SPAM_REPORT_EMAIL_API = 'https://sendcloud.sohu.com/webapi/spamReported.get.json'

    @classmethod
    @retry(TIMEOUT_EXCEPTION, delay=7)
    def send_mail(
        cls,
        email_to,
        subject,
        html,
        files={},
        email_from=EMAIL_FROM,
        fromname=FROM_NAME,
        user=TRIGGER_API_USER,
        reply_to=REPLY_TO,
        label=None
    ):
        '''
        function:
            send trigger email
        param:
            email_to  email addr
            subject   email subject
            html      email content
            file      email attachment
            email_form  email from address
            fromname    eamil from name
            user        sendcloud email user
            reply_to    email to reply user address
            label     email tag label
        '''
        params = {
            "api_user": user,
            "api_key": cls.API_KEY,
            "to": email_to,
            "replyto": reply_to,
            "from": email_from,
            "fromname": fromname,
            "subject": subject,
            "html": html,
        }

        if label:
            params['label'] = label

        send_result = requests.post(cls.url, files=files, data=params)
        return send_result.json()

    @classmethod
    def bat_mail(
        cls,
        email_to,
        subject,
        html,
        files={},
        email_from=EMAIL_FROM,
        fromname=FROM_NAME,
        user=BAT_API_USER,
        reply_to=REPLY_TO,
        label=None
    ):
        '''
        function:
            send bat email
        param:
            email_to  email addr
            subject   email subject
            html      email content
            file      email attachment
            email_form  email from address
            fromname    eamil from name
            user        sendcloud email user
            reply_to    email to reply user address
        '''
        return cls.send_mail(
            email_to,
            subject,
            html,
            files,
            email_from,
            fromname,

            user=user,
            reply_to=reply_to,
            label=label
        )

    @classmethod
    def sendcloud_api(cls, api_url, params):
        res = requests.get(api_url, params=params)
        return res.json()

    @classmethod
    def sendcloud_useless_email(cls, api_url, useless_key):
        start_date_str = '2014-11-01'
        end_date_str = datetime.datetime.now().strftime('%Y-%m-%d')

        useless_email = []
        for i in xrange(0, 1000, 100):
            params = {
                'api_user': cls.BAT_API_USER,
                'api_key': cls.API_KEY,
                'start_date': start_date_str,
                'end_date': end_date_str,
                'start': i,
            }

            json_res = cls.sendcloud_api(api_url, params)
            if json_res.get('message') != 'success':
                break

            email_list = [record.get('email', '') for record in json_res.get(useless_key, [])]
            if not email_list:
                break

            useless_email.extend(email_list)

            if len(email_list) < 100:
                break

        return useless_email

    @classmethod
    def get_bounce_email(cls):
        return cls.sendcloud_useless_email(cls.BOUNCES_EMAIL_API, 'bounces')

    @classmethod
    def get_unsubscribes_email(cls):
        return cls.sendcloud_useless_email(cls.UNSUBSCRIBES_EMAIL_API, 'unsubscribes')

    @classmethod
    def get_spam_report_email(cls):
        return cls.sendcloud_useless_email(cls.SPAM_REPORT_EMAIL_API, 'bounces')

    @classmethod
    def get_useless_email(cls):
        useless_email = []
        bounce_email = cls.get_bounce_email()
        unsubscribes_email = cls.get_unsubscribes_email()
        spam_report_email = cls.get_spam_report_email()

        useless_email.extend(bounce_email)
        useless_email.extend(unsubscribes_email)
        useless_email.extend(spam_report_email)

        return list(set(useless_email))


class SubMailUtils(object):

    SEND_API_URL = 'https://api.submail.cn/mail/send.json'
    APP_ID = '10660'
    APP_KEY = 'aa1a1abf9c8793e18f17f54ed8480e30'

    BAT_APP_ID = '10661'
    BAT_APP_KEY = '9f181e79ffed6def4630c79a8035c5d6'
    EMAIL_FROM = 'team@smail.pinbot.me'
    FROM_NAME = '聘宝'

    @classmethod
    def send_mail(
            cls,
            email_to,
            subject,
            html,
            files={},
            email_from=EMAIL_FROM,
            fromname=FROM_NAME,
            app_id=APP_ID,
            app_key=APP_KEY,
            label=None,
    ):
        params = {
            "appid": app_id,
            "signature": app_key,
            "to": email_to,
            "from": email_from,
            "from_name": fromname,
            "subject": subject,
            "html": html,
        }
        if not email_to:
            return False

        send_result = requests.post(cls.SEND_API_URL, data=params)
        return send_result.json()

    @classmethod
    def bat_mail(
            cls,
            email_to,
            subject,
            html,
            files={},
            email_from=EMAIL_FROM,
            fromname=FROM_NAME,
            app_id=BAT_APP_ID,
            app_key=BAT_APP_KEY,
            label=None,
    ):
        return cls.send_mail(
            email_to,
            subject,
            html,
            files={},
            email_from=email_from,
            fromname=fromname,
            app_id=app_id,
            app_key=app_key,
            label=None,
        )


asyn_bat_mail = app.task(name='send-bat-mail')(SubMailUtils.bat_mail)
asyn_send_mail = app.task(name='send-trigger-mail')(SubMailUtils.send_mail)
sendcloud_bat_mail = app.task(name='sendcloud-bat-mail')(MailUtils.bat_mail)
