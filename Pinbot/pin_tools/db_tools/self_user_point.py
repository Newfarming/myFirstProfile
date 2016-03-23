# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from django.db.models import Sum

from app.vip.models import (
    UserVip,
)
from app.pinbot_point.point_utils import point_utils


start_time = datetime.datetime(2015, 9, 16)


def add_self_point(uservip):
    role_point = uservip.vip_role.pinbot_point
    user = uservip.user
    aggregate_record = user.pointrecord_set.filter(
        record_time__gte=start_time,
        record_type__in=[
            'download_resume',
            'accu_return_point',
            'send_company_card',
            'self_service_point',
        ],
    ).aggregate(
        download_point=Sum('point'),
    )
    total_point = aggregate_record.get('download_point', 0)

    if total_point > 0:
        return 'not_add', 0

    add_points = role_point + total_point
    if add_points < 0:
        return 'over_max', 0

    vip_name = uservip.vip_role.vip_name
    record_type = 'self_service_point'
    detail = '购买{0}添加聘点'.format(vip_name)
    point_rule = 'self_service_point'
    return point_utils.add_point(user, add_points, record_type, detail, point_rule)


def main():
    now = datetime.datetime.now()
    uservip_query = UserVip.objects.select_related(
        'user',
        'vip_role',
    ).filter(
        is_active=True,
        expire_time__gt=now,
    ).exclude(
        vip_role__code_name='experience_user',
    )

    for uservip in uservip_query:
        status, point = add_self_point(uservip)
        username = uservip.user.username
        print '{0} add point {1}, status {2}'.format(username, status, point)


if __name__ == '__main__':
    main()
