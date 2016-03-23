# coding: utf-8

import xadmin

from .models import (
    SendCompanyCard,
    CompanyCategory,
    UserFavourCompany,
    Industry,
    Company
)
from .job_utils import (
    JobUtils
)


class SendCompanyCardAdmin(object):
    list_display = [
        'show_user',
        'resume_id',
        "to_email",
        'send_status',
        'send_time',
        'job',
        'feedback_status',
        'feedback_time',
        'points_used',
    ]
    list_display_links = ['show_user',"to_email"]

    ordering = [
        '-send_time',
    ]

    list_filter = [
        'send_user',
        'resume_id',
        "to_email",
        'send_status',
        'send_msg',
        'send_time',
        'job',
        'feedback_status',
        'feedback_time',
        'points_used',
    ]

    search_fields = [
        'resume_id',
    ]


class CompanyCategoryAdmin(object):
    list_display = (
        'industry',
        'category',
        'code_name',
        'display',
        'brick_display',
        'sort',
    )
    ordering = (
        '-sort',
    )
    search_fields = (
        'category',
        'code_name',
    )


class UserFavourCompanyAdmin(object):
    list_display = (
        'company',
        'user',
        'time',
    )
    list_filter = (
        'user',
        'company',
        'time',
    )

class IndustryAdmin(object):
    list_display = (
        'industry_name',
        'code_name'
    )
    list_filter = (
        'industry_name',
        'code_name'
    )


class CompanyAdmin(object):

    list_display = [
        'user',
        'company_name',
        'industry',
        'category',
        'key_points',
        "desc",
        'core_team',
        'company_stage',
        'url',
        'product_url',
        'add_time',
        'get_id',
        'pinbot_recommend',
        'favour_count',
        'need_recommend',
    ]
    list_display_links = ['company_name']

    ordering = [
        '-add_time',
    ]

    list_filter = [
        'user',
        'company_name',
        'url',
        'product_url',
        'favour_count',
    ]

    search_fields = [
        'company_name',
        'key_points',
        'desc',
    ]


xadmin.site.register(SendCompanyCard, SendCompanyCardAdmin)
xadmin.site.register(CompanyCategory, CompanyCategoryAdmin)
xadmin.site.register(UserFavourCompany, UserFavourCompanyAdmin)
xadmin.site.register(Industry, IndustryAdmin)
xadmin.site.register(Company, CompanyAdmin)

