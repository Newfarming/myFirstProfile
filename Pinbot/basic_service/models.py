# coding: utf-8
from datetime import datetime
from django.db import models
STATUS_CHOICES = (
    ('success', u'发送成功'),
    ('fail', u'发送失败'),
)

class EmailSendLog(models.Model):
    """
    邮件发送记录
    """
    from_email = models.CharField(max_length=50, verbose_name=u'发送者')
    send_time = models.DateTimeField(default=datetime.now(), verbose_name=u'发送时间')
    subject = models.CharField(max_length=100, verbose_name=u'邮件主题', blank=True, null=True)
    
    to_email = models.CharField(max_length=500, verbose_name=u'接收方', blank=True, null=True)
    
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, verbose_name=u'发送结果', blank=True, null=True)
    error_info = models.CharField(max_length=200, verbose_name=u'错误信息', blank=True, null=True)
    
    class Meta:
        db_table = 'email_send_log'
        verbose_name = u'邮件发送详情'
        verbose_name_plural = u'邮件发送详情'
    meta = {
            "indexes":[
                'from_email',
                'send_time',
                "subject",
                'to_email',
                'status',
                'error_info',
                ]
            }


class EmailSendLogAdmin(object):
    list_display = [
            'from_email',
            'send_time',
            "subject",
            'to_email',
            'status',
            'error_info',
            ]
    list_display_links = ['from_email']
     
    ordering = [
        '-send_time',
        ]
     
    list_filter = [
        'send_time',
        'subject',
        'to_email',
        'status',
        ]
     
    search_fields = [
        'subject',
        'to_email',
        'status',
        ] 
