# coding: utf-8

from django.contrib import admin


from .models import (
    InviteCode,
    InviteCodeApply,
)


class InviteCodeAdmin(admin.ModelAdmin):

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


class InviteCodeApplyAdmin(admin.ModelAdmin):

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

admin.site.register(InviteCode, InviteCodeAdmin)
admin.site.register(InviteCodeApply, InviteCodeApplyAdmin)
