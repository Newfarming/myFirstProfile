# coding: utf-8

import logging
from datetime import datetime
from Pinbot.settings import ON_LINE_TIME

from django.db import transaction
from django.db.models import Q
from django.views.generic.base import View

from .models import (
    Task,
    TaskFinishedStatus,
    TaskFinishedNotify,
    Coupon,
    RealReward,
)
from .mixin import TaskCheckMixin
from .forms import AddressForm
from .tasks import send_weixin_redpack

from users.models import UserProfile
from app.pinbot_point.point_utils import (
    point_utils,
    coin_utils,
)

from pin_utils.django_utils import JsonResponse
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)

logger = logging.getLogger('django')


class TaskStatusList(LoginRequiredMixin, View):

    def get_coupon_used_time(self, user, task_status):
        if task_status.task.reward_type == 3:
            time_query = Coupon.objects.filter(
                user=user,
                task=task_status.task,
            ).values_list("coupon_used_time", flat=True)
            coupon_used_time = time_query[0] if time_query else None
            return coupon_used_time
        return None

    def get(self, request):

        task_status_query = TaskFinishedStatus.objects.select_related(
            'taskname__task_name',
            'taskname__description',
            'taskname__task_code',
            'taskname__task_count',
            'taskname__task_reward',
        ).filter(
            Q(
                user=request.user,
                finished_status=2,
                reward_time__gt=ON_LINE_TIME,
            ) | Q(
                user=request.user,
                repeat_times__gte=1,
                task__task_level__in=[4, 5],
            )
        )
        task_status_list = []
        for task_status in task_status_query:
            coupon_used_time = self.get_coupon_used_time(
                request.user,
                task_status,
            )
            task_status_list.append({
                'task_name': task_status.task.task_name,
                'task_code': "{count}_{code}".format(
                    count=task_status.task.task_count,
                    code=task_status.task.task_code
                ),
                'description': task_status.task.description,
                'task_reward': ' x '.join([
                    str(task_status.repeat_times),
                    task_status.task.task_reward
                ]) if task_status.task.task_level in [4, 5] else task_status.task.task_reward,
                'reward_due_time': task_status.reward_due_time,
                'reward_time': task_status.reward_time,
                'coupon_used_time': coupon_used_time,
            })
        return JsonResponse({
            'status': 'ok',
            'finished_count': len(task_status_list),
            'data': task_status_list,
        })


class TaskList(LoginRequiredMixin, TaskCheckMixin, View):

    def protect_user_privacy(self, username):
        pre, at, tail = username.rpartition('@')
        pre_length = len(pre)
        if pre_length > 2:
            pre = '{nchg}{chg}'.format(
                nchg=pre[:-2],
                chg='**',
            )
        else:
            pre = '{nchg}{chg}'.format(
                nchg=pre[:-1],
                chg='*',
            )
        return '{pre}@{tail}'.format(
            pre=pre,
            tail=tail,
        )

    def get_recently_reward_records(self):
        recently_reward_records_query = TaskFinishedStatus.objects.select_related(
            'taskname'
        ).filter(
            reward_status=2
        ).order_by("-reward_time")[:10]
        recent_reward_detail = [
            "恭喜用户{username} 获得了{task_reward}".format(
                username=self.protect_user_privacy(record.user.username),
                task_reward=record.task.task_reward,
            ) for record in recently_reward_records_query
        ]
        return recent_reward_detail

    def task_status_dict_mapper(self, task_status_query):
        task_dict = {
            task_status.get('task'): task_status
            for task_status in task_status_query
        }
        return task_dict

    def add_task_finished_status(self, task_query, task_status_dict):
        task_status = []
        for task in task_query:
            task_code = "{count}_{code}".format(
                count=task.task_count,
                code=task.task_code,
            )
            status_dict = task_status_dict.get(task.id, {})
            origin_finished_status = status_dict.get('finished_status', 1)
            reward_status = status_dict.get('reward_status', 1)
            finished_status = origin_finished_status
            if origin_finished_status == 2:
                if reward_status == 1:
                    finished_status = 3
                if reward_status == 2:
                    finished_status = 1
            else:
                finished_status = 2
            if task.task_type == 3 and status_dict.get('current_process') != task.task_count:
                continue
            if finished_status != 3 and not task.is_apply:
                continue
            task_status.append({
                'task_code': task_code,
                'task_name': task.task_name,
                'description': task.description,
                'task_type': task.task_type,
                'reward_type': task.reward_type,
                'task_reward': task.task_reward,
                'task_count': task.task_count if task.task_count else u'∞',
                'current_process': status_dict.get('current_process', 0),
                'finished_status': finished_status,
                'task': reward_status,
                'task_url': task.task_url,
            })
        return task_status

    def check_once_task_is_finished(self, user, task_status):
        finished_task_code = {}
        new_finished_task = []
        for status in task_status:
            finished_task_code[status['task_code']] = status['finished_status']
        onece_task_code_list = [
            '1_is_user_active',
            '1_is_user_weixin_bind',
            '1_is_user_email_bind',
            '1_is_user_company_detail',
        ]

        for task_code in onece_task_code_list:
            if finished_task_code.get(task_code) == 2:
                if self.check_task_is_finished(user, task_code):
                    new_finished_task.append(task_code)
        for status in task_status:
            if status['task_code'] in new_finished_task:
                status['current_process'] = 1
                status['finished_status'] = 3
        return task_status

    def order_status_list(self, task_status_list):
        return sorted(task_status_list, key=lambda x: x['finished_status'], reverse=True)

    def get(self, request):

        task_query = Task.objects.all()
        task_status_query = TaskFinishedStatus.objects.filter(
            user=request.user
        ).values(
            'task',
            'current_process',
            'finished_status',
            'reward_status',
        )
        task_status_dict = self.task_status_dict_mapper(task_status_query)
        task_status = self.add_task_finished_status(task_query, task_status_dict)
        task_status = self.check_once_task_is_finished(request.user, task_status)
        recent_reward_detail = self.get_recently_reward_records()
        task_status = self.order_status_list(task_status)

        all_task = {
            'status': 'ok',
            'task_count': len(task_status),
            'data': task_status,
            'recent': recent_reward_detail,
        }
        return JsonResponse(all_task)


class ReceiveReward(LoginRequiredMixin, View):

    def reward_provide(self, task, user):
        def reward_pin_point_or_coin(task, user):
            if task.reward_type == 1:
                utils = point_utils
            if task.reward_type == 2:
                utils = coin_utils
            utils.add_point(
                user,
                task.reward_num,
                record_type='task_provide',
                detail='{taskname}任务完成奖励'.format(
                    taskname=task.task_name
                ),
                point_rule='task_provide',
            )

        def reward_coupon(task, user):
            Coupon.objects.create(
                user=user,
                task=task,
                coupon_type=task.coupon_type,
                coupon_num=task.reward_num,
            )

        def reward_redpack(task, user):
            send_weixin_redpack.delay(user, task.reward_num)
            logger.info(
                "{user} get {reward_num} yuan weixin_redpack by {task_count}_{task_code}".format(
                    user=user.username,
                    reward_num=task.reward_num,
                    task_code=task.task_code,
                    task_count=task.task_count,
                )
            )

        def reward_real(task, user):
            RealReward.objects.create(
                user=user,
                award_item=task.task_reward,
            )
        reward_mapper = {
            1: reward_pin_point_or_coin,
            2: reward_pin_point_or_coin,
            3: reward_coupon,
            4: reward_redpack,
            5: reward_real,
        }
        reward_mapper.get(task.reward_type)(task, user)

    def check_weixin_is_required(self, user, task):
        if task.reward_type == 4 and not hasattr(user, 'weixin_user'):
            return True
        return False

    def check_user_nofity_status(self, user):
        left_reward = TaskFinishedStatus.objects.filter(
            user=user,
            reward_status=1,
            finished_status=2,
        ).count()
        if left_reward == 0:
            TaskFinishedNotify.objects.filter(
                user=user,
            ).update(
                notify_status='task_to_do'
            )

    def is_address_add(self, user, task):
        if task.reward_type == 5:
            if (user.userprofile.province
                and user.userprofile.street
                and user.userprofile.city
            ):
                return False
            return True
        return False

    @transaction.atomic
    def post(self, request):

        data = request.POST
        user = request.user
        task_data = data.get('task_data')
        task_times, task_code = task_data.split('_', 1)
        task_times = int(task_times)
        task = Task.objects.filter(
            task_code=task_code,
            task_count=task_times
        )

        if not task:
            return JsonResponse({
                'status': 'error',
                'msg': 'error task_code',
            })

        task = task[0]

        if self.check_weixin_is_required(user, task):
            return JsonResponse({
                'status': 'error',
                'msg': 'weixin bind required',
            })
        if self.is_address_add(user, task):
            return JsonResponse({
                'status': 'error',
                'msg': 'address required'
            })

        if task.task_level in [1, 2, 3]:
            not_receive_num = TaskFinishedStatus.objects.filter(
                user=request.user,
                task=task,
                finished_status=2,
                task_times=task_times,
                reward_status=1,
            ).update(
                reward_status=2,
                reward_time=datetime.now()
            )
        elif task.task_level == 4:
            not_receive_num = TaskFinishedStatus.objects.filter(
                user=request.user,
                task=task,
                finished_status=2,
                task_times=task_times,
                reward_status=1,
            ).update(
                reward_status=1,
                finished_status=1,
            )
        elif task.task_level == 5:
            not_receive_num = TaskFinishedStatus.objects.filter(
                user=request.user,
                task=task,
                finished_status=2,
                task_times=task_times,
                reward_status=1,
            ).update(
                reward_status=1,
                finished_status=1,
                current_process=0,
                reward_time=None,
            )

        self.check_user_nofity_status(user)

        if not_receive_num == 0:
            return JsonResponse({
                'status': 'error',
                'msg': 'task_code error or reward_status is due'
            })

        self.reward_provide(task, user)
        return JsonResponse({
            'status': 'ok',
            'msg': 'success',
        })


class TaskStatus(LoginRequiredMixin, View):

    def get(self, request):
        user_status_query = TaskFinishedNotify.objects.get_or_create(
            user=request.user
        )
        if user_status_query:
            return JsonResponse({
                'status': 'ok',
                'msg': user_status_query[0].notify_status
            })
        return JsonResponse({
            'status': 'error',
            'msg': 'not user',
        })


class UserRealRewardAddress(LoginRequiredMixin, View):

    def get(self, request):

        user = request.user
        name = user.userprofile.name
        province = user.userprofile.province
        city = user.userprofile.city
        street = user.userprofile.street

        return JsonResponse({
            'name': name,
            'province': province,
            'city': city,
            'street': street,
        })

    def post(self, request):

        user = request.user
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            update_num = UserProfile.objects.filter(
                user=user,
            ).update(
                **data
            )
            if update_num:
                return JsonResponse({
                    'status': 'ok',
                    'msg': 'sucess'
                })
        return JsonResponse({
            'status': 'error',
            'msg': 'error'
        })
