# coding: utf-8

from django import template

register = template.Library()


@register.filter
def has_receive_msg(user):
    count = user.receiver_msgs.filter(receiver_read=False)
    return count
