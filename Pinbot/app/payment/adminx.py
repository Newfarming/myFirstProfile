# coding: utf-8
import xadmin


from app.payment.models import (
    WeixinPackRecord
)


class WeixinPackRecordAdmin(object):

    def username(self, instance):
        return instance.user.user.username
    username.short_description = '用户名'

    list_display = (
        'username',
        'amount',
        'send_time',
        'send_status',
        'send_msg',
    )

    list_filter = (
        'user__user',
        'send_time',
        'amount',
        'send_status',
    )

xadmin.site.register(WeixinPackRecord, WeixinPackRecordAdmin)
