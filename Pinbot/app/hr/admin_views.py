# coding: utf-8

from django.views.generic import View
from django.db import transaction
from django.contrib.auth.models import User

from app.vip.vip_utils import VipRoleUtils
from app.vip.runtime.self_service import (
    SelfService,
)

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    JsonResponse,
)


class AdminActiveUser(StaffRequiredMixin, View):

    @transaction.atomic
    def get(self, request, username):

        user_query = User.objects.filter(
            username=username,
            vip_roles=None,
        ).exclude(
            userprofile=None,
        )

        if not user_query:
            return JsonResponse({
                'status': 'error',
                'data': '用户数据有误',
            })

        user = user_query[0]
        user.is_active = True
        user.save()

        experience_service = VipRoleUtils.get_experience_vip()
        srv_meta = {
            'service_name': 'self_service',
            'product': experience_service,
            'user': user,
        }
        experience_srv = SelfService(**srv_meta)
        srv = experience_srv.create_service()
        ret = experience_srv.active_service() if srv else False

        return JsonResponse({
            'status': 'ok',
            'data': '操作成功',
            'ret': ret,
        })
