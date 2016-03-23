# coding: utf-8

from pin_celery.celery_app import app

from .email_utils import UselessEmailUtils

sync_useless_email_task = app.task(
    name='sync-useless-email-task'
)(UselessEmailUtils.sync_useless_email)
