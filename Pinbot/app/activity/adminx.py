# coding: utf-8

import xadmin

from .models import (
    EasterEgg,
    EggRecord,
    CloseEasterRecord,
    Questionnaire,
    QuestionnaireResult,
    QuestionnaireAnwserResult,
)


class EasterEggAdmin(object):

    list_display = (
        'name',
        'code_name',
        'egg_type',
        'amount',
        'price',
        'is_active'
    )

    list_editable = (
        'is_active',
    )

    search_fields = (
        'name',
    )


class EggRecordAdmin(object):

    def addr_info(self, instance):
        return instance.user.userprofile.show_addr()

    addr_info.short_description = '邮寄地址'

    list_display = (
        'user',
        'egg',
        'create_time',
        'claim_status',
        'claim_time',
        'addr_info',
        'user_need',
    )

    list_editable = (
        'claim_status',
    )

    list_select_related = (
        'user',
        'egg',
    )

    list_filter = (
        'user',
        'egg__name',
        'create_time',
        'claim_status',
        'user_need'
    )

    search_fields = (
        'user__username',
    )


class CloseEasterRecordAdmin(object):
    list_display = (
        'username',
        'close_time',
    )

    list_filter = (
        'close_time',
    )

    search_fields = (
        'username',
    )


class QuestionnaireAdmin(object):
    list_display = (
        'question',
        'anwser_options',
        'order',
        'question_type',
        'anwser_type',
        'is_active',
    )
    list_editable = (
        'order',
        'question_type',
        'anwser_type',
        'is_active',
        'question',
        'anwser_options',
    )


class QuestionnaireResultAdmin(object):
    list_display = (
        'user',
        'submit_time',
    )


class QuestionnaireAnwserResultAdmin(object):
    list_display = (
        'question',
        'anwser',
        'questionnaire_page',
    )

    list_filter = (
        'question',
        'anwser',
        'questionnaire_page__user',
    )


xadmin.site.register(EasterEgg, EasterEggAdmin)
xadmin.site.register(EggRecord, EggRecordAdmin)
xadmin.site.register(CloseEasterRecord, CloseEasterRecordAdmin)
xadmin.site.register(Questionnaire, QuestionnaireAdmin)
xadmin.site.register(QuestionnaireResult, QuestionnaireResultAdmin)
xadmin.site.register(QuestionnaireAnwserResult, QuestionnaireAnwserResultAdmin)
