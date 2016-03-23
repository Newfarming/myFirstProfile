# coding:utf-8
'''
Created on 2015年1月28日

@author: likaiguo

celery-best-practices 最佳实践
http://my.oschina.net/siddontang/blog/284107

官方推荐:最佳实践
http://celery.readthedocs.org/en/latest/userguide/tasks.html#task-best-practices

'''
"""
1.基本设置
"""

from Brick.settings import RECO_BROKER_URL
from kombu import Queue, Exchange

# 中继消息队列服务器
# 173 flower: admin Hopperclouds2014
# BROKER_URL = 'amqp://admin:root@218.244.150.173:5672'

# BROKER_URL = 'mongodb://localhost:27017/celery'
BROKER_URL = RECO_BROKER_URL


# 任务序列化格式
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# 时区设置
# CELERY_ENABLE_UTC = True
# CELERY_TIMEZONE = 'Asia/Chongqing'


# celery worker的并发数
# 也是命令行-c指定的数目,事实上实践发现
# 并不是worker也多越好,保证任务不堆积,加上一定新增任务的预留就可以
CELERYD_CONCURRENCY = 50

# celery worker 每次去rabbitmq取任务的数量，
# 这里预取了4个慢慢执行,因为任务有长有短没有预取太多
CELERYD_PREFETCH_MULTIPLIER = 4

# 每个worker执行了多少任务就会死掉
# 数量可以大一些，比如200
CELERYD_MAX_TASKS_PER_CHILD = 40

#######################################################################
"""
2.设置queue, exchange [direct , fanout,topic],route
"""
# 默认的队列，
# 如果一个消息不符合其他的队列就会放在默认队列里面
CELERY_DEFAULT_QUEUE = "default"

CELERY_QUEUES = (
     Queue('default', Exchange('default'), routing_key='default'),
     Queue('for_reco_job', Exchange('for_reco_Job'), routing_key='for_reco_job'),
     Queue('for_dump_feed2es', Exchange('for_dump_feed2es'), routing_key='for_dump_feed2es'),
    )
CELERY_ROUTES = {
       'reco_job':{'queue':'for_reco_job', 'routing_key':'for_reco_job'},
       'reco_job':{'queue':'for_dump_feed2es', 'routing_key':'for_dump_feed2es'},
  }

#########################################################################
"""
3.执行结果存储相关

'"""

# 官网优化的地方也推荐使用c的librabbitmq
# 展示暂时使用mongo做结果存储
CELERY_RESULT_BACKEND = 'mongodb://celery:hopper201313@db1.pinbot.me,db2.pinbot.me,db3.pinbot.me:27017/celery?replicaSet=rs0&readPreference=secondaryPreferred'
CELERY_RESULT_SERIALIZER = 'json'
# celery任务执行结果的超时时间，我的任务都不需要返回结果,只需要正确执行就行
CELERY_TASK_RESULT_EXPIRES = 12000
