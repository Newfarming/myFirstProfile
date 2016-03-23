# coding: utf-8

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class InviteCode(models.Model):
    STATUS_META = (
        ('unused', '未使用'),
        ('used', '已使用'),
        ('expire', '已过期'),
    )

    STATUS_DICT = {
        i[0]: i[1]
        for i in STATUS_META
    }

    code = models.CharField(
        max_length=50,
        verbose_name='邀请码',
        default='',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='生成时间',
    )
    status = models.CharField(
        max_length=20,
        verbose_name='使用状态',
        choices=STATUS_META,
        default='unused',
    )

    def __unicode__(self):
        return self.code

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '邀请码'
        verbose_name_plural = verbose_name


class InviteCodeApply(models.Model):

    STATUS_META = (
        ('', '全部'),
        ('unverify', '未审核'),
        ('success', '审核通过'),
        ('fail', '未通过'),
    )
    email = models.CharField(
        max_length=60,
        verbose_name='申请邮箱',
    )
    job = models.CharField(
        max_length=30,
        verbose_name='职业',
    )
    city = models.CharField(
        max_length=30,
        verbose_name='城市',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='电话',
    )
    apply_desc = models.CharField(
        max_length=60,
        verbose_name='申请宣言',
    )
    ip = models.CharField(
        max_length=20,
        verbose_name='IP地址',
    )
    status = models.CharField(
        max_length=20,
        verbose_name='申请状态',
        choices=STATUS_META,
        default='unverify',
    )
    apply_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='申请时间',
    )
    invite_code = models.CharField(
        max_length=50,
        verbose_name='邀请码',
        default='',
    )

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.__unicode__()

    def apply_verify(self):
        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('invite-apply-verify-form', args=(self.id,))

        return mark_safe(interface)

    apply_verify.short_description = u'操作'

    def code_status(self):
        if not self.invite_code:
            return mark_safe('')

        invite_code_query = InviteCode.objects.filter(
            code=self.invite_code,
        )
        if not invite_code_query:
            return mark_safe('')

        invite_code = invite_code_query[0]
        code_status = invite_code.STATUS_DICT.get(
            invite_code.status,
            invite_code.status
        )
        return mark_safe(code_status)

    code_status.short_description = u'使用状态'

    class Meta:
        verbose_name = '申请信息'
        verbose_name_plural = verbose_name
