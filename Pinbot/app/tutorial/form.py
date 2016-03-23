# coding: utf8

from django import forms

from .models import FeedBackText
from pin_utils.django_utils import error_email
from pin_utils.form_mixin import FormErrors
from Common.forms import NormalizeFormStringMixin


class FeedBackTextForm(NormalizeFormStringMixin, forms.ModelForm, FormErrors):

    def clean_contact_email(self):
        email = self.cleaned_data['contact_email'].lower().strip()
        if error_email(email):
            raise forms.ValidationError(u'邮件格式错误')
        return email

    class Meta:
        model = FeedBackText
        fields = (
            'feedback_text',
            'contact_email'
        )
