# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from django.contrib.auth.models import User

from app.pinbot_point.point_utils import point_utils


register_date = datetime.datetime(2015, 10, 11)
max_date = register_date + datetime.timedelta(days=1)


def main():
    users = User.objects.filter(
        date_joined__gte=register_date,
        date_joined__lt=max_date,
        is_active=True,
    )

    print 'total user', users.count()

    for i in users:
        point_utils.register_point(i)
        print i.username, 'success'


if __name__ == '__main__':
    main()
