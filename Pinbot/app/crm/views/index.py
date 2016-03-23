# coding: utf-8

from django.views.generic import View, ListView
from django.shortcuts import render, redirect

from pin_utils.mixin_utils import (
    StaffRequiredMixin
)


class Home(StaffRequiredMixin, View):

    def get(self, request):
        template_name = 'home.html'
        return render(
            request,
            template_name
        )


class CandidaeDetails(StaffRequiredMixin, View):

    def get(self, request):
        template_name = 'candidate/details.html'
        return render(
            request,
            template_name
        )
