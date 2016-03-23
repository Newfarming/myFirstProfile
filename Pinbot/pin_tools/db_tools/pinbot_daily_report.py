# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from app.dash.models import (
    PinbotDailyReport,
)
from users.models import (
    UserProfile,
)
from statistics.models import (
    StatisticsModel,
)
from transaction.models import (
    UserChargePackage,
)

from pin_utils.django_utils import (
    get_today,
    get_object_or_none,
)


def user_daily_dash(report, dash_time):
    end_dash_time = dash_time + datetime.timedelta(days=1)
    register_user_count = UserProfile.objects.filter(
        user__is_active=True,
        user__date_joined__gte=dash_time,
        user__date_joined__lt=end_dash_time,
    ).count()

    total_user_count = UserProfile.objects.filter(
        user__is_active=True,
        user__date_joined__lt=end_dash_time,
    ).count()
    login_user_count = len(StatisticsModel.objects.filter(
        access_time__gte=dash_time,
        access_time__lt=end_dash_time
    ).distinct('username'))

    report.register_user_count = register_user_count
    report.total_user_count = total_user_count
    report.login_user_count = login_user_count
    return report


def get_pkg_dash(report, dash_time):
    end_dash_time = dash_time + datetime.timedelta(days=1)
    pay_user_count = UserChargePackage.objects.filter(
        start_time__gte=dash_time,
        start_time__lt=end_dash_time,
        actual_cost__gt=1,
    ).count()
    total_pay_count = UserChargePackage.objects.filter(
        start_time__lt=end_dash_time,
        actual_cost__gt=1,
    ).count()
    report.pay_user_count = pay_user_count
    report.total_pay_count = total_pay_count
    return report


def main():
    start_time = datetime.datetime(2014, 01, 01)
    today = get_today()

    while 1:
        if start_time >= today:
            print 'dash done, last dash time', start_time.strftime('%Y-%m-%d')
            break

        report = get_object_or_none(
            PinbotDailyReport,
            report_date=start_time
        )
        if not report:
            report = PinbotDailyReport(
                report_date=start_time
            )

        user_daily_dash(report, start_time)
        get_pkg_dash(report, start_time)
        report.save()
        print start_time.strftime('%Y-%m-%d'), 'dash success'
        start_time = start_time + datetime.timedelta(days=1)


if __name__ == '__main__':
    main()
