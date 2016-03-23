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
os.environ['DJANGO_SETTINGS_MODULE'] = 'Brick.settings'

import requests

from Brick.BCelery.celery_app import app
from Brick.Utils.retry import retry

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
        )


class MailGunUtils(object):

    API = 'https://api.mailgun.net/v2/email.pinbot.me/messages'
    API_KEY = 'key-02bdc2dd409792588e442476b7d1b441'
    FROM = '聘宝<Pinbot@email.Pinbot.me>'

    @classmethod
    @retry(TIMEOUT_EXCEPTION, delay=7)
    def send_mail(cls, to, subject, html):
        result = requests.post(
            cls.API,
            auth=("api", cls.API_KEY),
            data={
                "from": cls.FROM,
                "to": to,
                "subject": subject,
                "html": html,
            }
        )
        return True if result.status_code == 200 else False


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

asyn_mg_mail = app.task(name='send-mg-mail')(MailGunUtils.send_mail)
