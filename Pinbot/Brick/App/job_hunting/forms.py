# coding: utf-8

from django import forms

from .models import JobMessage


class JobMessageForm(forms.ModelForm):

    class Meta:
        model = JobMessage
        fields = ('message', )
