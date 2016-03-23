# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from users.models import (
    User
)
from app.vip.runtime.self_service import (
    SelfService
)
from app.vip.models import (
    VipRoleSetting
)
from pin_utils.django_utils import (
    get_object_or_none
)

join_date = datetime.datetime(2015, 10, 8)


def main():
    product = get_object_or_none(VipRoleSetting, code_name='experience_user')
    users = User.objects.filter(
        is_active=True,
        date_joined__gte=join_date,
        vip_roles=None,
    ).exclude(
        userprofile=None,
    )

    for old_user in users:
        self_srv = SelfService()
        self_srv.user = old_user
        self_srv.product = product
        self_srv.service_name = 'self_service'
        self_service_obj = self_srv.create_service()
        self_srv.service_id = self_service_obj.id
        self_srv.active_service()
        print 'conver user success! %s' % (old_user)


if __name__ == '__main__':
    main()
