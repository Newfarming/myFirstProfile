# coding: utf-8
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from app.vip.models import (
    UserVip
)

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

if __name__ == '__main__':

    active_uid_list = list(UserVip.objects.filter(is_active=True).values_list('user_id', flat=True))

    deactive_uid_list = list(set(list(UserVip.objects.select_related('user').filter(is_active=False)\
                                      .exclude(user__id__in=active_uid_list).values_list('user_id', flat=True))))

    old_user_list = User.objects.filter(id__in=deactive_uid_list)

    print 'old_user count:', len(old_user_list)

    product = get_object_or_none(VipRoleSetting, code_name='experience_user')

    for old_user in old_user_list:
        self_srv = SelfService()
        self_srv.user = old_user
        self_srv.product = product
        self_srv.service_name = 'self_service'
        self_service_obj = self_srv.create_service()
        self_srv.service_id = self_service_obj.id
        self_srv.active_service()
        print 'conver user success! %s' % (old_user)




