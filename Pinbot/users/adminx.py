# coding: utf-8

import xadmin

from users.models import (
    UserProfile,
    NewIndustryBookin
)

class UserProfileAdmin(object):

    list_display = [
        'user',
        'name',
        'show_date_join',
        'show_company',
        'show_addr',
        'user_email',
        'is_email_bind',
        'phone',
        'is_phone_bind',
        'show_user_active',
        'show_active',
        'service_level',
        'calc_level',
        'show_source',
    ]

    list_filter = [
        'user__is_active',
        'source',
        'service_level',
        'calc_level',
        'client_level',
        'is_email_bind',
        'is_phone_bind',
        'user__date_joined'
    ]

    search_fields = [
        'user__first_name',
        'user__username',
        'user_email',
        'company_name',
        'name',
        'phone'
    ]

    list_select_related = [
        'user',
    ]

    list_editable = [
        'is_review',
        'service_level',
        'calc_level',
    ]


class NewIndustryBookinAdmin(object):

    def phone(self, instance):
        return instance.user.phone

    phone.short_description = '联系电话'

    def username(self, instance):
        return instance.user.user.username

    username.short_description = '用户名'

    def company(self, instance):
        return instance.user.company_name

    company.short_description = '公司名'

    list_display = [
        'username',
        'company',
        'phone',
        'type',
        'add_time'
    ]

    list_filter = [
        'type',
    ]


xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(NewIndustryBookin, NewIndustryBookinAdmin)

