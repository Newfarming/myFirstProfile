# coding: utf-8

from django.views.generic import View
from django.shortcuts import render

from .mixin_utils import StaffRequiredMixin


class XAdminOperationForm(StaffRequiredMixin, View):
    template = ''

    def get(self, request, op_id):
        return render(
            request,
            self.template,
            {'op_id': op_id},
        )
