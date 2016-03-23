# coding: utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
REGULAR_CHOICES = [
('max', u'最大值'), 
]

TITLE_CHOICES = [
('upload', u'简历上传奖励'),
('login', u'登录奖励'),
('promotion', u'推广奖励'),
]

class RewardConfig(models.Model):
    """
    积分赠送配置
    """
    points = models.IntegerField(default=0, verbose_name=u'积分') #赠送的积分
    regular =  models.CharField(choices=REGULAR_CHOICES,max_length=255,null=True, blank=True, verbose_name=u'规则')  #奖励规则
    regular_value = models.IntegerField(default=0,null=True, blank=True, verbose_name=u'规则值') #规则值
    max_points_total = models.IntegerField(default=0, verbose_name=u'积分最大值') #该赠送积分的最大值
    title = models.CharField(choices=TITLE_CHOICES,max_length=255, verbose_name=u'奖励类型')  #奖励
    desc = models.CharField(max_length=255,null=True, blank=True, verbose_name=u'奖励描述')  #奖励描述
    
    class Meta:
        verbose_name = u'积分赠送配置'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.title

class PointsDetail(models.Model):
    """
    积分赠送详细信息
    """
    user = models.ForeignKey(User, verbose_name=u'用户')
    time = models.DateTimeField(verbose_name=u'奖励时间')  #赠送时间
    type = models.ForeignKey(RewardConfig, verbose_name=u'奖励类型',null=True, blank=True)  #奖励类型
    access_type = models.IntegerField(default=0, verbose_name=u'积分使用类型',null=True, blank=True) #积分使用类型 0表示增加，1表示消费
    points = models.IntegerField(default=0, verbose_name=u'赠送的积分') #赠送的积分
    detail_info = models.CharField(max_length=255,null=True, blank=True, verbose_name=u'描述')  #详细信息
    
    class Meta:
        verbose_name = u'积分赠送详细信息'
        verbose_name_plural = verbose_name
        
class UserPoints(models.Model):
    """
    用户积分
    """
    user = models.ForeignKey(User, verbose_name=u'用户')
    login_points = models.IntegerField(default=0, verbose_name=u'登录奖励积分总和')  #登录奖励积分总和
    upload_points = models.IntegerField(default=0, verbose_name=u'简历上传积分总和')  #简历上传奖励积分总和
    promotion_points = models.IntegerField(default=0, verbose_name=u'推广积分总和')  #推广奖励积分总和
    total = models.IntegerField(default=0, verbose_name=u'积分总和')  #积分总和
    consumed_points = models.IntegerField(default=0, verbose_name=u'消费积分总和')  #消费积分总和
    class Meta:
        verbose_name = u'用户积分'
        verbose_name_plural = verbose_name


class RewardConfigAdmin(object):
    list_display = [
                    'title',
                    'desc',
           'points',
            'regular',
            
            'regular_value',
            'max_points_total',
        ]
    
    list_display_links = [
#           'show_qq',
        "title"
        ]
    
    
    list_editable = [
            'points',
            'regular',
            
            'regular_value',
            'title',
            'desc',
    ]
    
class PointsDetailAdmin(object):
    list_display = [
           'user',
            'time',
            
            'type',
            'points',
            'detail_info',
        ]
    
    list_display_links = [
        "user"
        ]
    
    list_editable = [
            'detail_info',
    ]

class UserPointsAdmin(object):
    list_display = [
           'user',
            'login_points',
            
            'upload_points',
            'promotion_points',
        ]
    
    list_display_links = [
        "user"
        ]
