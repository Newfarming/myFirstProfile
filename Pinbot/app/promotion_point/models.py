# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

VERIFY_STATUS = (
    (0, u'待审核'),
    (1, u'已通过'),
    (2, u'已失败'),
)


class PromotionPointRecord(models.Model):
    register_user = models.ForeignKey(
        User,
        verbose_name='注册用户',
        unique=True,
    )
    promotion_user = models.ForeignKey(
        User,
        verbose_name='推广用户',
        related_name='promotion_record'
    )
    point = models.IntegerField(
        default=0,
        verbose_name='获得点数'
    )
    coin = models.FloatField(
        default=0,
        verbose_name='金币',
    )
    promotion_date = models.DateTimeField(
        auto_now=True,
        verbose_name='生成时间'
    )
    verify_status = models.IntegerField(
        default=0,
        choices=VERIFY_STATUS,
        verbose_name=u'审核状态',
    )

    def __str__(self):
        return '%s promotion %s register' % (
            self.promotion_user.username,
            self.register_user.username,
        )

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = u'推广记录'
        verbose_name_plural = u'推广记录'


class PromotionToken(models.Model):
    promotion_user = models.OneToOneField(
        User,
        verbose_name='推广用户'
    )
    token = models.CharField(
        max_length=50,
        verbose_name='推广的token',
        unique=True,
    )
    create_date = models.DateTimeField(
        auto_now=True,
        verbose_name='生成时间'
    )

    def __unicode__(self):
        return self.promotion_user.username

    class Meta:
        verbose_name = u'推广积分token'
        verbose_name_plural = u'推广积分token'


class PromotionClickRecord(models.Model):
    user = models.ForeignKey(User, verbose_name='点击用户')
    click_date = models.DateField(
        auto_now=True,
        verbose_name='点击时间',
        db_index=True,
    )
    click_times = models.IntegerField(default=1, verbose_name='点击次数')

    def company(self):
        return self.user.userprofile.company_name

    company.short_description = u'公司名称'

    class Meta:
        verbose_name = u'推广点击记录'
        verbose_name_plural = u'推广点击记录'
