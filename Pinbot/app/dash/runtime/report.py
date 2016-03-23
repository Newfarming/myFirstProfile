# coding: utf-8
import sys
import types
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'
from time import strptime, strftime
from datetime import date, timedelta
import datetime
import calendar


from django.db.models import Sum
from django.core import serializers

from app.dash.models import (
    PartnerDailyReportData,
    UserDailyReportData,
    ResumeDailyReportData,
    CoreDailyReportData
)
from pin_utils.django_utils import (
    get_object_or_none,
    get_today,
    get_contrast,
)
from app.dash.settings.report_settings import (
    REPORT_SCHEMA
)

WEEK_START_NO = 24
MONTH_START_NO = 5
YEAR_START_NO = 2015


def get_week_days(year, week):
    d = date(year, 1, 1)
    if (d.weekday() > 3):
        d = d + timedelta(7 - d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days=(week-1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)


def get_month_day_range(year, month_no):

    month_list = []
    for month in range(13):
        if month >= month_no:
            x_date = datetime.date(year, month, 1)
            first_day = x_date.replace(day = 1)
            last_day = x_date.replace(day=calendar.monthrange(x_date.year, x_date.month)[1])
            if date.today() > last_day:
                month_list.append((first_day, last_day))
    return month_list


def str_to_class(field):
    try:
        identifier = getattr(sys.modules[__name__], field)
    except AttributeError:
        raise NameError("%s doesn't exist." % field)
    if isinstance(identifier, (types.ClassType, types.TypeType)):
        return identifier
    raise TypeError("%s is not a class." % field)


def get_final_data(current_ret, previous_ret, fields, report_name):

    fields_doc = {}

    """求非total数据的合"""
    for field in fields:

        if 'total_' not in field and field != 'task_accedpted_count_contrast':
            fields_doc[field] = Sum(field)

        if field == 'task_total_count':
            fields_doc[field] = Sum(field)

    current_data = current_ret.aggregate(**fields_doc)
    previous_data = previous_ret.aggregate(**fields_doc)

    if current_ret and previous_ret:

        """获取total数据"""
        for field in fields:

            if 'total_' in field and field != 'task_total_count':
                current_data[field] = current_ret.last().__dict__.get(field, 0)
                previous_data[field] = previous_ret.last().__dict__.get(field, 0)

    """为用户周/月报表单独处理部分"""
    if report_name == 'user_daily_report':

        try:
            previous_data['week_repeat_visit_count'] = previous_ret.first().week_repeat_visit_count
            previous_data['month_repeat_visit_count'] = previous_ret.first().month_repeat_visit_count
            previous_data['week_lively_user_count'] = previous_ret.first().week_lively_user_count
            previous_data['month_lively_user_count'] = previous_ret.first().month_lively_user_count

        except (IndexError, AttributeError), e:
            previous_data['week_repeat_visit_count'] = 0
            previous_data['month_repeat_visit_count'] = 0
            previous_data['week_lively_user_count'] = 0
            previous_data['month_lively_user_count'] = 0

        try:
            current_data['week_repeat_visit_count'] = current_ret.first().week_repeat_visit_count
            current_data['month_repeat_visit_count'] = current_ret.first().month_repeat_visit_count
            current_data['week_lively_user_count'] = current_ret.first().week_lively_user_count
            current_data['month_lively_user_count'] = current_ret.first().month_lively_user_count

        except (IndexError, AttributeError), e:
            current_data['week_repeat_visit_count'] = 0
            current_data['month_repeat_visit_count'] = 0
            current_data['week_lively_user_count'] = 0
            current_data['month_lively_user_count'] = 0

    return current_data, previous_data


class PinbotDashReport(object):
    """Pinbot数据报表"""

    def __init__(self, *args, **kwargs):
        self.report_name = kwargs['report_name']
        report_table_name = self.get_report_settings()['report_table_name']
        self.report_table_obj = str_to_class(report_table_name)

    def get_report_settings(self):
        return REPORT_SCHEMA[self.report_name]

    def get_today_report(self, date_range=None):
        if date_range is not None:

            results = self.report_table_obj.objects.filter(
                report_date__gte=date_range[0],
                report_date__lte=date_range[1],
            )
        else:
            results = self.report_table_obj.objects.all()

        return [result.as_json() for result in results]

    def get_week_report(self):

        report_data = []
        week_list = []
        for i in xrange(WEEK_START_NO, 54):
            x = get_week_days(YEAR_START_NO, i)
            if date.today() > x[0]:
                week_list.append(x)

        for week in week_list:
            index = week_list.index(week)
            if  index > 0:
                current_week_first = week[0]
                current_week_last = week[1]
                previous_week_first = week_list[index-1][0]
                previous_week_last = week_list[index-1][1]

                current_ret = self.report_table_obj.objects.filter(
                    report_date__gte=current_week_first,
                    report_date__lte=current_week_last
                )

                previous_ret = self.report_table_obj.objects.filter(
                    report_date__gte=previous_week_first,
                    report_date__lte=previous_week_last
                )
                fields = self.get_report_settings()['schema'].keys()
                if self.report_name == 'user_daily_report':
                    fields.append('new_member_count')

                current_data, previous_data = get_final_data(current_ret, previous_ret, fields, self.report_name)

                result_doc = {}
                for key, data in current_data.items():

                    result_doc[key] = data
                    result_doc['%s_contrast' % (key)] = get_contrast(data, previous_data[key])

                result_doc['report_date'] = '{0}-{1}'.format(current_week_first.strftime('%Y年-%m月-%d日'),
                                                             current_week_last.strftime('%Y年-%m月-%d日')
                                                             )
                report_data.append(result_doc)

        return report_data[::-1]

    def get_month_report(self):

        report_data = []
        month_list = get_month_day_range(YEAR_START_NO, MONTH_START_NO)
        for month in month_list:
            index = month_list.index(month)
            if  index > 0:
                current_month_first = month[0]
                current_month_last = month[1]
                previous_month_first = month_list[index-1][0]
                previous_month_last = month_list[index-1][1]

                current_ret = self.report_table_obj.objects.filter(
                    report_date__gte=current_month_first,
                    report_date__lte=current_month_last
                )

                previous_ret = self.report_table_obj.objects.filter(
                    report_date__gte=previous_month_first,
                    report_date__lte=previous_month_last
                )

                fields = self.get_report_settings()['schema'].keys()
                if self.report_name == 'user_daily_report':
                    fields.append('new_member_count')
                current_data, previous_data = get_final_data(current_ret, previous_ret, fields, self.report_name)

                result_doc = {}

                for key, data in current_data.items():
                    if data is None:
                        data = 1

                    result_doc[key] = data
                    result_doc['%s_contrast' % (key)] = get_contrast(data, previous_data[key])

                result_doc['report_date'] = '{0}-{1}'.format(current_month_first.strftime('%Y年-%m月-%d日'),
                                                             current_month_last.strftime('%Y年-%m月-%d日')
                                                             )
                report_data.append(result_doc)
        return report_data[::-1]

if __name__ == '__main__':
    pinbot_dash_report = PinbotDashReport(report_name='partner_daily_report')
    print pinbot_dash_report.get_today_report()
    print pinbot_dash_report.get_week_report()
    #print pinbot_dash_report.get_month_report()