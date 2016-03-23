# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from Brick.App.my_resume.models import (
    Resume,
    SearchTag,
)
from feed.models import Feed
from jobs.models import Job


class RecommendJob(models.Model):
    '''
    用户推荐职位列表
    '''
    READ_META = (
        ('read', '已读'),
        ('unread', '未读'),
    )
    ACTION_META = (
        ('', '无'),
        ('favorite', '收藏'),
        ('send', '投递'),
        ('dislike', '不感兴趣'),
    )
    COMPANY_ACTION_META = (
        ('', '无'),
        ('waiting', '等待企业反馈'),
        ('download', '面试邀请中'),
        ('no_reply', '无回复'),
        ('unfit', '不合适'),
    )
    hr_user = models.ForeignKey(
        User,
        verbose_name='HR用户',
        related_name='receive_jobs',
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name='推荐用户',
        related_name='recommend_jobs',
    )
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
    )
    search_tag = models.ForeignKey(
        SearchTag,
        verbose_name='搜索Tag',
        blank=True,
        null=True,
    )
    job = models.ForeignKey(
        Feed,
        verbose_name='推荐职位',
    )
    reco_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='推荐时间',
        db_index=True,
    )
    read_status = models.CharField(
        max_length=10,
        choices=READ_META,
        verbose_name='阅读状态',
        default='unread',
    )
    action = models.CharField(
        max_length=30,
        choices=ACTION_META,
        verbose_name='用户动作',
        default='',
    )
    succ_rate = models.FloatField(
        verbose_name='投递成功率',
        default=66.6,
    )
    company_action = models.CharField(
        max_length=30,
        verbose_name='企业反馈',
        choices=COMPANY_ACTION_META,
        default='',
    )
    delete = models.BooleanField(
        default=False,
        verbose_name='删除状态',
    )
    action_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='操作时间',
        db_index=True,
    )
    company_action_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='企业反馈时间',
        db_index=True,
    )
    company_delete = models.BooleanField(
        default=False,
        verbose_name='企业删除',
    )
    reco_index = models.IntegerField(
        default=1,
        verbose_name='推荐程度',
        db_index=True,
    )
    display = models.BooleanField(
        default=True,
        verbose_name='是否展示',
    )

    def __unicode__(self):
        return u'用户%s' % (
            self.user.username,
        )

    def __str__(self):
        return self.__unicode__()

    def job_company_name(self):
        return self.job.company.company_name

    job_company_name.short_description = '公司名'

    def hr_source(self):
        return self.hr_user.userprofile.show_source()

    hr_source.short_description = 'HR来源'

    def resume_display(self):
        if self.action == 'send':
            resume_id = self.resume.resume_id
            interface = '''
            <a href="/resumes/display/%s/0" target="_blank">查看简历</a>
            ''' % resume_id
        else:
            interface = ''
        return mark_safe(interface)

    resume_display.short_description = '简历'

    class Meta:
        unique_together = (
            ('search_tag', 'hr_user', 'user', 'job'),
        )
        verbose_name = '职位推荐列表'
        verbose_name_plural = verbose_name


class RecommendConf(models.Model):
    '''
    用户推荐设置
    '''
    user = models.ForeignKey(
        User,
        verbose_name='用户',
    )
    position = models.CharField(
        max_length=30,
        verbose_name='职位类别',
        default='',
    )

    def __unicode__(self):
        return '%s' % self.user.username

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '用户推荐设置'
        verbose_name_plural = verbose_name


class JobMessage(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='留言用户',
    )
    message = models.CharField(
        max_length=300,
        verbose_name='留言',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='留言时间',
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='回复',
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u'%s用户留言' % self.user.username

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name


class CompanyCardJob(models.Model):

    STATUS_META = (
        ('waiting', '等待回复'),
        ('accept', '感兴趣'),
        ('reject', '不感兴趣'),
        ('expire', '已过期'),
    )

    job = models.ForeignKey(
        Job,
        verbose_name='工作',
        related_name='send_jobs'
    )
    hr_user = models.ForeignKey(
        User,
        verbose_name='HR',
        related_name='send_card_jobs',
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='card_jobs',
    )
    send_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='发送时间',
    )
    status = models.CharField(
        max_length=30,
        verbose_name='状态',
        choices=STATUS_META,
        default='waiting',
    )
    action_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='操作时间',
    )
    delete = models.BooleanField(
        default=False,
        verbose_name='删除状态',
    )
    token = models.CharField(
        max_length=70,
        verbose_name='验证Token',
        default='',
    )

    def __unicode__(self):
        return u'工作%s' % self.job.title

    def __str__(self):
        return self.__unicode__()

    class Meta:
        unique_together = (
            ('hr_user', 'user', 'job'),
        )
        verbose_name = '发送职位卡片'
        verbose_name_plural = verbose_name
