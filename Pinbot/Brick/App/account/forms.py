# coding: utf-8

import re

from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import login, authenticate

from .models import (
    UserProfile,
)
from .account_utils import (
    SendMailMixin,
)

from app.invite.models import (
    InviteCode,
    InviteCodeApply,
)

from Brick.Utils.form_mixin import FormErrors
from Brick.Utils.django_utils import (
    get_object_or_none,
    error_email,
)


class RegisterUserForm(forms.Form, FormErrors, SendMailMixin):

    # 由于前期生成了重复的邀请码，这两个邀请码需要同时验证邀请码
    # 和邮箱才能通过
    SPECIAL_CODE = ['pauq3k7FDf', 'wFoTjyM2DY']

    username = forms.CharField(
        max_length=30,
        label=u'账户',
        widget=forms.TextInput(attrs={'placeholder': '手机/邮箱'})
    )
    password = forms.CharField(
        max_length=30,
        label=u'密码',
        widget=forms.TextInput(attrs={'placeholder': '密码', 'type': 'password'})
    )
    invite_code = forms.CharField(
        max_length=20,
        label=u'邀请码',
        widget=forms.TextInput(attrs={'placeholder': '邀请码'})
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()

        if error_email(username):
            raise forms.ValidationError('请输入正确格式的邮箱！')

        self.user = get_object_or_none(
            User,
            username=username
        )

        try:
            brick_profile = self.user.brick_user_profile if self.user else None
        except UserProfile.DoesNotExist:
            brick_profile = None

        if brick_profile:
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if self.user:
            return password

        is_strong = re.match(r'(?=.*\d)(?=.*([a-z]|[A-Z])).{8,20}', password)
        if not is_strong:
            raise forms.ValidationError('密码应为8~20个数字+字母！')
        return password

    def clean_invite_code(self):
        code = self.cleaned_data['invite_code']

        if code in self.SPECIAL_CODE:
            # special code must valid code and apply email
            # because those code are duplicate
            email = self.data['username']
            invite_code = get_object_or_none(
                InviteCodeApply,
                email=email,
                invite_code=code,
                status='success',
            )
            if not invite_code:
                raise forms.ValidationError('邀请码必须跟申请邀请码邮箱一致')
        else:
            invite_code = get_object_or_none(
                InviteCode,
                code=code,
                status='unused'
            )
            if not invite_code:
                raise forms.ValidationError('邀请码不正确！')
        return code

    def save(self):
        form_data = self.cleaned_data
        username = form_data['username'].lower()
        password = form_data['password']
        invite_code = form_data['invite_code']

        with transaction.atomic():
            if not self.user:
                user = User.objects.create_user(
                    username,
                    password=password,
                )
                user.is_active = False
                user.save()
            else:
                user = self.user

            user_profile = UserProfile(user=user)
            user_profile.save()

            InviteCode.objects.filter(
                code=invite_code
            ).update(
                status='used'
            )
            return user_profile


class CheckUserInForm(RegisterUserForm):
    '''Check user in form'''

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckUserInForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if error_email(username):
            raise forms.ValidationError('请输入有效的邮箱')
        return username

    def check_in_result(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = get_object_or_none(
            User,
            username=username,
        )
        if not user:
            user_profile = self.save()
            self.send_active_email(user_profile.user)
            return {
                'status': 'register_success',
                'msg': u'注册成功',
            }
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            login(self.request, auth_user)
            return {
                'status': 'ok',
                'msg': u'登录成功',
            }
        else:
            return {
                'status': 'passwd_error',
                'msg': u'密码错误',
            }


class BaseChangePassword(forms.Form, FormErrors):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseChangePassword, self).__init__(*args, **kwargs)

    password = forms.CharField(
        max_length=30,
        label=u'新密码',
        widget=forms.TextInput(attrs={'placeholder': '密码', 'type': 'password'})
    )
    confirm_password = forms.CharField(
        max_length=30,
        label=u'确认密码',
        widget=forms.TextInput(attrs={'placeholder': '密码', 'type': 'password'})
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        is_strong = re.match(r'(?=.*\d)(?=.*([a-z]|[A-Z])).{8,20}', password)
        if not is_strong:
            raise forms.ValidationError('密码应为8~20个数字+字母！')
        return password

    def clean_confirm_password(self):
        password = self.data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('两次密码不一样')
        return confirm_password

    def change_user_password(self):
        password = self.cleaned_data['password']
        self.user.set_password(password)
        self.user.save()
        return True


class ResetPasswordForm(BaseChangePassword):
    pass


class ChangePasswordForm(BaseChangePassword):

    old_password = forms.CharField(
        max_length=30,
        label=u'旧密码',
        widget=forms.TextInput(attrs={'placeholder': '密码', 'type': 'password'})
    )

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']

        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码错误')
        return old_password


class LoginForm(forms.Form):
    '''Login form'''
    username = forms.CharField(
        max_length=60,
        label="账户",
        widget=forms.TextInput(attrs={'placeholder': '手机/邮箱'})
    )
    password = forms.CharField(
        max_length=30,
        label=u'密码',
        widget=forms.TextInput(attrs={'placeholder': '密码', 'type': 'password'})
    )
