# coding: utf-8

import xadmin

from .models import (
    UserAcceptTask,
    UserTaskResume,
    UploadTaskSetting,
    TaskCoinRecord,
    RecoResumeTask,
    UploadResume,
    FollowTaskRecord,
    PartnerLevelManage,
    UserLevelState,
    HotTaskSetting,
)


class UserAcceptTaskAdmin(object):

    list_display = (
        'user',
        'feed',
        'accept_time',
        'update_time',
        'task_id',
        'has_hr_info',
    )

    list_filter = (
        'user',
        'has_hr_info',
    )


class UserTaskResumeAdmin(object):

    def queryset(self):
        qs = super(UserTaskResumeAdmin, self).queryset()
        qs = qs.select_related(
            'resume',
            'task',
            'task__user',
            'task__feed',
            'task__feed__user',
        ).prefetch_related(
            'resume__resume_coin_records',
        )
        return qs

    list_per_page = 20

    list_display = (
        'task_user',
        'task',
        'hr',
        'display_resume',
        'upload_time',
        'resume_update_time',
        'grant_coin',
        'resume_status',
        'verify',
        'operation',
        'extra_grant',
        'extra_operation',
    )
    list_filter = (
        'task__feed__user',
        'task__user',
        'resume_status',
        'verify',
        'extra_grant',
    )

    list_editable = (
        'verify',
    )


class TaskCoinRecordAdmin(object):

    list_display = (
        'task',
        'show_hr',
        'upload_resume',
        'show_user',
        'coin',
        'desc',
        'record_time',
        'record_type',
    )

    list_filter = (
        'task__user',
        'task__feed__user',
        'record_type',
    )

    list_select_related = (
        'task__user',
        'task__feed__user',
    )


class UploadTaskSettingAdmin(object):

    list_display = (
        'user',
        'title',
        'job_domains',
        'citys',
        'task_time',
    )

    list_filter = (
        'user',
    )


class RecoResumeTaskAdmin(object):

    list_display = (
        'feed',
        'display_resume',
        'reco_time',
        'action',
        'display',
        'reco_index',
        'user',
        'upload_resume',
    )

    list_filter = (
        'user',
        'action',
        'reco_time',
    )

    search_fields = (
        'feed__feed_obj_id',
        'upload_resume__resume_id',
        'user__username',
    )


class UploadResumeAdmin(object):

    list_display = (
        'user',
        'name',
        'phone',
        'email',
        'expect_work_place',
        'expect_position',
        'last_contact',
        'hr_evaluate',
        'display_resume',
        'resume_id',
    )

    list_filter = (
        'user',
    )

    search_fields = (
        'resume_id',
    )


class FollowTaskRecordAdmin(object):

    list_display = (
        'follow_user',
        'follow_task',
        'hr_user',
        'display_resume',
        'follow_time',
        'follow_type',
        'desc',
        'resume_status',
        'has_check',
        'check_time',
    )

    list_filter = (
        'task_resume__task__user',
        'task_resume__task__feed__user',
        'has_check',
        'follow_type',
        'follow_time',
        'check_time',
    )

    list_select_related = (
        'task_resume',
        'task_resume__task',
        'task_resume__task__user',
        'task_resume__task__feed__user',
    )


class PartnerLevelManageAdmin(object):

    list_display = (
        'level_type',
        'level',
        'exp',
        'ratio',
        'bonus_coin',
        'next_level',
        'next_exp',
        'next_ratio',
        'next_bonus_coin',
        'is_max_level',
    )


class UserLevelStateAdmin(object):

    list_display = (
        'username',
        'check_count',
        'download_count',
        'interview_count',
        'taking_work_count',
        'download_ratio',
        'interview_ratio',
        'taking_work_ratio',
    )

    list_filter = (
        'username',
    )


class HotTaskSettingAdmin(object):

    list_display = (
        'name',
    )
    list_filter = (
        'name',
    )


xadmin.site.register(UploadTaskSetting, UploadTaskSettingAdmin)
xadmin.site.register(UploadResume, UploadResumeAdmin)
xadmin.site.register(UserAcceptTask, UserAcceptTaskAdmin)
xadmin.site.register(UserTaskResume, UserTaskResumeAdmin)
xadmin.site.register(TaskCoinRecord, TaskCoinRecordAdmin)
xadmin.site.register(RecoResumeTask, RecoResumeTaskAdmin)
xadmin.site.register(FollowTaskRecord, FollowTaskRecordAdmin)
xadmin.site.register(PartnerLevelManage, PartnerLevelManageAdmin)
xadmin.site.register(UserLevelState, UserLevelStateAdmin)
xadmin.site.register(HotTaskSetting, HotTaskSettingAdmin)
