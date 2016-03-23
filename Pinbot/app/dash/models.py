# coding: utf-8

from django.db import models


class WeixinDailyReportData(models.Model):
    """微信报表"""
    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )
    new_bind_count = models.IntegerField(
        default=0,
        verbose_name='新增绑定'
    )
    new_reg_count = models.IntegerField(
        default=0,
        verbose_name='新增注册'
    )
    total_bind_count = models.IntegerField(
        default=0,
        verbose_name='总绑定用户'
    )
    lively_member_count = models.IntegerField(
        default=0,
        verbose_name='活跃会员数'
    )
    lively_user_count = models.IntegerField(
        default=0,
        verbose_name='活跃用户数'
    )
    feed_notify_send_count = models.IntegerField(
        default=0,
        verbose_name='简历推荐通知数'
    )
    feed_notify_view_count = models.IntegerField(
        default=0,
        verbose_name='通知点击数'
    )
    new_feed_count = models.IntegerField(
        default=0,
        verbose_name='新增定制数'
    )
    new_feed_favours_count = models.IntegerField(
        default=0,
        verbose_name='简历收藏数'
    )

    class Meta:
        app_label = 'dash'
        verbose_name = '微信端使用情况报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class FeedDailyReportData(models.Model):
    """定制使用情况"""
    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )

    lively_feed_count = models.IntegerField(
        default=0,
        verbose_name='活跃定制数'
    )
    new_feed_count = models.IntegerField(
        default=0,
        verbose_name='新增定制数'
    )
    lively_feed_user_count = models.IntegerField(
        default=0,
        verbose_name='定制活跃用户数'
    )
    lively_feed_member_count = models.IntegerField(
        default=0,
        verbose_name='定制活跃用户数'
    )

    class Meta:
        verbose_name = '定制使用情况报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class WeekReportData(models.Model):
    """周报报表"""
    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )
    week_lively_user_count = models.IntegerField(
        default=0,
        verbose_name='周活跃用户数',
    )
    week_lively_member_count = models.IntegerField(
        default=0,
        verbose_name='周活跃会员',
    )
    week_repeat_visit_user_count = models.IntegerField(
        default=0,
        verbose_name='周重复访问用户数',
    )
    week_repeat_visit_member_count = models.IntegerField(
        default=0,
        verbose_name='周重复访问会员数',
    )

    class Meta:
        app_label = 'dash'
        verbose_name = '周报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class MonthReportData(models.Model):
    """月报报表"""
    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )
    month_lively_user_count = models.IntegerField(
        default=0,
        verbose_name='月活跃用户数',
    )
    month_lively_member_count = models.IntegerField(
        default=0,
        verbose_name='月活跃会员',
    )
    month_repeat_visit_user_count = models.IntegerField(
        default=0,
        verbose_name='月重复访问用户数',
    )
    month_repeat_visit_member_count = models.IntegerField(
        default=0,
        verbose_name='月重复访问会员数',
    )

    class Meta:
        app_label = 'dash'
        verbose_name = '月报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class CoreDailyReportData(models.Model):
    """核心业务报表"""

    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )
    register_user_count = models.IntegerField(
        default=0,
        verbose_name='新注册用户数',
    )
    active_user_count = models.IntegerField(
        default=0,
        verbose_name='激活用户数'
    )
    member_count = models.IntegerField(
        default=0,
        verbose_name='会员用户数'
    )
    lively_user_count = models.IntegerField(
        default=0,
        verbose_name='活跃用户数'
    )
    lively_member_count = models.IntegerField(
        default=0,
        verbose_name='活跃会员数'
    )
    repeat_visit_count = models.IntegerField(
        default=0,
        verbose_name='重复访问用户数',
    )

    class Meta:
        app_label = 'dash'
        verbose_name = '核心业务数据报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class PartnerDailyReportData(models.Model):
    """互助伙伴日报表"""

    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )
    accept_task_user_count = models.IntegerField(
        default=0,
        verbose_name='当日认领任务用户数量'
    )
    accept_task_user_total_count = models.IntegerField(
        default=0,
        verbose_name='互助伙伴总量'
    )
    task_total_count = models.IntegerField(
        default=0,
        verbose_name='任务总数'
    )
    task_viewed_count = models.IntegerField(
        default=0,
        verbose_name='被查看任务数'
    )
    task_accedpted_count = models.IntegerField(
        default=0,
        verbose_name='被认领任务数'
    )
    task_accedpted_count_contrast = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='被认领任务占比'
    )
    task_accedpted_total_count = models.IntegerField(
        default=0,
        verbose_name='被认领任务总量'
    )
    upload_resume_count = models.IntegerField(
        default=0,
        verbose_name='上传简历数'
    )
    upload_resume_total_count = models.IntegerField(
        default=0,
        verbose_name='上传简历总量'
    )
    do_task_count = models.IntegerField(
        default=0,
        verbose_name='做任务次数'
    )
    do_task_total_count = models.IntegerField(
        default=0,
        verbose_name='做任务总次数'
    )
    resume_viewed_count = models.IntegerField(
        default=0,
        verbose_name='简历查看量'
    )
    resume_viewed_total_count = models.IntegerField(
        default=0,
        verbose_name='简历查看总量'
    )
    resume_download_count = models.IntegerField(
        default=0,
        verbose_name='简历下载量'
    )
    resume_download_total_count = models.IntegerField(
        default=0,
        verbose_name='简历下载总量'
    )
    interviewed_count = models.IntegerField(
        default=0,
        verbose_name='进入面试量'
    )
    interviewed_total_count = models.IntegerField(
        default=0,
        verbose_name='进入面试总量'
    )
    entered_count = models.IntegerField(
        default=0,
        verbose_name='入职量'
    )
    entered_total_count = models.IntegerField(
        default=0,
        verbose_name='总入职量'
    )
    accusation_count = models.IntegerField(
        default=0,
        verbose_name='举报数量'
    )
    accusation_total_count = models.IntegerField(
        default=0,
        verbose_name='举报总量'
    )
    today_commend_and_check_count = models.IntegerField(
        default=0,
        verbose_name='当天推荐当天查看量'
    )
    today_commend_and_download_count = models.IntegerField(
        default=0,
        verbose_name='当天推荐当天下载量'
    )
    today_reward_coin_count = models.IntegerField(
        default=0,
        verbose_name='当天奖励金币数'
    )
    all_reward_coin_count = models.IntegerField(
        default=0,
        verbose_name='总共奖励金币数'
    )
    today_extra_reward_coin_count = models.IntegerField(
        default=0,
        verbose_name='当天额外奖励金币数'
    )
    all_extra_reward_coin_count = models.IntegerField(
        default=0,
        verbose_name='总共额外奖励金币数'
    )

    class Meta:
        app_label = 'dash'
        verbose_name = '互助伙伴日报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class ResumeDailyReportData(models.Model):
    """简历日报表"""

    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='简历日报表',
    )
    resume_commends_count = models.IntegerField(
        default=0,
        verbose_name='简历推荐量',
    )
    resume_view_count = models.IntegerField(
        default=0,
        verbose_name='简历查看量',
    )
    resume_view_proportion = models.CharField(
        max_length=20,
        verbose_name='简历查看率',
        default=''
    )
    resume_fav_count = models.IntegerField(
        default=0,
        verbose_name='简历收藏量',
    )
    resume_down_count = models.IntegerField(
        default=0,
        verbose_name='简历下载量',
    )
    resume_down_proportion = models.CharField(
        max_length=20,
        verbose_name='简历下载率',
    )
    company_card_send_count = models.IntegerField(
        default=0,
        verbose_name='企业名片发送量',
    )
    interviewed_count = models.IntegerField(
        default=0,
        verbose_name='入面试量',
    )
    entered_count = models.IntegerField(
        default=0,
        verbose_name='入职量',
    )

    def __unicode__(self):
        return self.report_date.strftime('%Y-%m-%d')

    def __str__(self):
        return self.__unicode__()

    class Meta:
        app_label = 'dash'
        verbose_name = '简历日报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']



class ResumeWhitoutStaffDailyReportData(models.Model):
    """简历日报表,去除管理员数据"""

    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='简历日报表',
    )
    resume_commends_count = models.IntegerField(
        default=0,
        verbose_name='简历推荐量',
    )
    resume_view_count = models.IntegerField(
        default=0,
        verbose_name='简历查看量',
    )
    resume_view_proportion = models.CharField(
        max_length=20,
        verbose_name='简历查看率',
        default=''
    )
    resume_fav_count = models.IntegerField(
        default=0,
        verbose_name='简历收藏量',
    )
    resume_down_count = models.IntegerField(
        default=0,
        verbose_name='简历下载量',
    )
    resume_down_proportion = models.CharField(
        max_length=20,
        verbose_name='简历下载率',
    )
    company_card_send_count = models.IntegerField(
        default=0,
        verbose_name='企业名片发送量',
    )
    interviewed_count = models.IntegerField(
        default=0,
        verbose_name='入面试量',
    )
    entered_count = models.IntegerField(
        default=0,
        verbose_name='入职量',
    )

    def __unicode__(self):
        return self.report_date.strftime('%Y-%m-%d')

    def __str__(self):
        return self.__unicode__()

    class Meta:
        app_label = 'dash'
        verbose_name = '简历日报表(去除管理员)'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class UserDailyReportData(models.Model):
    """用户日报表"""
    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )
    new_register_user_count = models.IntegerField(
        default=0,
        verbose_name='新注册用户数',
    )
    new_experience_user_count = models.IntegerField(
        default=0,
        verbose_name='新体验用户数',
    )
    new_member_count = models.IntegerField(
        default=0,
        verbose_name='新会员用户数',
    )
    new_self_member_count = models.IntegerField(
        default=0,
        verbose_name='新自助会员数',
    )
    new_manual_member_count = models.IntegerField(
        default=0,
        verbose_name='新省心会员数',
    )
    all_total_active_user_count = models.IntegerField(
        default=0,
        verbose_name='总激活⽤用户数',
    )
    total_register_user_count = models.IntegerField(
        default=0,
        verbose_name='注册用户数',
    )
    total_experience_user_count = models.IntegerField(
        default=0,
        verbose_name='体验用户数',
    )
    total_member_count = models.IntegerField(
        default=0,
        verbose_name='会员用户数',
    )
    total_self_member_count = models.IntegerField(
        default=0,
        verbose_name='自助会员数',
    )
    total_manual_member_count = models.IntegerField(
        default=0,
        verbose_name='省心会员数',
    )

    def __unicode__(self):
        return self.report_date.strftime('%Y-%m-%d')

    def __str__(self):
        return self.__unicode__()

    class Meta:
        app_label = 'dash'
        verbose_name = '用户日报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class TaskSystemDailyReportData(models.Model):
    """任务系统日报表"""
    report_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='统计日期'
    )
    task_A1_count = models.IntegerField(
        default=0,
        verbose_name='账户激活【新手】',
    )
    task_A2_count = models.IntegerField(
        default=0,
        verbose_name='微信绑定',
    )
    task_A3_count = models.IntegerField(
        default=0,
        verbose_name='绑定邮箱',
    )
    task_A4_count = models.IntegerField(
        default=0,
        verbose_name='完善企业名片',
    )
    task_A5_count = models.IntegerField(
        default=0,
        verbose_name='提交1个定制',
    )
    task_A6_count = models.IntegerField(
        default=0,
        verbose_name='查看简历详情',
    )
    task_A6_R1_count = models.IntegerField(
        default=0,
        verbose_name='查看10次简历',
    )
    task_A6_R2_count = models.IntegerField(
        default=0,
        verbose_name='查看50次简历',
    )
    task_A6_L1_count = models.IntegerField(
        default=0,
        verbose_name='连续3天查看简历',
    )
    task_A7_count = models.IntegerField(
        default=0,
        verbose_name='收藏1份简历',
    )
    task_A7_R1_count = models.IntegerField(
        default=0,
        verbose_name='收藏20份简历',
    )
    task_A7_R2_count = models.IntegerField(
        default=0,
        verbose_name='收藏50份简历',
    )
    task_A7_R3_count = models.IntegerField(
        default=0,
        verbose_name='收藏100简历',
    )
    task_A8_count = models.IntegerField(
        default=0,
        verbose_name='标记1份简历',
    )
    task_A8_R1_count = models.IntegerField(
        default=0,
        verbose_name='标记20份简历',
    )
    task_A8_R2_count = models.IntegerField(
        default=0,
        verbose_name='标记50份简历',
    )
    task_A8_R3_count = models.IntegerField(
        default=0,
        verbose_name='标记80份简历',
    )
    task_A9_count = models.IntegerField(
        default=0,
        verbose_name='下载1份简历',
    )
    task_A9_R1_count = models.IntegerField(
        default=0,
        verbose_name='下载10份简历',
    )
    task_A9_R2_count = models.IntegerField(
        default=0,
        verbose_name='下载30份简历',
    )
    task_A9_R3_count = models.IntegerField(
        default=0,
        verbose_name='下载60份简历',
    )
    task_A10_count = models.IntegerField(
        default=0,
        verbose_name='点击不感兴趣按钮',
    )
    task_A10_R1_count = models.IntegerField(
        default=0,
        verbose_name='隐藏任务',
    )
    task_A11_count = models.IntegerField(
        default=0,
        verbose_name='购买套餐',
    )
    task_A12_count = models.IntegerField(
        default=0,
        verbose_name='发送企业名片',
    )
    task_A13_count = models.IntegerField(
        default=0,
        verbose_name='扩展匹配查看简历',
    )
    task_A14_L1_count = models.IntegerField(
        default=0,
        verbose_name='推荐HR',
    )
    task_A15_count = models.IntegerField(
        default=0,
        verbose_name='录入1封简历',
    )
    task_A15_R1_count = models.IntegerField(
        default=0,
        verbose_name='录入5封简历',
    )
    task_A15_R2_count = models.IntegerField(
        default=0,
        verbose_name='录入10封简历',
    )
    task_A16_count = models.IntegerField(
        default=0,
        verbose_name='我问你答',
    )
    task_A17_count = models.IntegerField(
        default=0,
        verbose_name='工作日认领5次互助任务',
    )
    task_A18_R1_count = models.IntegerField(
        default=0,
        verbose_name='周末认领10次互助任务',
    )
    task_A18_R2_count = models.IntegerField(
        default=0,
        verbose_name='周末认领20次互助任务',
    )

    def __unicode__(self):
        return self.report_date.strftime('%Y-%m-%d')

    def __str__(self):
        return self.__unicode__()

    class Meta:
        app_label = 'dash'
        verbose_name = '任务系统日报表'
        verbose_name_plural = verbose_name
        ordering = ['-report_date']


class PinbotDailyReport(models.Model):

    pv = models.IntegerField(
        default=0,
        verbose_name='PV',
    )
    uv = models.IntegerField(
        default=0,
        verbose_name='UV',
    )
    register_user_count = models.IntegerField(
        default=0,
        verbose_name='新增用户数',
    )
    total_user_count = models.IntegerField(
        default=0,
        verbose_name='总用户数',
    )
    login_user_count = models.IntegerField(
        default=0,
        verbose_name='登陆用户数',
    )
    pay_user_count = models.IntegerField(
        default=0,
        verbose_name='付费用户数'
    )
    total_pay_count = models.IntegerField(
        default=0,
        verbose_name='总付费用户数',
    )
    report_date = models.DateField(
        verbose_name='统计日期',
    )

    def __unicode__(self):
        return self.report_date.strftime('%Y-%m-%d')

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = 'B端日报'
        verbose_name_plural = verbose_name
