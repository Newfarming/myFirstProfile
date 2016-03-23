# coding: utf-8

from django import forms

from .models import Company

from Common.forms import NormalizeFormStringMixin
from pin_utils.form_mixin import FormErrors


class CompanyForm(NormalizeFormStringMixin, forms.ModelForm, FormErrors):
    product_url = forms.URLField(
        max_length=100,
        required=False,
        label='网址',
        error_messages={
            'max_length': 'url长度不能超过100个字符',
        }
    )

    class Meta:
        model = Company
        exclude = (
            'user',
            'add_time',
            'core_team',
            'pinbot_recommend',
            'favour_count',
            'need_recommend',
            'url',
        )
