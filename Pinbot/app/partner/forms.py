# coding: utf-8

from django import forms

from .models import (
    UploadResume,
    UploadTaskSetting,
    ResumeWork,
    ResumeProject,
    ResumeEducation,
    ResumeSkill,
)

from Common.forms import (
    NormalizeFormStringMixin,
    DatetimeCleanMixin,
)

from resumes.models import (
    ContactInfoData,
)

from pin_utils.django_utils import (
    error_phone,
    error_email,
    error_qq,
)


class UploadTaskSettingForm(NormalizeFormStringMixin, forms.ModelForm):

    class Meta:
        model = UploadTaskSetting
        exclude = [
            'user',
        ]


class ResumePersonInfoForm(
        NormalizeFormStringMixin,
        forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.resume = kwargs.pop('update_resume', None)
        super(ResumePersonInfoForm, self).__init__(*args, **kwargs)
        self.fields['qq'].required = False

    def clean_target_salary(self):
        salary = self.cleaned_data['target_salary']
        if salary < 1 or salary > 999:
            raise forms.ValidationError(u'期望薪资必须在1k~999k之间')
        return salary * 1000

    def clean_email(self):
        '''
        判断简历重复需要从上传简历和简历库判断
        新录入简历判断重复，直接从pinbot简历库ContactInfoData里判断是否存在，
        即没有录入简历UploadResume并且ContactInfoData不存在才能通过

        编辑简历判断重复，如果用户编辑的简历联系信息是自己上传的简历UploadResume即可以录入
        如果用户编辑的简历联系信息不存在，并且不在聘宝简历库中，与新简历信息录入判断逻辑一
        致
        '''

        email = self.cleaned_data['email'].lower()
        if error_email(email):
            raise forms.ValidationError('邮件格式有误，请重新填写')

        has_email_resume = UploadResume.objects.filter(
            email=email
        ).values_list('id', flat=True)

        has_contact_email = ContactInfoData.objects.filter(
            email=email
        ).exists()

        if not has_email_resume and not has_contact_email:
            return email

        if self.resume and self.resume.id in has_email_resume:
            return email

        raise forms.ValidationError('邮箱已存在，请重新填写')

    def clean_phone(self):
        '''
        判断简历重复需要从上传简历和简历库判断
        新录入简历判断重复，直接从pinbot简历库ContactInfoData里判断是否存在，
        即没有录入简历UploadResume并且ContactInfoData不存在才能通过

        编辑简历判断重复，如果用户编辑的简历联系信息是自己上传的简历UploadResume即可以录入
        如果用户编辑的简历联系信息不存在，并且不在聘宝简历库中，与新简历信息录入判断逻辑一
        致
        '''

        phone = self.cleaned_data['phone']
        if error_phone(phone):
            raise forms.ValidationError('电话号码有误，请填写正确格式的电话号码')

        has_phone_resume = UploadResume.objects.filter(
            phone=phone
        ).values_list('id', flat=True)

        has_contact_phone = ContactInfoData.objects.filter(
            phone=phone
        ).exists()

        if not has_phone_resume and not has_contact_phone:
            return phone

        if self.resume and self.resume.id in has_phone_resume:
            return phone

        raise forms.ValidationError('电话已经存在，请重新填写')

    def clean_qq(self):
        qq = self.cleaned_data['qq']
        if not qq:
            return ''

        if error_qq(qq):
            raise forms.ValidationError('QQ格式有误，请重新填写')
        return qq

    class Meta:
        model = UploadResume
        fields = (
            'name',
            'gender',
            'phone',
            'email',
            'work_years',
            'age',
            'self_evaluation',
            'degree',
            'qq',
            'address',
            'job_hunting_state',
            'expect_work_place',
            'expect_position',
            'target_salary',
            'last_contact',
            'hr_evaluate',
        )


class ResumeWorkInfoForm(NormalizeFormStringMixin, forms.ModelForm, DatetimeCleanMixin):

    start_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )

    class Meta:
        model = ResumeWork
        fields = (
            'start_time',
            'end_time',
            'position_title',
            'company_name',
            'job_desc',
        )


class ResumeProjectInfoForm(NormalizeFormStringMixin, forms.ModelForm, DatetimeCleanMixin):

    start_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )

    class Meta:
        model = ResumeProject
        fields = (
            'start_time',
            'end_time',
            'project_name',
            'project_desc',
        )


class ResumeSkillInfoForm(NormalizeFormStringMixin, forms.ModelForm):

    class Meta:
        model = ResumeSkill
        fields = (
            'skill_desc',
            'proficiency',
        )


class ResumeEduInfoForm(NormalizeFormStringMixin, forms.ModelForm, DatetimeCleanMixin):
    start_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )

    class Meta:
        model = ResumeEducation
        fields = (
            'start_time',
            'end_time',
            'school',
            'degree',
            'major',
        )
