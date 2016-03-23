# coding:utf-8
'''
Created on 2013-11-8

@author: dell

@summary:
以每一个客户为单位，统计每日0:00-24:00时间区段的以下信息：
1、聘宝登陆次数；
2、使用聘宝分析次数；
3、聘宝简历查看次数；
4、原简历中使用聘宝插件次数；
5、当天首次登陆时间；
6、当天末次使用时间；
7、关键词搜索明细；
8、聘宝简历关注数量。

'''
import datetime
from mongoengine import *
from mongoengine.queryset import queryset_manager
from statistics.global_variables import *

class StatisticsDataQuerySet(QuerySet):

    def get_awesome(self):
        return self.filter(awesome=True)
    
    def get_username_list(self):
        
        return self.distinct("username")
    
    def get_user_access_count(self):
        
        return self.count()
    
    def get_lateset_access_time(self):
        return self.order_by('-access_time')[0]

class StatisticsModel(Document):
    '''
    @summary: 数据统计模型
    '''
    
    username = StringField(default='', required=False)
    
    access_time = DateTimeField()
    # 访问的页面id代号
    page_id = IntField(default=0)
    cost_time = FloatField(default=0)
    search_keywords = StringField(default='', required=False)
    url = StringField(default='', required=False)
 
    meta = {"collection": "statistic_data" , 'queryset_class': StatisticsDataQuerySet}
    ip = StringField(default='')
    access_url = StringField(default='')
    refer_url = StringField(default='')
    http_meta = StringField(default='')
    user_agent = StringField(default='')
    
    meta = { 
            "collection": "statistic_data"  ,
            'queryset_class': StatisticsDataQuerySet,
            "indexes":[
                       "username",
                       "-access_time",
                       "page_id",
                       "cost_time",
                       "url",
                       "ip",
                 
                       ]
                
                }

 
    @queryset_manager
    @staticmethod
    def test(doc_cls, queryset):
        
        pass


class UserActionRecord(Document):
    username = StringField(default='', required=False)
    access_time = DateTimeField()
    action_id = IntField(default=0)
    ip = StringField(default='')

class FeedResultSta(Document):
    feed_id = ObjectIdField()
    report_day = DateTimeField()
    date_time_from = DateTimeField()
    date_time_to = DateTimeField()
    
    staff_improper_clicks = IntField(default=0)
    customer_improper_clicks = IntField(default=0)
    improper_clicks = IntField(default=0)
    publish_num = IntField(default=0)
    unpublish_num = IntField(default=0)
    machine_recommand_num = IntField(default=0)
    manual_recommand_num = IntField(default=0)
    manchine_publish_num = IntField(default=0)
    manchine_unpublish_num = IntField(default=0)
    manual_publish_num = IntField(default=0)

class UserFeedBack(Document):
    """
@summary: 用户反馈统计
"""
    username = StringField(default='', required=False)
    add_time = DateTimeField(default=datetime.datetime.now())
    feedback_conent = StringField(default='', required=False) 