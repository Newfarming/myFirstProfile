# coding: utf-8

from django import template

register = template.Library()


@register.filter
def has_notify(user):
    count = user.notifications.unread().count()
    return count
