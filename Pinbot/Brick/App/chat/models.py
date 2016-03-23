# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from jobs.models import Job
from feed.models import Feed
from Brick.App.my_resume.models import Resume


class Chat(models.Model):

    CHAT_META = (
        ('job', '职位卡片'),
        ('feed', '定制'),
    )
    job_hunter = models.ForeignKey(
        User,
        verbose_name='求职者',
        related_name='hunter_chat',
    )
    hr = models.ForeignKey(
        User,
        verbose_name='HR',
        related_name='hr_chat',
    )
    job = models.ForeignKey(
        Job,
        verbose_name='职位卡片',
        related_name='job_chat',
        null=True,
        blank=True,
    )
    feed = models.ForeignKey(
        Feed,
        verbose_name='定制',
        related_name='feed_chat',
        null=True,
        blank=True,
    )
    chat_type = models.CharField(
        default='job',
        choices=CHAT_META,
        max_length=15,
    )
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='resume_chat',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )

    def __unicode__(self):
        return u'求职者:%s,HR:%s会话' % (self.job_hunter.username, self.hr.username)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '会话'
        verbose_name_plural = verbose_name


class ChatMessage(models.Model):

    chat = models.ForeignKey(
        Chat,
        verbose_name='会话',
    )
    sender = models.ForeignKey(
        User,
        verbose_name='发送人',
        related_name='sender_msgs',
    )
    receiver = models.ForeignKey(
        User,
        verbose_name='接收人',
        related_name='receiver_msgs',
    )
    msg = models.CharField(
        max_length=200,
        verbose_name='消息',
    )
    send_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='发送时间',
    )
    sender_delete = models.BooleanField(
        verbose_name='发送方删除',
        default=False,
    )
    sender_read = models.BooleanField(
        verbose_name='发送方已读',
        default=False,
    )
    receiver_delete = models.BooleanField(
        verbose_name='接收方删除',
        default=False,
    )
    receiver_read = models.BooleanField(
        verbose_name='接收方已读',
        default=False,
    )

    def __unicode__(self):
        return '%s' % (self.chat)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
