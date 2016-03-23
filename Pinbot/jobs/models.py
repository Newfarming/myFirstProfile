# coding:utf-8

from mongoengine import *
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.safestring import mark_safe
from django import forms

DEGREE_CHOICES = (
    (0, u'不限'),
    (3, u'大专'),
    (4, u'本科'),
    (7, u'硕士'),
    (10, u'博士'),
)

INTEREST_CHOICES = (
    (1, u'公司'),
    (2, u'职位'),
    (3, u'产品地址'),
    (4, u'官网'),
)

CLICK_CHOICES = (
    (1, u'进一步了解'),
    (2, u'官网'),
    (3, u'产品地址'),
    (4, u'感兴趣'),
    (5, u'不感兴趣'),
)


RECOMMEND_CHOICES = (
    (1, u'推荐'),
    (0, u'不推荐')
)


class JobKeywords(Document):

    """
    @summary: 工作与关键词映射

    """
    tags = StringField(default='')
    class_count = IntField()
    cluster_id = IntField()
    jobs_id_list = ListField(default=[])
    job_category = StringField(default='')

    meta = {"collection": 'jobs_class_keywords'}


class EmailSendToken(Document):

    """
    @summary: 邮件发送的详细情况,用于处理邮件中的点击处理
    """
    token = StringField(default='')
    type = StringField(default='')  # companycard表示企业名片,market表示营销邮件
    send_info_dict = DictField(required=False)
    send_status = BooleanField()  # 邮件是否发送成功
    send_time = DateTimeField(default=datetime.now())


class Industry(models.Model):

    industry_name = models.CharField(
        max_length=30,
        verbose_name='行业名称'
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )
    def __unicode__(self):
        return self.industry_name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '行业名称'
        verbose_name_plural = verbose_name


class CompanyCategory(models.Model):

    industry = models.ForeignKey(
        Industry,
        related_name='company_category_industry',
        verbose_name='所属行业'
    )
    category = models.CharField(
        max_length=30,
        verbose_name='公司类别',
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )
    display = models.BooleanField(
        default=True,
        verbose_name='B端展示',
    )
    brick_display = models.BooleanField(
        default=True,
        verbose_name='C端展示'
    )
    sort = models.IntegerField(
        default=0,
        verbose_name='排序',
    )

    def __unicode__(self):
        return self.category

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '公司领域'
        verbose_name_plural = verbose_name


class Company(models.Model):

    """
    @summary:公司模型
    """
    RECOMMEND_CHOICES = (
        (1, u'推荐'),
        (0, u'不推荐')
    )
    company_name = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'公司名'
    )
    key_points = models.CharField(
        default='',
        max_length=1000,
        verbose_name=u'公司亮点'
    )
    desc = models.CharField(
        default='',
        max_length=1000,
        verbose_name=u'企业简介'
    )
    core_team = models.CharField(
        default='',
        max_length=1000,
        verbose_name=u'核心团队',
        blank=True,
    )
    company_stage = models.CharField(
        default='',
        max_length=1000,
        verbose_name=u'企业发展阶段',
    )
    url = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'公司网址',
        blank=True
    )
    product_url = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'产品地址',
        blank=True
    )
    add_time = models.DateTimeField(
        verbose_name=u'录入时间',
        default=datetime.now()
    )
    user = models.ForeignKey(
        User,
        verbose_name=u'聘宝用户'
    )
    pinbot_recommend = models.CharField(
        max_length=300,
        verbose_name='聘宝推荐',
        blank=True,
        default='',
    )
    category = models.ManyToManyField(
        CompanyCategory,
        verbose_name='类别',
        null=True,
        blank=True,
    )
    favour_count = models.IntegerField(
        default=0,
        verbose_name='点赞数',
    )
    need_recommend = models.IntegerField(
        choices=RECOMMEND_CHOICES,
        default=1,
        verbose_name=u'是否推荐',
    )

    def __unicode__(self):
        return self.company_name

    def get_id(self):
        return str(self.id)
    get_id.short_description = '公司id'


    def industry(self):
        return self.category.all().first().industry

    industry.short_description = '行业'

    class Meta:
        verbose_name = u'公司信息'
        verbose_name_plural = u'公司信息'


class Job(models.Model):

    """
    @summary: 职位模型
    """
    title = models.CharField(default='', max_length=100, verbose_name=u'职位名称')
    salary_low = models.IntegerField(default=0, verbose_name=u'最低工资')
    salary_high = models.IntegerField(default=0, verbose_name=u'最高工资')
    work_years = models.IntegerField(default=0, verbose_name=u'最低工作年限')
    address = models.CharField(default='', max_length=100, verbose_name=u'工作地')
    # 0表示不限，3表示大专，4表示本科，7表示硕士，10表示博士
    degree = models.IntegerField(
        choices=DEGREE_CHOICES, default=0, verbose_name=u'最低学历')
    key_points = models.CharField(
        default='', max_length=1000, verbose_name=u'职位诱惑', null=True, blank=True)
    desc = models.CharField(
        default='', max_length=1000, verbose_name=u'职位描述', null=True, blank=True)
    skill_desc = models.CharField(
        default='', max_length=1000, verbose_name=u'技能描述', null=True, blank=True)
    company = models.ForeignKey(Company, verbose_name=u'公司')
    add_time = models.DateTimeField(
        verbose_name=u'录入时间', default=datetime.now())
    user = models.ForeignKey(User, verbose_name=u'添加用户', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_id(self):
        pinbot_resume_url = "<a href=%s target=%s>%s</a>" % (
            '/companycard/job/preview/' + str(self.id) + '/', str(self.id), '点击发送邮件')
        return mark_safe(pinbot_resume_url)
    get_id.short_description = '职位查看'

    class Meta:
        verbose_name = u'职位信息'
        verbose_name_plural = u'职位信息'


class HunterInterest(models.Model):

    """
    @summary: 求职者公司关系表，用于记录用户是否对公司或者职位感兴趣
    """
    user = models.CharField(default='', max_length=1000, verbose_name=u'求职者')
    interest_type = models.IntegerField(
        choices=INTEREST_CHOICES, default=1, verbose_name=u'类型')  # 1表示公司，2表示职位 3.表示产品地址 4表示官网
    company = models.ForeignKey(
        Company, verbose_name=u'公司', null=True, blank=True)
    job = models.ForeignKey(Job, verbose_name=u'职位', null=True, blank=True)
    is_interest = models.BooleanField(default=True, verbose_name=u'是否感兴趣')
    add_time = models.DateTimeField(
        verbose_name=u'反馈时间', default=datetime.now())
    # 1表示进一步了解，2表示官网 3.表示产品地址 4表示感兴趣 5表示不感兴趣
    click = models.IntegerField(
        choices=CLICK_CHOICES, default=1, verbose_name=u'用户点击', null=True, blank=True)
    ip = models.CharField(
        default='', max_length=200, verbose_name=u'来源', null=True, blank=True)
    access_url = models.CharField(
        default='', max_length=200, verbose_name=u'来源', null=True, blank=True)
    refer_url = models.CharField(
        default='', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = u'用户兴趣'
        verbose_name_plural = u'用户兴趣'


SEND_CHOICES = (
    (0, u'发送失败'),
    (1, u'发送成功'),
    (2, u'待发送'),
)

FEEDBACK_CHOICES = (
    (0, u'待反馈'),
    (1, u'候选人反馈感兴趣'),
    (2, u'候选人不感兴趣'),
    (3, u'候选人无回复'),
)


class SendCompanyCard(models.Model):

    """
    @summary: 企业名片发送情况
    """
    send_user = models.ForeignKey(User, verbose_name=u'招聘方')
    resume_id = models.CharField(
        default='', max_length=100, verbose_name=u'简历id')
    feed_id = models.CharField(
        default='', max_length=100, verbose_name=u'定制id', null=True, blank=True)
    has_download = models.BooleanField(
        default=False, verbose_name=u'简历下载是否有联系信息')
    download_status = models.BooleanField(default=True, verbose_name=u'下载状态')
    to_email = models.CharField(
        default='', max_length=100, verbose_name=u'求职者', null=True, blank=True)
    send_status = models.IntegerField(
        choices=SEND_CHOICES, verbose_name=u'发送情况', null=True, blank=True, default=2)
    send_msg = models.CharField(
        default='', max_length=100, verbose_name=u'发送信息', null=True, blank=True)
    send_time = models.DateTimeField(
        verbose_name=u'发送时间', default=datetime.now())

    job = models.ForeignKey(Job, verbose_name=u'职位', null=True, blank=True)

    feedback_status = models.IntegerField(
        choices=FEEDBACK_CHOICES, verbose_name=u'用户反馈', null=True, blank=True, default=0)
    feedback_time = models.DateTimeField(
        verbose_name=u'用户反馈时间', default=datetime.now())
    points_used = models.IntegerField(
        verbose_name=u'积分消耗', null=True, blank=True, default=0)

    def show_user(self):
        return self.send_user.first_name

    def __unicode__(self):
        return self.send_user.first_name

    class Meta:
        unique_together = (
            ('send_user', 'resume_id'),
        )
        verbose_name = u'企业名片发送'
        verbose_name_plural = u'企业名片发送'


class JobModelForm(forms.ModelForm):
    key_points = forms.CharField(
        widget=forms.Textarea, label=u'职位诱惑', required=False)
    desc = forms.CharField(
        widget=forms.Textarea, label=u'职位描述', required=False)
    skill_desc = forms.CharField(
        widget=forms.Textarea, label=u'技能描述', required=False)

    class Meta:
        model = Job


class UserFavourCompany(models.Model):
    company = models.ForeignKey(
        Company,
        related_name='user_favours',
        verbose_name='公司'
    )
    user = models.ForeignKey(
        User,
        related_name='favour_companys',
        verbose_name='用户',
    )
    time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='点赞时间',
    )

    def __unicode__(self):
        return self.company.company_name, self.user.username

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '公司点赞'
        verbose_name_plural = verbose_name


class JobAdmin(object):

    list_display = [
        'title',
        'salary_low',
        "salary_high",
        'work_years',
        'address',
        'degree',
        'key_points',
        'desc',
        'skill_desc',
        'company',
        'add_time',
        'get_id',
    ]
    list_display_links = ['title']

    ordering = [
        '-add_time',
    ]

    list_filter = [
        'title',
        'salary_low',
        'salary_high',
        'work_years',
        'address',
        'degree',
    ]

    search_fields = [
        'title',
    ]


class HunterInterestAdmin(object):
    list_display = [
        'user',
        'click',
        'interest_type',
        "company",
        'is_interest',
        'add_time',
    ]
    list_display_links = ['user']

    ordering = [
        '-add_time',
    ]

    list_filter = [
        'click',
        'user',
        'interest_type',
        'company',
        'job',
        'is_interest',
    ]

    search_fields = [
        'user',
        'click',
    ]


class CompanyModelForm(forms.ModelForm):
    key_points = forms.CharField(
        widget=forms.Textarea, label=u'公司亮点', required=False)
    desc = forms.CharField(
        widget=forms.Textarea, label=u'公司简介', required=False)
    core_team = forms.CharField(
        widget=forms.Textarea, label=u'核心团队', required=False)
    company_stage = forms.CharField(
        widget=forms.Textarea, label=u'公司发展阶段和计划', required=False)

    class Meta:
        model = Company