# coding: utf-8
import requests
import json
from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from users.models import (
    UserProfile as bUserProfile
)
from Brick.App.account.models import (
    UserProfile as cUserProfile
)

from app.sendemail.models import (
    MailTemplate,
    MailTemplateCategory,
    MailTags
)

from pin_utils.form_mixin import (
    FormErrors,
)
from pin_utils.django_utils import (
    get_object_or_none
)

from pin_utils.email.send_mail import (
    MailUtils
)


class MailTemplateManage(forms.ModelForm, FormErrors):

    """邮件模板管理类"""
    TEST_USERS = [
        "shigang@hopperclouds.com",
        "liguangyi@hopperclouds.com",
        "fengjingyi@hopperclouds.com",
        "lilinpu@hopperclouds.com",
        "houxinqi@hopperclouds.com",
        "zengwawa@hopperclouds.com",
        "chenchao@hopperclouds.com"
    ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MailTemplateManage, self).__init__(*args, **kwargs)
        # assign a (computed, I assume) default value to the choice field
        self.initial['category'] = 1
        # you should NOT do this:
        self.fields['category'].initial = 1

    def clean_name(self):
        name = self.cleaned_data['name'].lower()

        exist_tpl_name = get_object_or_none(
            MailTemplate,
            name=name
        )

        if exist_tpl_name:
            raise forms.ValidationError('模板名已存在!')
        return name

    def clean_tag_name(self):
        tag_name = self.cleaned_data['tag_name'].lower()

        exist_tpl_name = get_object_or_none(
            MailTemplate,
            name=tag_name
        )

        if exist_tpl_name:
            raise forms.ValidationError('模板标签已存在!')
        return tag_name

    def add_tpl(self):
        self.save()
        return True

    @classmethod
    def edit_tpl(self, tpl_id, category_id, template_name, template_content):
        category_obj = get_object_or_none(
            MailTemplateCategory,
            id=category_id,
        )

        template_obj = self.get_tpl(id=tpl_id)
        if template_obj.name != template_name:
            template_obj.name = template_name
        template_obj.category = category_obj
        template_obj.content = template_content
        template_obj.save()

        return True

    @classmethod
    def get_tpl(self, **kwargs):
        template = get_object_or_none(
            MailTemplate,
            **kwargs
        )
        return template

    @classmethod
    def get_all_tpl(self):
        return MailTemplate.objects.all()

    @classmethod
    def get_send_target(self, **kwargs):

        send_users = []

        if kwargs['test_users']:
            send_users.extend(self.TEST_USERS)
        if kwargs['b_user']:
            b_users = bUserProfile.objects.filter(is_email_bind=True).values_list('user_email', flat=True)
            send_users.extend(b_users)
        if kwargs['c_user']:
            c_users = cUserProfile.objects.select_related('user').filter(user__is_active=True).values_list('user__username', flat=True)
            send_users.extend(c_users)
        if kwargs.get('b_unactive_user'):
            b_unactive_user = bUserProfile.objects.select_related('user').filter(user__is_active=False).values_list('user__username', flat=True)
            send_users.extend(b_unactive_user)

        return send_users

    class Meta:
        model = MailTemplate

        widgets = {
            'content': SummernoteInplaceWidget()
        }


class MailTemplateCategoryManage(forms.ModelForm, FormErrors):

    """邮件模板分类管理类"""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MailTemplateCategoryManage, self).__init__(*args, **kwargs)

    @classmethod
    def clean_name(self):
        name = self.cleaned_data['name'].lower()

        exist_tpl_name = get_object_or_none(
            MailTemplateCategory,
            name=name
        )

        if exist_tpl_name:
            raise forms.ValidationError('分类名已存在!')
        return name

    @classmethod
    def add_tpl_category(self):
        self.save()

    @classmethod
    def get_all_category(self):
        return MailTemplateCategory.objects.all()

    class Meta:
        model = MailTemplateCategory


class MailTagsManage(forms.ModelForm, FormErrors):

    """邮件标签管理类"""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MailTagsManage, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name'].lower()

        exist_tpl_name = get_object_or_none(
            MailTemplateCategory,
            name=name
        )

        if exist_tpl_name:
            raise forms.ValidationError('标签名已存在!')
        return name

    def add_tag(self):

        self.save()
        tag_name = self.cleaned_data['tag_name']

        tag_obj = MailTags.objects.get(tag_name=tag_name)
        tag_id = self.create_taglabel(tag_name=tag_name)
        tag_obj.tag_id = tag_id
        tag_obj.save()
        return tag_obj

    def create_taglabel(self, **kwargs):

        add_tag_url = '%s%s' % (
            MailUtils.create_label_url,
            kwargs['tag_name']
        )
        ret = json.loads(requests.get(add_tag_url).content)
        label_id = None
        if ret['message'] == 'success':
            label_id = ret['label']['labelId']
        return label_id

    def delete_tablabel(self, tag_id):

        del_tag_url = '%s%s' % (
            MailUtils.delete_label_url,
            tag_id
        )
        tag_obj = MailTags.objects.get(tag_id=tag_id)
        tag_obj.delete()
        ret = json.loads(requests.get(del_tag_url).content)

        if ret['message'] == 'success':
            return True
        return False

    @classmethod
    def get_tag(self, **kwargs):
        return MailTags.objects.get(**kwargs)

    @classmethod
    def get_all_tags(self):
        return MailTags.objects.all()

    class Meta:
        model = MailTags
