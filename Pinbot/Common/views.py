# coding: utf-8

from django.views.generic import TemplateView

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)


class AdminTplView(StaffRequiredMixin, TemplateView):
    pass
