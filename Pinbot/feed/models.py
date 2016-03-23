# coding:utf-8
'''
Created on 2013-11-25

@author: dell
'''

import jieba
from datetime import datetime

from basic_service.judge_unicode import (
    uniform,
    is_other,
    is_num_word,
    get_ordered_unique,
)

from django.db.models import *
from django.db import models
from django.contrib.auth.models import User
from resumes.models import ResumeData
from transaction.models import *
import mongoengine
from mongoengine import Document, ReferenceField, ListField, IntField, EmbeddedDocument, EmbeddedDocumentField, ObjectIdField

from pin_utils.django_utils import after7day, get_tomommow


class Feed(Model):
    """
    @summary: 所有订阅内容

    @change: likaiguo.happy@163.com 2014-6-15 18:43:18 加入外键,映射Feed所对应使用的套餐
    """
    FEED_META = (
        (1, '用户购买'),
        (2, '聘宝生成'),
    )
    DEGREE_CHOICES = (
        (0, u'不限'),
        (3, u'大专'),
        (4, u'本科'),
        (7, u'硕士'),
        (10, u'博士'),
    )

    feed_obj_id = CharField(
        default='',
        max_length=100,
        verbose_name=u'在mongo中的id',
        db_index=True,
    )
    keywords = CharField(default='', max_length=350, verbose_name=u'关键字')
    job_type = CharField(default='', max_length=100, verbose_name=u'职位类型')
    talent_level = CharField(default='', max_length=100, verbose_name=u'人才级别')
    expect_area = CharField(default='', max_length=100, verbose_name=u'期望工作地')
    job_desc = CharField(default='', max_length=5000, verbose_name=u'职位描述')

    deleted = BooleanField(default=False, verbose_name=u'删除状态')
    delete_time = DateTimeField(
        verbose_name=u'删除时间',
        auto_now_add=True,
    )
    add_time = DateTimeField(
        verbose_name=u'添加时间',
        auto_now_add=True,
    )
    expire_time = DateTimeField(
        null=True,
        blank=True,
        verbose_name='套餐到期'
    )

    username = CharField(default='', max_length=100)
    user = ForeignKey(User, verbose_name=u'用户')
    # 最新增加对于每个订阅职位的理解,更好辅助算法.
    ignored = BooleanField(default=False)  # 忽略用户输入关键词
    last_click_time = DateTimeField(
        verbose_name=u'最后点击',
        auto_now_add=True,
    )
    feed_expire_time = DateTimeField(
        verbose_name=u'刷新到',
        default=after7day(),
        db_index=True,
    )
    feed_type = IntegerField(
        verbose_name='定制来源',
        choices=FEED_META,
        default=1,
    )
    title = models.CharField(
        max_length=100,
        verbose_name='职位名称',
        default='',
    )
    salary_min = models.IntegerField(
        default=0,
        verbose_name='最低薪资',
    )
    salary_max = models.IntegerField(
        default=0,
        verbose_name='最高工资',
    )
    work_years_min = models.IntegerField(
        default=0,
        verbose_name='最低工作年限',
    )
    work_years_max = models.IntegerField(
        default=0,
        verbose_name='最高工作年限',
    )
    type = models.CharField(
        max_length=30,
        default='',
        verbose_name='工作性质',
    )
    category = models.CharField(
        max_length=30,
        default='',
        verbose_name='职位类别',
    )
    degree = models.IntegerField(
        choices=DEGREE_CHOICES,
        default=0,
        verbose_name=u'最低学历'
    )
    key_points = models.CharField(
        default='',
        max_length=1000,
        verbose_name=u'职位诱惑',
    )
    skill_required = models.CharField(
        default='',
        max_length=1000,
        verbose_name=u'岗位要求',
    )
    company = models.ForeignKey(
        'jobs.Company',
        verbose_name=u'公司',
        null=True,
        blank=True,
    )
    recruit_num = models.IntegerField(
        default=0,
        verbose_name=u'招聘人数'
    )
    job_tag = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'标签',
    )
    report_to = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'汇报对象'
    )
    department_to = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'所属部门',
    )
    language = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'语言要求',
    )
    gender = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'性别要求',
    )
    major = models.CharField(
        default='',
        max_length=100,
        verbose_name=u'专业要求',
    )
    display = models.BooleanField(
        default=True,
        verbose_name=u'是否展示',
    )
    job_url = models.CharField(
        default='',
        max_length=200,
        verbose_name=u'职位地址',
    )
    job_domain = models.ManyToManyField(
        'jobs.CompanyCategory',
        verbose_name='类别',
        null=True,
        blank=True,
    )
    is_related = models.BooleanField(
        default=True,
        verbose_name='是否相关',
    )
    job_welfare = models.CharField(
        default='',
        max_length=200,
        verbose_name='职位诱惑',
    )
    company_prefer = models.ManyToManyField(
        'system.CompanyCategoryPrefer',
        verbose_name='职位偏好',
        null=True,
        blank=True,
    )
    update_time = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name='更新时间',
    )
    analyze_titles = models.CharField(
        default='',
        max_length=350,
        verbose_name='职位扩展名',
        blank=True,
    )

    def __unicode__(self):
        return "%s %s %s %s" % (self.expect_area, self.job_type, self.talent_level, self.keywords)

    def get_salary(self):
        salary_low, salary_high = self.salary_min, self.salary_max
        if salary_low == 0 and salary_high == 0:
            return '面议'
        if salary_low == 0 and salary_high == 1000000:
            return '面议'
        if salary_low > 0 and salary_high == 1000000:
            return '%dK以上' % (salary_low / 1000)
        if salary_low == 0 and salary_high < 1000000:
            return '%dK以下' % (salary_high / 1000)
        return '%dK－%dK' % (salary_low / 1000, salary_high / 1000)

    def fast_find(self):
        fast_url = 'http://pinbot.me:8888/search?kw=%s&addr=%s&jt=%s' % (self.keywords, self.expect_area, self.job_type)
        return mark_safe("<a href='%s' target=%d>%s</a>" % (fast_url, self.id, self.keywords[:6] + '...'))

    fast_find.short_description = '快速查找人才'

    def reco_results(self):
        url = '/statis/feed_result/group/%s?username=%s#/group/%s' % (self.feed_obj_id, self.user.username, self.feed_obj_id)
        return mark_safe("<a href='%s' target=reco_%d>%s</a>" % (url, self.id, u'管理推荐'))

    reco_results.short_description = '推荐结果预览'

    def feed_expire_status(self):
        tomorrow = get_tomommow()
        feed_has_expire = self.feed_expire_time < tomorrow
        return u'是' if feed_has_expire else u'否'
    feed_expire_status.short_description = u'7天到期'

    def show_company_name(self):
        return self.user.first_name
    show_company_name.short_description = u'公司'

    class Meta:
        db_table = 'feed_feed'
        app_label = 'feed'
        verbose_name = u'订阅管理'
        verbose_name_plural = verbose_name
        permissions = (
            ('visit_taocv', '淘CV访问权限'),
            ('visit_feed', '专属定制访问权限'),
        )


class Remark(EmbeddedDocument):
    """
    @summary: 对每个HR的订阅的,人工理解
    """
    necessary_keywords = ListField(StringField(), required=False)  # 必含词
    latent_semantic_keywords = ListField(StringField(), required=False)  # 加分扩展词

    exclude_job_keywords = ListField(StringField(), required=False)  # 屏蔽职位词
    op_time = mongoengine.DateTimeField(default=datetime.now(), required=False)  # 操作时间
    username = StringField()  # 管理员


class EmailSendInfo(Document):
    user = mongoengine.IntField()  #
    username = mongoengine.StringField()
    sendFrequency = mongoengine.IntField(default=1)  # 邮件发送频率
    lastSendDate = mongoengine.DateTimeField(default=datetime.now())  # 上一次发送的时间
    send_status = mongoengine.StringField()

    meta = {
        'collection': 'email_send_info',
        'indexes': [
            'username',
        ]
    }


class Feed2(Document):
    """
    @summary: 所有订阅内容
    """
    keywords = StringField(default='')
    job_type = StringField(default='')  # 工作类型
    talent_level = StringField(default='')  # 人才级别
    expect_area = StringField(default='')  # 期望工作地
    job_desc = StringField(default='')  # 职位描述

    deleted = mongoengine.BooleanField(default=False)
    add_time = mongoengine.DateTimeField(default=datetime.now())
    delete_time = mongoengine.DateTimeField(default=datetime.now())
    expire_time = mongoengine.DateTimeField(required=False)
    calced = mongoengine.BooleanField(
        default=False,
    )

    username = StringField(default='')
    # 最新增加对于每个订阅职位的理解,更好辅助算法.
    remarks = ListField(EmbeddedDocumentField(Remark), default=[], required=False)
    ignored = mongoengine.BooleanField(default=False)  # 忽略用户输入关键词
    last_click_time = mongoengine.DateTimeField(default=datetime.now())
    feed_expire_time = mongoengine.DateTimeField(default=after7day())
    feed_type = mongoengine.IntField(default=1)

    title = mongoengine.StringField(
        default='',
    )
    salary_min = mongoengine.IntField(
        default=0,
    )
    salary_max = mongoengine.IntField(
        default=0,
    )
    work_years_min = mongoengine.IntField(
        default=0,
    )
    work_years_max = mongoengine.IntField(
        default=0,
    )
    type = mongoengine.StringField(
        default='',
    )
    category = mongoengine.StringField(
        default='',
    )
    degree = mongoengine.IntField(
        default=0,
    )
    key_points = mongoengine.StringField(
        default='',
    )
    skill_required = mongoengine.StringField(
        default='',
    )
    recruit_num = mongoengine.IntField(
        default=0,
    )
    job_tag = mongoengine.StringField(
        default='',
    )
    report_to = mongoengine.StringField(
        default='',
    )
    department_to = mongoengine.StringField(
        default='',
    )
    language = mongoengine.StringField(
        default='',
    )
    gender = mongoengine.StringField(
        default='',
    )
    major = mongoengine.StringField(
        default='',
    )
    display = mongoengine.BooleanField(
        default=True,
    )
    job_url = mongoengine.StringField(
        default='',
    )
    is_related = mongoengine.BooleanField(
        default=True,
    )
    job_domain = mongoengine.ListField(StringField())
    job_welfare = mongoengine.ListField(StringField())
    company_prefer = mongoengine.ListField(StringField())
    update_time = mongoengine.DateTimeField(
        default=datetime.now(),
        required=False,
    )
    analyze_titles = mongoengine.StringField(
        default='',
    )

    meta = {
        'collection': 'feed',
        'index_background': True,
        'indexes': [
            'job_type',
            'feed_type',
            'talent_level',
            '-add_time',
            '-expect_area',
            '-username',
            '-delete_time',
            '-expire_time',
            '-last_click_time',
            '-feed_expire_time',
        ]
    }

    def __unicode__(self):
        return self.username

    class Meta:
        app_label = 'Feed'

    def get_keywords_area(self):
        return self.keywords.lower() + self.expect_area.lower()

    def get_area_list(self):
        return self.expect_area.split(',')

    def get_uniform_keywords(self):
        return uniform(self.keywords)

    def get_remarks_keywords_list(self):
        """
        @summary: 由于对每个订阅进行了人工备注,需要将其转换为,server计算时的格式.
        @author: likaiguo.happy@163.com 2014-2-17 10:06:28

        """
        return [list(jieba.cut("".join(remark.get_necessary_keywords()))) for remark in self.remarks]

    def get_exclude_job_words(self):
        """
        @summary: 获取需要屏蔽的职位词
        """
        exclude_job_words = []

        for remark in self.remarks:
            exclude_job_words.extend(remark.get_exclude_job_keywords())
        return exclude_job_words

    def get_latent_semantic_keywords(self):
        """
        @summary: 获取需要加分加权重的词
        """
        latent_semantic_keywords = []

        for remark in self.remarks:
            latent_semantic_keywords.extend(remark.get_latent_semantic_keywords())
        return latent_semantic_keywords

    def get_clean_keywords_list(self, unique=True):
        """
        @summary: 获取规则化的关键词列表,  由于用户输入关键词可能含有中文标点等情况.
        #统一为半角,小写,用户输入关键词按照1.自然分词  2.用户本身的输入间隔进行
        #返回这两种分割非重复的关键词列表.

        """
        uniform_keywords = uniform(self.keywords)
#         uniform_keywords = replace_punctuation(uniform_keywords)
        seg_keywords = jieba.cut(uniform_keywords)

        seg_keywords = [ keyword.lower() for keyword in seg_keywords if not is_other(keyword) ]

        user_seg_keywords = uniform_keywords.split()

        user_seg_keywords = [ keyword.lower() for keyword in user_seg_keywords if not is_other(keyword)]

        if unique:
            seg_keywords = get_ordered_unique(seg_keywords)
            user_seg_keywords = get_ordered_unique(user_seg_keywords)

        if seg_keywords == user_seg_keywords:
            return [seg_keywords]
        else:
            return [seg_keywords, user_seg_keywords]

    def get_all_eng_words(self, unique=True):
        """
        @summary: 获取关键词和职位描述中的所有单词或者单词+数字类型 ,如cocos2d
        """
        desc = uniform(self.keywords + ' ' + self.job_desc)

        words = jieba.cut(desc)

        eng_words = [word for word in words if is_num_word(word)]
        if unique:
            eng_words = get_ordered_unique(eng_words)
        return eng_words

    def get_user_remark_keywords(self):
        """
        @summary: 获取用户填的和人工备注的关键词.

        """

        keywords_list = []
        if not self.ignored:
            clean_keywords_list = self.get_clean_keywords_list()
            keywords_list.extend(clean_keywords_list)
        remark_keywords_list = self.get_remarks_keywords_list()
        if remark_keywords_list != [[]]:
            keywords_list.extend(remark_keywords_list)

        return keywords_list


class FeedRemark(Model):
    feed = ForeignKey(Feed, verbose_name=u'订阅')  # 订阅
    keywords_type = CharField(max_length=100, verbose_name=u'类型')  # must表示必填词，extends表示加分词,shield表示屏蔽词，
    keywords = CharField(max_length=100, verbose_name=u'关键词')
    add_user = ForeignKey(User, verbose_name=u'添加用户')  # 添加用户
    add_time = DateTimeField()


class UserReadResume(Model):
    user = ForeignKey(User, verbose_name=u'用户', null=True, blank=True)  # 添加用户
    source_type = IntegerField(default=1, null=True, blank=True)  # 1表示订阅简历已读，2表示来源于淘cv
    feed_id = CharField(max_length=100, null=True, blank=True)
    resume_id = CharField(max_length=100, null=True, blank=True)
    access_time = DateTimeField()


class UserFeed(Model):
    user = ForeignKey(
        User,
        verbose_name=u'用户',
    )
    feed = ForeignKey(
        Feed,
        verbose_name=u'订阅',
    )
    user_charge_pkg = ForeignKey(
        UserChargePackage,
        verbose_name=u'使用套餐',
        null=True,
        blank=True
    )
    is_deleted = BooleanField(
        default=False,
        verbose_name=u'是否删除'
    )
    delete_time = DateTimeField(
        default=datetime.now(),
        verbose_name=u'删除时间'
    )
    add_time = DateTimeField(
        verbose_name=u'添加时间',
        auto_now_add=True,
    )
    expire_time = DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'过期时间',
    )

    class Meta:
        verbose_name = u'用户订阅'
        verbose_name_plural = verbose_name


class UserFeed2(Document):
    """
    @summary: 用户与订阅之间的映射关系
    """

    username = StringField(default='')
    feed = ReferenceField(Feed2, reverse_delete_rule=DO_NOTHING)

    is_deleted = mongoengine.BooleanField(default=False)  # 是否被删除

    add_time = mongoengine.DateTimeField(default=datetime.now())
    delete_time = mongoengine.DateTimeField(default=datetime.now())
    expire_time = mongoengine.DateTimeField(required=False)
    read_id_list = ListField(default=[])  # 已读简历id列表

    read_count = IntField(default=0)  # 读过简历数量

    meta = {
            'collection':'user_feed',
            'indexes':[
                'feed',
                'username',
                'is_deleted',
                '-add_time',
                ]

            }


class Tags(EmbeddedDocument):
    """
    @summary:
    语义理解和自定义标注

    @param:
    domains 相关领域,行业(互联网,游戏,移动互联网)
    company_type 公司偏好
    school_type 985 211 海外 世界名校 中国顶尖
    foreign_language 留学或海外经历,或者特种语言,(英语4级以上，精通韩语)
    major_related 相关专业(计算机,新闻学、传播学、市场营销广告学及市场营销)
    keywords 关键词
    degree_related 学历相关,(本科以上学历,专科以上学历)
    """
    domains = ListField(required=False, verbose_name='行业')
    company_type = ListField(required=False, verbose_name='公司类别')
    school_type = ListField(required=False, verbose_name='学校类别')
    foreign_language = ListField(required=False, verbose_name='语言要求')
    major_related = ListField(required=False, verbose_name='专业要求')
    keywords = ListField(required=False, verbose_name='关键词')
    degree_related = ListField(required=False, verbose_name='学历要求')


class FeedResult(Document):
    """
    @summary: 订阅结果
    """
    RECO_FEEDBACK = (
        ('title_match', '职位名称匹配'),
        ('title_not_match', '职位名称不匹配'),
        ('degree_low', '学历偏低'),
        ('degree_high', '学历偏高'),
        ('salary_low', '薪资偏低'),
        ('salary_high', '薪资偏高'),
        ('level_low', '级别偏低'),
        ('level_high', '级别偏高'),
        ('industry_not_match', '行业不匹配'),
    )

    feed = ReferenceField(Feed2, reverse_delete_rule=DO_NOTHING)  # 所属的订阅
    resume = ReferenceField(ResumeData, reverse_delete_rule=DO_NOTHING)  # 计算过的简历
    resume_score = StringField(default='')  # 该简历的这个关键词的得分
    is_recommended = mongoengine.BooleanField(default=False)  # 是否推荐该简历
    calc_time = mongoengine.DateTimeField(default=datetime.now())  # 该订阅计算时间
    resume_update_time = mongoengine.DateTimeField(default=datetime.now())  # 改简历更新时间
    resume_grab_time = mongoengine.DateTimeField(default=datetime.now())  # 改简历的抓取时间
    pub_time = mongoengine.DateTimeField(default=datetime.now())  # 简历发布时间

    cos = mongoengine.FloatField(default=0.0)  # 订阅职位描述和简历之间的余弦值
    reco_index = mongoengine.FloatField(default=0.0)  # 简历推荐指数
    job_related = mongoengine.IntField(default=0)  # 职位相关度
    algorithm = StringField(default='')
    talent_level = StringField(default='')  # 人才级别
    is_manual = mongoengine.BooleanField(default=False)
    manual_ensure_time = mongoengine.DateTimeField()  # 人工确认时间,也就是发布时间
    published = mongoengine.BooleanField()  # 人工确认该数据是否推送给用户

    admin = StringField(default='')  # 系统管理员才操作记录,积重难返了,这个字段表示操作的人的名称
    is_staff = IntegerField(default=1)  # 表示操作的账号是否为管理员账号
    user_read_status = StringField(default='unread')  # 用户阅读状态
    admin_read_status = StringField(default='unread')  # 管理员阅读状态
    user_read_time = mongoengine.DateTimeField(required=False)
    user_feedback_time = mongoengine.DateTimeField(required=False)
    display_time = mongoengine.DateTimeField(required=False)  # 简历显示时间
    feed_source = StringField(default='')
    tags = EmbeddedDocumentField(Tags, required=False)
    publisher = StringField(default='')
    resume_source = StringField(default='', required=False)
    sync_partner = mongoengine.BooleanField(default=False)
    # 展示数
    display_count = mongoengine.IntField(default=0)
    # 点击查看简历数
    click_count = IntField(default=0)
    watch = mongoengine.BooleanField(default=False, required=False)
    download = mongoengine.BooleanField(default=False, required=False)
    feedback_list = mongoengine.ListField(
        mongoengine.StringField(choices=RECO_FEEDBACK),
        required=False,
    )
    score = mongoengine.DictField()

    meta = {
        "collection": "feed_result",
        "index_background": True,
        'indexes': [
            'feed',
            'resume',
            '-calc_time',
            '-resume_update_time',
            'job_related',
            '-manual_ensure_time',
            'admin',
            '-display_time',
            '-display_count',
            '-click_count',
            'user_read_time',
        ],
    }


class ManualPushResume(Document):
    """
    @summary: 添加人工干预订阅结果存储
    """

    username = StringField(default='')
    feed = ReferenceField(Feed2, reverse_delete_rule=DO_NOTHING)  # 所属的订阅
    resume = ReferenceField(ResumeData, reverse_delete_rule=DO_NOTHING)  # 计算过的简历
    url = StringField()  # 简历url
    reco_index = mongoengine.FloatField(default=0.0)  # 简历推荐指数，不推荐时 0，非常推荐 1
    op_time = mongoengine.DateTimeField(default=datetime.now())  # 操作时间
    has_collected = mongoengine.BooleanField(default=True)  # 在简历添加的时候是否已经被添加到pinbot库中

from mongoengine import DateTimeField
class  SearchResult(Document):
    """
    @summary: 记录各个平台的搜索结果信息

    """

    feed_id = ObjectIdField()  # 该订阅在pinbot的id
    search_time = DateTimeField()  # 该订阅搜索时间
    resume_urls = ListField()  # 对应于的平台的url列表
    resume_id_list = ListField(ObjectIdField())  # 对应于pinbot平台的id列表
    plantform = StringField()  # 对应于的平台
    keywords_str = StringField()  # 提交的关键词字符串
    related_num = IntField()  # 对应的搜索结果总量
    new_count = IntField()  # 对应于Pinbot平台的简历新增数量
    area_list = ListField(StringField())


class LogFeedQuery(Document):
    username = mongoengine.StringField(default='', required=True)
    resume_list = ListField(mongoengine.StringField(), required=False) # 本次请求返回的resumeid列表
    total_num = IntField(default=0, required=False)
    feed_id = mongoengine.StringField(default='', required=True)
    access_time = DateTimeField(default=datetime.now())


class PubFeedData(Document):

    email = StringField()
    pub_admin = StringField()
    feed = ReferenceField(Feed2, reverse_delete_rule=DO_NOTHING)
    resumes = ListField(ReferenceField(ResumeData))
    pub_time = mongoengine.DateTimeField()
    display_time = mongoengine.DateTimeField(required=False)

    meta = {
        "indexes": [
            'feed',
            'email',
            'pub_admin',
            'pub_time',
        ]
    }


class EmailFeedData(Document):
    email = StringField()
    pub_admin = StringField()
    feed = ReferenceField(Feed2, reverse_delete_rule=DO_NOTHING)
    resumes = ListField(ReferenceField(ResumeData))
    is_send = mongoengine.BooleanField(default=False)

    meta = {
        "indexes": [
            'feed',
            'email',
            'pub_admin',
        ]
    }
