# coding: utf-8

from django.db import models

from django.contrib.auth.models import User

from resumes.models import (
    ContactInfoData,
)
from feed.models import (
    Feed,
)


class CandidateTag(models.Model):
    '''
    候选人标签管理
    '''

    name = models.CharField(
        max_length=30,
        verbose_name='标签名称',
    )
    display = models.BooleanField(
        default=True,
        blank=True,
        verbose_name='是否展示',
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = '候选人标签管理'
        verbose_name_plural = verbose_name


class Candidate(models.Model):
    '''
    候选人管理
    '''
    contact_info = models.OneToOneField(
        ContactInfoData,
        related_name='candidate',
        verbose_name='联系人',
    )
    admin = models.ForeignKey(
        User,
        null=True,
        related_name='candidates',
        verbose_name='管理员',
    )
    tags = models.ManyToManyField(
        'CandidateTag',
        null=True,
        blank=True,
        verbose_name='候选人标签',
    )
    has_contact = models.BooleanField(
        default=False,
        verbose_name='是否联系',
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
    )

    def __unicode__(self):
        return u'已联系' if self.has_contact else u'未联系'

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '候选人管理'
        verbose_name_plural = verbose_name


class CandidateRemark(models.Model):
    '''
    候选人备注
    '''

    REMARK_META = (
        (0, '个人信息更新'),
        (1, '求职要求'),
        (2, '个人喜好'),
        (3, '其他'),
    )

    candidate = models.ForeignKey(
        Candidate,
        related_name='candidate_remarks',
        verbose_name='候选人',
    )
    remark_type = models.IntegerField(
        default=0,
        choices=REMARK_META,
        verbose_name='备注类型',
    )
    desc = models.CharField(
        max_length=500,
        verbose_name='描述',
    )
    remark_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='记录时间',
    )
    admin = models.ForeignKey(
        User,
        related_name='candidate_remark',
        verbose_name='管理员',
    )

    def __unicode__(self):
        return self.remark_type

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '候选人备注'
        verbose_name_plural = verbose_name


class CompanyCardSendRecord(models.Model):
    """企业名片发送记录"""

    STATUS_META = (
        (0, '待发送'),
        (1, '已成功'),
        (2, '已失败'),
    )
    job = models.ForeignKey(
        Feed,
        verbose_name='推荐职位',
    )
    candidate = models.ForeignKey(
        Candidate,
        related_name='send_records',
        verbose_name='候选人',
    )
    operator = models.ForeignKey(
        User,
        verbose_name='管理员',
    )
    status = models.IntegerField(
        default=1,
        choices=STATUS_META,
        verbose_name='状态',
    )
    send_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='发送时间'
    )

    def __unicode__(self):
        return self.tag_title

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '企业名片发送记录'
        verbose_name_plural = verbose_name
        ordering = ['-send_time']


class CRMClientInfo(models.Model):

    client = models.OneToOneField(
        User,
        related_name='crm_client_info',
        verbose_name='客户',
    )
    admin = models.ForeignKey(
        User,
        related_name='crm_clients',
        verbose_name='管理员',
        blank=True,
        null=True,
    )
    last_time = models.DateTimeField(
        auto_now=True,
        verbose_name='最后操作时间'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    last_operate_staff = models.CharField(
        default='',
        null=True,
        blank=True,
        max_length=30,
        verbose_name='最后操作内容',
    )
    last_operate_admin = models.ForeignKey(
        User,
        related_name='last_operate_clients',
        verbose_name='最后操作人',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.client.username

    class Meta:
        verbose_name = 'CRM客户信息'
        verbose_name_plural = verbose_name


class CRMDownloadResume(models.Model):

    buy_resume = models.OneToOneField(
        'transaction.ResumeBuyRecord',
        related_name='crm_resume_info',
        verbose_name='下载记录',
    )
    admin = models.ForeignKey(
        User,
        related_name='crm_download_resumes',
        verbose_name='管理员',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
    )

    def __unicode__(self):
        return self.buy_resume.resume_id

    class Meta:
        verbose_name = 'CRM下载简历信息'
        verbose_name_plural = verbose_name


class CRMFeedRemark(models.Model):

    REMARK_META = (
        (1, '公司信息更新'),
        (2, '公司特别要求'),
        (3, '职位特别要求'),
    )

    feed = models.ForeignKey(
        'feed.Feed',
        related_name='crm_remarks',
        verbose_name='定制',
    )
    admin = models.ForeignKey(
        User,
        related_name='crm_feed_remarks',
        verbose_name='管理员',
    )
    remark_type = models.IntegerField(
        choices=REMARK_META,
        default=1,
        verbose_name='备注类型',
    )
    remark = models.CharField(
        max_length=200,
        verbose_name='内容',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
    )

    def __unicode__(self):
        return self.remark

    class Meta:
        verbose_name = 'CRM职位评价'
        verbose_name_plural = verbose_name


class AdminSchedule(models.Model):

    BACK_GROUND_COLOR = (
        ('red', '红色'),
        ('orange', '橙色'),
        ('yellow', '黄色'),
        ('green', ' 绿色'),
        ('blue', ' 蓝色'),
        ('purple', ' 紫色'),
    )

    user = models.ForeignKey(
        User,
        related_name='schedule_user',
        verbose_name='管理员'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='日程'
    )
    start_time = models.DateTimeField(
        verbose_name='时间'
    )
    url = models.CharField(
        default='',
        blank=True,
        max_length=100,
        verbose_name='备注简历URL',
    )
    backgroundcolor = models.CharField(
        choices=BACK_GROUND_COLOR,
        max_length=15,
        verbose_name='背景色'
    )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = '自定义日程'
        verbose_name_plural = verbose_name
