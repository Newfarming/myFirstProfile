# coding: utf-8

import datetime

from django.contrib.auth.models import User
from app.dash.models import (
    PinbotDailyReport,
)
from users.models import (
    UserProfile,
)
from transaction.models import (
    UserChargePackage,
)
from statistics.models import (
    StatisticsModel,
)

from pin_utils.django_utils import (
    get_today,
    get_object_or_none,
)

from Brick.BCelery.celery_app import app


class PinbotDailyTask(object):

    def user_daily_dash(self, report, dash_time):
        staff_username_list = list(User.objects.filter(
            is_staff=True
        ).values_list(
            'username',
            flat=True,
        ))
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
            access_time__lt=end_dash_time,
            username__nin=staff_username_list,
        ).distinct('username'))

        report.register_user_count = register_user_count
        report.total_user_count = total_user_count
        report.login_user_count = login_user_count
        return report

    def get_pkg_dash(self, report, dash_time):
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

    def pinbot_daily_task(self):
        today = get_today()
        start_time = today + datetime.timedelta(days=-1)

        report = get_object_or_none(
            PinbotDailyReport,
            report_date=start_time
        )
        if not report:
            report = PinbotDailyReport(
                report_date=start_time
            )

        self.user_daily_dash(report, start_time)
        self.get_pkg_dash(report, start_time)
        report.save()
        return report


pinbot_task = PinbotDailyTask()
asyn_pinbot_daily_task = app.task(
    name='pinbot-daily-task'
)(pinbot_task.pinbot_daily_task)
