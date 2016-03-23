# coding: utf-8

import xadmin

from notifications.models import Notification


class NotificationAdmin(object):

    list_display = (
        'recipient',
        'user_role',
        'notify_type',
        'verb',
        'timestamp',
        'unread',
    )
    list_filter = (
        'recipient',
        'user_role',
        'notify_type',
        'timestamp'
    )


xadmin.site.register(Notification, NotificationAdmin)
