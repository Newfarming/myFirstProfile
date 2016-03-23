# coding:utf-8

from datetime import datetime, timedelta
from urlparse import urlparse

from django.db.models import *
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from pinbot_package.models import *
from app.payment.models import PaymentOrder
from jobs.models import SendCompanyCard
from resumes.models import ContactInfoData

from pin_utils.django_utils import (
    get_object_or_none,
)

default_datetime = datetime(2014, 1, 1, 0, 0)

# 套餐购买的支付状态
PAY_STATUS_CHOICES = [
    ('Start', u'暂未付款'),  # 发起购买流程
    ('finished', u'完成支付'),  # 处理完毕
]

PAY_STATUS_CHOICES_DICT = dict(PAY_STATUS_CHOICES)
PACKAGE_TYPE = [
    (1, u'基础套餐'),
    (2, u'订阅套餐'),
    (3, u'特殊套餐'),
]
FEEDBACK_CHECK_CHOICES = (
    ('checking', u'审核中'),
    ('success', u'通过'),
    ('failed', u'否决'),
    ('fail', u'否决'),
)
NOTIFY_CHOICES = (
    ('need_notify', u'需要通知'),
    ('notified', u'已经通知'),
    ('read', u'通知已读'),
)
CHECK_CHOICES = (
    ('checking', u'已举报,审核中'),
    ('pass', u'审核通过'),
    ('deny', u'审核未通过'),
)
CHECK_CHOICES_DICT = dict(CHECK_CHOICES)


class FeedBackType(Model):
    """
    @summary:用户的反馈类别如：候选人无求职意愿，无法联系候选人
    """
    desc = CharField(max_length=50, verbose_name=u'反馈类型')  # 反馈类别描述
    re_points = IntegerField(default=0, verbose_name=u'返还点数')  # 返还点数

    class Meta:
        db_table = 'transaction_feedbacktype'
        verbose_name = u'简历反馈类别'
        verbose_name_plural = u'简历反馈类别'

    def __str__(self):
        return self.desc

    def __unicode__(self):
        return self.desc


class FeedBackInfo(Model):
    """
    @summary: 简历反馈选择
    """
    type = ForeignKey(FeedBackType, verbose_name=u'反馈类型')
    feedback_id = IntegerField(default=0, verbose_name=u'编号')  # 反馈编号
    feedback_desc = CharField(max_length=50, verbose_name=u'反馈描述')  # 反馈描述

    def get_type(self):
        return self.type.desc
    get_type.short_description = '反馈类型'

    class Meta:
        db_table = 'transaction_feedbackinfo'
        verbose_name = u'简历反馈选择'
        verbose_name_plural = u'简历反馈选择'

    def __str__(self):
        return self.feedback_desc

    def __unicode__(self):
        return self.feedback_desc


class UserResumeFeedback(Model):
    """
    @summary: 用户点数返还记录
    """

    user = ForeignKey(User, verbose_name='用户')
    resume_id = CharField(max_length=50, verbose_name=u'简历id')  # 简历id
    feedback_info = ForeignKey(FeedBackInfo, verbose_name=u'用户选择')
    feedback_value = CharField(
        blank=True,
        default='',
        max_length=50,
        verbose_name=u'反馈值'
    )
    check_status = CharField(choices=CHECK_CHOICES, max_length=50, verbose_name=u'反馈状态', default='checking')  # 反馈状态
    check_comment = CharField(
        blank=True,
        default='',
        max_length=50,
        verbose_name=u'审核意见'
    )
    notify_status = BooleanField(default=False, verbose_name=u'是否已通知')  # 通知用户的状态
    create_time = DateTimeField(null=True, blank=True, verbose_name=u'反馈时间', default=datetime.now())  # 用户反馈时间

    def __str__(self):
        return '%s反馈%s' % (self.user.username, self.resume_id)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        db_table = 'transaction_userresumefeedback'
        verbose_name = u'简历反馈处理'
        verbose_name_plural = verbose_name

    def get_feedback_info(self):

        info = ''
        self.feedback_value = self.feedback_value or ''
        if '_' in self.feedback_info.feedback_desc:
            info = self.feedback_info.feedback_desc.replace('_', "<b>%s</b>" % self.feedback_value)
        else:
            info = "<b>%s</b>" % self.feedback_info.feedback_desc+":" + self.feedback_value

        return mark_safe(self.feedback_info.type.desc + ":   " + info)

    get_feedback_info.short_description = '客户反馈'

    def company_name(self):
        return self.user.username + "(" + self.user.first_name + ")"

    company_name.short_description = '公司名'

    def show_resume(self):
        url = "<a href='/resumes/display/%s' target=%s>%s</a>" % (self.resume_id, self.resume_id, '查看简历')
        return mark_safe(url)

    show_resume.short_description = '简历地址'

    def expect_return_points(self):
        """
        @summary: 用户期待返还的点数
        """

        return self.feedback_info.type.re_points

    expect_return_points.short_description = '返还积点'

    def check_op(self):

        if self.check_status == 'checking':
            if self.feedback_info.type.id != 3:
                url = """<a data-link-confirm="/transaction/return/deny/%s/" href="javascript:void(0)">拒绝</a>  """ % (self.id)
                url += """ |<a data-link-confirm="/transaction/return/pass/%s" href="javascript:void(0)">通过</a>""" % (self.id)
            else:
                return '通过'
            return mark_safe(url)
        else:
            return CHECK_CHOICES_DICT.get(self.check_status, '未知')

    check_op.short_description = '审核操作'


class UserChargePackage(Model):
    """
    @summary: 用户购买的套餐
    """
    PKG_SOURCE_META = (
        (1, '购买或试用'),
        (2, '聘宝专享定制'),
    )
    time_new = datetime.now() + timedelta(days=365)

    user = ForeignKey(User, verbose_name=u'用户')  #
    package_type = IntegerField(default=0, choices=PACKAGE_TYPE, verbose_name=u'套餐类别')  # 1表示简历套餐，2表示订阅套餐
    resume_package = ForeignKey(ResumePackge, verbose_name=u'简历套餐', null=True, blank=True)  # 购买的简历套餐
    feed_package = ForeignKey(FeedService, verbose_name=u'订阅套餐', null=True, blank=True)  # 购买的订阅服务
    extra_feed_num = IntegerField(default=0, verbose_name='订阅总数', null=True, blank=True)

    start_time = DateTimeField(verbose_name='服务开始时间', default=datetime.now())  # 服务开始时间
    resume_end_time = DateTimeField(
        default=time_new,
        verbose_name='下载到期',
        db_index=True,
    )
    feed_end_time = DateTimeField(
        default=time_new,
        verbose_name='赠送订阅到期',
        db_index=True,
    )
    actual_cost = FloatField(default=0, verbose_name=u'实际付费')  # 实际资费

    rest_feed = IntegerField(default=0, verbose_name=u'剩余订阅数')  # 剩余订阅数量
    rest_points = IntegerField(default=0, verbose_name=u'套餐剩余点数')  # 剩余点数 剩余点数等于返点数加上简历套餐剩余点数
    re_points = IntegerField(default=0, verbose_name=u'反馈返点')  # 返点
    pay_status = CharField(choices=PAY_STATUS_CHOICES, max_length=50, verbose_name=u'支付状态', default='Start')  # 支付状态

    zero_points_notify_status = CharField(choices=NOTIFY_CHOICES, max_length=50, default='read', verbose_name=u'积分为0提醒通知状态')  # 积分为0提醒通知
    order = ForeignKey(PaymentOrder, verbose_name='订单', null=True, blank=True)

    pkg_source = IntegerField(
        default=1,
        verbose_name='套餐来源',
        choices=PKG_SOURCE_META,
    )

    def __unicode__(self):
        pkg_id = self.id if self.id else ''
        username = self.user if self.user else ''
        base_pkg = self.resume_package if self.resume_package else u'无'
        fd_pkg = self.feed_package if self.feed_package else u'无'
        return u'id:%d 用户:%s 基础套餐:%s ,订阅套餐:  %s' % (pkg_id, username, base_pkg, fd_pkg)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'用户已购套餐'
        verbose_name_plural = verbose_name

    def has_expired(self):
        """
        @summary: 此处需要根据简历套餐或者订阅套餐来判断是否过期
        """
        if self.package_type == 1 and self.resume_end_time < datetime.now():
            return True
        elif self.package_type == 2 and self.feed_end_time < datetime.now():
            return True
        else:
            return False

    def pkg_used_up(self):
        """
        @summary: 判断套餐是否用完
        """
        if self.package_type == 1:
            if self.rest_points + self.re_points > 0:
                return False
            else:
                return True
        elif self.package_type == 2:
            """
            @summary: 此处查询用户已经使用的订阅数
            """
            return False

    def company_name(self):
        return self.user.first_name

    company_name.short_description = '公司名称'

    def actural_rest_points(self):
        """
        @summary: 实际剩余点数
        @athor: likaiguo.happy@163.com
        """
        return self.re_points + self.rest_points

    actural_rest_points.short_description = '实际可用点数'


class UserChargePackageAdmin(object):
    list_display = [
        'user',
        'company_name',
        'package_type',
        'resume_package',
        'feed_package',
        'extra_feed_num',
        'rest_feed',
        'rest_points',
        're_points',
        'actural_rest_points',
        'start_time',
        'resume_end_time',
        'feed_end_time',
        'actual_cost',
    ]
    list_editable = [
        'extra_feed_num',
        'rest_points',
    ]
    list_display_links = [
        'user',
        'company_name',
    ]
    list_filter = [
        'package_type',
        'resume_package',
        'pay_status',
        'feed_package',
        'extra_feed_num',
        'rest_feed',
        'rest_points',
        're_points',
        'start_time',
        'resume_end_time',
        'feed_end_time',
        'actual_cost',
    ]
    search_fields = [
        'user__first_name',
        'user__email',
    ]

STATUS_CHOICES = (
    ('Start', u'等待管理员购买'), # 发起购买流程
    # ('Crawling', u'正在爬取'), # 正在爬取
    # ('Parsing', u'正在解析'), # 正在解析
    ('LookUp', u'用户可以查阅'), # 可以查阅了
    ('Used_UP', u'用户套餐用完'), # 用户套餐用完
    ('Secret', u'信息保密-已返点'), # 用户套餐用完
    # ('LookUp_Used_UP', u'pinbot平台有-用户自己套餐用完'),  # pinbot平台有,但是用户自己套餐用完了
)
STATUS_CHOICES_DICT = dict(STATUS_CHOICES)


class ResumeBuyRecord(Model):
    """
    @summary: 用户简历购买记录
    """
    user = ForeignKey(User, verbose_name=u'用户名')

    # 想购买的简历id,由于简历存储是用mongodb进行的,所以只能存str,不能用外键
    resume_id = CharField(
        max_length=100,
        db_index=True,
    )
    resume_url = URLField(verbose_name=u'简历源',max_length=1000)  # 简历源URL,便于进行爬虫爬取
    # 购买的发起时间
    op_time = DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'购买时间',
    )
    # 购买的完成时间
    finished_time = DateTimeField(
        null=True,
        blank=True,
        default=default_datetime,
        verbose_name=u'完成时间',
        db_index=True,
    )
    status = CharField(choices=STATUS_CHOICES, max_length=100, verbose_name=u'代购状态')

    feed_id = CharField(max_length=100, verbose_name=u'订阅ID', default='', null=True, blank=True)  # 订阅id
    keywords = CharField(max_length=100, verbose_name=u'搜索/订阅关键词', default='') # 关键词

    # 简历反馈信息
    feedback_info = ForeignKey(FeedBackInfo, verbose_name=u'用户选择', null=True, blank=True)
    send_card = ForeignKey(SendCompanyCard,verbose_name=u'企业名片发送', null=True, blank=True)

    def company_name(self):
        return self.user.username + "(" + self.user.first_name + ")"

    company_name.short_description = '公司名'

    def show_resume_url(self):
        result = urlparse(self.resume_url)
        origin_url = "<a href=%s target=%s>%s</a>" % (self.resume_url, self.resume_id + '_1' , result.hostname)
        return mark_safe(origin_url)

    show_resume_url.short_description = '原网址'

    def show_pinbot_url(self):
        pinbot_resume_url = '''
        <a href="/crm/candidate/details/{0}/" target="_blank">CRM查看</a> <br><br>
        <a href="/resumes/display/{0}/?feed_id={1}" target="_blank">简历详情</a>
        '''.format(self.resume_id, self.feed_id)
        return mark_safe(pinbot_resume_url)

    show_pinbot_url.short_description = 'pinbot网址'

    def show_feed_url(self):
        feed_title = self.feed_title if hasattr(self, 'feed_title') else self.feed_id
        feed_url = '<a href="http://admin.pinbot.me/xadmin/feed/feed/?_p_feed_obj_id__contains=%s" target="_blank">%s</a>' % (
            self.feed_id,
            feed_title,
        )
        return mark_safe(feed_url)

    show_feed_url.short_description = '定制'

    def __unicode__(self):
        return self.resume_id

    def __str__(self):
        return self.__unicode__()

    def check_op(self):

        if self.status == 'Start' or self.status == 'NeedAdmin':
            url = """
            <a data-link-confirm="/transaction/return/secret/%s" href="javascript:void(0)">改简历保密</a>
            <br><br><a href="/xadmin/resumes/contactinfodata/add/" target="_blank">手工添加联系方式</a>
            <br>%s
            """ % (self.id, self.resume_id)
            return mark_safe(url)
        else:
            return STATUS_CHOICES_DICT.get(self.status, '未知')

    check_op.short_description = '保密返点操作'

    def show_company_card(self):
        if self.send_card:
            return self.send_card.send_user.username + "(" + self.send_card.send_user.first_name + ")"
        else:
            return "直接购买"

    show_company_card.short_description = '企业名片发送方'

    def mark_resume(self):
        url = '''
        <a href="/transaction/mark_resume/%s/">标记简历</a>
        ''' % self.id
        return mark_safe(url)

    mark_resume.short_description = '标记简历'

    class Meta:
        unique_together = (
            ('user', 'resume_id'),
        )
        verbose_name = u'简历购买处理'
        verbose_name_plural = verbose_name


class DownloadResumeMark(models.Model):
    VERIFY_META = (
        (0, '未审批'),
        (1, '已通过'),
        (2, '未通过'),
    )
    ACCU_META = (
        (0, '未举报'),
        (1, '已举报'),
        (2, '审核通过'),
        (3, '审核失败'),
    )

    buy_record = models.OneToOneField(
        ResumeBuyRecord,
        related_name='resume_mark',
        verbose_name='购买纪录',
    )
    last_mark = models.ForeignKey(
        'system.ResumeMarkSetting',
        verbose_name='上次标记',
        null=True,
        blank=True,
        related_name='last_marks',
        on_delete=models.SET_NULL,
    )
    current_mark = models.ForeignKey(
        'system.ResumeMarkSetting',
        verbose_name='标记状态',
        related_name='current_marks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    pay_status = models.IntegerField(
        default=0,
        verbose_name='付款状态',
    )
    mark_time = models.DateTimeField(
        auto_now=True,
        verbose_name='标记时间',
    )
    verify_status = models.IntegerField(
        default=0,
        choices=VERIFY_META,
        verbose_name='审批状态',
    )
    has_interview = models.BooleanField(
        default=False,
        verbose_name='已经面试'
    )
    accu_status = models.IntegerField(
        default=0,
        choices=ACCU_META,
        verbose_name='举报状态',
    )

    def __unicode__(self):
        return self.buy_record.resume_id

    def __str__(self):
        return self.__unicode__()

    def username(self):
        return '%s(%s)' % (
            self.buy_record.user.username,
            self.buy_record.user.first_name
        )

    username.short_description = '用户名'

    def feed(self):
        feed_obj_id = self.buy_record.feed_id
        if not feed_obj_id or feed_obj_id == 'None':
            return '无'

        from feed.models import Feed
        feed = get_object_or_none(
            Feed,
            feed_obj_id=feed_obj_id,
        )
        if not feed:
            return '无'

        feed_url = '''
        <a href="/statis/feed_result/group/%s?username=%s#/group/%s" target="_blank">%s</a>
        ''' % (
            feed_obj_id,
            self.buy_record.user.username,
            feed_obj_id,
            feed.title or feed.keywords
        )
        return mark_safe(feed_url)

    feed.short_description = '定制'

    def resume_info(self):
        resume_id = self.buy_record.resume_id
        if not resume_id:
            return '无'

        contact_info = get_object_or_none(
            ContactInfoData,
            resume_id=resume_id,
        )
        if not contact_info:
            return '无'

        resume_url = '''
        <a href="%s" target="_blank">%s<br />%s</a>
        ''' % (
            reverse('resume-display-resume', args=(self.buy_record.resume_id, 0)),
            contact_info.name,
            contact_info.phone,
        )
        return mark_safe(resume_url)

    resume_info.short_description = '简历信息'

    def mark_log(self):
        all_log = list(self.mark_logs.all())
        log = ''.join('%s<br>%s<br>' % (l.mark_time.strftime('%Y-%m-%d %H:%M'), l.mark.name) for l in all_log)
        return mark_safe(log)

    mark_log.short_description = '标记记录'

    def change_mark(self):
        ui = '''
        <a href="/transaction/mark_resume/%s/">查看并修改</a>
        ''' % self.buy_record.id
        return mark_safe(ui)

    change_mark.short_description = '修改'

    def admin_remark(self):
        all_admin_log = list(self.admin_logs.all())
        log = ''.join(
            '%s<br>%s<br>%s<br>' % (l.log_time.strftime('%Y-%m-%d %H:%M'), l.user.username, l.desc)
            for l in all_admin_log
        )
        ui = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="备注"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field"></span>
        ''' % reverse('transaction-admin-remark-form', args=(self.id,))
        ui = log + ui
        return mark_safe(ui)

    admin_remark.short_description = '备注'

    def show_resume(self):
        resume_url = '''
        <a href="%s" target="_blank">查看</a>
        ''' % reverse('resume-display-resume', args=(self.buy_record.resume_id, 0))
        return mark_safe(resume_url)

    show_resume.short_description = '查看简历'

    class Meta:
        verbose_name = '用户标记记录'
        verbose_name_plural = verbose_name


class UserMarkLog(models.Model):

    resume_mark = models.ForeignKey(
        DownloadResumeMark,
        related_name='mark_logs',
    )
    mark_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='标记时间',
    )
    mark = models.ForeignKey(
        'system.ResumeMarkSetting',
        verbose_name='标记状态',
        related_name='mark_logs',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name='标记用户',
        related_name='user_mark_logs',
        null=True,
        blank=True,
    )
    is_display = models.BooleanField(
        default=False,
        verbose_name="是否展示给客户",
        blank=True,
    )
    desc = models.CharField(
        max_length=200,
        verbose_name='描述',
    )

    def __unicode__(self):
        return self.mark.desc

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '简历标记日志'
        verbose_name_plural = verbose_name


class AdminMarkLog(models.Model):

    resume_mark = models.ForeignKey(
        DownloadResumeMark,
        related_name='admin_logs',
    )
    user = models.ForeignKey(
        User,
        verbose_name='管理员',
    )
    log_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='记录时间',
    )
    desc = models.CharField(
        max_length=100,
        verbose_name='描述',
    )

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '管理员标记'
        verbose_name_plural = verbose_name


class InterviewAlarm(models.Model):
    """
    面试提醒记录
    """

    buy_record = models.OneToOneField(
        'transaction.ResumeBuyRecord',
        related_name='interview_alarm',
        verbose_name='购买记录',
    )
    interview_count = models.IntegerField(
        default=0,
        verbose_name='面试次数',
    )
    interview_time = models.DateTimeField(
        verbose_name='面试时间',
        db_index=True,
    )
    has_alarm = models.BooleanField(
        default=False,
        verbose_name='是否提醒',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )

    def __str__(self):
        return u'%s' % (
            self.interview_time.strftime('%Y-%m-%d %H:%M'),
        )

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = '面试提醒记录'
        verbose_name_plural = verbose_name


class BuyResumeCategory(models.Model):

    user = models.ForeignKey(
        User,
        related_name='buy_resume_categories',
        verbose_name='用户',
    )
    category_name = models.CharField(
        max_length=15,
        verbose_name='分类名',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    resumes = models.ManyToManyField(
        ResumeBuyRecord,
        related_name='resume_categories',
        verbose_name='购买简历',
    )

    def __str__(self):
        return self.category_name

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = '用户自定义文件夹'
        verbose_name_plural = verbose_name
