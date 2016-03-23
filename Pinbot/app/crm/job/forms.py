# coding: utf-8

from django import forms

from ..models import (
    CRMFeedRemark,
)


class CRMFeedRemarkForm(forms.ModelForm):

    class Meta:
        model = CRMFeedRemark
        fields = (
            'feed',
            'remark_type',
            'remark',
        )
