# coding: utf-8

import bleach
from django.db import models

from datetime import datetime
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


check_status = [
    (-1, '审核失败'),
    (0, '未审核'),
    (1, '通过审核'),
]


class UserProfile(models.Model):

    """
    用户的基本信息
    """
    ROLE_TYPE = (
        ('', ''),
        ('hr', u'HR'),
        ('headhunting', u'猎头'),
        ('web_practitioner', u'互联网从业者'),
        ('other', u'其他'),
    )
    SOURCE_META = (
        (1, '注册'),
        (2, '爬虫'),
    )
    LEVEL_META = (
        (0, '自动发布'),
        (1, '人工发布'),
    )
    CALC_META = (
        (0, '默认'),
        (1, '优先计算'),
    )
    CLIENT_META = (
        (0, '普通客户'),
        (1, '重点客户'),
    )
    SOURCE_DICT = {
        i[0]: i[1]
        for i in SOURCE_META
    }
    user = models.OneToOneField(User, verbose_name='用户名')
    user_email = models.EmailField(max_length=80, verbose_name='接收邮箱')
    company_name = models.CharField(max_length=255, verbose_name='公司')
    company_email = models.EmailField()
    name = models.CharField(max_length=80, default='', verbose_name='HR')
    is_review = models.IntegerField(
        choices=check_status, default=0, verbose_name='审核状态')  # -1表示审核失败 0表示未审核 1表示审核通过
    phone = models.CharField(max_length=50, verbose_name='电话')
    url = models.URLField(
        blank=True, null=True, max_length=200, verbose_name='公司网站')
    qq = models.CharField(
        blank=True, null=True, max_length=50, name='qq')  # qq号码
    status = models.IntegerField(
        default=0, verbose_name='用户状态')  # 用户状态，0表示冻结，1表示激活
    street = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='街道/小区/号码'
    )
    area = models.CharField(
        max_length=30,
        default='',
        blank=True,
        verbose_name='区/县'
    )
    city = models.CharField(
        max_length=30,
        default='',
        blank=True,
        verbose_name='城市'
    )
    province = models.CharField(
        max_length=30,
        default='',
        blank=True,
        verbose_name='省份'
    )
    postcode = models.CharField(
        max_length=30,
        default='',
        blank=True,
        verbose_name='邮编'
    )
    recv_phone = models.CharField(
        max_length=50,
        default='',
        blank=True,
        verbose_name='收货人电话'
    )
    recv_name = models.CharField(
        max_length=50,
        default='',
        blank=True,
        verbose_name='收货人姓名'
    )
    activation_key = models.CharField(
        max_length=40, default='')  # 用户的激活码，用于用于注册后的邮箱验证
    ip = models.IPAddressField()
    guide_switch = models.BooleanField(default=False)
    role = models.CharField(
        max_length=40,
        default='',
        blank=True,
        choices=ROLE_TYPE,
        verbose_name='职业',
    )
    source = models.IntegerField(
        verbose_name='来源',
        default=1,
        choices=SOURCE_META,
    )
    trans_time = models.DateTimeField(
        auto_now=True,
        verbose_name='转换时间',
    )
    service_level = models.IntegerField(
        default=0,
        choices=LEVEL_META,
        verbose_name='服务级别',
        blank=True,
    )
    calc_level = models.IntegerField(
        default=0,
        choices=CALC_META,
        verbose_name='计算级别',
        blank=True,
    )
    client_level = models.IntegerField(
        default=0,
        choices=CLIENT_META,
        verbose_name='客户级别',
        blank=True,
    )
    login_days = models.IntegerField(
        default=0,
        verbose_name='登录天数',
        blank=True,
        db_index=True,
    )
    is_email_bind = models.BooleanField(
        default=False,
        verbose_name='绑定接收邮箱'
    )
    is_phone_bind = models.BooleanField(
        default=False,
        verbose_name='绑定手机号'
    )

    def show_ip(self):

        url = "<a href=http://ip138.com/ips138.asp?ip=%s&action=2 target=%s>%s</a>" % (
            self.ip, self.ip, self.ip)
        return mark_safe(url)

    show_ip.short_description = '注册IP'

    def show_date_join(self):

        return str(self.user.date_joined)

    show_date_join.short_description = '注册日期'

    def show_company(self):
        """
        @summary: 展示公司信息
        """
        company = ''
        if self.url:
            if 'http://' not in self.url:
                link = 'http://' + self.url
            else:
                link = self.url

            url = "<a href=%s target=%s>%s</a>" % (
                link, self.url, self.company_name)
            company = url
        else:
            company = self.company_name
        company = bleach.clean(company, tags=[], strip=True)

        content = """
        HR: %s<br>
        电话:%s<br>
        邮箱:%s<br>
        QQ: %s<br>
        公司:%s<br>
        网站:%s
        """ % (
            self.name,
            self.phone,
            self.user_email,
            self.qq,
            company,
            self.url,
        )
        return mark_safe(content)

    show_company.short_description = '公司'

    def show_active(self):
        url = """
        <a data-link-confirm="/hr/active_user/{0}/" href="javascript:void(0)">通过</a>
        """.format(self.user.username)

        return mark_safe(url)

    show_active.short_description = '人工激活'

    def show_user_active(self):
        user_active = u'激活' if self.user.is_active else u'未激活'
        return mark_safe(user_active)

    show_user_active.short_description = '激活状态'

    def show_source(self):
        return mark_safe(self.SOURCE_DICT.get(int(self.source or 0), self.source))

    @property
    def notify_email(self):
        return self.user_email if self.is_email_bind else None

    show_source.short_description = '用户来源'

    def show_addr(self):
        return '{0}{1}{2}{3} {4}{5}'.format(
            self.province, self.city, self.area, self.street, self.recv_name, self.recv_phone
        )

    show_addr.short_description = '邮寄地址'

    class Meta:
        db_table = 'users_userprofile'
        verbose_name = u'用户审核'
        verbose_name_plural = verbose_name


class UserContactInfo(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='用户名',
        related_name='contact_infos'
    )
    user_email = models.EmailField(
        max_length=60,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=40,
        verbose_name='姓名'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='电话'
    )

    def __unicode__(self):
        return self.name, self.phone

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '用户联系信息'
        verbose_name_plural = verbose_name


class UserMailbox(models.Model):

    """
    用于同步邮箱简历的邮箱信息
    """
    user = models.ForeignKey(User)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    serverAddr = models.CharField(max_length=255)  # 服务器地址
    interval = models.IntegerField(default=30)  # 邮箱同步的时间间隔（分钟）
    port = models.IntegerField()  # 邮箱端口
    mailType = models.CharField(max_length=255)  # 邮箱类型
    addTime = models.DateField()  # 邮箱添加时间
    lastSyncTime = models.DateField()  # 上一次同步时间
    latestSendTime = models.DateField()  # 最近一封邮箱的发送时间
    firstTime = models.BooleanField()  # 是否第一次同步
    latestMailTotal = models.IntegerField(default=0)  # 最近一次处理的邮箱数量
    latestResumeNum = models.IntegerField(default=0)  # 最近一次获取的简历数量
    totalResumeNum = models.IntegerField(default=0)  # 总共同步的简历数量
    totalMailNum = models.IntegerField(default=0)  # 总共处理的邮件数量
    uploadPath = models.CharField(max_length=255)  # 简历上传路径


class StaffCustomerAssgin(models.Model):

    """
    员工客户分配表
    """
    customer = models.ForeignKey(
        User, related_name='stafftaskassign_customers', verbose_name=u'客户')
    staff = models.ForeignKey(
        User, related_name='stafftaskassign_staffs', verbose_name=u'员工')
    operator = models.ForeignKey(
        User, related_name='stafftaskassign_operator', verbose_name=u'操作者', null=True, blank=True)
    create_time = models.DateTimeField(
        verbose_name=u'生成时间', default=datetime.now())
    is_active = models.BooleanField(default=True, verbose_name=u'是否有效')

    def show_customer(self):
        return self.customer.first_name
    show_customer.short_description = '客户'

    def show_staff(self):
        return self.staff.first_name
    show_staff.short_description = '员工'

    class Meta:
        db_table = 'report_staffcustomerassgin'


class NewIndustryBookin(models.Model):

    BOOKIN_META = (
        (1, '4月16日北京场'),
        (2, '4月24日成都场'),
    )

    user = models.ForeignKey(
        UserProfile,
        related_name='user_enlist',
        verbose_name='新行业用户报名'
    )
    type = models.IntegerField(
        choices=BOOKIN_META,
        verbose_name='报名类型'
    )
    add_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='报名时间'
    )
    def __unicode__(self):
        return self.type

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '新行业报名情况'
        verbose_name_plural = verbose_name