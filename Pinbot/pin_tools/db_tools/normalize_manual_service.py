# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime
from django.db import transaction

from app.vip.models import (
    UserManualService,
    UserVip,
)
from app.vip.vip_utils import (
    VipRoleUtils,
)


def set_experience_vip(uservip):
    custom_feed = uservip.custom_feed
    custom_point = uservip.custom_point
    active_time = uservip.active_time
    expire_time = uservip.expire_time
    user = uservip.user

    experience_user_query = UserVip.objects.filter(
        vip_role__code_name='experience_user',
        user=user,
    )
    if experience_user_query:
        experience_user = experience_user_query[0]
        experience_user.custom_feed = custom_feed
        experience_user.custom_point = custom_point
        experience_user.active_time = active_time
        experience_user.expire_time = expire_time
        experience_user.is_active = True
    else:
        experience_service = VipRoleUtils.get_experience_vip()
        experience_user = UserVip(
            vip_role=experience_service,
            custom_feed=custom_feed,
            custom_point=custom_point,
            user=user,
            is_active=True,
            active_time=active_time,
            expire_time=expire_time,
        )

    uservip.is_active = False
    uservip.custom_point = 0
    uservip.custom_feed = 0

    with transaction.atomic():
        experience_user.save()
        uservip.save()
    return experience_user


def main():
    now = datetime.datetime.now()
    manual_user_id_list = UserManualService.objects.filter(
        expire_time__gt=now,
        is_active=True,
    ).values_list(
        'user_id',
        flat=True,
    )

    uservip_query = UserVip.objects.select_related(
        'user',
        'vip_role',
    ).filter(
        is_active=True,
        user_id__in=list(manual_user_id_list),
    ).exclude(
        vip_role__code_name='experience_user',
    )

    for uservip in uservip_query:
        set_experience_vip(uservip)
        print '{0} change success'.format(uservip.user.username)


if __name__ == '__main__':
    main()
