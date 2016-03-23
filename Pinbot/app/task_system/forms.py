# coding: utf-8

from django import forms
from Common.forms import NormalizeFormStringMixin


class AddressForm(NormalizeFormStringMixin, forms.Form):

    name = forms.CharField(max_length=8)
    province = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    street = forms.CharField(max_length=50)
