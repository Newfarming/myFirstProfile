# coding:utf-8
from django.db.models import *

from django.contrib.auth.models import User,Group

from datetime import datetime
from mongoengine.fields import StringField
from pinbot_package.models import *
default_datetime = datetime(2014, 1, 1, 0, 0)

# PINBOT_SERVICE = [
# ('taocv', u'淘简历'),  # 发起购买流程
# ('feed', u'人才订阅'),  # 处理中
# ]

