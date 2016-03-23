# coding: utf-8

from django import template

from Brick.App.job_hunting.models import (
    Resume,
)

register = template.Library()


JOB_CN_DISPLAY = {
    'male': '男',
    'female': '女',
    2: '0-1年',
    3: '1-3年',
    4: '3-5年',
    5: '5-8年',
    6: '8年以上',
    'waiting': '等待企业反馈',
    'download': '面试邀请中',
    'no_reply': '无回复',
    'unfit': '不合适',
}

DEGREE_META = {
    d[0]: d[1]
    for d in Resume.DEGREE_META
}

JOB_CN_DISPLAY.update(DEGREE_META)

CARD_DEGREE_CHOICES = {
    0: u'不限',
    3: u'大专',
    4: u'本科',
    7: u'硕士',
    10: u'博士',
}


@register.filter
def cn_display(en_str):
    return JOB_CN_DISPLAY.get(en_str, en_str)


@register.filter
def divide(d, divisor=1000):
    return d / divisor


@register.filter
def card_cn_display(en_str):
    return CARD_DEGREE_CHOICES.get(en_str, en_str)


@register.filter
def get_city(resume):
    return ','.join(c.city.name for c in resume.expectation_area.all())


@register.filter
def get_work(resume):
    works = resume.works.all()
    return works[0].company_name if works else ''


@register.simple_tag(takes_context=True)
def get_salary(context, salary_low, salary_high):
    if salary_low == 0 and salary_high == 1000000:
        return '面议'
    if salary_low > 0 and salary_high == 1000000:
        return '%dK以上' % (salary_low / 1000)
    if salary_low == 0 and salary_high < 1000000:
        return '%dK以下' % (salary_high / 1000)
    return '%dK－%dK' % (salary_low / 1000, salary_high / 1000)


@register.filter
def show_category(category):
    return '  '.join('#%s#' % i for i in category)
