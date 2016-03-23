# coding: utf-8

import datetime
import bleach

from django import forms

from .models import (
    Resume,
    WorkExperience,
    Project,
    Education,
    ProfessionalSkill,
)

from pin_utils.django_utils import (
    error_phone,
)


class DatetimeCleanMixin(object):
    start_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )
    min_time = datetime.datetime(1990, 01, 01)
    max_time = datetime.datetime(2100, 01, 01)

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if self.max_time < start_time or start_time < self.min_time:
            raise forms.ValidationError('所选时间必须在1990-01~2100-01之间')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        if self.max_time < end_time or end_time < self.min_time:
            raise forms.ValidationError('所选时间必须在1990-01~2100-01之间')
        return end_time


class NormalizeFormStringMixin(object):

    def clean(self):
        super(forms.ModelForm, self).clean()
        for key, value in self.cleaned_data.iteritems():
            if isinstance(value, basestring):
                value = bleach.clean(value.strip(), tags=['br'], strip=True)
            self.cleaned_data[key] = value
        return self.cleaned_data


class SocialPageForm(forms.Form):
    url = forms.URLField(
        max_length=100,
        error_messages={
            'max_length': 'url长度不能超过100个字符',
        }
    )


class PersonInfoForm(NormalizeFormStringMixin, forms.ModelForm):

    class Meta:
        model = Resume
        fields = ('name', 'age', 'self_evaluation')


class ContactInfoForm(forms.ModelForm):

    def clean_phone(self):
        phone = self.data['phone']

        if error_phone(phone):
            raise forms.ValidationError(
                u'电话号码格式错误，请填写正确的手机号'
            )
        return phone

    class Meta:
        model = Resume
        fields = ('phone', 'email')


class SelfIntroForm(NormalizeFormStringMixin, forms.ModelForm):

    class Meta:
        model = Resume
        fields = ('self_evaluation',)


class WorkExperienceForm(NormalizeFormStringMixin, forms.ModelForm, DatetimeCleanMixin):

    start_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )

    class Meta:
        model = WorkExperience
        fields = (
            'start_time',
            'end_time',
            'position_title',
            'company_name',
            'job_desc',
        )


class ProjectForm(NormalizeFormStringMixin, forms.ModelForm, DatetimeCleanMixin):

    start_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )

    class Meta:
        model = Project
        fields = (
            'project_desc',
            'start_time',
            'end_time',
            'responsible_for',
            'company_name',
            'project_name',
        )


class EducationForm(NormalizeFormStringMixin, forms.ModelForm, DatetimeCleanMixin):

    start_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y-%m',
        ),
    )

    class Meta:
        model = Education
        fields = (
            'start_time',
            'end_time',
            'school',
            'degree',
            'major',
        )


class ProfessionalSkillForm(NormalizeFormStringMixin, forms.ModelForm):

    class Meta:
        model = ProfessionalSkill
        fields = (
            'skill_desc',
            'proficiency',
            'month',
        )
