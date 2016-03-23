# coding: utf-8

import datetime

from dateutil.relativedelta import relativedelta

from django.views.generic import (
    View,
    ListView,
    TemplateView,
)
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import (
    VipRoleSetting,
    UserOrder,
    UserVip,
    WithdrawRecord,
    ItemRecord,
)
from .vip_utils import (
    VipRoleUtils,
)
from .runtime.self_service import (
    SelfServiceUtils,
)

from app.pinbot_point.point_utils import (
    point_utils,
    coin_utils,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    CSRFExemptMixin,
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    get_object_or_none,
    JsonResponse,
    get_float,
    get_int,
    get_today,
)
from pin_utils.order_utils import (
    create_order_id,
)
from pin_utils.alipay.alipay_utils import (
    AlipayUtils
)
from pin_utils.package_utils import (
    PackageUtils,
)
from pin_utils.pdf_utils import (
    PDFUtils,
)
from pin_utils.order_utils import (
    create_order_id as get_protocol_id
)


class VipUserRequiredMixin(object):

    redirect_url = '/vip/old_pkg_info/'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser and PackageUtils.has_base_pkg(user):
            return redirect(
                self.redirect_url
            )
        return super(VipUserRequiredMixin, self).dispatch(request, *args, **kwargs)


class VipRoleInfo(LoginRequiredMixin, VipUserRequiredMixin, ListView):

    context_object_name = 'data'
    template_name = 'register_select_level.html'

    def get_queryset(self):
        settings = VipRoleSetting.objects.filter(
            allow_apply=True,
        ).order_by('level')
        return settings

    def get_context_data(self, *args, **kwargs):
        context = super(VipRoleInfo, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['current_vip'] = VipRoleUtils.get_current_vip(user)
        return context


class OrderPaymentTerms(LoginRequiredMixin, VipUserRequiredMixin, TemplateView):

    template_name = 'register_select_payway.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderPaymentTerms, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['user_vip'] = VipRoleUtils.get_apply_vip(user)
        context['current_vip'] = VipRoleUtils.get_current_vip(user)
        return context


class DeleteUselessDataMixin(object):

    def delete_useless_order(self):
        '''
        删除没有完成的订单和vip数据
        '''
        UserOrder.objects.filter(
            order_status='unpay',
            user=self.user,
        ).delete()
        return True

    def delete_useless_user_vip(self):
        UserVip.objects.filter(
            apply_status='applying',
            user=self.user,
        ).delete()
        return True


class ApplyRole(LoginRequiredMixin, View, DeleteUselessDataMixin):

    def create_user_vip(self):
        user_vip = UserVip(
            user=self.user,
            vip_role=self.vip_role,
        )
        user_vip.save()
        return user_vip

    @transaction.atomic
    def get(self, request, role_id):
        self.user = request.user

        unsign_vip = VipRoleUtils.get_unsign_vip(self.user)
        if unsign_vip:
            return JsonResponse({
                'status': 'error',
                'msg': '还有未签订协议的vip服务，请先签订协议',
                'download_url': '/vip/download_contact/%s/' % unsign_vip.vip_role.id,
            })

        self.current_vip = VipRoleUtils.get_current_vip(self.user)
        current_vip_level = self.current_vip.vip_role.level if self.current_vip else 0

        self.vip_role = get_object_or_none(
            VipRoleSetting,
            id=role_id,
            allow_apply=True,
            level__gt=current_vip_level,
        )
        if not self.vip_role:
            return JsonResponse({
                'status': 'invalid',
                'msg': '请选择正确的vip服务',
            })

        self.create_user_vip()

        return JsonResponse({
            'status': 'ok',
            'msg': '申请成功',
            'redirect_url': reverse('vip-select-payway') if not self.current_vip else reverse('vip-upgrade-payment'),
        })


class CreateOrder(
        LoginRequiredMixin,
        VipUserRequiredMixin,
        View,
        DeleteUselessDataMixin):

    def get_order_price(self):
        vip_role = self.apply_vip.vip_role
        vip_price = vip_role.price
        user_vip_query = self.user.vip_roles.select_related(
            'vip_role'
        ).filter(is_active=True)
        if user_vip_query:
            order_price = vip_price - user_vip_query[0].vip_role.price
        else:
            order_price = vip_price
        return order_price

    def create_order(self):
        price = self.get_order_price()
        order = UserOrder.objects.create(
            user=self.user,
            order_price=price,
            actual_price=price,
            item=self.apply_vip,
        )

        order.order_id = create_order_id()

        order.save()
        return order

    @transaction.atomic
    def get(self, request):
        self.user = request.user
        self.apply_vip = VipRoleUtils.get_apply_vip(self.user)
        if not self.apply_vip:
            return JsonResponse({
                'status': 'apply_error',
                'msg': '没有申请信息',
            })

        order = self.create_order()
        alipay_return_url = request.build_absolute_uri(
            reverse('vip-alipay-return')
        )
        alipay_notify_url = request.build_absolute_uri(
            reverse('vip-alipay-notify')
        )
        pay_url = AlipayUtils.submit_order_url(
            order,
            return_url=alipay_return_url,
            notify_url=alipay_notify_url,
            order_price=order.order_price,
        )

        return JsonResponse({
            'status': 'ok',
            'msg': '订单生成成功',
            'pay_url': pay_url,
            'order_id': order.id,
        })


class VipApplySuccessMixin(object):

    def update_vip_perms(self, user_vip, admin=False):
        if user_vip.vip_role.auto_active or admin:
            user = user_vip.user
            taocv_perm = get_object_or_none(
                Permission,
                codename='visit_taocv',
            )
            feed_perm = get_object_or_none(
                Permission,
                codename='visit_feed',
            )
            user.user_permissions.add(taocv_perm, feed_perm)
            return True
        return False

    def order_already_success(self, order_id):
        order = get_object_or_none(
            UserOrder,
            order_id=order_id,
            order_status='paid',
        )
        return order if order else False

    def update_guide_switch(self, user):
        current_vip = VipRoleUtils.get_current_vip(user)
        if current_vip:
            return False
        user.userprofile.guide_switch = True
        user.userprofile.save()
        return user

    def update_user_vip(self, user_vip, admin=False):
        user_vip.apply_status = 'success'
        user = user_vip.user

        if user_vip.vip_role.auto_active or admin:
            self.update_guide_switch(user)

            UserVip.objects.filter(
                user=user,
                is_active=True,
            ).update(
                is_active=False,
            )

            service_time = user_vip.vip_role.service_time
            now = datetime.datetime.now()
            today = get_today()
            expire_time = today + relativedelta(months=service_time)

            user_vip.is_active = True
            user_vip.active_time = now
            user_vip.expire_time = expire_time

        user_vip.save()
        UserVip.objects.filter(
            apply_status='applying',
            user=user,
        ).delete()
        return user_vip

    def update_vip_pkg(self, user_vip, admin=False):
        vip_role = user_vip.vip_role
        user = user_vip.user

        vip_feed_pkg = PackageUtils.get_vip_feed_pkg(user)
        if user_vip.vip_role.auto_active or admin:
            feed_count = vip_role.feed_count if not user_vip.custom_feed else user_vip.custom_feed
            add_count = feed_count - vip_feed_pkg.extra_feed_num
            if add_count > 0:
                vip_feed_pkg.rest_feed += add_count
                vip_feed_pkg.extra_feed_num += add_count
            vip_feed_pkg.pay_status = 'finished'
            vip_feed_pkg.feed_end_time = user_vip.expire_time
        vip_feed_pkg.save()

        return vip_feed_pkg

    def update_vip_point(self, user_vip, admin=False):
        if user_vip.vip_role.auto_active or admin:
            point_utils.vip_point(user_vip.user, vip_user=user_vip)

    def update_order(self, order_id, actual_price=None, payment_terms=None):
        order = get_object_or_none(
            UserOrder,
            order_id=order_id,
        )
        if not actual_price:
            actual_price = order.order_price

        now = datetime.datetime.now()

        order.order_status = 'paid'
        order.actual_price = actual_price
        order.pay_time = now

        if payment_terms:
            order.payment_terms = payment_terms
        order.save()

        UserOrder.objects.filter(
            order_status='unpay',
            item_content_type=ContentType.objects.get_for_model(order.item),
            user=order.user,
        ).delete()

        return order

    def make_order_success(self):
        order_id = self.request.REQUEST.get('out_trade_no')

        success_order = self.order_already_success(order_id)
        if success_order:
            return success_order

        actual_price = get_float(self.request.REQUEST.get('total_fee'))

        order = self.update_order(order_id, actual_price)
        self.update_user_vip(order.item)
        self.update_vip_pkg(order.item)
        self.update_vip_point(order.item)
        self.update_vip_perms(order.item)

        return order


class AlipayReturn(LoginRequiredMixin, View, VipApplySuccessMixin):

    template_name = 'register_finish.html'

    @transaction.atomic
    def get(self, request):
        alipay_success = AlipayUtils.verify_alipay_notify(request.REQUEST)

        order = self.make_order_success() if alipay_success else None
        user = self.request.user
        if VipRoleUtils.is_upgrade(user, order):
            self.template_name = 'vip_result.html'

        return render(
            request,
            self.template_name,
            {
                'order': order,
            }
        )


class AlipayNotify(CSRFExemptMixin, View, VipApplySuccessMixin):

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


class AlipayResult(LoginRequiredMixin, View):

    template = 'register_finish.html'

    def get(self, request, order_id):
        order = get_object_or_none(
            UserOrder,
            user=request.user,
            id=order_id,
        )

        user = self.request.user
        if VipRoleUtils.is_upgrade(user, order):
            self.template = 'vip_result.html'

        return render(
            request,
            self.template,
            {'order': order},
        )


class OfflinePaySuccess(StaffRequiredMixin, View, VipApplySuccessMixin):

    @transaction.atomic
    def post(self, request, order_id):
        order = self.update_order(order_id, payment_terms='offline')
        self.update_user_vip(order.item)
        return JsonResponse({
            'result': 'success',
            'new_data': {'offline_pay': u'支付成功'},
            'new_html': {'offline_pay': u'支付成功'},
        })


class ApplyUserVip(StaffRequiredMixin, View, VipApplySuccessMixin):

    @transaction.atomic
    def post(self, request, vip_id):
        user_vip_query = UserVip.objects.select_related(
            'user',
            'vip_role',
        ).filter(
            id=vip_id,
        )
        if not user_vip_query:
            raise Http404

        user_vip = user_vip_query[0]
        user = user_vip.user

        if not user_vip.is_active:
            self.update_user_vip(user_vip, admin=True)
            point_utils.self_service_point(user, user_vip)

        self.update_vip_pkg(user_vip, admin=True)
        self.update_vip_point(user_vip, admin=True)
        self.update_vip_perms(user_vip, admin=True)

        return JsonResponse({
            'result': 'success',
            'new_data': {'offline_pay': u'操作成功'},
            'new_html': {'offline_pay': u'操作成功'},
        })


class OldPkgInfo(LoginRequiredMixin, TemplateView):

    template_name = 'vip_old_pkg_info.html'


class DownloadPDFView(LoginRequiredMixin, View):

    template_name = 'service_contact.html'
    filename = '聘宝用户协议.pdf'

    def get_context_data(self, *args, **kwargs):
        vip_id = self.kwargs.get('vip_id', 0)
        vip_setting = get_object_or_none(
            VipRoleSetting,
            id=vip_id
        )
        return {
            'vip_setting': vip_setting,
            'protocol_id': get_protocol_id(length=4),
        }

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(*args, **kwargs)
        return PDFUtils.download_pdf(
            self.template_name,
            context_data,
            self.filename
        )


class Withdraw(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request):
        money = get_int(request.POST.get('money') or 0)
        if money <= 0:
            return JsonResponse({
                'status': 'money_error',
                'msg': '提现金额必须是大于0的整数',
            })

        user = request.user
        pinbot_point = coin_utils._get_pinbot_point(user)

        if money > pinbot_point.coin:
            return JsonResponse({
                'status': 'no_coin',
                'msg': '金币不足',
            })

        now = datetime.datetime.now()
        has_withdraw = get_object_or_none(
            WithdrawRecord,
            user=user,
            verify_status__in=(0, 1),
            create_time__year=now.year,
            create_time__month=now.month,
        )

        if has_withdraw:
            return JsonResponse({
                'status': 'has_withdraw',
                'msg': '您本月已经提现过一次，请下个月再来',
            })

        withdraw = WithdrawRecord.objects.create(
            user=user,
            money=money,
        )

        order = UserOrder.objects.create(
            user=user,
            order_price=-money,
            actual_price=-money,
            item=withdraw,
            order_desc='提现',
            order_type=5,
        )
        order.order_id = create_order_id()
        order.save()

        ItemRecord.objects.create(
            num=1,
            total_price=order.order_price,
            order=order,
            item=withdraw,
        )

        return JsonResponse({
            'status': 'ok',
            'msg': '提现请求提交成功',
        })


class WithdrawOperation(StaffRequiredMixin, View):

    def save_withdraw_record(self, withdraw_record, operation, verify_remark):
        now = datetime.datetime.now()
        withdraw_record.verify_status = operation
        withdraw_record.verify_time = now
        withdraw_record.verify_remark = verify_remark
        withdraw_record.save()
        return withdraw_record

    def save_userorder(self, withdraw_record, operation, verify_remark):
        userorder_query = UserOrder.objects.filter(
            item_content_type=ContentType.objects.get_for_model(withdraw_record),
            item_object_id=withdraw_record.id,
        )
        userorder = userorder_query[0]
        userorder.order_status = 'paid' if operation == 1 else 'fail'
        userorder.order_remark = verify_remark
        userorder.save()
        return userorder

    def save_pinbot_coin(self, withdraw_record, operation):
        if operation == 1:
            result, _ = coin_utils.withdraw_coin(
                withdraw_record.user,
                withdraw_record.money,
            )
        else:
            result = False
        return result

    @transaction.atomic
    def post(self, request, record_id):
        operation = get_int(request.POST.get('operation') or 0)
        verify_remark = request.POST.get('verify_remark', '')

        if operation not in (1, 2):
            return JsonResponse({
                'result': 'fail',
                'new_data': {'offline_pay': u'请选择操作'},
                'new_html': {'offline_pay': u'请选择操作'},
            })

        withdraw_record = get_object_or_none(
            WithdrawRecord,
            id=record_id,
        )

        if not withdraw_record:
            return JsonResponse({
                'result': 'fail',
                'new_data': {'offline_pay': u'无法找到记录'},
                'new_html': {'offline_pay': u'无法找到记录'},
            })

        user = withdraw_record.user
        pinbot_point = coin_utils._get_pinbot_point(user)
        if operation == 1 and pinbot_point.coin - withdraw_record.money < 0:
            return JsonResponse({
                'result': 'fail',
                'new_data': {'offline_pay': u'金币数不够'},
                'new_html': {'offline_pay': u'金币数不够'},
            })

        self.save_withdraw_record(withdraw_record, operation, verify_remark)
        self.save_userorder(withdraw_record, operation, verify_remark)
        self.save_pinbot_coin(withdraw_record, operation)

        return JsonResponse({
            'result': 'success',
            'new_data': {'offline_pay': u'操作成功'},
            'new_html': {'offline_pay': u'操作成功'},
        })


class DisableUserVip(StaffRequiredMixin, View, VipApplySuccessMixin):

    @transaction.atomic
    def post(self, request, vip_id):
        user_vip_query = UserVip.objects.select_related(
            'user',
        ).filter(
            id=vip_id,
        )
        if not user_vip_query:
            raise Http404

        expire_time = datetime.datetime.now()
        user_vip = user_vip_query[0]
        user = user_vip.user
        user_vip.expire_time = expire_time

        user_vip.save()
        SelfServiceUtils.set_experience_user(user)

        return JsonResponse({
            'result': 'success',
            'new_data': {'offline_pay': u'操作成功'},
            'new_html': {'offline_pay': u'操作成功'},
        })
