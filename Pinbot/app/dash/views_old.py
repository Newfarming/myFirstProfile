# coding: utf-8

import csv

from django.views.generic import View
from django.http import HttpResponse

from .models import (
    PinbotDailyReport,
)

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)


class WeekReportCSV(StaffRequiredMixin, View):

    filename = 'weekreport'

    def get_queryset(self):
        queryset = PinbotDailyReport.objects.raw(
            '''
            SELECT
            `dash_pinbotdailyreport`.`id`,
            SUM(`dash_pinbotdailyreport`.`register_user_count`) AS `register_user_count`,
            MAX(`dash_pinbotdailyreport`.`total_user_count`) AS `total_user_count`,
            SUM(`dash_pinbotdailyreport`.`login_user_count`) AS `login_user_count`,
            SUM(`dash_pinbotdailyreport`.`pay_user_count`) AS `pay_user_count`,
            MAX(`dash_pinbotdailyreport`.`total_pay_count`) AS `total_pay_count`,
            DATE_ADD(`report_date`, INTERVAL(1-DAYOFWEEK(`report_date`)) DAY) AS `start_date`,
            DATE_ADD(`report_date`, INTERVAL(7-DAYOFWEEK(`report_date`)) DAY) AS `end_date`
            FROM `dash_pinbotdailyreport`
            GROUP BY YEARWEEK(`dash_pinbotdailyreport`.`report_date`)
            ORDER BY YEARWEEK(`dash_pinbotdailyreport`.`report_date`)
            '''
        )
        return queryset

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.filename
        response.write('\xEF\xBB\xBF')
        writer = csv.writer(response)
        writer.writerow(
            ['开始时间', '结束时间', '注册用户数', '总用户数', '登陆用户数', '付款用户数', '付款用户总数']
        )
        queryset = self.get_queryset()
        for row in queryset:
            writer.writerow([
                row.start_date.strftime('%Y-%m-%d'),
                row.end_date.strftime('%Y-%m-%d'),
                row.register_user_count,
                row.total_user_count,
                row.login_user_count,
                row.pay_user_count,
                row.total_pay_count,
            ])
        return response


class MonthReportCSV(WeekReportCSV):

    filename = 'monthreport'

    def get_queryset(self):
        queryset = PinbotDailyReport.objects.raw(
            '''
            SELECT
            `dash_pinbotdailyreport`.`id`,
            SUM(`dash_pinbotdailyreport`.`register_user_count`) AS `register_user_count`,
            MAX(`dash_pinbotdailyreport`.`total_user_count`) AS `total_user_count`,
            SUM(`dash_pinbotdailyreport`.`login_user_count`) AS `login_user_count`,
            SUM(`dash_pinbotdailyreport`.`pay_user_count`) AS `pay_user_count`,
            MAX(`dash_pinbotdailyreport`.`total_pay_count`) AS `total_pay_count`,
            DATE_SUB(`report_date`, INTERVAL DAYOFMONTH(`report_date`)-1 DAY) AS `start_date`,
            LAST_DAY(`report_date`) AS `end_date`
            FROM `dash_pinbotdailyreport`
            GROUP BY YEAR(`dash_pinbotdailyreport`.`report_date`), MONTH(`dash_pinbotdailyreport`.`report_date`)
            ORDER BY YEAR(`dash_pinbotdailyreport`.`report_date`), MONTH(`dash_pinbotdailyreport`.`report_date`)
            '''
        )
        return queryset
