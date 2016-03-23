# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from Brick.App.system.models import (
    ResumeMarkSetting,
    ResumeMarkRelation,
)
from pin_utils.django_utils import (
    get_object_or_none,
)

MARK_SETTING = {
    'invite_interview': {
        'name': '已约到面试',
        'code_name': 'invite_interview',
        'desc': '已约到面试',
        'display': True,
        'end_status': False,
        'good_result': True,
        'classify': 0,
        'change': False,
    },
    'join_interview': {
        'name': '已参加面试',
        'code_name': 'join_interview',
        'desc': '已参加面试',
        'display': True,
        'end_status': False,
        'good_result': True,
        'classify': 0,
        'change': False,
    },
    'next_interview': {
        'name': '下一轮面试',
        'code_name': 'next_interview',
        'desc': '已经约定下一轮面试',
        'display': True,
        'end_status': False,
        'good_result': True,
        'classify': 0,
        'change': False,
    },

    'send_offer': {
        'name': '已发offer',
        'code_name': 'send_offer',
        'desc': '已发offer',
        'display': True,
        'end_status': False,
        'good_result': True,
        'classify': 1,
        'change': False,
    },
    'entry': {
        'name': '已入职',
        'code_name': 'entry',
        'desc': '已入职',
        'display': True,
        'end_status': True,
        'good_result': True,
        'classify': 1,
        'change': False,
    },

    'no_will': {
        'name': '无求职意愿',
        'code_name': 'no_will',
        'desc': '候选人无求职意愿',
        'display': True,
        'end_status': True,
        'good_result': False,
        'classify': 2,
        'change': True,
    },
    'invite_lower_ability': {
        'name': '能力不匹配，约面不成功',
        'code_name': 'invite_lower_ability',
        'desc': '地点／能力不匹配，约面不成功',
        'display': True,
        'end_status': True,
        'good_result': False,
        'classify': 2,
        'change': True,
    },
    'invite_no_interest': {
        'name': '对公司不感兴趣，约面不成功',
        'code_name': 'invite_no_interest',
        'desc': '候选人对公司／项目不感兴趣，约面不成功',
        'display': True,
        'end_status': True,
        'good_result': False,
        'classify': 2,
        'change': True,
    },

    'break_invite': {
        'name': '约面后爽约',
        'code_name': 'break_invite',
        'desc': '约面后爽约',
        'display': True,
        'end_status': True,
        'good_result': False,
        'classify': 3,
        'change': True,
    },
    'lower_ability': {
        'name': '能力不匹配',
        'code_name': 'lower_ability',
        'desc': '薪资／地点／经验／能力不匹配',
        'display': True,
        'end_status': True,
        'good_result': False,
        'classify': 3,
        'change': True,
    },
    'no_interest': {
        'name': '对公司项目不感兴趣',
        'code_name': 'no_interest',
        'desc': '候选人对公司／项目不感兴趣',
        'display': True,
        'end_status': True,
        'good_result': False,
        'classify': 3,
        'change': True,
    },

    'reject_offer': {
        'name': '拒绝offer',
        'code_name': 'reject_offer',
        'desc': '候选人拒绝offer',
        'display': True,
        'end_status': True,
        'good_result': False,
        'classify': 4,
        'change': True,
    },
}

CHOICES_META = {
    'invite_interview': ['join_interview', 'next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'lower_ability', 'no_interest'],

    'next_interview': ['break_invite', 'send_offer', 'reject_offer', 'entry', 'no_interest', 'lower_ability'],

    'join_interview': ['next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'no_interest', 'lower_ability'],

    'break_invite': ['invite_interview', 'join_interview', 'next_interview', 'send_offer', 'reject_offer', 'entry', 'no_interest', 'lower_ability'],

    'reject_offer': ['entry'],

    'entry': [],

    'lower_ability': ['invite_interview', 'join_interview', 'next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'no_interest'],

    'no_interest': ['invite_interview', 'join_interview', 'next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'lower_ability'],

    'no_will': ['invite_interview', 'join_interview', 'next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'lower_ability', 'no_interest'],

    'invite_no_interest': ['invite_interview', 'join_interview', 'next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'lower_ability', 'no_interest'],

    'invite_lower_ability': ['invite_interview', 'join_interview', 'next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'lower_ability', 'no_interest'],

    'send_offer': ['reject_offer', 'entry'],
    'accu_fail': ['invite_interview', 'join_interview', 'next_interview', 'break_invite', 'send_offer', 'reject_offer', 'entry', 'lower_ability', 'no_interest', 'invite_lower_ability', 'invite_no_interest'],
}


def save_mark(code_name):
    mark_setting = MARK_SETTING[code_name]
    mark = ResumeMarkSetting(**mark_setting)
    return mark


def main():
    for key, value in CHOICES_META.iteritems():
        parent = get_object_or_none(
            ResumeMarkSetting,
            parent=None,
            code_name=key,
        )
        if not parent:
            parent = save_mark(key)
        parent.save()

        for c in value:
            choice = get_object_or_none(
                ResumeMarkSetting,
                parent=parent,
                code_name=c,
            )
            if choice:
                continue

            choice = save_mark(c)
            choice.parent = parent
            choice.save()
        print key, 'save_success'


def save_relation(code_name):
    mark = get_object_or_none(
        ResumeMarkSetting,
        code_name=code_name,
    )
    if not mark:
        mark = save_mark(code_name)
        mark.save()

    relation = ResumeMarkRelation(
        mark=mark
    )
    return relation


def init_mark_relation():
    for key, value in CHOICES_META.iteritems():
        null_parent = get_object_or_none(
            ResumeMarkRelation,
            mark__code_name=key,
            parent=None,
        )
        if not null_parent:
            null_parent = save_relation(key)
            null_parent.save()

        parent = get_object_or_none(
            ResumeMarkSetting,
            code_name=key,
        )
        if not parent:
            parent = save_mark(key)
        parent.save()

        for c in value:
            choice = get_object_or_none(
                ResumeMarkRelation,
                parent=parent,
                mark__code_name=c,
            )
            if choice:
                continue

            choice = save_relation(c)
            choice.parent = parent
            choice.save()
        print key, 'save_success'


if __name__ == '__main__':
    init_mark_relation()
