# coding: utf-8

import json
import datetime

from django.views.generic import View, ListView
from django.shortcuts import render

from transaction.models import (
    UserChargePackage
)
from app.pinbot_point.point_utils import (
    point_utils,
    coin_utils,
)
from app.pinbot_point.models import (
    PointRecord
)
from app.vip.models import (
    UserOrder,
    UserManualService,
)
from app.vip.vip_utils import (
    VipRoleUtils,
    WithdrawUtils,
)
from app.partner.partner_utils import (
    PartnerUtils,
)

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.package_utils import PackageUtils
from pin_utils.django_utils import (
    get_int,
    JsonResponse,
)


class MyPayment(LoginRequiredMixin, View):
    template = 'payment_pinbot_point_record.html'

    def get(self, request):
        user = request.user
        now = datetime.datetime.now()
        charge_pkgs = UserChargePackage.objects.select_related(
            'resume_package',
        ).filter(
            user=user,
            package_type=1,
            pay_status='finished',
            resume_end_time__gt=now,
        ).order_by('-resume_end_time')

        user_feeds = UserChargePackage.objects.select_related(
            'feed_package',
        ).filter(
            user=user,
            package_type=2,
            pay_status='finished',
            extra_feed_num__gt=0,
            feed_end_time__gt=now,
        ).order_by('-id')

        has_pkg = UserChargePackage.objects.filter(
            user=user,
            package_type=1,
            pay_status='finished',
            resume_end_time__gt=now,
        )

        user_point = point_utils.get_user_pinbot_point(user)
        pinbot_point = point_utils._get_pinbot_point(user)
        current_vip = VipRoleUtils.get_current_vip(user)
        highest_vip_level = VipRoleUtils.get_highest_vip_level()
        unsign_vip = VipRoleUtils.get_unsign_vip(user)
        rest_feed_count = PackageUtils.rest_feed_count(user)
        coin_stat = coin_utils.get_coin_statistic(user)
        withdraw_data = json.dumps(
            WithdrawUtils.get_withdraw_status(user),
            ensure_ascii=False
        )
        is_partner = PartnerUtils.is_partner(user)

        return render(
            request,
            self.template,
            {
                'charge_pkgs': charge_pkgs,
                'user_feeds': user_feeds,
                'user_point': user_point,
                'pinbot_point': pinbot_point,
                'current_vip': current_vip,
                'highest_vip_level': highest_vip_level,
                'unsign_vip': unsign_vip,
                'rest_feed_count': rest_feed_count,
                'has_pkg': has_pkg,
                'coin_stat': coin_stat,
                'withdraw_data': withdraw_data,
                'is_partner': is_partner,
            },
        )


class PaymentRecord(LoginRequiredMixin, PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 6

    def query_order_type(self, query_cond):
        record_type = get_int(self.request.GET.get('record_type', ''))
        query_keys = dict(UserOrder.ORDER_TYPE_META).keys()

        if record_type == -1:
            query_cond.update({'order_type__in': [1, 2, 3, 4, 6]})
            return query_cond

        if record_type == -2:
            query_cond.update({'order_type': 5})
            return query_cond

        if record_type not in query_keys:
            return query_cond

        query_cond.update({'order_type': record_type})
        return query_cond

    def query_order_status(self, query_cond):
        order_status = self.request.GET.get('order_status', '')
        if order_status not in dict(UserOrder.ORDER_STATUS_META).keys():
            return query_cond
        query_cond.update({'order_status': order_status})
        return query_cond

    def get_query_cond(self):
        query_cond = {}
        query_cond = self.query_order_type(query_cond)
        query_cond = self.query_order_status(query_cond)
        return query_cond

    def get_queryset(self):
        user = self.request.user
        query_cond = self.get_query_cond()
        user_orders = UserOrder.objects.filter(
            user=user,
            is_delete=False,
            **query_cond
        ).order_by('-id')

        return user_orders

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentRecord, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        context['data'] = [
            {
                'id': d.id,
                'order_id': d.order_id,
                'order_status': d.get_order_status_display(),
                'order_status_key': d.order_status,
                'actual_price': d.actual_price,
                'order_desc': d.order_desc,
                'create_time': d.create_time.strftime('%Y-%m-%d %H:%M'),
                'pay_time': d.pay_time.strftime('%Y-%m-%d %H:%M'),
                'order_type': d.get_order_type_display(),
                'order_type_key': d.order_type,
            }
            for d in data
        ]
        context['per_page'] = self.paginate_by
        return context


class ManualServiceList(LoginRequiredMixin, PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 6

    def query_pkg_status(self, query_cond):
        status = self.request.GET.get('status', '')
        if status not in dict(UserManualService.PACKAGE_STATUS_META).keys():
            return query_cond
        query_cond.update({'status': status})
        return query_cond

    def get_query_cond(self):
        query_cond = {}
        query_cond = self.query_pkg_status(query_cond)
        return query_cond

    def get_queryset(self):
        user = self.request.user
        query_cond = self.get_query_cond()
        queryset = UserManualService.objects.select_related(
            'item',
        ).filter(
            user=user,
            **query_cond
        ).order_by('-id')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ManualServiceList, self).get_context_data(*args, **kwargs)

        data = context.get('data', [])

        context['data'] = [
            {
                'id': d.id,
                'service_desc': d.item.get_desc,
                'price': d.order_price,
                'create_time': d.create_time.strftime('%Y-%m-%d %H:%M'),
                'active_time': d.active_time.strftime('%Y-%m-%d %H:%M'),
                'expire_time': d.expire_time.strftime('%Y-%m-%d %H:%M'),
                'status': d.get_status_display(),
                'is_insurance': d.is_insurance
            }
            for d in data
        ]
        context['per_page'] = self.paginate_by
        return context


class PinbotPointRecord(LoginRequiredMixin, ListView):

    context_object_name = 'point_record'
    template_name = 'my_payment_point_record.html'
    model = PointRecord

    def get_queryset(self):
        user = self.request.user
        records = self.model.objects.filter(
            user=user,
        ).order_by('-id')
        return records


class DeleteUserOrder(LoginRequiredMixin, View):

    def get(self, request):
        order_id = get_int(request.GET.get('obj_id', ''))
        UserOrder.objects.filter(
            id=order_id,
            user=request.user,
        ).update(
            is_delete=True,
        )
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok'
        })
