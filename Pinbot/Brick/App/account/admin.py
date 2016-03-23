# coding: utf-8

from django.contrib import admin

from .models import (
    UserProfile,
    UserToken,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'nickname',
        'gender',
        'birthday',
        'phone',
    )
    list_filter = (
        'gender',
    )
    search_field = (
        'nickname',
        'phone',
    )


class UserTokenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'token',
        'active',
    )
    search_field = (
        'user',
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserToken, UserTokenAdmin)
