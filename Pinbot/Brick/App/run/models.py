# coding: utf-8

from django.db import models


class AbstractReportModel(models.Model):

    code_count = models.IntegerField(
        default=0,
        verbose_name='获得邀请码用户数',
    )
    register_user_count = models.IntegerField(
        default=0,
        verbose_name='新增用户',
    )
    total_user_count = models.IntegerField(
        default=0,
        verbose_name='用户总数',
    )
    login_user_count = models.IntegerField(
        default=0,
        verbose_name='活跃用户数',
    )
    login_percent = models.FloatField(
        default=0,
        verbose_name='活跃度',
    )
    reco_job_count = models.IntegerField(
        default=0,
        verbose_name='岗位推荐量',
    )
    check_job_count = models.IntegerField(
        default=0,
        verbose_name='岗位浏览量',
    )
    favour_job_count = models.IntegerField(
        default=0,
        verbose_name='岗位收藏量',
    )
    send_job_count = models.IntegerField(
        default=0,
        verbose_name='岗位投递量'
    )
    dislike_job_count = models.IntegerField(
        default=0,
        verbose_name='不感兴趣量',
    )
    refresh_job_count = models.IntegerField(
        default=0,
        verbose_name='刷新的量',
    )
    favour_company_count = models.IntegerField(
        default=0,
        verbose_name='点赞的量',
    )

    class Meta:
        abstract = True


class DailyReport(AbstractReportModel):

    report_date = models.DateField(
        verbose_name='统计日期',
        db_index=True,
    )

    def __unicode__(self):
        return self.report_date.strftime('%Y-%m-%d')

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = 'C端日报'
        verbose_name_plural = verbose_name


class WeekReport(AbstractReportModel):

    start_date = models.DateField(
        verbose_name='开始时间',
        db_index=True,
    )
    end_date = models.DateField(
        verbose_name='结束时间',
        db_index=True,
    )
    code_chain = models.FloatField(
        default=0,
        verbose_name='获得邀请码环比',
    )
    register_user_chain = models.FloatField(
        default=0,
        verbose_name='新增用户环比',
    )
    total_user_chain = models.FloatField(
        default=0,
        verbose_name='用户总数环比',
    )
    login_user_chain = models.FloatField(
        default=0,
        verbose_name='活跃用户环比',
    )
    remain_user_percent = models.FloatField(
        default=0,
        verbose_name='留存率',
    )
    reco_job_chain = models.FloatField(
        default=0,
        verbose_name='推荐量环比',
    )
    check_job_chain = models.FloatField(
        default=0,
        verbose_name='浏览量环比',
    )
    favour_job_chain = models.FloatField(
        default=0,
        verbose_name='收藏量环比',
    )
    send_job_chain = models.FloatField(
        default=0,
        verbose_name='投递量环比'
    )
    dislike_job_chain = models.FloatField(
        default=0,
        verbose_name='不感兴趣量环比',
    )
    refresh_job_chain = models.FloatField(
        default=0,
        verbose_name='刷新量环比',
    )
    favour_company_chain = models.FloatField(
        default=0,
        verbose_name='点赞量环比',
    )

    def __unicode__(self):
        return '%s~%s' % (
            self.start_date.strftime('%Y-%m-%d'),
            self.end_date.strftime('%Y-%m-%d'),
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = 'C端周报'
        verbose_name_plural = verbose_name
