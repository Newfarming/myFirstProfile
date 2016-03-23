# coding: utf-8

import datetime

from django import forms

from .models import (
    ResumeBuyRecord,
    DownloadResumeMark,
    UserMarkLog,
    InterviewAlarm,
)

from app.partner.partner_utils import (
    PartnerCoinUtils,
)

from Brick.App.system.models import (
    ResumeMarkSetting,
    ResumeMarkRelation,
)

from pin_utils.django_utils import (
    get_object_or_none,
)
from pin_utils.form_mixin import FormErrors


class MarkResumeForm(forms.Form):

    code_name = forms.CharField(label='标记选项')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.record_id = kwargs.pop('record_id', None)
        self.user = self.request.user

        super(MarkResumeForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 管理员可以修改任何用户的记录
        if self.user.is_staff:
            self.buy_record_query = ResumeBuyRecord.objects.select_related(
                'resume_mark',
            ).filter(
                id=self.record_id,
                status='LookUp',
            )
        else:
            self.buy_record_query = ResumeBuyRecord.objects.select_related(
                'resume_mark',
            ).filter(
                user=self.user,
                id=self.record_id,
                status='LookUp',
            )

        if not self.buy_record_query:
            raise forms.ValidationError('暂无下载记录，请先下载简历')

        self.buy_record = self.buy_record_query[0]

        code_name = self.data.get('code_name') or ''

        if not hasattr(self.buy_record, 'resume_mark'):
            self.mark = get_object_or_none(
                ResumeMarkSetting,
                code_name=code_name,
            )
            if not self.mark:
                raise forms.ValidationError('标记状态错误，请重新选择')
        else:
            resume_mark = self.buy_record.resume_mark

            if resume_mark.accu_status in (1, 2):
                raise forms.ValidationError('改记录处于举报中，不能进行标记')

            current_mark = resume_mark.current_mark
            self.mark_relation = ResumeMarkRelation.objects.select_related(
                'mark'
            ).filter(
                parent=current_mark,
                mark__code_name=code_name,
            )
            if not self.mark_relation:
                raise forms.ValidationError('标记状态错误，请重新选择')

            self.mark = self.mark_relation[0].mark

        return self.cleaned_data

    def save(self):
        if not hasattr(self.buy_record, 'resume_mark'):
            resume_mark = DownloadResumeMark(
                buy_record=self.buy_record,
                current_mark=self.mark,
            )
        else:
            resume_mark = self.buy_record.resume_mark
            resume_mark.last_mark = resume_mark.current_mark
            resume_mark.current_mark = self.mark

        if self.mark.has_interview:
            resume_mark.has_interview = True
            PartnerCoinUtils.interview(
                self.buy_record.feed_id,
                self.buy_record.resume_id
            )

        if not self.mark.is_accu:
            resume_mark.accu_status = 0

        if self.mark.is_taking_work:
            PartnerCoinUtils.verify_taking_work(
                self.buy_record.feed_id,
                self.buy_record.resume_id
            )

        resume_mark.save()

        desc = self.request.POST.get('desc', '')
        is_display = True if self.request.POST.get('is_display') else False
        user = self.request.user
        mark_log = UserMarkLog(
            resume_mark=resume_mark,
            mark=self.mark,
            desc=desc,
            is_display=is_display,
            user=user,
        )
        mark_log.save()
        return resume_mark


class InterviewTimeMixin(object):

    def clean_interview_time(self):
        now = datetime.datetime.now()
        interview_time = self.cleaned_data['interview_time']
        if interview_time < now:
            raise forms.ValidationError('面试时间不能小于当前时间')
        return interview_time


class InterviewMarkForm(MarkResumeForm, InterviewTimeMixin, FormErrors):
    CODE_NAME_CHOICES = (
        ('invite_interview', '安排面试'),
        ('next_interview', '安排面试'),
    )
    code_name = forms.ChoiceField(label='标记选项', choices=CODE_NAME_CHOICES)
    interview_time = forms.DateTimeField(label='面试时间')


class UpdateInterviewAlarmForm(forms.ModelForm, InterviewTimeMixin, FormErrors):

    class Meta:
        model = InterviewAlarm
        fields = (
            'interview_time',
        )
