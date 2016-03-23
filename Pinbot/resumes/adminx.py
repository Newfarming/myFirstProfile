# coding: utf-8

import xadmin

from . import models


class CommentAdmin(object):

    list_display = (
        'user',
        'show_resume',
        'content',
        'comment_time',
    )
    list_select_related = (
        'user',
    )
    search_fields = (
        'user__username',
    )
    list_filter = (
        'comment_time',
    )


class HistoryContactAdmin(object):

    list_display = [
        'contact_info',
        'name',
        'source',
        'source_id',
        'phone',
        'email',
        'identity_id',
        'status',
        'add_time',
        'origin',
    ]
    list_display_links = [
        'name'
    ]
    list_filter = [
        'source',
        'source_id',
        'email',
        'resume_id',
        'phone',
        'status'
    ]
    search_fields = [
        'resume_id',
        'name',
        'source',
        'source_id',
        'phone',
        'email',
        'qq',
        'identity_id',
    ]
    list_select_related = [
        'contact_info',
    ]


class ContactInfoDataAdmin(object):
    list_display = [
        'name',
        'source',
        "source_id",
        "phone",
        'email',
        'identity_id',
        'show_resume_url',
        'status',
        'add_time',
        'update_time',
        'origin',
    ]
    list_display_links = [
        'name'
    ]
    list_editable = [
        'source',
        'phone',
        'email',
    ]
    list_filter = [
        'source',
        'source_id',
        'email',
        'resume_id',
        'phone',
        'status',
        'origin',
        'add_time',
        'update_time',
    ]
    search_fields = [
        'resume_id',
        'name',
        'source',
        'source_id',
        'phone',
        'email',
        'qq',
        'weibo',
        'identity_id',
        'status'
    ]


xadmin.site.register(models.ContactInfoData, ContactInfoDataAdmin)
xadmin.site.register(models.HistoryContactInfo, HistoryContactAdmin)
xadmin.site.register(models.Comment, CommentAdmin)
