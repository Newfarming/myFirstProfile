# coding: utf-8

import json

from bson import json_util
from django import template

from resumes.helper import mongo_to_dict

register = template.Library()


@register.filter
def get_json_remark(feed):
    data = {
        'remarks': [mongo_to_dict(r, {}) for r in feed.remarks or []],
        'ignored': feed.ignored,
    }
    return json.dumps(
        data,
        default=json_util.default,
        ensure_ascii=False,
    )


@register.simple_tag(takes_context=True)
def get_salary(context, salary_low, salary_high):
    if salary_low == 0 and salary_high == 1000000:
        return '面议'
    if salary_low > 0 and salary_high == 1000000:
        return '%dK以上' % (salary_low / 1000)
    if salary_low == 0 and salary_high < 1000000:
        return '%dK以下' % (salary_high / 1000)
    return '%dK－%dK' % (salary_low / 1000, salary_high / 1000)
