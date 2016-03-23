# coding: utf-8

import datetime

from django.db import models
from django.contrib.auth.models import User

from Brick.Utils.django_utils import upload_filepath


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('', '未知'),
    )
    DEFAULT_BIRTHDAY = datetime.datetime.strptime(
        '1990-1-1',
        '%Y-%m-%d'
    )

    user = models.OneToOneField(
        User,
        verbose_name='登录用户',
        related_name='brick_user_profile',
    )
    nickname = models.CharField(
        verbose_name='昵称',
        max_length=50,
        default='',
    )
    gender = models.CharField(
        verbose_name='性别',
        max_length=10,
        choices=GENDER_CHOICES,
        default='',
    )
    birthday = models.DateField(
        verbose_name='生日',
        default=DEFAULT_BIRTHDAY,
    )
    phone = models.CharField(
        verbose_name='电话',
        max_length=20,
        default=''
    )
    avatar = models.ImageField(
        verbose_name='头像',
        max_length=200,
        upload_to=upload_filepath('avaters'),
        default=''
    )
    is_active = models.BooleanField(
        verbose_name='激活状态',
        default=False,
    )
    no_pub = models.BooleanField(
        verbose_name='公开联系方式',
        default=False,
    )
    allow_recommend = models.BooleanField(
        verbose_name='允许推荐',
        default=True,
    )

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'


class UserToken(models.Model):

    TOKEN_META = (
        ('register', '注册激活'),
        ('reset', '密码重置'),
    )

    user = models.ForeignKey(
        User,
        verbose_name=u'登录用户',
        related_name='user_token',
    )
    token = models.CharField(
        max_length=60,
        verbose_name='TOKEN',
    )
    active = models.BooleanField(
        verbose_name='状态',
        default=True,
    )
    token_type = models.CharField(
        max_length=30,
        verbose_name='TOKEN类型',
        choices=TOKEN_META,
        default='register',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'创建时间'
    )

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = u'用户TOKEN'
        verbose_name_plural = verbose_name
