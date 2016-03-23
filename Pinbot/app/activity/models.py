# coding: utf-8

from django.db import models
from django.contrib.auth.models import User


class EasterEgg(models.Model):

    EGG_TYPE_META = (
        (1, '调侃'),
        (2, '实物奖品'),
    )

    name = models.CharField(
        max_length=20,
        verbose_name='礼物名字',
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )
    amount = models.PositiveIntegerField(
        verbose_name='数量',
    )
    is_active = models.BooleanField(
        blank=True,
        default=True,
        verbose_name='是否生效',
    )
    egg_type = models.IntegerField(
        choices=EGG_TYPE_META,
        verbose_name='奖品类型',
    )
    price = models.FloatField(
        default=0,
        blank=True,
        verbose_name='中奖金额'
    )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '彩蛋列表'
        verbose_name_plural = verbose_name


class EggRecord(models.Model):

    CLAIM_META = (
        (1, '未领奖'),
        (2, '已领奖'),
        (3, '不予奖励'),
    )

    user = models.ForeignKey(
        User,
        related_name='egg_records',
        verbose_name='用户'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='中奖时间',
        db_index=True,
    )
    egg = models.ForeignKey(
        'EasterEgg',
        related_name='egg_records',
        verbose_name='奖品',
    )
    claim_status = models.IntegerField(
        choices=CLAIM_META,
        default=1,
        verbose_name='领奖状态',
    )
    claim_time = models.DateTimeField(
        auto_now=True,
        verbose_name='领奖时间',
    )
    user_need = models.BooleanField(
        default=False,
        verbose_name='用户认领'
    )

    def __unicode__(self):
        return '{0}'.format(self.egg_id)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '获奖记录'
        verbose_name_plural = verbose_name


class CloseEasterRecord(models.Model):

    username = models.CharField(
        max_length=80,
        verbose_name='用户名',
    )
    close_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='关闭时间',
    )

    class Meta:
        verbose_name = '关闭记录'
        verbose_name_plural = verbose_name


class Questionnaire(models.Model):

    ANWSER_TYPE_META = (
        ('single_choies', '单选类型'),
        ('multi_choies', '复选类型'),
        ('single_choies_or_text', '单选或文本类型'),
        ('multi_choies_or_text', '复选或文本类型'),
        ('address', '地址'),
        ('short_text', '短文本'),
        ('long_text', '长文本'),
    )
    QUESTION_TYPE_META = (
        ('user_info', '用户基本信息'),
        ('company_info', '公司基本信息'),
        ('about_pinbot', '关于聘宝'),
    )

    order = models.IntegerField(
        default=1,
        verbose_name='问题排序权重'
    )
    question_type = models.CharField(
        choices=QUESTION_TYPE_META,
        max_length=40,
        verbose_name='问题类型'
    )
    anwser_type = models.CharField(
        choices=ANWSER_TYPE_META,
        max_length=40,
        verbose_name='答案类型'
    )
    is_active = models.BooleanField(
        verbose_name='是否应用'
    )
    question = models.CharField(
        max_length=100,
        verbose_name='问题'
    )
    anwser_options = models.CharField(
        default="",
        blank=True,
        max_length=300,
        verbose_name='答案选项'
    )

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '问卷问题'
        verbose_name_plural = verbose_name


class QuestionnaireResult(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='投票用户',
        related_name='questionnaire_page'
    )
    submit_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='提交日期'
    )

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '投票结果'
        verbose_name_plural = verbose_name


class QuestionnaireAnwserResult(models.Model):

    question = models.ForeignKey(
        Questionnaire,
        verbose_name='问题',
        related_name='anwser_result'
    )
    anwser = models.CharField(
        max_length=300,
        verbose_name='答案'
    )
    questionnaire_page = models.ForeignKey(
        QuestionnaireResult,
        verbose_name='所属问卷',
        related_name='question_anwser_results'
    )

    def __unicode__(self):
        return '{question}:{anwser}'.format(
            question=self.question.question,
            anwser=self.anwser
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '问题提交答案'
        verbose_name_plural = verbose_name
