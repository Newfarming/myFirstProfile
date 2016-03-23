# coding: utf-8

from django.contrib import admin

from .models import (
    Chat,
    ChatMessage,
)


class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'job_hunter',
        'hr',
        'job',
        'resume',
    )

    search_fields = (
        'job_hunter',
        'hr',
    )


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        'chat',
        'sender',
        'receiver',
        'msg',
    )

    search_fields = (
        'sender',
        'receiver',
    )


admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
