# coding: utf-8

from django.db import models
from django.contrib.auth.models import (
    User,
)
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from Common.models import (
    AbstractResume,
    AbstractWorkExperience,
    AbstractProject,
    AbstractEducation,
    AbstractProfessionalSkill,
)

from feed.models import (
    Feed,
)
from jobs.models import (
    CompanyCategory,
)

from Brick.App.system.models import (
    City,
)

RECORD_TYPE_META = (
    ('check', '查看'),
    ('download', '下载'),
    ('interview', '面试'),
    ('taking_work', '入职'),
    ('accusation', '举报'),
    ('extra_download', '下载额外'),
    ('extra_interview', '面试额外'),
    ('extra_taking_work', '入职额外'),
)


class UploadTaskSetting(models.Model):

    TASK_TIME_META = (
        (0, '不限时间'),
        (1, '休息时间'),
    )
    user = models.OneToOneField(
        User,
        verbose_name='用户',
        related_name='task_setting',
    )
    title = models.CharField(
        max_length=100,
        verbose_name='擅长的职位',
        blank=True,
    )
    job_domains = models.ManyToManyField(
        CompanyCategory,
        verbose_name='擅长的领域',
        null=True,
        blank=True,
    )
    citys = models.ManyToManyField(
        City,
        verbose_name='所在城市',
        null=True,
        blank=True,
    )
    task_time = models.IntegerField(
        default=0,
        choices=TASK_TIME_META,
    )

    def __unicode__(self):
        return '%s设置' % self.user.username

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '用户偏好设置'
        verbose_name_plural = verbose_name


class UploadResume(AbstractResume):

    CONTACT_META = (
        (0, '未知'),
        (1, '一周'),
        (2, '一个月'),
        (3, '3个月'),
    )
    expect_work_place = models.CharField(
        max_length=30,
        default='',
        blank=True,
        verbose_name='期望工作地',
    )
    expect_position = models.CharField(
        max_length=80,
        default='',
        blank=True,
        verbose_name='期望职位',
    )
    last_contact = models.IntegerField(
        choices=CONTACT_META,
        default=0,
        blank=True,
        verbose_name='最近联系',
    )
    hr_evaluate = models.CharField(
        max_length=500,
        default='',
        blank=True,
        verbose_name='HR评价',
    )

    def display_resume(self):
        ui = '''
        <a href="/resumes/display/%s/" target="_blank">查看简历</a>
        ''' % self.resume_id
        return mark_safe(ui)

    display_resume.short_description = '查看'

    class Meta:
        verbose_name = '简历信息'
        verbose_name_plural = verbose_name


class ResumeWork(AbstractWorkExperience):

    resume = models.ForeignKey(
        UploadResume,
        related_name='resume_works',
        verbose_name='简历',
    )

    class Meta:
        verbose_name = '工作经历'
        verbose_name_plural = verbose_name


class ResumeProject(AbstractProject):
    resume = models.ForeignKey(
        UploadResume,
        related_name='resume_projects',
        verbose_name='简历',
    )

    class Meta:
        verbose_name = '项目经历'
        verbose_name_plural = verbose_name


class ResumeEducation(AbstractEducation):
    resume = models.ForeignKey(
        UploadResume,
        related_name='resume_educations',
        verbose_name='简历',
    )

    class Meta:
        verbose_name = '教育经历'
        verbose_name_plural = verbose_name


class ResumeSkill(AbstractProfessionalSkill):
    resume = models.ForeignKey(
        UploadResume,
        related_name='resume_skills',
        verbose_name='简历',
    )

    class Meta:
        verbose_name = '技能经历'
        verbose_name_plural = verbose_name


class AbstractRecoTask(models.Model):
    ACTION_META = (
        (0, '推荐'),
        (1, '接受'),
    )

    feed = models.ForeignKey(
        Feed,
        verbose_name='定制',
    )
    reco_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='推荐时间',
        db_index=True,
    )
    action = models.IntegerField(
        default=0,
        choices=ACTION_META,
        verbose_name='状态',
    )
    action_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='操作时间',
    )
    display = models.BooleanField(
        default=True,
        verbose_name='是否展示',
    )
    reco_index = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name='推荐度',
    )
    user = models.ForeignKey(
        User,
        verbose_name='推荐用户'
    )

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.__str__()

    class Meta:
        abstract = True


class UserAcceptTask(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='互助伙伴',
    )
    feed = models.ForeignKey(
        Feed,
        verbose_name='定制',
    )
    accept_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='接受时间',
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        db_index=True,
    )
    task_id = models.CharField(
        max_length=30,
        verbose_name='任务ID',
        db_index=True,
    )
    has_hr_info = models.BooleanField(
        default=False,
        verbose_name='获取HR信息',
    )

    def __str__(self):
        return self.feed.title

    def __unicode__(self):
        return self.__str__()

    class Meta:
        unique_together = (
            ('user', 'feed'),
        )
        verbose_name = '任务信息'
        verbose_name_plural = verbose_name


class UserTaskResume(models.Model):

    RESUME_STATUS_META = (
        (0, '已推荐'),
        (1, '已被查看'),
        (2, '已被下载'),
        (3, '进入面试'),
        (4, '已入职'),
        (5, '被举报'),
    )

    task = models.ForeignKey(
        UserAcceptTask,
        verbose_name='上传任务',
        related_name='task_resumes',
    )

    resume = models.ForeignKey(
        UploadResume,
        verbose_name='上传简历',
        related_name='resume_tasks',
    )

    upload_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='上传时间',
    )

    resume_status = models.IntegerField(
        default=0,
        choices=RESUME_STATUS_META,
        verbose_name='简历状态',
    )
    accusation_reason = models.CharField(
        default='',
        max_length=200,
        verbose_name='举报理由',
    )

    verify = models.BooleanField(
        default=False,
        verbose_name='已标记入职',
    )

    extra_grant = models.BooleanField(
        default=False,
        verbose_name='需要额外奖励',
    )

    def hr(self):
        return self.task.feed.user

    hr.short_description = 'HR'

    def task_user(self):
        return self.task.user

    task_user.short_description = '互助伙伴'

    def resume_update_time(self):
        return self.resume.update_time

    resume_update_time.short_description = '简历更新时间'

    def display_resume(self):
        ui = '''
        <a href="/resumes/display/%s/?feed_id=%s" target="_blank">查看简历</a>
        ''' % (self.resume.resume_id, self.task.feed.feed_obj_id)
        return mark_safe(ui)

    display_resume.short_description = '简历'

    def grant_coin(self):
        coin = sum(i.coin for i in list(self.resume.resume_coin_records.all()) if i.task_id == self.task_id)
        return coin

    grant_coin.short_description = '获得金币'

    def operation(self):
        if not self.verify:
            return ''
        interface = '''
        <div class="btn-group pull-right">
        <a class="editable-handler" title="" data-editable-field="pay_status" data-editable-loadurl="%s" data-original-title="奖励"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">奖励金币</span>
         ''' % reverse('partner-grant-form', args=(self.id, ))

        return mark_safe(interface)

    operation.short_description = '操作'

    def extra_operation(self):
        if not self.extra_grant:
            return ''

        from .partner_utils import PartnerLevelUtils
        user = self.task.user
        level_utils = PartnerLevelUtils(user)
        taking_work_level = level_utils.get_taking_work_level()

        if taking_work_level['level'] <= 1:
            return ''

        interface = '''
        <div class="btn-group pull-right">
        <a class="editable-handler" title="" data-editable-field="pay_status" data-editable-loadurl="%s" data-original-title="奖励"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">额外奖励金币(%s级)</span>
         ''' % (
            reverse('partner-extra-grant-form', args=(self.id, )),
            taking_work_level['level']
        )
        return mark_safe(interface)

    extra_operation.short_description = '额外奖励'

    class Meta:
        unique_together = (
            ('task', 'resume'),
        )
        verbose_name = '任务认领信息'
        verbose_name_plural = verbose_name


class RecoResumeTask(AbstractRecoTask):

    upload_resume = models.ForeignKey(
        UploadResume,
        verbose_name='上传简历',
        related_name='reco_resume_tasks',
    )

    def display_resume(self):
        ui = '''
        <a href="/resumes/display/%s/?feed_id=%s" target="_blank">查看简历</a>
        ''' % (self.upload_resume.resume_id, self.feed.feed_obj_id)
        return mark_safe(ui)

    display_resume.short_description = '查看简历'

    class Meta:
        verbose_name = '简历推荐任务'
        verbose_name_plural = verbose_name


class TaskCoinRecord(models.Model):

    task = models.ForeignKey(
        UserAcceptTask,
        verbose_name='任务',
        related_name='task_coin_records',
    )
    upload_resume = models.ForeignKey(
        UploadResume,
        verbose_name='上传简历',
        related_name='resume_coin_records',
    )
    coin = models.FloatField(
        verbose_name='金币',
    )
    desc = models.CharField(
        max_length=100,
        verbose_name='描述',
    )
    record_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='记录时间',
    )
    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPE_META,
        verbose_name='记录类型',
    )

    def __str__(self):
        return '%s' % self.record_type

    def __unicode__(self):
        return self.__str__()

    def show_hr(self):
        return self.task.feed.user.username

    show_hr.short_description = 'hr'

    def show_user(self):
        return self.task.user.username

    show_user.short_description = '互助伙伴'

    class Meta:
        unique_together = (
            ('task', 'upload_resume', 'record_type'),
        )
        verbose_name = '任务奖励记录'
        verbose_name_plural = verbose_name


class FollowTaskRecord(models.Model):

    FOLLOW_TYPE_META = (
        (1, '发站内信'),
        (2, '获取Hr信息'),
    )

    task_resume = models.ForeignKey(
        UserTaskResume,
        verbose_name='简历任务',
        related_name='follow_records',
    )
    follow_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='跟进时间',
    )
    follow_type = models.IntegerField(
        choices=FOLLOW_TYPE_META,
        verbose_name='跟进类型',
    )
    desc = models.CharField(
        default='',
        max_length=200,
        verbose_name='发送内容',
    )
    has_check = models.BooleanField(
        default=False,
        verbose_name='已经查看',
    )
    check_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='查看时间',
    )

    def __str__(self):
        return self.task_resume.resume.user.username

    def __unicode__(self):
        return self.__str__()

    def follow_user(self):
        return self.task_resume.task.user

    follow_user.short_description = '互助用户'

    def hr_user(self):
        return self.task_resume.task.feed.user

    hr_user.short_description = 'Hr用户'

    def follow_task(self):
        return self.task_resume.task.feed

    follow_task.short_description = '任务'

    def resume_status(self):
        return dict(UserTaskResume.RESUME_STATUS_META).get(self.task_resume.resume_status)

    resume_status.short_description = '简历状态'

    def display_resume(self):
        ui = '''
        <a href="/resumes/display/%s/?feed_id=%s" target="_blank">查看简历</a>
        ''' % (self.task_resume.resume.resume_id, self.task_resume.task.feed.feed_obj_id)
        return mark_safe(ui)

    display_resume.short_description = '简历'

    class Meta:
        verbose_name = '跟进记录'
        verbose_name_plural = verbose_name


class PartnerLevelManage(models.Model):

    LEVEL_TYPE_META = (
        (0, '下载简历'),
        (1, '面试'),
        (2, '入职'),
    )

    level_type = models.IntegerField(
        choices=LEVEL_TYPE_META,
        verbose_name='等级类型',
    )
    exp = models.IntegerField(
        verbose_name='经验值',
    )
    bonus_coin = models.IntegerField(
        verbose_name='额外奖励',
    )
    level = models.IntegerField(
        verbose_name='等级',
    )
    ratio = models.FloatField(
        default=0,
        verbose_name='比率',
    )
    next_level = models.IntegerField(
        verbose_name='下一等级',
    )
    next_exp = models.IntegerField(
        verbose_name='升级经验值',
    )
    next_ratio = models.FloatField(
        default=0,
        verbose_name='升级比率',
    )
    next_bonus_coin = models.IntegerField(
        verbose_name='升级奖励',
    )
    is_max_level = models.BooleanField(
        default=False,
        verbose_name='最高级别',
    )

    class Meta:
        verbose_name = '等级配置'
        verbose_name_plural = verbose_name


class UserLevelState(models.Model):

    username = models.CharField(
        max_length=60,
        verbose_name='用户',
    )
    check_count = models.IntegerField(
        verbose_name='查看数',
    )
    download_count = models.IntegerField(
        verbose_name='下载数',
    )
    interview_count = models.IntegerField(
        verbose_name='面试数',
    )
    taking_work_count = models.IntegerField(
        verbose_name='入职数',
    )

    def download_ratio(self):
        return round(float(self.download_count) / float(self.check_count), 2) if self.check_count else 0

    download_ratio.short_description = '下载率'

    def interview_ratio(self):
        return round(float(self.interview_count) / float(self.download_count), 2) if self.download_count else 0

    interview_ratio.short_description = '面试率'

    def taking_work_ratio(self):
        return round(float(self.taking_work_count) / float(self.interview_count), 2) if self.interview_count else 0

    taking_work_ratio.short_description = '入职率'

    class Meta:
        managed = False
        db_table = 'partner_user_level_state'
        verbose_name = '用户健康状态'
        verbose_name_plural = verbose_name


class HotTaskSetting(models.Model):

    name = models.CharField(
        max_length=40,
        verbose_name='任务名',
    )

    class Meta:
        verbose_name = '热门任务设置'
        verbose_name_plural = '热门任务设置'
