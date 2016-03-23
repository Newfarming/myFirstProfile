# coding: utf-8
from mongoengine import (DateTimeField,
                         StringField,
                         Document,
                         DictField,
                         BooleanField
                         ) 
from datetime import datetime

class MarketEmailSendDetail(Document):
    """
    @summary: 营销邮件发送详情
    """
    send_time = DateTimeField(default=datetime.now(),verbose_name=u'发送时间')
    from_email = StringField(max_length=50, verbose_name=u'发送者')
    subject = StringField(verbose_name=u'邮件主题', required=False)
    to_email = StringField(verbose_name=u'接收方',required=False)
    status = BooleanField(default=True,verbose_name=u'发送结果')
    error_info = StringField(verbose_name=u'错误信息',required=False)
    type = StringField(verbose_name=u'邮件类型',required=False)
    info_dict = DictField(required=False)
    user_request = StringField(verbose_name=u'用户request信息',required=False)
    click_time = DateTimeField(default=datetime.now(),verbose_name=u'反馈时间')