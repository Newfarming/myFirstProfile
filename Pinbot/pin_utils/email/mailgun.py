# coding: utf-8

import requests

from pin_utils.retry import retry

from pin_celery.celery_app import app

TIMEOUT_EXCEPTION = requests.exceptions.ConnectionError


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


asyn_gun_mail = app.task(name='gun-send-mail')(MailGunUtils.send_mail)
