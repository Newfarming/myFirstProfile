# coding: utf-8

import datetime

from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import (
    View,
)

from ..runtime.order import OrderManage
from ..models import UserVip

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.django_utils import (
    JsonResponse,
    get_int,
)
from pin_utils.alipay.alipay_utils import (
    AlipayUtils
)


class RenewUserVip(LoginRequiredMixin, View):

    def get(self, request, user_vip_id):

        user = request.user
        user_vip_query = user.vip_roles.select_related(
            'vip_role',
        ).filter(
            id=user_vip_id,
            is_active=True,
        )

        if not user_vip_query:
            raise Http404

        user_vip = user_vip_query[0]
        now = datetime.datetime.now()

        if (user_vip.expire_time - now).days > 7:
            raise Http404

        vip_role = user_vip.vip_role

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'id': user_vip.id,
                'vip_name': vip_role.vip_name,
                'feed_count': vip_role.feed_count,
                'pinbot_point': vip_role.pinbot_point,
                'active_time': user_vip.active_time,
                'expire_time': user_vip.expire_time,
                'month_price': vip_role.month_price,
            },
        })


class CreateRenewOrder(LoginRequiredMixin, View):
    '''
    创建自助服务续期订单
    '''
    valid_month = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

    def get_pay_url(self, order):
        request = self.request
        product_type = 'renew_service'
        alipay_return_url = request.build_absolute_uri(
            reverse('order-alipay-return')
        )
        alipay_notify_url = request.build_absolute_uri(
            reverse('order-alipay-notify')
        )

        pay_url = AlipayUtils.submit_order_url(
            order,
            return_url=alipay_return_url,
            notify_url=alipay_notify_url,
            order_price=order.order_price,
            extra_common_param=product_type
        )
        return pay_url

    def post(self, request, user_vip_id):
        renew_month = get_int(request.JSON.get('renew_month'))

        if renew_month not in self.valid_month:
            return JsonResponse({
                'status': 'valid_month',
                'msg': '请选择正确的续期月份',
            })

        user = request.user
        user_vip_query = UserVip.objects.select_related(
            'vip_role',
            'user',
        ).filter(
            user=user,
            is_active=True,
            id=user_vip_id,
        )
        if not user_vip_query:
            raise Http404

        user_vip = user_vip_query[0]
        now = datetime.datetime.now()

        if (user_vip.expire_time - now).days > 7:
            raise Http404

        order = OrderManage.create_renew_order(user_vip, renew_month)
        pay_url = self.get_pay_url(order)

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'pay_url': pay_url,
            'order_id': order.order_id,
            'payment_terms': 'alipay',
        })
