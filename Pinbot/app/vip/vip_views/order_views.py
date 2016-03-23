# coding: utf-8

from django.http import Http404

from django.views.generic import (
    View,
)
from django.http import HttpResponse
from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect

from app.pinbot_point.point_utils import (
    point_utils,
)
from ..models import (
    Coin,
    PinbotPoint,
    PackageItem,
    VipRoleSetting,
    ItemRecord,
    UserOrder,
    UserManualService,
)
from ..service_utils import (
    ServiceUtils
)
from app.crm.common import record_operate_admin
from app.vip.runtime.order import (
    OrderManage
)
from app.vip.runtime.self_service import (
    SelfService
)
from app.vip.runtime.manual_service import (
    ManualService
)
from pin_utils.django_utils import (
    get_int,
    JsonResponse,
    get_object_or_none,
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    StaffRequiredMixin,
    CSRFExemptMixin
)

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)
from pin_utils.alipay.alipay_utils import (
    AlipayUtils
)


class OrderInfo(LoginRequiredMixin, View):
    '''
    购买信息抽象类，通过指定不同的model获取不同商品的信息
    '''

    model = None

    def get_order_info(self):
        pid = get_int(self.request.GET.get('pid', ''))
        info_model = get_object_or_404(self.model, pk=pid)
        order_info = {
            'price': info_model.price,
            'product_name': info_model.product_name,
            'product_type': info_model.get_product_type,
        }
        return order_info

    def get(self, request):

        if not self.model:
            raise Http404

        order_info = self.get_order_info()
        user = request.user
        pinbot_point = point_utils._get_pinbot_point(user)
        coin = pinbot_point.coin

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'order_info': order_info,
            'coin': coin,
        })


class CoinOrderInfo(OrderInfo):
    '''
    金币购买信息
    '''
    model = Coin


class PointOrderInfo(OrderInfo):
    '''
    聘点购买信息
    '''
    model = PinbotPoint


class ManualServiceOrderInfo(OrderInfo):
    '''
    省心服务购买信息
    '''
    model = PackageItem


class SelfOrderInfo(OrderInfo):
    '''
    自助服务购买信息
    '''
    model = VipRoleSetting


class PayOrderInfo(OrderInfo):
    '''
    查看生成订单商品信息
    '''

    def get_order_info(self):
        order_id = get_int(self.request.GET.get('order_id', ''))
        order_record_query = ItemRecord.objects.filter(
            order__id=order_id,
        )

        if not order_record_query:
            raise Http404

        order_item = order_record_query[0].item
        order_info = {
            'price': order_item.get_price(),
            'product_name': order_item.get_product_name(),
        }
        return order_info


class GetUserOrderList(LoginRequiredMixin, View):

    template_name = 'user_order_list.html'

    def get(self, request, order_status):
        self.user = request.user

        if order_status:
            order_list = OrderManage.get_order_list(
                user=self.user,
                order_status=order_status
            )
        else:
            order_list = OrderManage.get_order_list(
                user=self.user
            )

        return render(
            request,
            self.template_name,
            {
                'order_list': order_list,
            }
        )


class ChangeUserOrderStatus(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request):
        self.user = request.user
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        OrderManage.change_order_status(
            user=self.user,
            order_id=order_id,
            status=status
        )
        return JsonResponse({
            'status': 'ok',
            'msg': '更新订单状态成功'
        })


class CoinPaidOrder(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        order_id = request.POST.get('order_id')

        ret = OrderManage.paid_order(
            order_id=order_id,
            user=user
        )

        if ret:
            return JsonResponse({
                'status': 'ok',
                'msg': '订单支付成功'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': '订单支付失败'
            })


class CreateUserOrder(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
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

        pay_url = ''
        if payment_terms == 'alipay':

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

        if payment_terms == 'coin':
            pay_url = reverse('vip-coin-paid-order')

        return JsonResponse({
            'status': 'ok',
            'msg': '订单生成成功',
            'pay_url': pay_url,
            'order_id': order.order_id,
            'payment_terms': order.payment_terms,
            'order_price': order.order_price
        })


class Repaid(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        order_id = request.POST.get('order_id')

        order = OrderManage.get_order_info(
            order_id=order_id,
            user=user,
        )
        payment_terms = order.payment_terms

        if order.order_status != 'unpay':
            return JsonResponse({
                'status': 'error',
                'msg': '申请重新支付失败',
            })

        pay_url = ''

        if payment_terms == 'alipay':

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
                extra_common_param=order.item.get_product_type
            )

        if payment_terms == 'coin':
            pay_url = reverse('vip-coin-paid-order')

        return JsonResponse({
            'status': 'ok',
            'msg': '申请重新支付订单成功',
            'pay_url': pay_url,
            'order_id': order.order_id,
            'payment_terms': order.payment_terms
        })


class GetSelfServiceSelect(LoginRequiredMixin, PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 15

    def get_queryset(self):
        query = VipRoleSetting.objects.filter(is_show=True)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(GetSelfServiceSelect, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        manual_srv = ManualService()
        user = self.request.user
        has_manual_service = manual_srv.has_active_service(
            user=user
        )
        context['data'] = [
            {
                'pid': d.id,
                'name': d.product_name,
                'code_name': d.code_name,
                'pinbot_point': d.pinbot_point,
                'feed_count': d.feed_count,
                'price': d.price,
                'allow_buy': True,
                'is_show': d.is_show,
                'index': d.index,
                'has_manual_service': has_manual_service,
                'product_type': d.get_product_type,

            }
            for d in data
        ]
        return context


class GetSelfServiceSelectExample(PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 15

    def get_queryset(self):
        query = VipRoleSetting.objects.filter(is_show=True)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(GetSelfServiceSelectExample, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        context['data'] = [
            {
                'pid': d.id,
                'name': d.product_name,
                'code_name': d.code_name,
                'pinbot_point': d.pinbot_point,
                'feed_count': d.feed_count,
                'price': d.price,
                'is_show': d.is_show,
                'index': d.index,
                'product_type': d.get_product_type,

            }
            for d in data
        ]
        return context


class GetManualServiceSelect(LoginRequiredMixin, PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 15

    def get_queryset(self):
        query = PackageItem.objects.filter(status='enable', is_show=True)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(GetManualServiceSelect, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        context['data'] = [
            {
                'pid': d.id,
                'name': d.product_name,
                'code_name': d.code_name,
                'pinbot_point': d.pinbot_point,
                'feed_count': d.feed_count,
                'price': d.price,
                'salary_range': d.salary_range,
                'service_month': d.service_month,
                'candidate_num': d.candidate_num,
                'desc': d.desc,
                'is_commend': d.is_commend,
                'product_type': d.get_product_type,
                'is_show': d.is_show,
            }
            for d in data
        ]
        return context


class VipRoleInfoExample(View):

    template_name = 'register_select_level_example.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(
                reverse('vip-role-info')
            )
        else:
            return render(
                request,
                self.template_name,
                {}
            )


class GetManualServiceSelectExample(PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 15

    def get_queryset(self):
        query = PackageItem.objects.filter(status='enable', is_show=True)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(GetManualServiceSelectExample, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        context['data'] = [
            {
                'pid': d.id,
                'name': d.product_name,
                'code_name': d.code_name,
                'pinbot_point': d.pinbot_point,
                'feed_count': d.feed_count,
                'price': d.price,
                'salary_range': d.salary_range,
                'service_month': d.service_month,
                'candidate_num': d.candidate_num,
                'desc': d.desc,
                'is_commend': d.is_commend,
                'product_type': d.get_product_type,
                'is_show': d.is_show,
            }
            for d in data
        ]
        return context


class CloseOrder(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request):
        user = request.user
        service_id = request.POST.get('service_id')
        order_id = ServiceUtils.get_order_by_manual_serviceid(
            service_id=service_id
        ).order_id
        ret = OrderManage.close_order(
            order_id=order_id,
            user=user
        )

        if ret:
            return JsonResponse({
                'status': 'ok',
                'msg': '关闭订单成功'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': '关闭订单失败'
            })


class DeleteOrder(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request):
        user = request.user
        order_id = request.POST.get('order_id')
        service_id = request.POST.get('service_id')

        if service_id:
            order_id = ServiceUtils.get_order_by_manual_serviceid(
                service_id=order_id
            ).order_id

        ret = OrderManage.delete_order(
            order_id=order_id,
            user=user
        )

        if ret:
            return JsonResponse({
                'status': 'ok',
                'msg': '取消订单成功'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': '取消订单失败'
            })


class CancelOrder(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request):
        user = request.user
        service_id = request.POST.get('service_id')
        if service_id:
            order = ServiceUtils.get_order_by_manual_serviceid(
                service_id=service_id
            )
            order_id = order.order_id

        ret = OrderManage.cancel_order(
            order_id=order_id,
            user=user
        )

        if ret:
            return JsonResponse({
                'status': 'ok',
                'msg': '取消订单成功'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': '取消订单失败'
            })


class RefundOrder(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request):
        user = request.user
        service_id = request.POST.get('service_id')
        order = ServiceUtils.get_order_by_manual_serviceid(
            service_id=service_id
        )

        ret = OrderManage.refund_order(
            order_id=order.order_id,
            service_id=service_id,
            user=user
        )

        refund_doc = ret.get('refund_info')
        refund_doc['pay_fee'] = order.order_price

        if ret.get('service_result'):
            return JsonResponse({
                'status': 'ok',
                'msg': '申请订单退款成功',
                'data': ret.get('refund_info')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': '申请订单退款失败'
            })


class CancelRefundOrder(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request):
        user = request.user
        service_id = request.POST.get('service_id')
        order_id = ServiceUtils.get_order_by_manual_serviceid(
            service_id=service_id
        ).order_id
        ret = OrderManage.cancel_refund_order(
            order_id=order_id,
            user=user
        )

        if ret:
            return JsonResponse({
                'status': 'ok',
                'msg': '取消订单退款成功'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': '取消订单退款失败'
            })


class ConfirmRefundOrder(StaffRequiredMixin, View):

    @transaction.atomic
    @record_operate_admin('refunded')
    def post(self, request, op_id):
        user = request.user
        order_id = op_id

        ret = OrderManage.confirm_refund_order(
            order_id=order_id,
            user=user
        )

        if ret:
            return JsonResponse({
                'status': 'ok',
                'msg': '确认订单退款成功'
            })


class ApplyUserManualService(StaffRequiredMixin, View):

    @transaction.atomic
    @record_operate_admin('apply_manual_service')
    def post(self, request, manual_service_id):
        order = ServiceUtils.get_order_by_manual_serviceid(
            service_id=manual_service_id
        )
        if not order:
            raise Http404

        user = order.user
        OrderManage.paid_order(
            order_id=order.order_id,
            user=user
        )

        if request.POST.get('pay_status') == 'continue':
            UserManualService.objects.filter(
                id=manual_service_id
            ).update(
                status='continue'
            )

        return JsonResponse({
            'result': 'success',
            'new_data': {'offline_pay': u'操作成功'},
            'new_html': {'offline_pay': u'操作成功'},
        })


class VipApplySuccessMixin(object):

    def order_already_success(self, order_id):
        order = get_object_or_none(
            UserOrder,
            order_id=order_id,
            order_status='paid',
        )
        return order if order else False

    def make_order_success(self):

        order_id = self.request.REQUEST.get('out_trade_no')

        success_order = self.order_already_success(order_id)
        if success_order:
            return success_order

        order_obj = get_object_or_none(UserOrder, order_id=order_id)
        ret = OrderManage.paid_order(
            order_id=order_id,
            user=order_obj.user
        )
        return ret


class OrderAlipayReturn(LoginRequiredMixin, View, VipApplySuccessMixin):

    template_name = 'register_finish.html'

    @transaction.atomic
    def get(self, request):
        alipay_success = AlipayUtils.verify_alipay_notify(request.REQUEST)
        self.make_order_success() if alipay_success else None
        order_id = self.request.REQUEST.get('out_trade_no')
        extra_common_param = self.request.REQUEST.get('extra_common_param')
        order = OrderManage.get_order_info(
            order_id=order_id
        )
        return render(
            request,
            self.template_name,
            {
                'order': order,
                'extra_common_param': extra_common_param
            },
        )


class OrderAlipayNotify(CSRFExemptMixin, View, VipApplySuccessMixin):

    @transaction.atomic
    def get(self, request):
        alipay_success = AlipayUtils.verify_alipay_notify(request.REQUEST)

        if not alipay_success:
            return HttpResponse('fail')

        order_result = self.make_order_success()
        if order_result:
            return HttpResponse('success')

        return HttpResponse('fail')

    @transaction.atomic
    def post(self, request):
        return self.get(request)


class OrderAlipayResult(LoginRequiredMixin, View):

    template = 'register_finish.html'

    def get(self, request, order_id):
        self.template = 'vip_result.html'

        return render(
            request,
            self.template,
            {
                'order':
                {
                    'order_status': 'paid',
                    'subject_name': 'subject_name',
                    'order_price': 'order_price'
                }
            },
        )


class GetOrderStatus(LoginRequiredMixin, View):

    def post(self, request):
        order_id = request.POST.get('order_id')
        user = request.user

        order = OrderManage.get_order_info(
            order_id=order_id,
            user=user,
        )
        if not order:
            return JsonResponse({
                'status': 'error',
                'msg': '权限错误',
            })

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'order_id': order_id,
            'order_status': order.order_status,
        })


class GetCurrentUserInfo(LoginRequiredMixin, View):

    def get_pinbot_account(self):
        user = self.request.user
        point = point_utils._get_pinbot_point(user)
        data = {
            'coin': point.coin,
            'pinbot_point': point.point,
        }
        return data

    def get_manual_service(self):
        user = self.request.user
        service_utils = ManualService()
        if not service_utils.has_active_service(user=user):
            return {}

        data = {
            'user_status': '省心型用户',
            'can_update': False,
            'is_expired': False,
            'is_manual_service_user': True,
            'user_type': 'manual',
        }
        return data

    def get_self_service(self):
        user = self.request.user
        service_utils = SelfService()
        user_vip = service_utils.get_current_active_service(user=user)
        if not user_vip:
            return {}

        vip_role = user_vip.vip_role
        feed_count = user_vip.custom_feed if user_vip.custom_feed else vip_role.feed_count
        data = {
            'user_vip_id': user_vip.id,
            'user_status': vip_role.product_name,
            'feed_count': feed_count,
            'self_pinbot_point': vip_role.pinbot_point,
            'month_price': vip_role.month_price,
            'active_time': user_vip.active_time,
            'expire_time': user_vip.expire_time,
            'is_expire': False,
            'can_update': True,
            'is_experience_user': True if vip_role.code_name == 'experience_user' else False,
            'user_type': 'self' if vip_role.code_name != 'experience_user' else 'experience',
        }
        return data

    def get(self, request):
        ret = {
            'status': 'ok',
            'msg': 'ok',
            'is_expired': True,
            'can_update': False,
            'is_experience_user': False,
            'is_manual_service_user': False,
            'user_status': '套餐用户',
            'user_type': 'package',
        }

        account_info = self.get_pinbot_account()
        ret.update(account_info)
        ret['account'] = account_info

        manual_info = self.get_manual_service()
        if manual_info:
            ret.update(manual_info)
            return JsonResponse(ret)

        self_info = self.get_self_service()
        ret.update(self_info)

        return JsonResponse(ret)


class OfflinePaySuccess(StaffRequiredMixin, View, VipApplySuccessMixin):

    @transaction.atomic
    def post(self, request, order_id):
        order = OrderManage.get_order_info(
            order_id=order_id
        )
        if order:

            OrderManage.paid_order(
                order_id=order.order_id,
                user=order.user
            )
            order.payment_terms = 'offline'
            order.order_status = 'paid'
            order.save()
        return JsonResponse({
            'result': 'success',
            'new_data': {'offline_pay': u'支付成功'},
            'new_html': {'offline_pay': u'支付成功'},
        })


class OrderPreRefund(LoginRequiredMixin, View):

    @transaction.atomic
    def get(self, request, service_id):
        user = request.user
        order = ServiceUtils.get_order_by_manual_serviceid(
            service_id=service_id
        )
        if not order:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '订单未找到!'
                }
            )

        if order.item.get_product_type != 'manual_service':
            return JsonResponse({
                'status': 'error',
                'msg': '非省心型服务无法退款!'
            })

        if order.user != user:
            return JsonResponse({
                'status': 'error',
                'msg': '没有查看权限!'
            })

        refund_doc = OrderManage.get_refund_info(
            service_id=service_id,
        )
        refund_doc['pay_fee'] = order.order_price
        if refund_doc:
            return JsonResponse({
                'status': 'ok',
                'msg': '查看退款申请',
                'data': refund_doc
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': '申请订单退款失败'
            })
