# coding:utf-8
'''
Created on Sep 26, 2013

@author: likaiguo.happy@gmail.com
'''

WRITE_LOG = True

STAR_LIST = [i / 2.0 for i in range(1, 11)]



# 评分相关全局变量
INDUSTRY_CATAGORY_LIST = [u'互联网/电子商务' , u'计算机软件', u'IT服务（系统/数据/维护）/多领域经营', u'通信/电信/网络设备', \
                          u'计算机硬件及网络设备' , u'通信/电信运营、增值服务', u'网络游戏', u'计算机软件', u'其它']

SPECIAL_INDUSTRY_DICT = {u'网络游戏':5, u'互联网/电子商务':3}  


POSTION_TITLE_DICT = {u'CTO':12, u'CEO':12 , u'首席技术官CTO':12, u'首席信息官CIO':12, \
                       u"总经理":11, u'总监':9, u'资深经理':7, u'高级经理':7 , \
                        u'产品经理':1, u'经理':5, u'组长':3 , u'leader':3, \
                         u'负责人':5, u'主管':5, u'team leader':3} 




responsibility_importance_dict = {r'.*负责.*?(项目|产品)':7,
                                  r'.*(独立负责|独自负责|主程|主美|主力程序员|主力开发).*':5,
                                  r'.*(独立完成|独自完成|独立实现|独自实现|独立设计|独自设计).*':3
                                  }
import re
RESPONSIBILITY_REGEX_LIST = [ (re.compile(regex) , weight)for regex , weight in responsibility_importance_dict.items()] 


DEGREE_TUPLE_LIST = [(u'大专', 1.5), (u'本科', 7), (u'硕士', 10), (u'博士', 15)]


PROFICIENCY_DICT = {u'了解':0.8, u'一般': 1.2, u'良好':1.5 , u'熟练':2 , u'精通':3}



