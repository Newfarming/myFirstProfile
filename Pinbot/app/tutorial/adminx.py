# coding: utf-8

import xadmin

from .models import(
    InterviewTermQuestions,
    FeedBackText,
)


class InterviewTermQuestionsAdmin(object):

    list_display = (
        'question',
        'anwser',
        'question_type',
    )


class FeedBackTextAdmin(object):

    list_display = (
        'contact_email',
        'feedback_text',
        'feedback_time',
    )

    search_fields = (
        'contact_email',
        'feedback_text',
    )

xadmin.site.register(InterviewTermQuestions, InterviewTermQuestionsAdmin)
xadmin.site.register(FeedBackText, FeedBackTextAdmin)
