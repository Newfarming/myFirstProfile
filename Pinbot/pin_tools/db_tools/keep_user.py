# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from users.models import UserProfile

from pin_utils.django_utils import (
    get_today
)


FROM_DATE = datetime.datetime(2015, 7, 9)
TODAY = get_today()
FILE_NAME = 'user_acc.csv'

RANGE_DAYS = (TODAY - FROM_DATE).days
CSV_FILE = 'keep.csv'


def login_user_group_by_date():
    with open(FILE_NAME, 'r') as login_file:
        login_user_list = login_file.readlines()

    login_user_mapper = {
        (FROM_DATE + datetime.timedelta(days=i)).strftime('%Y-%m-%d'): []
        for i in xrange(RANGE_DAYS)
    }

    for i in login_user_list:
        d, u, _ = i.split(',')
        d = d.strip()
        u = u.strip()
        login_user_mapper[d].append(u)
    return login_user_mapper


def reg_user_group_by_date():
    reg_user_mapper = {
        (FROM_DATE + datetime.timedelta(days=i)).strftime('%Y-%m-%d'): []
        for i in xrange(RANGE_DAYS)
    }
    register_user_list = UserProfile.objects.filter(
        user__date_joined__gte=FROM_DATE,
        user__date_joined__lt=TODAY,
        user__is_active=True,
    ).values_list('user__username', 'user__date_joined')

    for i in register_user_list:
        u, d = i
        d = d.strftime('%Y-%m-%d')
        reg_user_mapper[d].append(u)
    return reg_user_mapper


def calc_keep_user():
    reg_mapper = reg_user_group_by_date()
    login_mapper = login_user_group_by_date()

    stat = {
        (FROM_DATE + datetime.timedelta(days=i)).strftime('%Y-%m-%d'): {
            'next': 0,
            'next_3': 0,
            'next_7': 0,
            'next_30': 0,
        }
        for i in xrange(RANGE_DAYS)
    }
    for i, v in stat.iteritems():
        next_date = (datetime.datetime.strptime(i, '%Y-%m-%d') + datetime.timedelta(1)).strftime('%Y-%m-%d')
        next3_date = (datetime.datetime.strptime(i, '%Y-%m-%d') + datetime.timedelta(3)).strftime('%Y-%m-%d')
        next7_date = (datetime.datetime.strptime(i, '%Y-%m-%d') + datetime.timedelta(7)).strftime('%Y-%m-%d')
        next30_date = (datetime.datetime.strptime(i, '%Y-%m-%d') + datetime.timedelta(30)).strftime('%Y-%m-%d')

        reg_user = reg_mapper[i]
        next_login_user = login_mapper.get(next_date, [])
        next3_login_user = login_mapper.get(next3_date, [])
        next7_login_user = login_mapper.get(next7_date, [])
        next30_login_user = login_mapper.get(next30_date, [])

        v['next'] = len(list(set(next_login_user).intersection(set(reg_user))))
        v['next_3'] = len(list(set(next3_login_user).intersection(set(reg_user))))
        v['next_7'] = len(list(set(next7_login_user).intersection(set(reg_user))))
        v['next_30'] = len(list(set(next30_login_user).intersection(set(reg_user))))
        v['reg'] = len(reg_user)

    with open(CSV_FILE, 'aw') as f:
        for k, v in stat.iteritems():
            f.write('{0}, {1}, {2}, {3}, {4}\n'.format(k, v['reg'], v['next'], v['next_7'], v['next_30']))

    return stat

if __name__ == '__main__':
    calc_keep_user()
