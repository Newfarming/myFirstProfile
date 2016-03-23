# coding:utf-8

from Pinbot.settings import OTHER_DATABASE
from celery.schedules import crontab

address = OTHER_DATABASE.get('rabbitmq').get('host')
username = OTHER_DATABASE.get('rabbitmq').get('user')
password = OTHER_DATABASE.get('rabbitmq').get('password')

BROKER_URL = 'amqp://%s:%s@%s:5672//' % (username, password, address)

CELERY_IMPORTS = (
    "pin_celery.tasks",
    "pin_utils.email.send_mail",
    "pin_utils.email.mailgun",
    "pin_utils.email.django_mail",
    "app.vip.tasks",
    "app.partner.tasks",
    "app.sendemail.tasks",
    "app.activity.tasks",
    "pin_utils.sms.sms_code",
    "pin_utils.user_log",
    "pin_utils.spider_utils",
    "app.task_system.tasks",
    "app.resume.tasks",
    "pin_utils.sms.sms_utils",
)

CELERY_RESULT_BACKEND = "amqp"

CELERYBEAT_SCHEDULE = {
    # 每天00: 01 清理一次推荐条数限制
    # celery use UTC time
    # 16 + 0080 is 24:00
    # 17 + 0080 is 01:00
    'vip-point-task': {
        'task': 'vip-point-task',
        'schedule': crontab(hour=16, minute=10, day_of_week='sun'),
    },
    'pinbot-reco-resume-task': {
        'task': 'pinbot-reco-resume-task',
        'schedule': crontab(minute=0, hour='*/2'),
    },
    'pinbot-load-egg-task': {
        'task': 'pinbot-load-egg-task',
        'schedule': crontab(minute=1, hour=16),
    },
    'sync-useless-email-task': {
        'task': 'sync-useless-email-task',
        'schedule': crontab(minute=0, hour='*/2'),
    },
    'pinbot-clean-reco-task': {
        'task': 'pinbot-clean-reco-task',
        'schedule': crontab(minute=0, hour='*/4'),
    },
    'expire-manual-service': {
        'task': 'expire-manual-service',
        'schedule': crontab(minute=0, hour='*/5'),
    },
    'expire-self-service': {
        'task': 'expire-self-service',
        'schedule': crontab(minute=20, hour='*/6'),
    },
    'renew-experience-user': {
        'task': 'renew-experience-user',
        'schedule': crontab(minute=30, hour='*/6'),
    },
    'send-interview-alarm-task': {
        'task': 'send-interview-alarm',
        'schedule': crontab(minute=0, hour='0,1,2,3,4,5,6,7,8,9,10,11'),
    },
}

CELERY_TIMEZONE = 'Asia/Shanghai'
