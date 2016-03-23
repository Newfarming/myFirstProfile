# coding: utf-8

from django import template

register = template.Library()


@register.filter
def divide(d, divisor=1000):
    return d / divisor
