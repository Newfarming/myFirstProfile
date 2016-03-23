# coding: utf-8

from django import template

register = template.Library()


@register.filter
def has_unread(user):
    count = user.notifications.unread().count()
    return count


@register.filter
def has_msg(user):
    return 0
