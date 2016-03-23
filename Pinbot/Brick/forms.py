# coding: utf-8

from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    captcha = CaptchaField()
