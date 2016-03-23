# coding: utf-8

from celery import Celery, platforms
import celery_conf
import os


os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

app = Celery()
app.config_from_object(celery_conf)
platforms.C_FORCE_ROOT = True


if __name__ == '__main__':
    app.start()
