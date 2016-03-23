# coding: utf-8

from django.core.mail import EmailMessage

from Pinbot.settings import DEFAULT_FROM_EMAIL

from pin_celery.celery_app import app


class DjangoMail(object):

    @classmethod
    def send_mail(cls, to, subject, html):
        msg = EmailMessage(
            subject,
            html,
            DEFAULT_FROM_EMAIL,
            [to],
        )
        msg.content_subtype = "html"
        result = msg.send()
        return result


asyn_django_mail = app.task(name='django-send-mail')(DjangoMail.send_mail)
