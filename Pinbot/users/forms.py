# coding: utf-8

import re
import bleach

from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, UserContactInfo
from users.runtime.account import (
    PinbotAccount
)
from jobs.models import (
    Company,
    CompanyCategory,
)

from Common.forms import (
    NormalizeFormStringMixin,
)

from pin_utils.form_mixin import (
    FormErrors,
)
from pin_utils.django_utils import (
    error_phone,
    error_email,
    get_object_or_none,
)
from pin_utils.sms.sms_code import (
    SmsCode
)


class UserRegistrationForm(forms.Form):
    company_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class UserProfileForm(NormalizeFormStringMixin, forms.Form):
    company_name = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=False)
    qq = forms.CharField(required=False, max_length=255)
    phone = forms.CharField(required=False)
    url = forms.URLField(required=False)
    name = forms.CharField(required=False, max_length=100)
    notify_email = forms.CharField(required=False, max_length=100)
    is_email_bind = forms.CharField(required=False, max_length=100)
    is_phone_bind = forms.CharField(required=False, max_length=100)
    province = forms.CharField(required=False, max_length=50)
    city = forms.CharField(required=False, max_length=50)
    street = forms.CharField(required=False, max_length=100)
    postcode = forms.CharField(required=False, max_length=10)
    area = forms.CharField(required=False, max_length=50)
    recv_name = forms.CharField(required=False, max_length=50)
    recv_phone = forms.CharField(required=False, max_length=50)


class SimpleEmailForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    server = forms.CharField(max_length=50)


class PasswordResetForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(max_length=10)


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(max_length=20)
    new_password2 = forms.CharField(max_length=20)


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(required=True, max_length=20)
    new_password1 = forms.CharField(required=True, max_length=20)
    new_password2 = forms.CharField(required=True, max_length=20)


class BaseRegisterForm(NormalizeFormStringMixin, forms.ModelForm, FormErrors):

    '''
    注册form
    '''
    password = forms.CharField(
        max_length=30,
        label=u'密码',
        widget=forms.TextInput(attrs={'placeholder': '密码', 'type': 'password'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BaseRegisterForm, self).__init__(*args, **kwargs)

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
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        is_strong = re.match(r'(?=.*\d)(?=.*([a-z]|[A-Z])).{6,20}', password)
        if not is_strong:
            raise forms.ValidationError('密码必须是包含字母和数字的6~20位字符')
        return password

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if error_phone(phone):
            raise forms.ValidationError('电话号码有误，请填写正确格式的电话号码')
        return phone

    def clean_confirm_password(self):
        password = self.data['password']
        confirm_password = self.data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('两次密码不一样，请重新输入。')
        return confirm_password

    def save_user_profile(self, user):
        company_name = self.cleaned_data['company_name']
        company_name = bleach.clean(company_name, tags=[], strip=True)
        user_profile = UserProfile(
            user=user,
            is_review=True,
            ip=self.request.environ['REMOTE_ADDR'],
            user_email=self.cleaned_data['user_email'],
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            qq=self.cleaned_data['qq'],
            role=self.cleaned_data['role'],
            company_name=company_name,
            url=self.cleaned_data['url'],
        )
        return user_profile

    def save(self):
        email = self.cleaned_data['user_email'].lower()
        password = self.cleaned_data['password']
        company_name = self.cleaned_data['company_name']

        user = User.objects.create_user(
            email,
            email,
            password,
        )
        user.is_active = False
        user.first_name = company_name
        user_profile = self.save_user_profile(user)
        user.save()
        user_profile.save()
        return user_profile

    class Meta:
        model = UserProfile
        exclude = (
            'user',
            'is_review',
            'status',
            'street',
            'city',
            'province',
            'postcode',
            'activation_key',
            'ip',
            'company_email',
            'source',
        )


class RegisterForm(BaseRegisterForm):
    confirm_password = forms.CharField(
        max_length=30,
        label=u'确认密码',
        widget=forms.TextInput(
            attrs={
                'placeholder': '确认密码',
                'type': 'password'
            }
        )
    )


class AccountCompanyForm(forms.Form, FormErrors):

    company_name = forms.CharField(
        label='公司名称',
        max_length=50,
    )
    company_url = forms.CharField(
        max_length=100,
        label='公司网址',
    )


class AccountMyInfoForm(forms.Form, FormErrors):

    realname = forms.CharField(
        label='真实姓名',
        max_length=20,
    )
    qq = forms.CharField(
        max_length=50,
        label='联系qq',
    )


class AccountMyRecvInfoForm(forms.Form, FormErrors):

    street = forms.CharField(
        label='收货地址',
        max_length=200,
    )
    province = forms.CharField(
        max_length=50,
        label='省份',
    )
    city = forms.CharField(
        max_length=50,
        label='城市',
    )
    area = forms.CharField(
        max_length=50,
        label='区县',
    )
    recv_phone = forms.CharField(
        max_length=50,
        label='收货人电话',
    )
    recv_name = forms.CharField(
        max_length=50,
        label='收货人姓名',
    )

    def clean_recv_phone(self):
        recv_phone = self.cleaned_data['recv_phone']
        if error_phone(recv_phone):
            raise forms.ValidationError('电话号码有误，请填写正确格式的电话号码')
        return recv_phone


class AccountMyPasswordForm(forms.Form, FormErrors):

    old_password = forms.CharField(
        required=True,
        max_length=20,
        label='旧密码',
    )
    new_password = forms.CharField(
        required=True,
        max_length=20,
        label='新密码',
    )
    confirm_password = forms.CharField(
        required=True,
        max_length=20,
        label='确认新密码',
    )

    def clean_new_password(self):

        new_password = self.cleaned_data['new_password']
        is_strong = re.match(r'(?=.*\d)(?=.*([a-z]|[A-Z])).{6,20}', new_password)
        if not is_strong:
            raise forms.ValidationError('密码必须是包含字母和数字的6~20位字符')
        return new_password

    def clean_confirm_password(self):
        new_password = self.data['new_password']
        confirm_password = self.data['confirm_password']

        if new_password != confirm_password:
            raise forms.ValidationError('两次密码不一样，请重新输入。')
        return confirm_password


class AccountRegisterForm(BaseRegisterForm):
    code = forms.CharField(
        max_length=30,
        label=u'短信验证码',
        widget=forms.TextInput(
            attrs={
                'placeholder': '短信验证码',
                'type': 'text'
            }
        )
    )
    select_fields = forms.ModelMultipleChoiceField(
        queryset=CompanyCategory.objects.all(),
        label=u'所在领域',
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if error_phone(phone):
            raise forms.ValidationError('电话号码有误，请填写正确格式的电话号码')

        if PinbotAccount.is_phone_bind(mobile=phone):
            raise forms.ValidationError('该手机号%s已被注册,请使用其他手机号注册!' % (phone))

        return phone

    def clean_code(self):
        code = self.cleaned_data['code']
        phone = self.data['phone']
        if not SmsCode.vaild_sms_code(code=code, mobile=phone, action_name='AccountReg'):
            raise forms.ValidationError('验证码错误错误')
        return code

    def save_user_profile(self, user):
        company_name = self.cleaned_data['company_name']
        phone = self.cleaned_data['phone']
        user_profile = UserProfile(
            user=user,
            is_review=True,
            ip=self.request.environ['REMOTE_ADDR'],
            user_email=self.cleaned_data['user_email'],
            name=self.cleaned_data['name'],
            phone=phone,
            qq=self.cleaned_data['qq'],
            company_name=company_name,
        )
        company = Company(
            company_name=company_name,
            user=user,
        )
        company.save()
        company.category.add(*self.cleaned_data['select_fields'])
        company.save()
        SmsCode.delete_cache_code(phone, 'AccountReg')
        return user_profile

    class Meta:
        model = UserProfile
        exclude = (
            'user',
            'is_review',
            'status',
            'street',
            'city',
            'province',
            'postcode',
            'activation_key',
            'ip',
            'company_email',
            'source',
            'role',
            'url',
        )


class VipRegisterForm(BaseRegisterForm):

    select_fields = forms.ModelMultipleChoiceField(
        queryset=CompanyCategory.objects.all(),
        label=u'所在领域',
    )

    def save_user_profile(self, user):
        company_name = self.cleaned_data['company_name']
        user_profile = UserProfile(
            user=user,
            is_review=True,
            ip=self.request.environ['REMOTE_ADDR'],
            user_email=self.cleaned_data['user_email'],
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            qq=self.cleaned_data['qq'],
            company_name=company_name,
        )
        company = Company(
            company_name=company_name,
            user=user,
        )
        company.save()
        company.category.add(*self.cleaned_data['select_fields'])
        company.save()
        return user_profile

    class Meta:
        model = UserProfile
        exclude = (
            'user',
            'is_review',
            'status',
            'street',
            'city',
            'province',
            'postcode',
            'activation_key',
            'ip',
            'company_email',
            'source',
            'role',
            'url',
        )


class BDUserPasswordForm(forms.Form, FormErrors):

    password = forms.CharField(max_length=20)
    confirm_password = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BDUserPasswordForm, self).__init__(*args, **kwargs)

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

    def save(self):
        self.user.is_active = True
        self.user.set_password(self.cleaned_data['password'])
        self.user.save()
        return True


class UserContactInfoForm(NormalizeFormStringMixin, forms.ModelForm, FormErrors):

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if error_phone(phone):
            raise forms.ValidationError('电话号码有误，请填写正确格式的电话号码')
        return phone

    class Meta:
        model = UserContactInfo
        fields = (
            'name',
            'phone',
        )
