# coding: utf-8

from django import forms

from .models import (
    InviteCodeApply,
)

from pin_utils.django_utils import (
    get_object_or_none,
    error_email,
    error_phone,
    get_client_ip,
)
from pin_utils.form_mixin import (
    FormErrors,
)


class InviteCodeApplyForm(forms.ModelForm, FormErrors):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InviteCodeApplyForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if error_email(email):
            raise forms.ValidationError('邮件格式有误，请重新填写')
        has_apply = get_object_or_none(
            InviteCodeApply,
            email=email,
        )
        if has_apply:
            raise forms.ValidationError('一个邮箱只能申请一次')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if error_phone(phone):
            raise forms.ValidationError('电话号码有误，请填写正确格式的电话号码')
        return phone

    def save(self):
        apply_data = self.cleaned_data
        ip = get_client_ip(self.request)
        other_city = self.request.POST.get('other_city')
        apply_city = apply_data['city']

        apply_info = InviteCodeApply(
            email=apply_data['email'],
            job=apply_data['job'],
            city=other_city if apply_city == '其他' else apply_city,
            phone=apply_data['phone'],
            apply_desc=apply_data['apply_desc'],
            ip=ip,
        )
        apply_info.save()
        return apply_info

    class Meta:
        model = InviteCodeApply
        exclude = ('ip', 'status', 'apply_time', 'invite_code')
