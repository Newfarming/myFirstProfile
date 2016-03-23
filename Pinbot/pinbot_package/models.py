# coding:utf-8
from django.db.models import *

from django.contrib.auth.models import User, Group

from datetime import datetime
from mongoengine.fields import StringField
default_datetime = datetime(2014, 1, 1, 0, 0)


def PackageGroups(Model):
    """
    套餐和用户组关系
    """
    package = ForeignKey(ResumePackge)
    group = ForeignKey(Group)  # 套餐所在组

DISPLAY_CHOICE = [
     (0, '隐藏'),
     (1, '可见')            
    ]
    
    
class FeedService(Model):
    """
    简历套餐
    """
    name = CharField(max_length=100, verbose_name=u'套餐名')  # 套餐名
    price = IntegerField(default=0, verbose_name=u'价格')  # 价格
    
    valid_days = IntegerField(default=0, verbose_name=u'有效天数')  # 有效天数
    remark = CharField(max_length=100, verbose_name=u'备注', null=True, blank=True)  # 该套餐的备注，如适合的企业等
    feed_num = IntegerField(default=1, verbose_name=u'可订数量')
    display = IntegerField(default=0, choices=DISPLAY_CHOICE, verbose_name=u'前端展示', null=True, blank=True)  # 是否显示给客户购买
    
    class Meta:
        verbose_name = u'订阅服务'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name



class ResumePackge(Model):
    """
    简历套餐
    """
    name = CharField(max_length=100, verbose_name=u'套餐名')  # 套餐名
    price = IntegerField(default=0, verbose_name=u'套餐价格')  # 套餐价格
    total_points = IntegerField(default=0, verbose_name=u'套餐点数')  # 总点数
    resume_num = IntegerField(default=0, verbose_name=u'可下载简历数')  # 可下载简历数
    actual_resume_num = IntegerField(default=0, verbose_name=u'实际下载简历数')  # 实际下载简历数
    feed_service_num = IntegerField(default=0, verbose_name=u'订阅数量')  # 订阅数量
    feed_service = ForeignKey(FeedService, verbose_name=u'订阅服务类型')  # 订阅服务类型
    feed_service_value = IntegerField(default=0, verbose_name=u'赠送订阅价值')  # 赠送订阅价值
    valid_days = IntegerField(default=0, verbose_name=u'有效天数')  # 有效天数
    
    display = IntegerField(default=0, choices=DISPLAY_CHOICE, verbose_name=u'前端展示', null=True, blank=True)  # 是否显示给客户购买
    company_type = CharField(max_length=100, verbose_name=u'适合企业', null=True, blank=True)  # 适合企业
    remark = CharField(max_length=100, verbose_name=u'备注', null=True, blank=True)  # 该套餐的备注，如适合的企业等
    
    group = ForeignKey(Group, verbose_name='该套餐权限')
#     objects = ResumePackageManager()
    class Meta:
        verbose_name = u'基础套餐'
        verbose_name_plural = verbose_name    
    
    def __unicode__(self):
        return self.name
    
class ResumePackgeAdmin(object):
    list_display = ['name', 'price', 'total_points', 'resume_num', \
                    'actual_resume_num',
                     'feed_service', \
                     'feed_service_num',
                    'feed_service_value',
                    
                    'valid_days', 'group', 'display']
    list_display_links = ['name']
    
    list_editable = ['name', 'price', 'total_points', 'resume_num', \
                    'actual_resume_num', 'feed_service_num', 'feed_service', \
                    'feed_service_value',
                    'valid_days', 'group', 'display']
    

class FeedServiceAdmin(object):
    list_display = ['name', 'price', 'valid_days', 'remark']
    list_display_links = ['name']
    list_editable = ['name']
