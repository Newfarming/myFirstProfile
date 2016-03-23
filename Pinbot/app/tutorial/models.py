# coding: utf-8

from django.db import models


class InterviewTermQuestions(models.Model):

    QUESTION_TYPE = (
        (1, '常见问题'),
        (2, '约面话术'),
    )

    question = models.CharField(
        max_length=254,
        verbose_name='问题'
    )
    anwser = models.TextField(
        max_length=254,
        verbose_name='答案'
    )
    question_type = models.IntegerField(
        default=1,
        choices=QUESTION_TYPE,
        verbose_name='问题类别'
    )

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '约面话术&常见问题'
        verbose_name_plural = verbose_name


class FeedBackText(models.Model):

    feedback_text = models.TextField(
        max_length=254,
        verbose_name='反馈内容',
    )
    contact_email = models.EmailField(
        max_length=254,
        verbose_name='反馈人联系方式',
    )
    feedback_time = models.DateTimeField(
        verbose_name='反馈日期',
        auto_now_add=True
    )

    def __unicode__(self):
        return self.contact_email

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '用户反馈信息'
        verbose_name_plural = verbose_name
