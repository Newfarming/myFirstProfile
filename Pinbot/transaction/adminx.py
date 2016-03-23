# coding: utf-8

import xadmin

from .models import (
    FeedBackInfo,
    DownloadResumeMark,
    ResumeBuyRecord,
    UserMarkLog,
    InterviewAlarm,
)

from feed.models import (
    Feed,
)


class FeedBackInfoAdmin(object):

    list_display = (
        'type',
        'feedback_id',
        'feedback_desc',
    )

    list_filter = (
        'type',
        'feedback_id',
        'feedback_desc',
    )


class ResumeBuyRecordAdmin(object):

    def make_result_list(self):
        result = super(ResumeBuyRecordAdmin, self).make_result_list()
        if not hasattr(self, 'result_list'):
            return result

        feed_id_list = [i.feed_id for i in self.result_list if i.feed_id]
        feed_query = Feed.objects.filter(
            feed_obj_id__in=feed_id_list,
        )
        feed_mapper = {
            i.feed_obj_id: i.title if i.title else i.keywords
            for i in feed_query
        }
        for i in self.result_list:
            i.feed_title = feed_mapper.get(i.feed_id, '')
        return result

    list_display = [
        'company_name',
        'op_time',
        'check_op',
        'finished_time',
        "show_pinbot_url",
        'status',
        "show_resume_url",
        'show_feed_url',
        'show_company_card',
        'mark_resume',
    ]
    list_display_links = [
        'company_name'
    ]
    list_editable = [
        'status',
        'finished_time',
        'resume_url',
        'payment',
    ]
    list_filter = [
        'user',
        'op_time',
        'finished_time',
        'status',
        'resume_id',
        "send_card__send_user__first_name",
        "send_card__send_user__username"
    ]
    search_fields = [
        'user__username',
        'resume_id',
        'resume_url',
        'send_card__send_user__first_name',
    ]
    ordering = [
        '-op_time',
        'status'
    ]


class DownloadResumeMarkAdmin(object):

    list_per_page = 20

    list_display = (
        'username',
        'feed',
        'resume_info',
        'last_mark',
        'current_mark',
        'mark_time',
        'has_interview',
        'mark_log',
        'admin_remark',
        'verify_status',
    )
    list_filter = (
        'buy_record__user',
        'last_mark',
        'current_mark',
        'mark_time',
        'verify_status',
        'has_interview',
    )
    list_editable = (
        'has_interview',
        'verify_status',
    )
    ordering = (
        '-mark_time',
    )


class UserMarkLogAdmin(object):

    list_display = (
        'resume_mark',
        'mark_time',
        'mark',
    )
    list_filter = (
        'mark_time',
        'mark',
    )
    list_select_related = (
        'mark',
    )


class InterviewAlarmAdmin(object):

    list_display = (
        'interview_count',
        'interview_time',
        'create_time',
        'has_alarm',
    )


xadmin.site.register(FeedBackInfo, FeedBackInfoAdmin)
xadmin.site.register(ResumeBuyRecord, ResumeBuyRecordAdmin)
xadmin.site.register(DownloadResumeMark, DownloadResumeMarkAdmin)
xadmin.site.register(UserMarkLog, UserMarkLogAdmin)
xadmin.site.register(InterviewAlarm, InterviewAlarmAdmin)
