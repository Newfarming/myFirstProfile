# coding: utf-8

import os
import sys
import time
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from django.contrib.auth.models import User
from app.task_system.tasks import send_weixin_redpack


def send_redpack(user, total_amount):
    result = send_weixin_redpack.delay(user, total_amount)
    return result


def main(filename):
    with open(filename, 'r') as read_file:
        all_data = [line.split(' ') for line in read_file]
    all_users = [data[0] for data in all_data]
    users_query = User.objects.filter(
        username__in=all_users
    )
    user_mapper = {user.username: user for user in users_query}
    for data in all_data:
        time.sleep(10)
        user = user_mapper.get(data[0])
        total_amount = float(data[1])
        if user is not None and total_amount:
            send_redpack(user, total_amount)
            print 'send to {user} redpack {total_amount}'.format(
                user=user.username,
                total_amount=total_amount,
            )

if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)
