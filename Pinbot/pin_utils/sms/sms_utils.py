# coding: utf-8

import requests
from django.conf import settings

from pin_celery.celery_app import app


class SMSUtils(object):

    SMS_SEND_URL = settings.SMS_SEND_URL
    SMS_SEND_APIKEY = settings.SMS_SEND_APIKEY

    @classmethod
    def send(cls, phone, content):
        param = {
            'apikey': cls.SMS_SEND_APIKEY,
            'mobile': phone,
            'text': content,
        }

        res = requests.post(
            url=cls.SMS_SEND_URL,
            data=param,
        )
        ret = res.json()
        return ret

asyn_send_sms = app.task(name='send-sms-task')(SMSUtils.send)
