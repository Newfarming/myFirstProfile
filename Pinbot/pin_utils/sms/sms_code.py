# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import shortuuid
import requests
from django.core.cache import cache
from django.conf import settings
from pin_utils.retry import retry
from pin_celery.celery_app import app

SMS_SEND_URL = settings.SMS_SEND_URL
SMS_SEND_APIKEY = settings.SMS_SEND_APIKEY
SMS_TEMPLATES = settings.SMS_TEMPLATES
SMS_CODE_EXPIRE_TIME = settings.SMS_CODE_EXPIRE_TIME

TIMEOUT_EXCEPTION = requests.exceptions.ConnectionError


class SmsCode(object):

    @classmethod
    def generation_code(self, mobile, action_name):
        sms_code = shortuuid.ShortUUID(alphabet="0123456789").random(length=6)
        code_key = '{0}_{1}'.format(mobile, action_name)
        cache.set(
            code_key,
            sms_code,
            SMS_CODE_EXPIRE_TIME
        )

        return sms_code

    @classmethod
    def vaild_sms_code(self, mobile, code, action_name):
        code_key = '{0}_{1}'.format(mobile, action_name)
        ret = cache.get(code_key)
        if ret == code:
            return True
        return False

    @classmethod
    def delete_cache_code(self, mobile, action_name):
        code_key = '{0}_{1}'.format(mobile, action_name)
        cache.delete(code_key)
        return True

    @classmethod
    def get_send_data(self, mobile, code, action_name):
        send_tpl_content = SMS_TEMPLATES.get(action_name)
        if not send_tpl_content:
            return False
        text = send_tpl_content % (code, SMS_CODE_EXPIRE_TIME / 60)

        send_data = {
            'apikey': SMS_SEND_APIKEY,
            'mobile': mobile,
            'text': text
        }

        return send_data

    @classmethod
    @retry(TIMEOUT_EXCEPTION, delay=7)
    def send_sms(self, mobile, action_name):

        code = self.generation_code(mobile, action_name)
        send_data = self.get_send_data(mobile, code, action_name)
        if not send_data:
            return False
        rep = requests.post(
            url=SMS_SEND_URL,
            data=send_data
        )
        return rep.json()


asyn_send_sms_code = app.task(name='send-sms-code')(SmsCode.send_sms)
