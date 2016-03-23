# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class MailTags(models.Model):
    """邮件标签,与sendclouds重的邮件标签对应"""
    tag_id = models.IntegerField(
                                 verbose_name='标签ID',
                                 unique=True,
                                 null = True,
                                 blank=True

                               )
    tag_name = models.CharField(
                                verbose_name='标签名称',
                                unique=True,
                                max_length=50
                                )

    def __unicode__(self):
        return self.tag_name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '邮件标签'
        verbose_name_plural = verbose_name


class MailTemplateCategory(models.Model):
    """邮件模板分类"""
    name = models.CharField(verbose_name='分类名称',
                            max_length=50,
                            )

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '邮件模板分类'
        verbose_name_plural = verbose_name


class MailTemplate(models.Model):
    """邮件模板"""
    category = models.ForeignKey(MailTemplateCategory, verbose_name='邮件模板分类')
    name = models.CharField(
                            verbose_name='模板名称',
                            max_length=100,
                            unique=True,
                            )
    content = models.TextField(
                            verbose_name='模板内容'
                            )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    last_update_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='最后更新时间'
    )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '邮件模板'
        verbose_name_plural = verbose_name