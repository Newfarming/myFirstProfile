# coding: utf-8

from django.db import models


class City(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='名称',
    )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name


class CompanyCategory(models.Model):
    category = models.CharField(
        max_length=30,
        verbose_name='公司类别',
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )

    def __unicode__(self):
        return self.category

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '公司类别'
        verbose_name_plural = verbose_name


class PositionCategory(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='职位类别'
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '职位类别'
        verbose_name_plural = verbose_name


class PositionCategoryTag(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='类别标签',
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )
    category = models.ForeignKey(
        PositionCategory,
        verbose_name='职位类别',
        related_name='category_tags',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='父级标签',
        related_name='child_tags',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __unicode__(self):
        return '%s' % (self.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '职位标签'
        verbose_name_plural = verbose_name


class CompanyCategoryPrefer(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='偏好',
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )
    sort = models.IntegerField(
        default=0,
        verbose_name='排序',
        db_index=True,
    )
    display = models.BooleanField(
        default=True,
        verbose_name='是否展示',
    )

    def __unicode__(self):
        return '%s' % (self.name)

    def __str__(self):
        return self.__unicode__(self)

    class Meta:
        verbose_name = '公司偏好'
        verbose_name_plural = verbose_name


class CompanyWelfare(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='职位诱惑',
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )
    sort = models.IntegerField(
        default=0,
        verbose_name='排序',
        db_index=True,
    )
    display = models.BooleanField(
        default=True,
        verbose_name='是否展示',
    )

    def __unicode__(self):
        return '%s' % (self.name)

    def __str__(self):
        return self.__unicode__(self)

    class Meta:
        verbose_name = '职位诱惑'
        verbose_name_plural = verbose_name


class ResumeMarkSetting(models.Model):

    CLASSIFY_META = (
        (0, '面试阶段'),
        (1, '入职阶段'),
        (2, '约面不成功'),
        (3, '面试不通过'),
        (4, '入职遇到问题'),
        (5, '举报'),
    )

    name = models.CharField(
        max_length=20,
        verbose_name='状态名',
    )
    code_name = models.CharField(
        max_length=30,
        verbose_name='代码别名',
    )
    desc = models.CharField(
        max_length=50,
        verbose_name='描述',
    )
    display = models.BooleanField(
        default=True,
        verbose_name='是否展示',
    )
    end_status = models.BooleanField(
        default=False,
        verbose_name='完结状态',
    )
    change = models.BooleanField(
        default=True,
        verbose_name='可以修改',
    )
    good_result = models.BooleanField(
        default=True,
        verbose_name='进展顺利',
    )
    classify = models.IntegerField(
        default=0,
        choices=CLASSIFY_META,
        verbose_name='分类',
    )
    has_interview = models.BooleanField(
        default=True,
        verbose_name='已经面试',
    )
    is_accu = models.BooleanField(
        default=False,
        verbose_name='举报状态',
    )
    is_taking_work = models.BooleanField(
        default=False,
        verbose_name='已经入职',
    )
    sort = models.IntegerField(
        default=0,
        verbose_name='排序',
    )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '标记选项配置'
        verbose_name_plural = verbose_name


class ResumeMarkRelation(models.Model):

    parent = models.ForeignKey(
        ResumeMarkSetting,
        related_name='main_marks',
        verbose_name='一级选项',
        null=True,
        blank=True,
    )
    mark = models.ForeignKey(
        ResumeMarkSetting,
        related_name='mark_relation',
        verbose_name='选项'
    )

    def __unicode__(self):
        return '%s, %s' % (self.parent, self.mark.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'标记关系配置'
        verbose_name_plural = verbose_name
