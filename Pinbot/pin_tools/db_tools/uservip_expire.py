# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime
from dateutil.relativedelta import relativedelta

from app.vip.models import (
    UserVip
)

from pin_utils.package_utils import PackageUtils


def main():
    trans_time = datetime.datetime(2015, 9, 16)
    old_expire_time = trans_time + relativedelta(months=3)

    user_vip_query = UserVip.objects.select_related(
        'user',
        'vip_role',
    ).filter(
        is_active=True,
    ).exclude(
        vip_role__code_name='experience_user',
    )

    for user_vip in user_vip_query:
        vip_role = user_vip.vip_role
        active_time = user_vip.active_time

        if active_time < trans_time:
            expire_time = old_expire_time
        else:
            expire_time = active_time + relativedelta(months=3)

        if active_time < trans_time and vip_role.code_name == 'self_a':
            price = 1

        elif active_time < trans_time and vip_role.code_name == 'self_b':
            price = 10
        else:
            price = vip_role.price

        user_vip.expire_time = expire_time
        user_vip.total_price = price
        user_vip.save()
        PackageUtils.update_uservip_package(user_vip)

        print 'trans user {0} vip type {1} success'.format(
            user_vip.user.username,
            vip_role.vip_name,
        )


if __name__ == '__main__':
    main()
