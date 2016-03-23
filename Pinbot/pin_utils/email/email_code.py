# coding: utf-8
import shortuuid
import requests
from django.core.cache import cache
from django.conf import settings

class EmailCode(object):

    @classmethod
    def generation_code(self, username, action_name):
        code = shortuuid.ShortUUID(alphabet="0123456789").random(length=6)
        code_key = '{0}_{1}'.format(username, action_name)
        cache.set(
            code_key,
            code,
            settings.EMAIL_TOKEN_EXPIRE_TIME
        )
        return code

    @classmethod
    def vaild_sms_code(slef, username, code, action_name):
        code_key = '{0}_{1}'.format(username, action_name)
        ret = cache.get(code_key)
        if ret == code:
            return True
        return False