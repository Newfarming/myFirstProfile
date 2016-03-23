# coding:utf-8

from Brick.settings import BROKER_URL
from celery.schedules import crontab


CELERY_IMPORTS = (
    "Brick.Utils.email.send_mail",
    "Brick.App.my_resume.resume_utils",
    "Brick.Schedule.tasks",
    "Brick.App.run.task",
)

CELERY_RESULT_BACKEND = "amqp"

CELERYBEAT_SCHEDULE = {
    # 每天00: 01 清理一次推荐条数限制
    # celery use UTC time
    # 16 + 0080 is 24:00
    # 17 + 0080 is 01:00
    'clear-reco-limit': {
        'task': 'clear-reco-limit',
        'schedule': crontab(minute=1, hour=16),
    },
    'daily-report': {
        'task': 'daily-report',
        'schedule': crontab(hour=16, minute=20),
    },
    'week-report': {
        'task': 'week-report',
        'schedule': crontab(hour=17, minute=21, day_of_week='sun'),
    },
}

CELERY_TIMEZONE = 'Asia/Shanghai'
