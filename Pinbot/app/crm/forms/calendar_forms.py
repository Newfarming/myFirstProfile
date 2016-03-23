# coding: utf-8

from django import forms

from app.crm.models import (
    AdminSchedule
)


class AdminScheduleForm(forms.ModelForm):

    class Meta:
        model = AdminSchedule
        fields = (
            'title',
            'start_time',
            'url',
            'backgroundcolor',
        )
