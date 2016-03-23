# coding: utf-8

import xadmin

from .models import (
    RecommendJob,
    JobMessage,
    CompanyCardJob,
)


class RecommendJobAdmin(object):
    list_display = (
        'user',
        'job',
        'hr_user',
        'hr_source',
        'job_company_name',
        'reco_time',
        'read_status',
        'search_tag',
        'action',
        'action_time',
        'company_action',
        'company_action_time',
        'resume_display',
        'reco_index',
    )
    list_filter = (
        'user',
        'hr_user',
        'reco_time',
        'action',
        'action_time',
        'company_action',
        'company_action_time',
        'reco_index',
        'read_status',
    )
    ordering = (
        '-reco_time',
    )
    search_fields = (
        'user__username',
    )


class JobMessageAdmin(object):
    list_display = (
        'user',
        'message',
        'create_time',
        'parent',
    )

    search_fields = (
        'user',
    )


class CompanyCardJobAdmin(object):
    list_display = (
        'job',
        'user',
        'send_time',
        'status',
        'action_time',
        'delete',
    )


xadmin.site.register(RecommendJob, RecommendJobAdmin)
xadmin.site.register(JobMessage, JobMessageAdmin)
xadmin.site.register(CompanyCardJob, CompanyCardJobAdmin)
