# coding: utf-8

from datetime import (
    datetime,
    timedelta,
)

from django.db import models

from django.contrib.auth.models import User


class Task(models.Model):

    REWARD_TYPE = (
        (1, '聘点'),
        (2, '金币'),
        (3, '抵用券'),
        (4, '微信红包'),
        (5, '实物奖励'),
    )

    TASK_LEVEL = (
        (1, '初级任务'),
        (2, '中级任务'),
        (3, '高级任务'),
        (4, '简单重复任务'),
        (5, '复杂重复任务'),
    )

    TASK_CODE = (
        ('is_user_active', 'is_user_active(用户激活)'),
        ('is_user_weixin_bind', 'is_user_weixin_bind(微信绑定)'),
        ('is_user_email_bind', 'is_user_email_bind(邮箱绑定)'),
        ('is_user_company_detail', 'is_user_company_detail(公司详细信息)'),
        ('commit_customization', 'commit_customization(提交定制)'),
        ('lookup_resume', 'lookup_resume(查看简历)'),
        ('collect_resume', 'collect_resume(收藏简历)'),
        ('mark_resume', 'mark_resume(标记简历)'),
        ('download_resume', 'download_resume(下载简历)'),
        ('feedback_resume', 'feedback_resume(反馈)'),
        ('buy_package', 'buy_package(购买套餐)'),

        ('send_company_card', 'send_company_card(发送企业名片)'),
        ('look_up_extention', 'look_up_extention(查看拓展匹配)'),
        ('invite_user', 'invite_user(邀请新用户加入聘宝)'),
        ('mutual_recruitment', 'mutual_recruitment(使用互助招聘)'),
        ('user_portrait', 'user_portrait(用户画像)'),
        ('continue_look_up_resume', 'continue_look_up_resume(连续查看简历)'),
        ('claim_task_weekend', 'claim_task_weekend(周末认领任务)'),
        ('claim_task_weekday', 'claim_task_weekday(工作日认领任务)'),
    )

    COUPON_TYPE = (
        (1, '打折券'),
        (2, '抵用券'),
    )

    TASK_TYPE = (
        (1, '新手任务'),
        (2, '成长任务'),
        (3, '隐藏任务'),
    )

    task_name = models.CharField(
        max_length=20,
        verbose_name='任务名称',
    )
    task_id = models.CharField(
        max_length=20,
        verbose_name='任务ID',
    )
    is_apply = models.BooleanField(
        default=True,
        verbose_name='是否应用'
    )
    task_code = models.CharField(
        max_length=40,
        choices=TASK_CODE,
        verbose_name='任务代码',
    )
    task_count = models.IntegerField(
        default=1,
        verbose_name='任务需求次数',
        help_text='默认为1，需要多次完成的，就填写对应的次数',
    )
    description = models.CharField(
        blank=False,
        max_length=200,
        verbose_name='任务描述',
    )
    task_level = models.IntegerField(
        choices=TASK_LEVEL,
        verbose_name='任务类型',
    )
    task_reward = models.CharField(
        max_length=100,
        verbose_name='任务奖励说明',
    )
    reward_due_time = models.FloatField(
        blank=True,
        null=True,
        verbose_name='奖励过期时间',
        help_text='单位是天'
    )
    reward_type = models.IntegerField(
        default=1,
        choices=REWARD_TYPE,
        verbose_name='奖励类型'
    )
    coupon_type = models.IntegerField(
        blank=True,
        null=True,
        choices=COUPON_TYPE,
        verbose_name='券类型',
        help_text='如果奖励是券，则填写此字段',
    )
    reward_num = models.FloatField(
        default=1,
        verbose_name='奖励数量',
    )
    task_url = models.CharField(
        max_length=30,
        verbose_name='任务地址',
    )
    weixin_required = models.BooleanField(
        verbose_name='是否要求微信绑定'
    )
    task_type = models.IntegerField(
        default=2,
        choices=TASK_TYPE,
        verbose_name='任务类型',
    )

    def __unicode__(self):
        return self.task_name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '任务列表'
        verbose_name_plural = verbose_name


class TaskFinishedStatus(models.Model):

    REWARD_STATUS = (
        (1, '未领取'),
        (2, '已经领取'),
    )

    FINISHED_STATUS = (
        (1, '未完成'),
        (2, '完成'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='task_finished_user',
    )
    task = models.ForeignKey(
        Task,
        verbose_name='任务名字',
        related_name='taskname',
    )
    finished_status = models.IntegerField(
        default=1,
        choices=FINISHED_STATUS,
        verbose_name='是否完成',
    )
    current_process = models.IntegerField(
        default=0,
        verbose_name='当前完成进度',
    )
    reward_status = models.IntegerField(
        default=1,
        choices=REWARD_STATUS,
        verbose_name='领奖状态',
    )
    reward_due_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='奖励过期时间',
    )
    finished_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='完成时间',
    )
    task_times = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='次数标记',
        help_text='此字段是作为完成次数的标记'
    )
    reward_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='领奖时间',
        db_index=True,
    )
    repeat_times = models.IntegerField(
        default=0,
        verbose_name='重复次数 ',
        help_text='已经完成重复任务的次数'
    )

    def __unicode__(self):
        return '{user} {task} {finished_time}'.format(
            user=self.user,
            task=self.task,
            finished_time=self.finished_time,
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        unique_together = (
            ("user", "task"),
        )
        verbose_name = '任务状态记录'
        verbose_name_plural = verbose_name


class TaskFinishedNotify(models.Model):

    NOTIFY_STATUS = (
        ('task_to_do', '有任务可以做'),
        ('reward_to_receive', '有奖励可以领取'),
        ('all_finished', '所有任务完成'),
    )

    user = models.OneToOneField(
        User,
        verbose_name='用户',
        related_name='notify_user'
    )
    notify_status = models.CharField(
        default='task_to_do',
        max_length=25,
        choices=NOTIFY_STATUS,
        verbose_name='任务状态通知'
    )

    def __unicode__(self):
        return '{user} {notify_status}'.format(
            user=self.user,
            notify_status=self.notify_status,
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '用户任务状态'
        verbose_name_plural = verbose_name


class Coupon(models.Model):

    COUPON_TYPE = (
        (1, '打折券'),
        (2, '抵用券'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='coupon_user',
    )
    task = models.ForeignKey(
        Task,
        verbose_name='对应任务',
        related_name='coupon_task'
    )
    coupon_type = models.IntegerField(
        default=1,
        choices=COUPON_TYPE,
        verbose_name='券类型',
    )
    coupon_num = models.FloatField(
        verbose_name='抵用额／打折',
        help_text='如果是打折，请填写小于1的小数,如果是抵用额,请填写抵用额'
    )
    coupon_start_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='优惠券领取时间',
    )
    coupon_used_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='优惠券使用时间',
    )
    coupon_due_time = models.DateTimeField(
        default=datetime.now() + timedelta(days=30)
    )

    def __unicode__(self):
        return '{user} {coupon_type}'.format(
            user=self.user,
            coupon_type=self.coupon_type,
        )

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name


class RealReward(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='reward_user',
    )
    award_item = models.CharField(
        max_length=100,
        verbose_name='奖励的实物',
    )
    award_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='奖励时间',
    )
    is_send = models.BooleanField(
        default=False,
        verbose_name='是否已经发放奖品',
    )
    send_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='寄送时间',
    )

    def __unicode__(self):
        return self.award_item

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '实物奖励记录'
        verbose_name_plural = verbose_name
