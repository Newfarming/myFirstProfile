# coding: utf-8

from django.contrib import admin

from .models import (
    RecommendJob,
    JobMessage,
    CompanyCardJob,
)


class RecommendJobAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'job',
        'reco_time',
        'read_status',
    )
    list_filter = (
        'user',
    )


class JobMessageAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'message',
        'create_time',
        'parent',
    )

    search_fields = (
        'user',
    )


class CompanyCardJobAdmin(admin.ModelAdmin):
    list_display = (
        'job',
        'user',
        'send_time',
        'status',
        'action_time',
        'delete',
    )


admin.site.register(RecommendJob, RecommendJobAdmin)
admin.site.register(JobMessage, JobMessageAdmin)
admin.site.register(CompanyCardJob, CompanyCardJobAdmin)
