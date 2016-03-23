# coding: utf-8

import datetime

from django import template

from pin_utils.cn_money import cncapital
from pin_utils.django_utils import get_int

register = template.Library()

EN_DISPLAY = {
    'unpay': u'进行中',
    'paid': u'交易成功',
    'fail': u'交易失败',
    'personal': u'个人',
    'company': u'单位',
}


@register.filter
def day2month(days):
    days = get_int(days)
    return u'%d 个月' % (days / 30)


@register.filter
def get_cn_money(total_price):
    total_price = get_int(total_price)
    return cncapital(total_price) if total_price else '零圆'


@register.filter
def get_payment_cn_display(pay_status):
    return EN_DISPLAY.get(pay_status, pay_status)


@register.filter
def get_order_content(order):
    package_name = order.package.name if order.package else ''
    feed_name = order.feed_service.name if order.feed_service else ''
    return '+'.join(i for i in (package_name, feed_name) if i)


@register.filter
def package_expire(resume_end_time):
    if not resume_end_time:
        return False

    now = datetime.datetime.now()
    return True if now > resume_end_time else False


@register.simple_tag
def user_rest_point(pkg, user_point):
    if not pkg:
        pkg_point = 0
    else:
        pkg_point = pkg.rest_points + pkg.re_points

    pinbot_point = user_point.point
    rest_point = pkg_point + pinbot_point
    return rest_point


@register.filter
def get_order_pay_price(price):
    return -price
