# coding: utf-8

from django.views.generic import View
from django.views.generic import TemplateView
from django.db import transaction
from django.contrib.auth.models import User

from app.crm.common import record_operate_admin
from app.vip.runtime.order import (
    OrderManage
)
from app.vip.runtime.manual_service import (
    ManualService
)
from ..models import (
    UserManualService,
)
from ..service_utils import (
    ServiceUtils,
)

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    get_object_or_none,
    JsonResponse,
)


class ConfirmRefundManualService(StaffRequiredMixin, View):

    @transaction.atomic
    def post(self, request, op_id):

        user = request.user
        service = get_object_or_none(
            UserManualService,
            id=op_id,
        )
        if not service:
            return JsonResponse({
                'status': 'error',
                'msg': 'not found service',
            })

        order = ServiceUtils.get_service_order(service)
        if not order:
            return JsonResponse({
                'status': 'error',
                'msg': 'not found order',
            })
        order_id = order.order_id

        OrderManage.confirm_refund_order(
            order_id=order_id,
            user=user
        )

        return JsonResponse({
            'status': 'ok',
            'msg': '确认订单退款成功'
        })


class FinishedManualService(StaffRequiredMixin, View):

    @record_operate_admin('finished_manual_service')
    def post(self, request, op_id):
        service = get_object_or_none(
            UserManualService,
            id=op_id,
        )
        manual_srv = ManualService()
        manual_srv.service_id = op_id
        manual_srv.user = service.user
        manual_srv.invalid_service(
            status='finished'
        )
        return JsonResponse({
            'status': 'ok',
            'msg': '确认服务已完结'
        })


class InvalidManualService(StaffRequiredMixin, View):

    def post(self, request, op_id):
        service = get_object_or_none(
            UserManualService,
            id=op_id,
        )
        manual_srv = ManualService()
        manual_srv.service_id = op_id
        manual_srv.user = service.user
        manual_srv.invalid_service(
            status='expired'
        )
        return JsonResponse({
            'status': 'ok',
            'msg': '确认服务已过期'
        })


class AdminOrderPage(StaffRequiredMixin, TemplateView):
    template_name = 'admin_order_page.html'


class AdminCreateOrder(StaffRequiredMixin, View):

    def post(self, request):
        username = request.POST.get('username', '')
        user = get_object_or_none(
            User,
            username=username,
        )
        if not user:
            return JsonResponse({
                'status': 'user_not_found',
                'msg': '用户不存在',
            })

        pid = request.POST.get('pid')
        num = request.POST.get('num', 1)
        payment_terms = request.POST.get('payment_terms')
        is_insurance = request.POST.get('is_insurance')
        product_type = request.POST.get('product_type')

        order = OrderManage.create_order(
            user=user,
            pid=pid,
            num=num,
            product_type=product_type,
            payment_terms=payment_terms,
            is_insurance=is_insurance
        )
        if (int(num) < 1):
            return JsonResponse({
                'status': 'error',
                'msg': '商品数量不能小于1',
            })

        if not order:
            return JsonResponse({
                'status': 'error',
                'msg': '支付失败,请勿重新购买!',
            })

        return JsonResponse({
            'status': 'ok',
            'msg': '订单生成成功',
            'pay_url': '',
            'order_id': order.order_id,
            'payment_terms': order.payment_terms,
            'order_price': order.order_price
        })
