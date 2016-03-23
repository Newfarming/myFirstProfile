# coding: utf-8

import json
import os
import bleach
from collections import OrderedDict

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from django.db.models import Count

from transaction.models import UserChargePackage
from pin_utils.django_utils import (
    str2datetime,
)

FONT_PATH = os.path.join(os.path.dirname(__file__), 'msyh.ttf')

register = template.Library()


@register.simple_tag(takes_context=True)
def user_package_perms(context, *group_name_list, **kwargs):
    request = context['request']

    for group in request.user.groups.all():
        if group.name in group_name_list:
            context['user_has_package'] = True

    # 如果套餐含有这个权限
    user_charges_pkgs = UserChargePackage.objects.filter(
        user=request.user,
        pay_status='finished',
    )

    for user_charges_pkg in user_charges_pkgs:
        if ((user_charges_pkg.package_type == 1
            and user_charges_pkg.resume_package.group.name in group_name_list)
            or user_charges_pkg.package_type == 2
        ):
            context['user_has_package'] = True
    context['user_has_package'] = False
    return True


@register.filter
@stringfilter
def to_str(value):
    return value


@register.inclusion_tag('pdf_zh_style.html')
def load_pdf_zh_style():
    return {'font': FONT_PATH}


@register.filter
def split_linebreak(s):
    return s.replace('<br>', '\n').replace('<br />', '\n').split('\n')


@register.filter
def get_job_hunt_stat(resume):
    source = resume.source
    hunt_stat = resume.job_target.job_hunting_brief(source) if resume.job_target else ''
    return hunt_stat


@register.filter
def get_position_title(resume):
    if not resume.works:
        return ''

    sorted_works = sorted(
        resume.works,
        key=lambda work: str2datetime(work.start_time),
        reverse=True
    )
    return sorted_works[0].position_title


@register.filter(is_safe=True)
def pdf_linebreak(s, download_type):
    s = bleach.clean(s, tags=[], strip=True)
    if download_type == 'html' or not s:
        return s

    s_len = len(s)
    chunk_size = 0
    chunk = 43
    start = 0
    s_list = []

    for i, c in enumerate(s):
        if ord(c) < 128:
            chunk_size += 0.5
        else:
            chunk_size += 1
        if chunk_size > chunk:
            s_list.append(s[start:i])
            start = i
            chunk_size = 0
        if i == s_len - 1:
            s_list.append(s[start: i + 1])

    if len(s_list) == 1:
        s_list.append('')

    return mark_safe(
        '<br>'.join(i.replace(' ', '') for i in s_list)
    )


@register.filter()
def string_safe(s):
    s = bleach.clean(s, tags=['br'], strip=True)
    return mark_safe(s)


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter()
def divide(value, arg):
    return int(value) / int(arg)


@register.simple_tag(takes_context=True)
def math_expr(context, *args):
    expr = ''.join(str(token or 0) for token in args)
    return eval(expr)


@register.filter
def to_json(var):
    return json.dumps(
        var,
        ensure_ascii=False
    )


@register.inclusion_tag('notice.html', takes_context=True)
def show_notice(context, user):
    notify_meta = OrderedDict([
        (
            'partner_upload_resume',
            {
                'url': '/notify/#/upload_resume/',
                'desc': '互助推荐简历信息',
                'count': 0,
            }
        ),
        (
            'partner_follow_resume',
            {
                'url': '/notify/#/follow_resume/',
                'desc': '互助伙伴发来的消息',
                'count': 0,
            }
        ),
        (
            'partner_reco_resume_task',
            {
                'url': '/notify/#/reco_task_resume/',
                'desc': '职位匹配消息',
                'count': 0,
            }
        ),
        (
            'resume_download_finished',
            {
                'url': '/notify/#/all/',
                'desc': '简历下载完成的消息',
                'count': 0,
            }
        ),
        (
            'egg_find_point',
            {
                'url': '/notify/#/all/',
                'desc': '砸中彩蛋的消息',
                'count': 0,
            }
        ),
        (
            'interview_alarm_notify',
            {
                'url': '/notify/#/all/',
                'desc': '面试提醒的消息',
                'count': 0,
            }
        ),
    ])

    notify_stat = user.notifications.filter(
        user_role='hr'
    ).unread().values(
        'notify_type',
    ).annotate(count=Count('notify_type'))

    for i in notify_stat:
        key = i['notify_type']
        count = i['count']
        if key in notify_meta:
            notify_meta[key]['count'] = count

    has_notify = sum([i['count'] for i in notify_stat])

    return {
        'all_notify': notify_meta,
        'has_unread': user.notifications.unread(),
        'has_notify': has_notify,
    }
