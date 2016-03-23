# coding:utf-8
'''
Created on 2015年1月29日
@author: likaiguo
# 发起职位推荐请求
result = app.send_task(
'reco_job_es',
['54c343b6c07f56bd949791e0'],
queue='for_reco_job'
)
print result.ready()
'''
from celery import Celery
import celeryconfig

app = Celery('reco_job')
app.config_from_object(celeryconfig)
