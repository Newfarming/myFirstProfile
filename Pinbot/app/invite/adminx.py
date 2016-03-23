# coding: utf-8

import xadmin

from .models import (
    InviteCode,
    InviteCodeApply,
)


class InviteCodeAdmin(object):

    list_display = (
        'code',
        'create_time',
        'status',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'code',
    )


class InviteCodeApplyAdmin(object):

    list_display = (
        'email',
        'job',
        'city',
        'phone',
        'apply_desc',
        'ip',
        'apply_time',
        'status',
        'apply_verify',
        'invite_code',
        'code_status',
    )

    list_editable = (
        'city',
    )

    list_filter = (
        'apply_time',
        'status',
    )

    search_fields = (
        'email',
        'city',
        'phone',
        'invite_code',
    )

xadmin.site.register(InviteCode, InviteCodeAdmin)
xadmin.site.register(InviteCodeApply, InviteCodeApplyAdmin)
