# coding: utf-8

'''
author: runforever

求职者简历的表设计
'''

import datetime

from django.db import models
from django.contrib.auth.models import User

from Brick.App.system.models import (
    City,
    PositionCategory,
    PositionCategoryTag,
)
from jobs.models import (
    CompanyCategory,
)


class Resume(models.Model):
    '''
    用户简历信息
    '''

    MARRY_STATUS = (
        ('married', '已婚'),
        ('single', '未婚'),
        ('', '未知'),
    )
    DEFAULT_BIRTH = datetime.datetime(1980, 1, 1)
    GENDER_STATUS = (
        ('male', '男'),
        ('female', '女'),
        ('', '未知'),
    )
    DEGREE_META = (
        ('', '未知'),
        ('bachelor', '本科'),
        ('master', '硕士'),
        ('phd', '博士'),
        ('hnd', '大专'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='用户',
    )
    current_salary = models.FloatField(
        verbose_name='目前薪水',
        default=0,
    )
    job_category = models.ForeignKey(
        PositionCategory,
        verbose_name='职位类型',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    job_hunting_state = models.CharField(
        max_length=20,
        verbose_name='求职状态',
        default='',
    )
    target_salary = models.FloatField(
        verbose_name='期望薪水',
        default=0,
    )
    certificate = models.CharField(
        max_length=200,
        verbose_name='认证信息',
        default='',
    )
    qq = models.CharField(
        max_length=20,
        verbose_name='QQ',
        default='',
    )
    name = models.CharField(
        max_length=30,
        verbose_name='名字',
        default='',
    )
    avatar_url = models.CharField(
        max_length=200,
        verbose_name='头像地址',
        default='',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='电话',
        default='',
    )
    email = models.CharField(
        max_length=60,
        verbose_name='邮箱',
        default='',
    )
    age = models.IntegerField(
        default=0,
        verbose_name='年龄',
    )
    school = models.CharField(
        max_length=40,
        verbose_name='学校',
        default='',
    )
    degree = models.CharField(
        max_length=20,
        choices=DEGREE_META,
        verbose_name='学历',
        default='',
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MARRY_STATUS,
        verbose_name='婚姻状况',
        default='',
    )
    major = models.CharField(
        max_length=30,
        verbose_name='专业',
        default='',
    )
    address = models.CharField(
        max_length=80,
        verbose_name='现居地',
        default='',
    )
    residence = models.CharField(
        max_length=60,
        verbose_name='常住地',
        default='',
    )
    work_years = models.IntegerField(
        verbose_name='工作年限',
        default=0,
    )
    birthday = models.DateTimeField(
        verbose_name='生日',
        default=DEFAULT_BIRTH,
    )
    political_landscape = models.CharField(
        max_length=20,
        verbose_name='政治面貌',
        default='',
    )
    identity_id = models.CharField(
        max_length=25,
        verbose_name='身份证号',
        default='',
    )
    gender = models.CharField(
        max_length=15,
        verbose_name='性别',
        default='',
    )
    homepage = models.CharField(
        max_length=200,
        verbose_name='主页',
        default=''
    )
    other_info = models.TextField(
        verbose_name='其他信息',
        default='',
    )
    research_perf = models.CharField(
        max_length=200,
        verbose_name='成就',
        default=''
    )
    hobbies = models.CharField(
        max_length=100,
        verbose_name='爱好',
        default=''
    )
    language_skills = models.CharField(
        max_length=100,
        verbose_name='语言能力',
        default='',
    )
    perf_at_school = models.CharField(
        max_length=200,
        verbose_name='学校奖项',
        default='',
    )
    self_evaluation = models.CharField(
        max_length=400,
        verbose_name='自我评价',
        default='',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
    )
    resume_id = models.CharField(
        max_length=50,
        verbose_name='简历ID',
        default='',
    )
    salary_lowest = models.IntegerField(
        default=0,
        verbose_name='最低薪资',
    )

    def __unicode__(self):
        return u'%s电话%s' % (self.name, self.phone)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '简历'
        verbose_name_plural = verbose_name


class ResumePositionTag(models.Model):
    '''
    简历的职位标签
    '''
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='position_tags',
    )
    position_tag = models.ForeignKey(
        PositionCategoryTag,
        verbose_name='职位标签'
    )

    def __unicode__(self):
        return u'简历%s标签%s' % (
            self.resume.name,
            self.position_tag.name
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '简历标签'
        verbose_name_plural = verbose_name


class ResumeTargetCity(models.Model):
    '''
    简历期望工作城市
    '''
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='expectation_area'
    )
    city = models.ForeignKey(
        City,
        verbose_name='城市',
    )

    def __unicode__(self):
        return u'简历%s期望城市%s' % (
            self.resume.name,
            self.city.name,
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '期望城市'
        verbose_name_plural = verbose_name


class WorkExperience(models.Model):
    '''
    求职者的工作经历
    与简历是一对多的关系（一份简历可以有多个工作经历）
    '''
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='works',
    )
    start_time = models.DateTimeField(
        verbose_name='开始时间',
        blank=True,
        null=True,
    )
    end_time = models.DateTimeField(
        verbose_name='结束时间',
        blank=True,
        null=True,
    )
    position_title = models.CharField(
        max_length=20,
        verbose_name='职称',
        default='',
    )
    duration = models.IntegerField(
        verbose_name='时长',
        default=0,
    )
    min_salary = models.FloatField(
        verbose_name='最低薪水',
        default=0,
    )
    max_salary = models.FloatField(
        verbose_name='最高薪水',
        default=0,
    )
    company_category = models.CharField(
        max_length=30,
        verbose_name='公司类别',
        default='',
    )
    industry_category = models.CharField(
        max_length=20,
        verbose_name='行业性质',
        default='',
    )
    company_name = models.CharField(
        max_length=40,
        verbose_name='公司名字',
        default='',
    )
    job_desc = models.TextField(
        verbose_name='工作描述',
        default='',
    )
    position_category = models.CharField(
        max_length=20,
        verbose_name='职位类别',
        default='',
    )

    def __unicode__(self):
        return '%s%s' % (self.resume.name, self.company_name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'工作经历'
        verbose_name_plural = verbose_name


class Project(models.Model):
    '''
    求职者的项目经历
    与求职者的简历是多对一的关系（一份简历对应多个项目经历）
    '''
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='projects',
    )
    project_desc = models.CharField(
        max_length=500,
        verbose_name='项目描述',
        default='',
    )
    project_name = models.CharField(
        max_length=80,
        verbose_name='项目名称',
        default='',
    )
    job_title = models.CharField(
        max_length=80,
        verbose_name='职位名称',
        default='',
    )
    start_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='开始时间',
    )
    end_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='结束时间',
    )
    responsible_for = models.CharField(
        max_length=300,
        verbose_name='职责',
        default='',
    )
    company_name = models.CharField(
        max_length=80,
        verbose_name='公司名称',
        default='',
    )

    def __unicode__(self):
        return '%s项目经历' % self.resume.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'项目经历'
        verbose_name_plural = verbose_name


class Education(models.Model):
    '''
    求职者的教育经历
    与简历是多对一的关系（一份简历对应多个教育经历）
    '''
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='educations',
    )
    start_time = models.DateTimeField(
        verbose_name='开始时间',
        null=True,
        blank=True,
    )
    end_time = models.DateTimeField(
        verbose_name='结束时间',
        null=True,
        blank=True,
    )
    school = models.CharField(
        max_length=60,
        verbose_name='学校',
        default='',
    )
    degree = models.CharField(
        max_length=20,
        verbose_name='学历',
        default='',
    )
    major = models.CharField(
        max_length=20,
        verbose_name='专业',
        default='',
    )

    def __unicode__(self):
        return '%s%s' % (self.resume.name, self.school)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'教育经历'
        verbose_name_plural = verbose_name


class Training(models.Model):
    '''
    求职者培训经历
    与简历是多对一的关系（一份简历对应多个培训经历）
    '''
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='trainings',
    )
    certificate = models.CharField(
        max_length=60,
        verbose_name='证书',
        default='',
    )
    course = models.CharField(
        max_length=80,
        verbose_name='课程',
        default='',
    )
    start_time = models.DateTimeField(
        verbose_name='开始时间',
    )
    end_time = models.DateTimeField(
        verbose_name='结束时间',
    )
    instituation = models.CharField(
        max_length=60,
        verbose_name='机构',
        default='',
    )
    location = models.CharField(
        max_length=60,
        verbose_name='位置',
        default='',
    )
    train_desc = models.CharField(
        max_length=200,
        verbose_name='培训描述',
        default='',
    )

    def __unicode__(self):
        return '%s%s' % (self.resume.name, self.instituation)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'培训经历'
        verbose_name_plural = verbose_name


class ProfessionalSkill(models.Model):
    '''
    求职者职业技能
    与简历是多对一的关系（一份简历对应多个职业技能）
    '''
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='professional_skills',
    )
    skill_desc = models.CharField(
        max_length=30,
        verbose_name='技能描述',
        default='',
    )
    proficiency = models.CharField(
        max_length=20,
        verbose_name='级别',
        default='',
    )
    month = models.IntegerField(
        verbose_name='使用时间',
        default=0,
    )

    def __unicode__(self):
        return '%s%s' % (self.resume.name, self.skill_desc)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'职业技能'
        verbose_name_plural = verbose_name


class SocialPage(models.Model):
    '''
    用户社交主页
    '''

    resume = models.OneToOneField(
        Resume,
        verbose_name='简历',
        related_name='social_page',
    )
    twitter = models.CharField(
        max_length=80,
        verbose_name='Twitter',
        default='',
    )
    weibo = models.CharField(
        max_length=80,
        verbose_name='Weibo',
        default='',
    )
    zhihu = models.CharField(
        max_length=80,
        verbose_name='Zhihu',
        default='',
    )
    github = models.CharField(
        max_length=80,
        verbose_name='github',
        default='',
    )
    dribbble = models.CharField(
        max_length=80,
        verbose_name='dribbble',
        default='',
    )
    douban = models.CharField(
        max_length=80,
        verbose_name='Douban',
        default='',
    )
    linkedin = models.CharField(
        max_length=80,
        verbose_name='linkedin',
        default='',
    )

    def __unicode__(self):
        return '%s' % (self.resume.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '社交页面'
        verbose_name_plural = verbose_name


class SearchTag(models.Model):
    resume = models.ForeignKey(
        Resume,
        verbose_name='简历',
        related_name='search_tags',
    )
    gender = models.CharField(
        max_length=20,
        verbose_name='性别',
        default='',
    )
    citys = models.CharField(
        max_length=80,
        verbose_name='城市',
        default='',
    )
    category = models.CharField(
        max_length=20,
        verbose_name='类别',
        default='',
    )
    degree = models.CharField(
        max_length=20,
        verbose_name='学历',
        default='',
    )
    tags = models.CharField(
        max_length=200,
        verbose_name='标签',
        default='',
    )
    company_domains = models.CharField(
        max_length=200,
        verbose_name='所在领域',
        default='',
    )
    salary_lowest = models.IntegerField(
        verbose_name='最低薪资',
        default=0,
    )
    work_years = models.CharField(
        max_length=30,
        verbose_name='工作年限',
        default='',
    )
    active = models.BooleanField(
        default=True,
        verbose_name='生效状态',
    )

    def __unicode__(self):
        return '%s,%s' % (self.citys, self.salary_lowest)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '搜索条件'
        verbose_name_plural = verbose_name


class ResumePreferField(models.Model):

    category = models.ForeignKey(
        CompanyCategory,
        related_name='category_prefer_fields'
    )
    resume = models.ForeignKey(
        Resume,
        related_name='prefer_fields'
    )

    def __unicode__(self):
        return u'简历%s偏好领域%s' % (
            self.resume.name,
            self.category.category,
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '偏好领域'
        verbose_name_plural = verbose_name
