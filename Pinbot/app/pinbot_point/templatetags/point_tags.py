# coding: utf-8

from django import template


register = template.Library()


@register.filter
def recent_point(user, point_type):
    return ''
