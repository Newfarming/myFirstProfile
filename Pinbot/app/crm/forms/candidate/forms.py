# coding: utf-8

from django import forms

from app.crm.models import (
    CandidateRemark,
)


class CandidateRemarkForm(forms.ModelForm):

    class Meta:
        model = CandidateRemark
        fields = (
            'remark_type',
            'desc',
        )
