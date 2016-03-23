# coding: utf-8

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class Product(models.Model):

    PRODUCT_STATUS = (
        ('enable', '允许购买'),
        ('disable', '限制购买'),
    )

    product_name = models.CharField(
        max_length=40,
        verbose_name='产品名称',
    )
    code_name = models.CharField(
        max_length=40,
        verbose_name='代码别名',
    )
    price = models.FloatField(
        verbose_name='产品单价'
    )
    desc = models.CharField(
        max_length=200,
        verbose_name='产品备注',
        blank=True,
        null=True,
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    status = models.CharField(
        max_length=20,
        choices=PRODUCT_STATUS,
        default='enable',
        verbose_name='产品状态',
    )
    is_show = models.BooleanField(
        default=False,
        verbose_name='是否显示到前台'
    )

    def __unicode__(self):
        return self.code_name

    def __str__(self):
        return self.__unicode__()

    def get_subject(self):
        return self.__unicode__()

    def get_detail(self):
        return self.desc

    def get_price(self):
        return self.price

    class Meta:
        verbose_name = '产品列表'
        verbose_name_plural = verbose_name
        abstract = True


class PackageItem(Product):

    salary_range = models.CharField(
        max_length=20,
        verbose_name='月薪范围'
    )
    service_month = models.IntegerField(
        default=1,
        verbose_name='服务月数'
    )
    candidate_num = models.IntegerField(
        default=1,
        verbose_name='候选人数量'
    )
    feed_count = models.IntegerField(
        default=0,
        verbose_name='定制数'
    )
    pinbot_point = models.IntegerField(
        default=0,
        verbose_name='每周聘点'
    )
    is_commend = models.BooleanField(
        default=False,
        verbose_name='是否为推荐套餐'
    )

    @property
    def get_product_type(self):
        return 'manual_service'

    @property
    def get_desc(self):
        salary_range = self.salary_range.split(',')

        if salary_range[0] == '30' and salary_range[1] == '100':
            retur_str = '30k以上, %s个月 ,%s名候选人' % (
                self.service_month,
                self.candidate_num
            )
        else:
            retur_str = '%sk-%sk, %s个月 ,%s名候选人' % (
                salary_range[0],
                salary_range[1],
                self.service_month,
                self.candidate_num
            )
        return retur_str

    def __unicode__(self):
        return self.product_name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '人工服务配置'
        verbose_name_plural = verbose_name


class PinbotPoint(Product):

    num = models.IntegerField(
        default=1,
        verbose_name='聘点数量'
    )

    def __unicode__(self):
        return self.product_name

    def __str__(self):
        return self.__unicode__()

    @property
    def get_product_type(self):
        return 'pinbot_point'

    @property
    def get_desc(self):
        return '充值聘点'

    class Meta:
        verbose_name = '聘点购买配置'
        verbose_name_plural = verbose_name


class Coin(Product):

    def __unicode__(self):
        return self.product_name

    def __str__(self):
        return self.__unicode__()

    @property
    def get_product_type(self):
        return 'coin'

    @property
    def get_desc(self):
        return '充值金币'

    class Meta:
        verbose_name = '金币购买配置'
        verbose_name_plural = verbose_name


class VipRoleSetting(Product):

    vip_name = models.CharField(
        max_length=20,
        verbose_name='会员名称',
    )
    feed_count = models.IntegerField(
        verbose_name='定制数',
    )
    pinbot_point = models.IntegerField(
        verbose_name='赠送聘点',
    )
    allow_apply = models.BooleanField(
        default=False,
        verbose_name='允许申请',
    )
    agreement = models.BooleanField(
        default=False,
        verbose_name='需要签订协议',
    )
    level = models.PositiveIntegerField(
        default=1,
        verbose_name='会员等级',
    )
    auto_active = models.BooleanField(
        default=False,
        verbose_name='自动生效',
    )
    attract_info = models.CharField(
        max_length=80,
        default='',
        blank=True,
        verbose_name='优惠信息',
    )
    index = models.IntegerField(
        default=0,
        verbose_name='栏位排序'
    )
    month_price = models.FloatField(
        default=0,
        verbose_name='每月价格',
    )
    service_time = models.IntegerField(
        default=3,
        verbose_name='服务时间',
    )

    def __unicode__(self):
        return self.vip_name

    def __str__(self):
        return self.__unicode__()

    @property
    def get_product_type(self):
        return 'self_service'

    @property
    def get_desc(self):
        desc = '{vip_name}, {feed_count}个定制, {pinbot_point}聘点'.format(
            vip_name=self.vip_name,
            feed_count=self.feed_count,
            pinbot_point=self.pinbot_point,
        )
        return desc

    class Meta:
        verbose_name = '自助服务配置'
        verbose_name_plural = verbose_name


class RenewRecord(models.Model):
    '''
    自助服务续期
    '''

    user_vip = models.ForeignKey(
        'vip.UserVip',
        related_name='renew_records',
        verbose_name='自助服务',
    )
    duration = models.IntegerField(
        verbose_name='续期时长',
    )
    price = models.FloatField(
        verbose_name='价格',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )

    @property
    def get_product_type(self):
        return 'renew_service'

    def __unicode__(self):
        return str(self.user_vip_id)

    def __str__(self):
        return self.__unicode__()

    def get_subject(self):
        return '自助服务续期'

    def get_detail(self):
        return '自助服务续期'

    class Meta:
        verbose_name = '自助服务续期'
        verbose_name_plural = verbose_name


class UserVip(models.Model):

    APPLY_STATUS_META = (
        ('applying', '申请中'),
        ('success', '申请完成'),
    )
    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='vip_roles',
    )
    vip_role = models.ForeignKey(
        VipRoleSetting,
        verbose_name='角色',
        related_name='setting_roles',
    )
    custom_point = models.IntegerField(
        default=0,
        verbose_name='配置每周点数',
    )
    custom_feed = models.IntegerField(
        default=0,
        verbose_name='配置定制数',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='生效状态',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='申请时间',
    )
    active_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='生效时间',
    )
    has_sign = models.BooleanField(
        default=False,
        verbose_name='协议签订',
    )
    apply_status = models.CharField(
        max_length=20,
        choices=APPLY_STATUS_META,
        default='applying',
        verbose_name='申请状态',
    )
    expire_time = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='过期时间',
    )
    total_price = models.FloatField(
        default=0,
        verbose_name='总价格',
    )

    def get_subject(self):
        return u'%s会员' % self.vip_role.vip_name

    def get_detail(self):
        return u'%s会员' % self.vip_role.vip_name

    def get_price(self):
        return self.vip_role.price

    @property
    def status(self):
        return self.apply_status

    @status.setter
    def status(self, value):
        self.apply_status = value

    def __unicode__(self):
        return u'%s,%s' % (self.user.username, self.vip_role.vip_name)

    def __str__(self):
        return self.__unicode__()

    @property
    def get_product_type(self):
        return 'self_service'

    @property
    def item(self):
        return self.vip_role

    def apply_vip_user(self):
        interface = '''
         <div class="btn-group">
         <a class="editable-handler"
         title=""
         data-editable-field="status"
         data-editable-loadurl="%s"
         data-original-title="输入审核状态"><i class="icon-edit"></i></a>
         </div>
         <span class="editable-field">操作</span>
          ''' % reverse('vip-apply-user-vip-form', args=(self.id,))

        return mark_safe(interface)

    apply_vip_user.short_description = 'vip生效'

    def disable_vip_user(self):
        interface = '''
         <div class="btn-group">
         <a class="editable-handler"
         title=""
         data-editable-field="status"
         data-editable-loadurl="%s"
         data-original-title="输入审核状态"><i class="icon-edit"></i></a>
         </div>
         <span class="editable-field">操作</span>
          ''' % reverse('vip-disable-form', args=(self.id,))

        return mark_safe(interface)

    disable_vip_user.short_description = '停用'

    def admin_order_page(self):
        interface = '''
        <a href="/vip/order/admin_page/#/usermode_noworry/?username={0}" target="_blank">省心套餐</a>
        '''.format(self.user.username)
        return mark_safe(interface)

    admin_order_page.short_description = '开通套餐'

    class Meta:
        verbose_name = '自助服务'
        verbose_name_plural = verbose_name


class UserOrder(models.Model):

    ORDER_STATUS_META = (
        ('unpay', '进行中'),
        ('paid', '交易成功'),
        ('fail', '交易失败'),
        ('refund', '退款中'),
        ('cancel_refund', '取消退款'),
        ('refunded', '退款成功'),
        ('closed', '已关闭'),
        ('canceled', '已取消'),
        ('deleted', '已删除'),
    )

    PAYMENT_TERMS_META = (
        ('alipay', '支付宝'),
        ('weixin', '微信'),
        ('offline', '线下'),
        ('coin', '金币支付'),
    )
    ORDER_TYPE_META = (
        (1, '自助服务'),
        (2, '人工服务'),
        (3, '购买聘点'),
        (4, '购买金币'),
        (5, '提现'),
        (6, '会员申请'),
        (7, '续期'),
    )

    item_content_type = models.ForeignKey(
        ContentType,
        related_name='order_type',
        verbose_name='订单类型',
    )
    item_object_id = models.PositiveIntegerField(
        verbose_name='订单类型id',
    )
    item = generic.GenericForeignKey(
        'item_content_type',
        'item_object_id',
    )
    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='user_orders',
    )
    order_id = models.CharField(
        max_length=30,
        verbose_name='订单id',
    )
    order_status = models.CharField(
        choices=ORDER_STATUS_META,
        default='unpay',
        max_length=30,
        verbose_name='订单状态',
    )
    order_price = models.FloatField(
        verbose_name='支付金额',
    )
    actual_price = models.FloatField(
        verbose_name='实际支付',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='生成时间',
    )
    pay_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='支付时间',
    )
    payment_terms = models.CharField(
        choices=PAYMENT_TERMS_META,
        default='alipay',
        max_length=30,
        verbose_name='支付方式',
    )
    order_remark = models.CharField(
        default='',
        max_length=30,
        verbose_name='交易备注',
    )
    order_type = models.IntegerField(
        choices=ORDER_TYPE_META,
        default=3,
        blank=True,
        verbose_name='订单类型',
    )
    order_desc = models.CharField(
        max_length=60,
        default='',
        blank=True,
        verbose_name='订单内容',
    )
    is_insurance = models.BooleanField(
        default=False,
        verbose_name='入职险'
    )
    is_delete = models.BooleanField(
        default=False,
        blank=True,
        verbose_name='已删除',
    )

    def __unicode__(self):
        return self.order_id

    def __str__(self):
        return self.__unicode__()

    def subject_name(self):
        return self.item.get_subject()

    def order_detail(self):
        return self.item.get_detail()

    def offline_pay(self):
        if self.order_status == 'paid':
            return mark_safe('已支付')

        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('vip-offline-pay-form', args=(self.order_id,))

        return mark_safe(interface)

    offline_pay.short_description = '离线支付'

    def refund(self):
        if self.order_status != 'refund':
            return ''

        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('order-refund-form', args=(self.order_id,))

        return mark_safe(interface)

    refund.short_description = '退款'

    class Meta:
        verbose_name = '用户订单'
        verbose_name_plural = verbose_name


class Mission(models.Model):

    MISSION_TYPE_META = (
        ('none', '无'),
        ('add_feed', '添加定制'),
        ('check_resume', '查看简历'),
    )
    MISSION_STATUS_META = (
        ('start', '开始'),
        ('finish', '已完成'),
    )
    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='missions',
    )
    mission_type = models.CharField(
        max_length=30,
        verbose_name='任务类型',
        choices=MISSION_TYPE_META,
    )
    mission_status = models.CharField(
        max_length=30,
        verbose_name='任务状态',
        choices=MISSION_STATUS_META,
        default='start',
    )
    start_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='开始时间',
    )
    finish_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='完成时间',
    )
    grant_status = models.BooleanField(
        default=False,
        verbose_name='领奖状态',
    )

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '新手任务'
        verbose_name_plural = verbose_name


class WithdrawRecord(models.Model):

    '''
    用户提现
    '''

    VERIFY_STATUS_META = (
        (0, '进行中'),
        (1, '审核成功'),
        (2, '审核失败'),
    )
    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='withdraw_records',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        db_index=True,
    )
    verify_status = models.IntegerField(
        choices=VERIFY_STATUS_META,
        default=0,
        verbose_name='审核状态',
    )
    verify_remark = models.CharField(
        default='',
        max_length=100,
        verbose_name='审核备注',
    )
    verify_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='审核时间',
    )
    money = models.FloatField(
        verbose_name='金额',
    )

    def get_subject(self):
        return u'提现'

    @property
    def get_product_type(self):
        return 'withdraw'

    def get_desc(self):
        return '金币提现'

    def __str__(self):
        return u'%s提现%s' % (self.user.username, self.money)

    def __unicode__(self):
        return self.__str__()

    def current_coin(self):
        return self.user.pinbotpoint.coin

    current_coin.short_description = '当前金币'

    def operation(self):
        if self.verify_status != 0:
            return ''

        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('vip-withdraw-form', args=(self.id,))

        return mark_safe(interface)

    operation.short_description = '操作'

    class Meta:
        verbose_name = '提现记录'
        verbose_name_plural = verbose_name


class UserManualService(models.Model):

    PACKAGE_STATUS_META = (
        ('applying', '申请中'),
        ('success', '已开通'),
        ('refund', '退款中'),
        ('continue', '续期用户'),
        ('cancel_refund', '取消退款'),
        ('refunded', '退款成功'),
        ('closed', '已关闭'),
        ('canceled', '已取消'),
        ('deleted', '已删除'),
        ('expired', '已过期'),
        ('finished', '已完结'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='manual_roles',
    )
    item = models.ForeignKey(
        PackageItem,
        verbose_name='配置',
        related_name='manual_settings',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='生效状态',
    )
    has_sign = models.BooleanField(
        default=False,
        verbose_name='协议签订',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='申请时间',
    )
    active_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='生效时间',
    )
    expire_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='过期时间',
        db_index=True,
    )
    status = models.CharField(
        choices=PACKAGE_STATUS_META,
        default='applying',
        max_length=30,
        verbose_name='套餐状态',
    )
    is_insurance = models.BooleanField(
        default=False,
        verbose_name='是否包含入职险'
    )
    order_price = models.FloatField(
        default=0.0,
        verbose_name='支付金额',
    )
    item_records = generic.GenericRelation('vip.ItemRecord')

    def get_subject(self):
        return u'%s会员' % self.item.code_name

    def get_detail(self):
        return u'%s会员' % self.item.code_name

    def get_price(self):
        return self.item.price

    def __unicode__(self):
        return '%s,%s' % (self.user.username, self.item.code_name)

    def apply_vip_user(self):
        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('vip-apply-user-manual-service-form', args=(self.id,))

        return mark_safe(interface)
    apply_vip_user.short_description = '人工服务生效'

    def refund(self):
        if self.status != 'refund':
            return ''

        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('vip-refund-manual-service-form', args=(self.id,))
        return mark_safe(interface)
    refund.short_description = '点击退款'

    def finished(self):
        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('vip-finished-manual-service-form', args=(self.id,))
        return mark_safe(interface)
    finished.short_description = '完结服务'

    def invalid(self):
        interface = '''
        <div class="btn-group">
        <a class="editable-handler"
        title=""
        data-editable-field="status"
        data-editable-loadurl="%s"
        data-original-title="输入审核状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">操作</span>
         ''' % reverse('vip-invalid-manual-service-form', args=(self.id,))
        return mark_safe(interface)
    invalid.short_description = '强制过期'

    @property
    def get_product_type(self):
        return 'manual_service'

    class Meta:
        verbose_name = '人工服务'
        verbose_name_plural = verbose_name


class ItemRecord(models.Model):

    num = models.IntegerField(
        default=0,
        verbose_name='商品数量'
    )
    total_price = models.FloatField(
        default=0,
        verbose_name='商品总价'
    )
    order = models.ForeignKey(
        UserOrder,
        verbose_name='订单'
    )
    item_content_type = models.ForeignKey(
        ContentType,
        related_name='item_type',
        verbose_name='商品类型',
    )
    item_object_id = models.PositiveIntegerField(
        verbose_name='商品id',
    )
    item = generic.GenericForeignKey(
        'item_content_type',
        'item_object_id',
    )

    @classmethod
    def fetch_related_item(cls, queryset):
        '''
        reference:
        http://stackoverflow.com/questions/12466945/django-prefetch-related-objects-of-a-genericforeignkey
        减少数据库查询次数，自定义fetch_related_item
        '''
        uservip_ctype = ContentType.objects.get_for_model(UserVip)
        manual_service_ctype = ContentType.objects.get_for_model(UserManualService)

        item_objects = {}
        item_objects[uservip_ctype.id] = UserVip.objects.select_related(
            'vip_role'
        ).in_bulk(
            [i.item_object_id for i in queryset if i.item_content_type_id == uservip_ctype.id]
        )
        item_objects[manual_service_ctype.id] = UserManualService.objects.select_related(
            'item'
        ).in_bulk(
            [i.item_object_id for i in queryset if i.item_content_type_id == manual_service_ctype.id]
        )

        for i in queryset:
            i.item_obj = item_objects[i.item_content_type_id][i.item_object_id]
        return queryset

    class Meta:
        verbose_name = '商品购买记录'
        verbose_name_plural = verbose_name
