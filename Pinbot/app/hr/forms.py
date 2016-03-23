# coding: utf-8

from django import forms
from django.contrib.auth import (
    authenticate,
)
from django.contrib.auth.models import User

from Common.forms import NormalizeFormStringMixin
from pin_utils.form_mixin import (
    FormErrors,
)

from ..weixin.runtime.weixin_utils import (
    WeixinService
)
from users.forms import BaseRegisterForm
from users.models import UserProfile
from jobs.models import (
    Company,
)

from pin_utils.django_utils import (
    error_email,
    get_object_or_none,
)
from pin_utils.sms.sms_code import (
    SmsCode
)


class RegisterForm(BaseRegisterForm, FormErrors):

    def clean_user_email(self):
        email = self.cleaned_data['user_email'].lower()
        if error_email(email):
            raise forms.ValidationError('邮件格式有误，请重新填写')
        exist_user = get_object_or_none(
            User,
            username=email,
        )
        if exist_user:
            raise forms.ValidationError('邮箱名已存在')

        openid = self.request.session.get('openid', '')
        has_weixin_user = WeixinService.get_weixin_user(openid=openid)
        if has_weixin_user:
            raise forms.ValidationError('微信用户已存在')
        return email

    def clean_code(self):
        code = self.cleaned_data['code']
        phone = self.data['phone']
        if not SmsCode.vaild_sms_code(code=code, mobile=phone, action_name='AccountReg'):
            raise forms.ValidationError('验证码错误错误')
        return code

    def save_user_profile(self, user):
        company_name = self.cleaned_data['company_name']
        user_profile = UserProfile(
            user=user,
            is_review=True,
            ip=self.request.environ['REMOTE_ADDR'],
            user_email=self.cleaned_data['user_email'],
            phone=self.cleaned_data['phone'],
            company_name=company_name,
            name=self.cleaned_data['name']
        )
        company = Company(
            company_name=company_name,
            user=user,
        )
        company.save()
        return user_profile

    class Meta:
        model = UserProfile
        fields = (
            'user_email',
            'company_name',
            'phone',
            'name'
        )


class LoginForm(NormalizeFormStringMixin, forms.Form, FormErrors):

    password = forms.CharField(
        label='密码',
    )
    username = forms.CharField(
        max_length=50,
        label='用户名',
    )

    def clean_username(self):
        form_data = self.data
        username = form_data.get('username', '')
        password = form_data.get('password', '')
        user = authenticate(
            username=username,
            password=password,
        )
        if not user:
            raise forms.ValidationError('用户名或密码错误')

        return username
