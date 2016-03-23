# coding: utf-8

from django.views.generic.base import View

from Brick.Utils.mixin_utils import (
    StaffRequiredMixin,
)
from Brick.Utils.django_utils import (
    JsonResponse,
)


class DailyReport(StaffRequiredMixin, View):

    def get(self, request):

        data = {}
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': data,
        })
