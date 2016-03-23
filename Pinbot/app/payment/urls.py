# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from views import (
    MyPayment,
    PaymentRecord,
    PinbotPointRecord,
    ManualServiceList,
    DeleteUserOrder,
)

from app.pinbot_point.models import (
    CoinRecord,
)

urlpatterns = patterns(
    '',
    # API接口：返回交易记录数据
    url(
        r'^payment_record/$',
        PaymentRecord.as_view(),
        name='payment-payment-record',
    ),
    url(
        r'^point_record/$',
        PinbotPointRecord.as_view(
            template_name='payment_pinbot_point_record.html'
        ),
        name='payment-point-record',
    ),
    url(
        '^my_account/$',
        MyPayment.as_view(
            template='my_account.html'
        ),
        name='payment-my-account',
    ),
    url(
        '^coin_record/$',
        PinbotPointRecord.as_view(
            template_name='coin_records.html',
            model=CoinRecord,
        ),
        name='payment-coin-record',
    ),
    url(
        '^service_list/$',
        ManualServiceList.as_view(),
        name='payment-manual-service-list',
    ),
    url(
        '^delete_order/$',
        DeleteUserOrder.as_view(),
        name='payment-delete-order',
    ),
    # 交易记录
    url(
        r'^trade_log/$',
        login_required(TemplateView.as_view(
            template_name='payment_records.html'
        )),
        name='payment-trade-log',
    ),
    # 我的套餐
    url(
        r'^my_package/$',
        login_required(TemplateView.as_view(
            template_name='my_package.html'
        )),
        name='payment-my-package',
    ),
    # 我的账户金币充值 payment-coin-recharge
    url(
        r'^coin_recharge/$',
        login_required(TemplateView.as_view(
            template_name='coin_recharge.html'
        )),
        name='payment-coin-recharge',
    ),
    # 我的账户购买聘点 payment-point-recharge
    url(
        r'^point_recharge/$',
        MyPayment.as_view(
            template='point_recharge.html'
        ),
        name='payment-point-recharge',
    ),
)
