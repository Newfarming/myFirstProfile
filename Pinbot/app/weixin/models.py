# coding: utf-8

from django.db import models
from django.contrib.auth.models import User


class WeixinUser(models.Model):

    SEX_META = (
        (0, '未知'),
        (1, '男'),
        (2, '女')
    )
    user = models.OneToOneField(
        User,
        verbose_name='用户',
        related_name='weixin_user',
    )
    openid = models.CharField(
        max_length=255,
        verbose_name='用户OPENID',
        unique=True
    )
    nickname = models.CharField(
        max_length=100,
        verbose_name='用户昵称',
        blank=True
    )
    sex = models.PositiveSmallIntegerField(
        default=0,
        choices=SEX_META,
        verbose_name='用户性别',
        blank=True
    )
    city = models.CharField(
        max_length=60,
        verbose_name='所在城市',
        blank=True
    )
    province = models.CharField(
        max_length=60,
        verbose_name='所在省份',
        blank=True
    )
    country = models.CharField(
        max_length=60,
        verbose_name='所在国家',
        blank=True
    )
    headimgurl = models.CharField(
        max_length=200,
        verbose_name='头像',
        blank=True
    )
    privilege = models.CharField(
        max_length=255,
        verbose_name='特权信息',
        blank=True
    )
    unionid = models.CharField(
        max_length=255,
        verbose_name='用户UNIONID',
        blank=True
    )
    is_bind = models.BooleanField(
        default=True,
        verbose_name='是否绑定'
    )
    is_subscribe = models.BooleanField(
        default=True,
        verbose_name='是否关注'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='初次绑定时间'
    )
    subscribe = models.BooleanField(
        default=True,
        verbose_name='关注状态'
    )
    subscribe_time = models.FloatField(
        default=0,
        verbose_name='关注时间'
    )
    remark = models.CharField(
        max_length=255,
        verbose_name='备注',
        blank=True
    )
    language = models.CharField(
        max_length=255,
        verbose_name='语言',
        blank=True
    )
    groupid = models.IntegerField(
        default=0,
        verbose_name='分组id',
    )

    def __unicode__(self):
        return u'%s,%s' % (self.user.username, self.openid)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '微信用户'
        verbose_name_plural = verbose_name


class MsgSendLog(models.Model):

    MSG_TYPE_META = (
        (1, '定制推荐'),
        (2, '其他通知')
    )

    weixin_user = models.ForeignKey(
        WeixinUser,
        verbose_name='微信用户',
        related_name='weixin_user',
    )
    msg_type = models.IntegerField(
        default=0,
        choices=MSG_TYPE_META,
        verbose_name='消息类型'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    reco_num = models.IntegerField(
        default=0,
        verbose_name='职位数量'
    )
    display_time = models.DateTimeField(
        verbose_name='显示时间'
    )
    url = models.CharField(
        max_length=200,
        verbose_name='推荐链接'
    )
    add_time = models.DateTimeField(
        auto_now_add=True
    )
    errcode = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='错误代码'
    )
    errmsg = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='错误信息'
    )

    def __unicode__(self):
        return u'%s' % (self.weixin_user.user.username)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '微信消息发送记录'
        verbose_name_plural = verbose_name
