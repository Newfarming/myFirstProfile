# coding:utf-8
from django.db import models
from users.models import User

# Create your models here.


CHECK_CHOICES = (
    ('checking', u'审核中'),
    ('success', u'审核通过'),
    ('fail', u'审核失败'),
)
NOTIFY_CHOICES = (
    ('need_notify', u'需要通知'),
    ('notified', u'已经通知'),
    ('read', u'通知已读'),
)


class TaocvConfig(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'分类名称')
    feed_id = models.CharField(max_length=50, verbose_name=u'订阅id')
    area = models.CharField(
        max_length=50, verbose_name=u'简历地区', blank=True, null=True, default="北京")
    display = models.BooleanField(default=True, verbose_name=u'是否显示在taocv中')
    sequence = models.IntegerField(
        default=1, blank=True, null=True, verbose_name=u'显示顺序')  # 顺序

    class Meta:
        verbose_name = u'淘简历配置'
        verbose_name_plural = u'淘简历配置'


class UserFeedbackPoints(models.Model):

    """
    记录用户的积分信息
    """
    user = models.ForeignKey(User)
    total_points = models.IntegerField(default=0)  # 用户总积分
    used_points = models.IntegerField(
        default=0, verbose_name=u'已使用')  # 用户已消费的积分
    reward_points = models.IntegerField(
        default=20, verbose_name=u'赠送积分')  # 赠送积分
    zero_points_notify_status = models.CharField(
        choices=NOTIFY_CHOICES, max_length=50, verbose_name=u'积分为0提醒通知状态')  # 积分为0提醒通知

    class Meta:
        db_table = 'rfd_user_fd_points'
        verbose_name = u'用户积分'
        verbose_name_plural = u'用户积分'

    def company_name(self):
        return self.user.username + "(" + self.user.first_name + ")"


class TaocvConfigAdmin(object):
    list_display = ['title', 'feed_id', 'area', 'display', 'sequence']
    lis_diplay_links = ['title']
    list_editable = ['title', 'feed_id', 'area', 'display', 'sequence']


class UserResumeFeedbackAdmin(object):
    list_display = [
        'create_time',
        'company_name',
        'show_resume',
        'get_feedback_info',
        'expect_return_points',
        'check_status',
        'check_op',
        'check_comment',

    ]
    list_display_links = ['company_name']
    list_editable = ['check_status', 'notify_status', 'check_comment']

    ordering = [
        'check_status',
        '-create_time',
    ]

    list_filter = [
        'user',
        'check_status',
        'create_time',
        'feedback_info',
        'feedback_value',
    ]

    search_fields = [
        'user__username',
        'feedback_value',
    ]
