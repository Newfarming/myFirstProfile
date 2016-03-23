# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from users.models import UserProfile


def load_service_level():
    user_level_mapper = {}

    with open('/Users/runforever/Downloads/client_level.csv') as f:
        log_lines = f.readlines()

    for i in log_lines:
        u, c = i.split(',')
        u = u.strip()
        c = int(c.strip())
        user_level_mapper[u] = c
    user_level_mapper = {
        i: v
        for i, v in user_level_mapper.iteritems() if v > 1
    }
    return user_level_mapper


def import_service_level():
    user_level_mapper = load_service_level()
    group_by_times = {}
    for key, value in sorted(user_level_mapper.iteritems()):
        group_by_times.setdefault(value, []).append(key)

    UserProfile.objects.filter(
        user__username__in=user_level_mapper.keys()
    ).update(
        client_level=1
    )
    for i, v in group_by_times.iteritems():
        UserProfile.objects.filter(
            user__username__in=v,
        ).update(
            login_days=i,
        )

if __name__ == '__main__':
    import_service_level()
