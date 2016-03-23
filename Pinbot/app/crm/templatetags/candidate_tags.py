# coding: utf-8

import json

from django import template

from pin_utils.django_utils import (
    get_http_url,
)

register = template.Library()

EN_DISPLAY = {
    'talent_partner': u'人才伙伴',
    'brick': u'C端投递',
    'zhilian': u'智联',
    '51job': u'51Job',
    'liepin': u'猎聘',
}

REMARK_TYPE_DISPLAY = dict([
    (0, '个人信息更新'),
    (1, '求职要求'),
    (2, '个人喜好'),
    (3, '其他'),
])


@register.filter
def get_candidate_cn(en_str):
    return EN_DISPLAY.get(en_str, en_str)


@register.filter
def get_remark_type_cn(remark_type):
    return REMARK_TYPE_DISPLAY.get(remark_type, remark_type)


@register.filter
def http_url(url):
    return get_http_url(url)


@register.filter
def json_job_remark(job_remark):
    json_remark = [
        {
            'create_time': i.create_time.strftime('%Y-%m-%d %H:%M'),
            'remark_type_display': i.get_remark_type_display(),
            'admin': i.admin.username,
            'remark': i.remark,
        }
        for i in list(job_remark)
    ]
    return json.dumps(json_remark, ensure_ascii=False)
