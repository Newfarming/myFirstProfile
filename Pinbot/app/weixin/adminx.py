# coding: utf-8
import xadmin

from .models import (
    WeixinUser
)


class WeixinUserAdmin(object):
    def reg_time(self, instance):
        return instance.user.date_joined
    reg_time.short_description = '注册时间'

    list_display = (
        'user',
        'openid',
        'nickname',
        'sex',
        'city',
        'create_time',
        'reg_time',
        'is_bind',
        'is_subscribe',
    )

    list_filter = (
        'user',
        'openid',
        'is_bind',
        'is_subscribe',
    )

xadmin.site.register(WeixinUser, WeixinUserAdmin)
