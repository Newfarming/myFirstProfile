# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

RECORD_TYPE = (
    ('partner', u'人才伙伴'),
    ('promotion', u'推广伙伴'),
    ('pkg', u'购买点数'),
    ('download_resume', u'下载简历'),
    ('send_company_card', u'发送企业名片'),
    ('send_resume', u'简历投递'),
    ('market_promotion', u'营销活动'),
    ('vip', u'聘宝VIP'),
    ('accu_return_point', u'返点'),
)


class PinbotPoint(models.Model):
    '''
    聘宝点数
    '''
    user = models.OneToOneField(User, verbose_name=u'注册用户')
    point = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name=u'点数',
    )
    coin = models.FloatField(
        default=0,
        verbose_name=u'金币',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'创建时间',
    )

    def get_total_point(self):
        return self.pkg_point + self.point

    def __unicode__(self):
        return u'用户:%s，点数%d' % (self.user.username, self.point)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'聘点'
        verbose_name_plural = verbose_name


class PointRecord(models.Model):
    '''
    点数使用记录
    '''
    user = models.ForeignKey(
        User,
        verbose_name=u'用户',
    )
    record_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=u'使用时间'
    )
    record_type = models.CharField(
        max_length=30,
        choices=RECORD_TYPE,
        verbose_name=u'记录类型',
    )
    detail = models.CharField(
        max_length=200,
        verbose_name=u'详细信息',
    )
    point = models.IntegerField(
        verbose_name=u'点数',
    )
    point_rule = models.CharField(
        max_length=30,
        default='',
        verbose_name=u'点数规则'
    )

    def __unicode__(self):
        return '%s，%s' % (self.user.username, self.detail)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'点数使用记录'
        verbose_name_plural = verbose_name


class PointRule(models.Model):
    '''
    点数规则
    '''
    RULE_TYPE = (
        ('add', u'增加'),
        ('consume', u'减少'),
    )
    RULE_CLASSIFY = (
        (0, '聘点'),
        (1, '金币'),
    )

    rule_name = models.CharField(
        max_length=200,
        verbose_name=u'规则名称',
    )
    point_rule = models.CharField(
        max_length=50,
        verbose_name=u'英文别名',
    )
    rule_type = models.CharField(
        max_length=20,
        choices=RULE_TYPE,
        verbose_name=u'点数规则',
    )
    rule_classify = models.IntegerField(
        default=0,
        choices=RULE_CLASSIFY,
        verbose_name='规则类型'
    )
    record_type = models.CharField(
        max_length=50,
        choices=RECORD_TYPE,
        verbose_name=u'规则应用于',
    )
    point = models.IntegerField(
        verbose_name=u'规则点数',
    )
    total_max_point = models.IntegerField(
        verbose_name=u'最大点数',
        default=0,
    )
    days_max_point = models.IntegerField(
        verbose_name=u'每天最大点数',
        default=0,
    )
    description = models.CharField(
        max_length=200,
        verbose_name=u'描述',
    )
    remark = models.CharField(
        max_length=200,
        verbose_name=u'备注',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'创建时间',
    )

    def __unicode__(self):
        return self.rule_name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'点数规则'
        verbose_name_plural = verbose_name


class CoinRecord(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='coin_records',
    )
    record_type = models.CharField(
        max_length=30,
        choices=RECORD_TYPE,
        verbose_name=u'记录类型',
    )
    desc = models.CharField(
        max_length=80,
        verbose_name='描述',
    )
    coin = models.FloatField(
        verbose_name='金币数',
    )
    record_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='记录时间',
    )
    point_rule = models.CharField(
        max_length=30,
        default='',
        verbose_name=u'点数规则'
    )

    def __str__(self):
        return '%s%s' % (self.user.username, self.coin)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = '金币记录'
        verbose_name_plural = verbose_name
