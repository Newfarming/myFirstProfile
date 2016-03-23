# coding: utf-8

from django.views.generic import View, ListView
from django.shortcuts import render, redirect

from app.dash.runtime.report import (
    PinbotDashReport
)

from pin_utils.django_utils import (
    JsonResponse,
    get_object_or_none,
)
from pin_utils.mixin_utils import (
    CSRFExemptMixin,
    StaffRequiredMixin
)


class ViewDailyReport(StaffRequiredMixin, View):
    """查看每日报表"""

    def get(self, request, report_type, report_name):
        if report_type == 'daily':
            template_name = 'report_daily.html'
        if report_type == 'week':
            template_name = 'report_week.html'
        if report_type == 'month':
            template_name = 'report_month.html'

        return render(
            request,
            template_name,
            {
                'report_name': report_name,
                'report_type': report_type
            }
        )


class GetDailyReport(StaffRequiredMixin, View):
    """查看今日报表"""

    def get(self, request, report_type, report_name, date_range=None):
        pinbot_dash_report = PinbotDashReport(report_name=report_name)
        if date_range is not None:
            date_range = (date_range[0:10], date_range[11:23])
            ret_data = pinbot_dash_report.get_today_report(date_range=date_range)
        else:
            if report_type == 'daily':
                ret_data = pinbot_dash_report.get_today_report()
            if report_type == 'week':
                ret_data = pinbot_dash_report.get_week_report()
            if report_type == 'month':
                ret_data = pinbot_dash_report.get_month_report()

        return JsonResponse(ret_data)