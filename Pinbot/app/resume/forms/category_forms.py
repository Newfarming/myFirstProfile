# coding: utf-8

from django import forms

from transaction.models import (
    BuyResumeCategory,
)

from Common.forms import NormalizeFormStringMixin


class CreateBuyRecordCategoryForm(NormalizeFormStringMixin, forms.ModelForm):

    class Meta:
        model = BuyResumeCategory
        fields = (
            'category_name',
        )


class UpdateBuyRecordCategoryForm(CreateBuyRecordCategoryForm):
    pass
