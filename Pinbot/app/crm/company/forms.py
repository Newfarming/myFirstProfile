# coding: utf-8

from django import forms

from ..models import (
    CRMClientInfo,
)


class CreateCRMClientInfoForm(forms.ModelForm):

    class Meta:
        model = CRMClientInfo
        fields = (
            'client',
            'admin',
        )


class UpdateCRMClientInfoForm(forms.ModelForm):

    class Meta:
        model = CRMClientInfo
        fields = (
            'admin',
        )
