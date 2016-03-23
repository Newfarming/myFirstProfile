# coding: utf-8

import xadmin

from .models import (
    City,
    CompanyCategoryPrefer,
    CompanyWelfare,
    ResumeMarkSetting,
    ResumeMarkRelation,
)


class CityAdmin(object):
    list_display = (
        'name',
    )


class CompanyCategoryPreferAdmin(object):
    list_display = (
        'name',
        'sort',
        'display',
    )


class CompanyWelfareAdmin(object):
    list_display = (
        'name',
        'sort',
        'display',
    )


class ResumeMarkSettingAdmin(object):
    list_display = (
        'name',
        'code_name',
        'desc',
        'display',
        'end_status',
        'change',
        'has_interview',
        'is_taking_work',
        'is_accu',
        'classify',
        'sort',
    )
    list_filter = (
        'name',
        'classify',
    )
    list_editable = (
        'name',
        'desc',
        'has_interview',
        'is_accu',
        'sort',
        'display',
        'is_taking_work',
        'end_status',
    )
    ordering = (
        '-sort',
    )


class ResumeMarkRelationAdmin(object):

    list_display = (
        'parent',
        'mark',
    )

    list_filter = (
        'parent',
        'mark',
    )


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CompanyCategoryPrefer, CompanyCategoryPreferAdmin)
xadmin.site.register(CompanyWelfare, CompanyWelfareAdmin)
xadmin.site.register(ResumeMarkSetting, ResumeMarkSettingAdmin)
xadmin.site.register(ResumeMarkRelation, ResumeMarkRelationAdmin)
