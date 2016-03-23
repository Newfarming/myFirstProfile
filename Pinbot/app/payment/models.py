# coding: utf-8

import datetime
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from pinbot_package.models import (
    ResumePackge,
    FeedService,
)
from app.weixin.models import (
    WeixinUser
)


class WeixinPackRecord(models.Model):
    '''
    微信红包发放纪录
    '''
    user = models.ForeignKey(WeixinUser, verbose_name='微信用户')
    amount = models.FloatField(
        default=0,
        verbose_name='发放金额'
    )
    send_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='发放时间'
    )
    send_status = models.BooleanField(
        default=False,
        verbose_name='发放状态'
    )
    send_msg = models.CharField(
        max_length=100,
        verbose_name='发放信息'
    )

    def __unicode__(self):
        return u'%s' % (self.user)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'红包发放'
        verbose_name_plural = verbose_name


class ShoppingCar(models.Model):
    '''
    购物车信息
    '''
    user = models.OneToOneField(User, verbose_name='注册用户')
    package = models.ForeignKey(
        ResumePackge,
        verbose_name='套餐类型',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    package_price = models.FloatField(
        verbose_name='套餐价格',
        default=0,
    )
    feed_service = models.ForeignKey(
        FeedService,
        verbose_name='订阅类型',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    feed_price = models.FloatField(verbose_name='订阅价格', default=0)
    feed_count = models.IntegerField(
        verbose_name='订阅数量',
        default=0,
        blank=True
    )
    total_price = models.FloatField(verbose_name='总额')

    def add_price_info(self):
        total_price = 0
        shopping_car = self

        if shopping_car.package:
            shopping_car.package_price = shopping_car.package.price
            total_price += shopping_car.package_price
        else:
            shopping_car.package_price = 0

        if shopping_car.feed_service:
            shopping_car.feed_price = shopping_car.feed_service.price * shopping_car.feed_count
            total_price += shopping_car.feed_price
        else:
            shopping_car.feed_price = 0
        shopping_car.total_price = total_price
        return True

    def __str__(self):
        return u'%s' % (
            self.user.username,
        )

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = u'购物车'
        verbose_name_plural = u'购物车'


class PaymentOrder(models.Model):
    '''
    订单信息
    '''
    PAY_STATUS = (
        ('paid', u'已支付'),
        ('unpay', u'未支付'),
    )

    PAYMENT_TERMS = (
        ('online', u'线上'),
        ('alipay', u'支付宝'),
        ('offline', u'线下'),
    )

    order_id = models.CharField(
        max_length=30,
        verbose_name='订单号',
        unique=True,
    )
    user = models.ForeignKey(User, verbose_name='注册用户')
    package = models.ForeignKey(
        ResumePackge,
        verbose_name='套餐类型',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    package_price = models.FloatField(verbose_name='套餐价格', default=0)
    feed_service = models.ForeignKey(
        FeedService,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name='订阅类型',
    )
    feed_price = models.FloatField(verbose_name='订阅价格', default=0)
    feed_count = models.IntegerField(
        default=0,
        verbose_name='订阅数量',
    )
    pay_status = models.CharField(
        max_length=20,
        choices=PAY_STATUS,
        verbose_name='支付状态',
        default='unpay',
    )
    total_price = models.FloatField(verbose_name='总额', default=0)
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='交易日期',
        db_index=True,
    )
    actual_price = models.FloatField(verbose_name='支付金额', default=0)
    payment_terms = models.CharField(
        verbose_name='支付方式',
        max_length=20,
        choices=PAYMENT_TERMS,
        default='alipay',
    )

    def add_order_id(self):
        uuid_str = '-' + str(uuid.uuid1()).split('-')[3]
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + uuid_str
        self.order_id = order_id

    def subject_name(self):
        return self.package.name if self.package else self.feed_service.name

    def order_detail(self):
        return self.package.name if self.package else self.feed_service.name

    def __str__(self):
        return u'%s' % (
            self.user.username,
        )

    def __unicode__(self):
        return self.__str__()

    def offline_pay_success(self):
        if self.pay_status == 'paid':
            return u''

        interface = '''
        <div class="btn-group pull-right">
        <a class="editable-handler" title="" data-editable-field="pay_status" data-editable-loadurl="%s" data-original-title="输入支付状态"><i class="icon-edit"></i></a>
        </div>
        <span class="editable-field">线下支付成功</span>
         ''' % reverse('payment-offline-pay-form', args=(self.order_id,))

        return mark_safe(interface)

    offline_pay_success.short_description = u'操作'

    class Meta:
        verbose_name = u'订单信息'
        verbose_name_plural = u'订单信息'


class CommonReceiverInfo(models.Model):
    '''
    通用收件人信息
    '''
    user = models.ForeignKey(User, verbose_name='注册用户')
    name = models.CharField(max_length=40, verbose_name='收件人', db_index=True)
    address = models.CharField(max_length=200, verbose_name='收件地址')
    phone = models.CharField(max_length=20, verbose_name='联系电话', db_index=True)

    def __str__(self):
        return u'%s' % (
            self.user.username,
        )

    def __unicode__(self):
        return self.__str__()

    class Meta:
        abstract = True


class CommonBillInfo(models.Model):
    '''
    通用发票信息
    '''
    TITLE_TYPE = (
        ('personal', '个人'),
        ('company', '单位'),
    )

    user = models.ForeignKey(User, verbose_name='注册用户')
    bill_type = models.CharField(
        max_length=20,
        choices=TITLE_TYPE,
        verbose_name='抬头类型',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='发票抬头',
        default='',
        blank=True,
    )
    content = models.CharField(max_length=300, verbose_name='发票内容')

    def __str__(self):
        return u'%s' % (
            self.user.username,
        )

    def __unicode__(self):
        return self.__str__()

    class Meta:
        abstract = True


class ReceiverInfo(CommonReceiverInfo):
    '''
    收件人信息
    '''

    DEFAULT_META = (
        ('yes', '是'),
        ('no', '否'),
    )

    default_addr = models.CharField(
        max_length=10,
        choices=DEFAULT_META,
        default='no',
        verbose_name=u'默认地址',
    )

    class Meta:
        verbose_name = u'收件人信息'
        verbose_name_plural = u'收件人信息'


class BillInfo(CommonBillInfo):
    '''
    发票信息
    '''

    class Meta:
        verbose_name = u'发票信息'
        verbose_name_plural = u'发票信息'


class OrderBillInfo(CommonBillInfo):
    '''
    订单发票信息
    '''
    order = models.OneToOneField(PaymentOrder, verbose_name='订单')

    class Meta:
        verbose_name = u'订单发票信息'
        verbose_name_plural = u'订单发票信息'


class OrderReceiverInfo(CommonReceiverInfo):
    '''
    订单收件人信息
    '''
    order = models.OneToOneField(PaymentOrder, verbose_name='订单')

    class Meta:
        verbose_name = u'订单收件人信息'
        verbose_name_plural = u'订单收件人信息'
