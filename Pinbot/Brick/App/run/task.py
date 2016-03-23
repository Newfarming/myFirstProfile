# coding: utf-8

import datetime

from .models import (
    DailyReport,
    WeekReport,
)

from app.invite.models import (
    InviteCode,
)
from jobs.models import (
    UserFavourCompany,
)

from Brick.App.account.models import (
    UserProfile,
)
from Brick.App.job_hunting.models import (
    RecommendJob,
)

from Brick.BCelery.celery_app import app

from Brick.Utils.django_utils import (
    get_yesterday,
    get_today,
    get_object_or_none,
)


class DailyReportTask(object):

    def init_date(self):
        self.YESTERDAY = get_yesterday()
        self.TODAY = get_today()
        return self.YESTERDAY, self.TODAY

    def invite_code_report(self, daily_report):
        count = InviteCode.objects.filter(
            create_time__gte=self.YESTERDAY,
            create_time__lt=self.TODAY,
        ).count()
        daily_report.code_count = count
        return daily_report

    def user_report(self, daily_report):
        total_count = UserProfile.objects.filter(
            is_active=True,
            user__date_joined__lt=self.TODAY,
        ).count()
        new_user_count = UserProfile.objects.filter(
            user__date_joined__gte=self.YESTERDAY,
            user__date_joined__lt=self.TODAY,
            user__is_active=True,
        ).count()
        login_user_count = UserProfile.objects.filter(
            user__last_login__gte=self.YESTERDAY,
            user__last_login__lt=self.TODAY,
            user__is_active=True,
        ).count()

        daily_report.register_user_count = new_user_count
        daily_report.total_user_count = total_count
        daily_report.login_user_count = login_user_count
        daily_report.login_percent = round(
            (login_user_count / float(total_count)), 2) if total_count != 0 else 0
        return daily_report

    def job_report(self, daily_report):
        reco_job_count = RecommendJob.objects.filter(
            reco_time__gte=self.YESTERDAY,
            reco_time__lt=self.TODAY,
        ).count()

        job_stat = RecommendJob.objects.raw(
            '''
            SELECT
            `job_hunting_recommendjob`.`id`,
            SUM(
            CASE WHEN `job_hunting_recommendjob`.`action` = 'favorite' THEN 1 ELSE 0 END) AS `favour_job_count`,
            SUM(
            CASE WHEN `job_hunting_recommendjob`.`action` = 'dislike' THEN 1 ELSE 0 END) AS `dislike_job_count`,
            SUM(
            CASE WHEN `job_hunting_recommendjob`.`action` = 'send' THEN 1 ELSE 0 END) AS `send_job_count`,
            SUM(
            CASE WHEN `job_hunting_recommendjob`.`read_status` = 'read' THEN 1 ELSE 0 END) AS `check_job_count`,
            SUM(
            CASE WHEN `job_hunting_recommendjob`.`read_status` = 'read' AND `job_hunting_recommendjob`.`action` = '' THEN 1 ELSE 0 END) AS `refresh_job_count`
            FROM `job_hunting_recommendjob`
            WHERE `job_hunting_recommendjob`.`action_time` < '%s' AND `job_hunting_recommendjob`.`action_time` >= '%s'
            ''' % (
                self.TODAY,
                self.YESTERDAY,
            )
        )[0]

        daily_report.reco_job_count = reco_job_count
        daily_report.check_job_count = job_stat.check_job_count or 0
        daily_report.favour_job_count = job_stat.favour_job_count or 0
        daily_report.send_job_count = job_stat.send_job_count or 0
        daily_report.dislike_job_count = job_stat.dislike_job_count or 0
        daily_report.refresh_job_count = job_stat.refresh_job_count or 0
        return daily_report

    def favour_company_report(self, daily_report):
        favour_count = UserFavourCompany.objects.filter(
            time__gte=self.YESTERDAY,
            time__lt=self.TODAY,
        ).count()
        daily_report.favour_company_count = favour_count
        return daily_report

    def daily_report_task(self):
        '''
        C端每天运营数据
        凌晨1点开始跑
        '''
        self.init_date()
        daily_report = get_object_or_none(
            DailyReport,
            report_date=self.YESTERDAY,
        )
        if not daily_report:
            daily_report = DailyReport(
                report_date=self.YESTERDAY,
            )

        self.invite_code_report(daily_report)
        self.user_report(daily_report)
        self.job_report(daily_report)
        self.favour_company_report(daily_report)

        daily_report.save()
        return daily_report


class WeekReportTask(object):

    def init_date(self):
        today = get_today()
        self.start_date = today - datetime.timedelta(days=today.weekday() + 7)
        self.end_date = self.start_date + datetime.timedelta(days=7)
        return self.start_date, self.end_date

    def init_last_date(self):
        self.last_start_date = self.start_date + datetime.timedelta(days=-7)
        self.last_end_date = self.last_start_date + datetime.timedelta(days=7)
        return self.last_start_date, self.last_end_date

    def get_last_week_report(self):
        last_week_report = get_object_or_none(
            WeekReport,
            start_date=self.last_start_date,
            end_date=self.last_end_date + datetime.timedelta(days=-1),
        )
        return last_week_report

    def week_report_count(self, week_report):
        week_stat = DailyReport.objects.raw(
            '''
            SELECT
            `run_dailyreport`.`id`,
            SUM(`run_dailyreport`.`code_count`) AS `code_count`,
            SUM(`run_dailyreport`.`register_user_count`) AS `register_user_count`,
            MAX(`run_dailyreport`.`total_user_count`) AS `total_user_count`,
            SUM(`run_dailyreport`.`login_user_count`) AS `login_user_count`,
            SUM(`run_dailyreport`.`reco_job_count`) AS `reco_job_count`,
            SUM(`run_dailyreport`.`check_job_count`) AS `check_job_count`,
            SUM(`run_dailyreport`.`favour_job_count`) AS `favour_job_count`,
            SUM(`run_dailyreport`.`send_job_count`) AS `send_job_count`,
            SUM(`run_dailyreport`.`dislike_job_count`) AS `dislike_job_count`,
            SUM(`run_dailyreport`.`refresh_job_count`) AS `refresh_job_count`,
            SUM(`run_dailyreport`.`favour_company_count`) AS `favour_company_count`,
            DATE_ADD(`report_date`, INTERVAL(1-DAYOFWEEK(`report_date`)) DAY) AS `start_date`,
            DATE_ADD(`report_date`, INTERVAL(7-DAYOFWEEK(`report_date`)) DAY) AS `end_date`
            FROM `run_dailyreport`
            WHERE `run_dailyreport`.`report_date` >= '%s' AND `run_dailyreport`.`report_date` < '%s'
            GROUP BY YEARWEEK(`run_dailyreport`.`report_date`)
            ORDER BY YEARWEEK(`run_dailyreport`.`report_date`)
            ''' % (
                self.start_date,
                self.end_date,
            )
        )[0]

        week_report.code_count = week_stat.code_count or 0
        week_report.register_user_count = week_stat.register_user_count or 0
        week_report.total_user_count = week_stat.total_user_count or 0
        week_report.login_user_count = week_stat.login_user_count or 0
        week_report.reco_job_count = week_stat.reco_job_count or 0
        week_report.check_job_count = week_stat.check_job_count or 0
        week_report.favour_job_count = week_stat.favour_job_count or 0
        week_report.send_job_count = week_stat.send_job_count or 0
        week_report.dislike_job_count = week_stat.dislike_job_count or 0
        week_report.refresh_job_count = week_stat.refresh_job_count or 0
        week_report.favour_company_count = week_stat.favour_company_count or 0

        if week_report.total_user_count != 0:
            week_report.login_percent = round(
                int(week_report.login_user_count) / float(week_report.total_user_count),
                2
            )
        return week_report

    def week_report_chain(self, week_report):
        last_week_report = self.get_last_week_report()
        if not last_week_report:
            return week_report

        report_chain_meta = (
            ('code_count', 'code_chain'),
            ('register_user_count', 'register_user_chain'),
            ('total_user_count', 'total_user_chain'),
            ('login_user_count', 'login_user_chain'),
            ('reco_job_count', 'reco_job_chain'),
            ('check_job_count', 'check_job_chain'),
            ('favour_job_count', 'favour_job_chain'),
            ('send_job_count', 'send_job_chain'),
            ('dislike_job_count', 'dislike_job_chain'),
            ('refresh_job_count', 'refresh_job_chain'),
            ('favour_company_count', 'favour_company_chain'),
        )
        for field, chain in report_chain_meta:
            if last_week_report.__dict__[field] != 0:
                week_report.__dict__[chain] = round(
                    float(week_report.__dict__[field]) / float(last_week_report.__dict__[field]),
                    2
                )
        return week_report

    def remain_user_percent(self, week_report):
        login_user_count = UserProfile.objects.filter(
            user__last_login__gte=self.start_date,
            user__last_login__lt=self.end_date,
            user__is_active=True,
            user__date_joined__gte=self.last_start_date,
            user__date_joined__lt=self.last_end_date,
        ).count()
        if week_report.login_user_count != 0:
            week_report.remain_user_percent = round(
                login_user_count / float(week_report.login_user_count),
                2,
            )
        return week_report

    def week_report_task(self):
        self.init_date()
        self.init_last_date()

        week_report = get_object_or_none(
            WeekReport,
            start_date=self.start_date,
            end_date=self.end_date + datetime.timedelta(days=-1),
        )
        if not week_report:
            week_report = WeekReport(
                start_date=self.start_date,
                end_date=self.end_date + datetime.timedelta(days=-1),
            )

        self.week_report_count(week_report)
        self.remain_user_percent(week_report)
        self.week_report_chain(week_report)

        week_report.save()
        return week_report


daily_report = DailyReportTask()
asyn_daily_report_task = app.task(
    name='daily-report'
)(daily_report.daily_report_task)

week_report = WeekReportTask()
asyn_week_report_task = app.task(
    name='week-report'
)(week_report.week_report_task)
