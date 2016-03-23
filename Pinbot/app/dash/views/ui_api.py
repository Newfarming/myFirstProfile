# coding: utf-8

import datetime

from django.views.generic import View
from django.core.cache import cache

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
    LoginRequiredMixin,
)
from pin_utils.django_utils import (
    get_today,
    JsonResponse,
)


class UICheck(LoginRequiredMixin, View):

    STAT_KEYS = (
        '智能匹配',
        '扩展匹配',
        '保存文本到本地',
    )
    REDIS_KEY_PREFIX = 'UI_STATISTIC'

    def get(self, request):
        ui_check = request.GET.get('ui_check', '')

        if ui_check in self.STAT_KEYS:
            today = get_today()
            today_key = today.strftime('%Y-%m-%d')

            cache_key = '{0}_{1}_{2}'.format(
                self.REDIS_KEY_PREFIX,
                today_key,
                ui_check,
            )
            cache_value = cache.get(cache_key, 0)
            cache_value += 1
            cache.set(cache_key, cache_value, None)

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class UIStatistic(StaffRequiredMixin, View):

    START_DATE = datetime.datetime(2015, 12, 21)
    STAT_KEYS = (
        '智能匹配',
        '扩展匹配',
        '保存文本到本地',
    )
    REDIS_KEY_PREFIX = 'UI_STATISTIC'

    def get(self, request):
        today = get_today()
        range_days = (today - self.START_DATE).days + 1

        ret = {}
        for day in xrange(range_days):
            today_key = (self.START_DATE + datetime.timedelta(days=day)).strftime('%Y-%m-%d')

            for ui_check in self.STAT_KEYS:
                cache_key = '{0}_{1}_{2}'.format(
                    self.REDIS_KEY_PREFIX,
                    today_key,
                    ui_check,
                )
                cache_value = cache.get(cache_key, 0)
                ret[cache_key] = cache_value

        return JsonResponse(ret)
