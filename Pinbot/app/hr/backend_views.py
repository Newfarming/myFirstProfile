# coding: utf-8

from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    JsonResponse,
    get_object_or_none,
)


class BackendLogin(StaffRequiredMixin, View):

    def get(self, request):
        username = request.GET.get('username', '')

        if not username:
            return JsonResponse({
                'statu': 'no_username',
            })

        user = get_object_or_none(
            User,
            username=username,
        )

        if not user:
            return JsonResponse({
                'status': 'no_user',
            })

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return JsonResponse({
            'status': 'ok',
        })
