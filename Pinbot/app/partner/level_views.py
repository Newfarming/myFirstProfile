# coding: utf-8

from collections import OrderedDict
from django.views.generic.base import View

from .partner_utils import (
    PartnerLevelUtils,
)
from app.pinbot_point.models import (
    PointRule,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.django_utils import (
    JsonResponse,
)


class LevelState(LoginRequiredMixin, View):

    def get_basic_grant(self):
        basic_grant = dict(PointRule.objects.filter(
            rule_classify=1,
            point_rule__in=(
                'download_resume',
                'interview',
                'taking_work',
            )
        ).values_list(
            'point_rule',
            'point',
        ))
        for key, value in basic_grant.items():
            if key == 'download_resume':
                basic_grant['download_level'] = value
            if key == 'interview':
                basic_grant['interview_level'] = value
            if key == 'taking_work':
                basic_grant['taking_work_level'] = value
        return basic_grant

    def normal_level_state(self, level_state):
        basic_grant = self.get_basic_grant()
        for key, value in level_state.items():
            value['bonus_coin'] += basic_grant[key]
            value['next_bonus_coin'] += basic_grant[key]
        return level_state

    def get_flowerpot(self, level_state):
        meta = OrderedDict([
            # 下载面试入职都是满级
            (
                'unbelievable',
                lambda level_state: sum([i['is_max_level'] for i in level_state.values() if i.get('is_max_level')]) == 3
            ),
            # 入职满级
            (
                'unusual_taking_work',
                lambda level_state: level_state.get('taking_work_level', {}).get('is_max_level')
            ),
            # 面试满级
            (
                'unusual_interview',
                lambda level_state: level_state.get('interview_level', {}).get('is_max_level')
            ),
            # 下载满级
            (
                'sunlight',
                lambda level_state: level_state.get('download_level', {}).get('is_max_level', False)
            ),
            # 下载面试入职有经验值
            (
                'ordinary',
                lambda level_state: sum([i['user_exp'] for i in level_state.values() if i.get('user_exp', 0) > 0]) > 0
            ),
            # 没有任何经验
            (
                'sick',
                lambda level_state: sum([i['user_exp'] for i in level_state.values() if i.get('user_exp', 0) > 0]) == 0
            ),
        ])
        for flowerpot, valid_method in meta.items():
            if valid_method(level_state):
                return flowerpot

    def get(self, request):
        user = request.user

        level_utils = PartnerLevelUtils(user)
        level_state = level_utils.get_level_state()
        level_state = self.normal_level_state(level_state)
        flowerpot = self.get_flowerpot(level_state)

        data = {}
        data.update(level_state)
        data['flowerpot'] = flowerpot

        return JsonResponse({
            'status': 'ok',
            'data': data,
        })
