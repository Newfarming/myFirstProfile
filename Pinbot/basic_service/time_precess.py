# coding:utf-8
'''
Created on 2013-11-11

@author: likaiguo.happy@163.com 2013-11-11 17:59:31
@summary: 时间相关处理
'''
import time 
from datetime import datetime, timedelta

def time_delt_str(days=-7, formart="%Y-%m-%d"):
    time_now = datetime.now()
    delt_days = timedelta(days=days)
    time_new = time_now + delt_days
    return time_new.strftime(formart)
 

if __name__ == '__main__':
    t1 = ""