# coding: utf-8

import xadmin

from .models import (
    Task,
    TaskFinishedStatus,
    TaskFinishedNotify,
    Coupon,
    RealReward,
)


class TaskAdmin(object):

    list_display = (
        'task_code',
        'is_apply',
        'task_id',
        'task_name',
        'description',
        'task_level',
        'task_reward',
        'reward_type',
        'task_url',
        'reward_due_time',
        'task_count',
        'coupon_type',
        'task_type',
    )

    list_editable = (
        'is_apply',
    )


class TaskFinishedStatusAdmin(object):

    list_display = (
        'user',
        'task',
        'reward_status',
        'finished_status',
        'current_process',
        'reward_due_time',
        'task_times',
        'finished_time',
        'reward_time',
    )

    list_filter = (
        'user',
        'task',
        'reward_status',
        'finished_time',
        'reward_time',
    )


class TaskFinishedNotifyAdmin(object):

    list_display = (
        'user',
        'notify_status',
    )

    list_filter = (
        'user',
        'notify_status',
    )


class CouponAdmin(object):

    list_display = (
        'user',
        'coupon_type',
        'coupon_num',
        'coupon_start_time',
        'coupon_used_time',
        'coupon_due_time',
    )

    list_filter = (
        'user',
        'coupon_type',
        'coupon_num',
        'coupon_start_time',
        'coupon_used_time',
        'coupon_due_time',
    )


class RealRewardAdmin(object):

    list_display = (
        'user',
        'award_item',
        'award_time',
        'is_send',
        'send_time',
    )

    list_filter = (
        'user',
    )

xadmin.site.register(Task, TaskAdmin)
xadmin.site.register(TaskFinishedStatus, TaskFinishedStatusAdmin)
xadmin.site.register(TaskFinishedNotify, TaskFinishedNotifyAdmin)
xadmin.site.register(Coupon, CouponAdmin)
xadmin.site.register(RealReward, RealRewardAdmin)
