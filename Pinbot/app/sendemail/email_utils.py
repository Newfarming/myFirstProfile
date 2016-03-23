# coding: utf-8

from django.core.cache import cache

from pin_utils.email.send_mail import MailUtils


class UselessEmailUtils(object):

    key = 'SENDCLOUD_USELESS_EMAIL'

    @classmethod
    def get_useless_email(cls):
        useless_email = cache.get(cls.key, [])
        if not useless_email:
            useless_email = cls.sync_useless_email()
        return useless_email

    @classmethod
    def sync_useless_email(cls):
        useless_email = MailUtils.get_useless_email()
        cache.set(cls.key, useless_email, 0)
        return useless_email
