# coding: utf-8

import hashlib
from uuid import uuid1

from django.shortcuts import render
from django.views.generic import View, ListView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.decorators import method_decorator

from .models import (
    PromotionToken,
    PromotionPointRecord,
    PromotionClickRecord,
)

from app.weixin.runtime.weixin_utils import WeixinService

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)

from pin_utils.django_utils import (
    get_object_or_none,
    get_today,
    JsonResponse,
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.cache_response import cache_response


class PromotionLink(LoginRequiredMixin, View):
    template_name = 'promotion_link.html'

    no_permission_tpl = 'no_promotion_perms.html'

    def _save_generate_token(self, user):
        username = user.username
        token = hashlib.md5(
            username + str(uuid1()).replace('-', '')
        ).hexdigest()

        promotion_token = PromotionToken(
            promotion_user=user,
            token=token,
        )
        promotion_token.save()
        return promotion_token

    def _get_promotion_token(self):
        user = self.request.user
        promotion_token = get_object_or_none(
            PromotionToken,
            promotion_user=user,
        )

        if not promotion_token:
            promotion_token = self._save_generate_token(user)
        return promotion_token

    def _get_promotion_link(self):
        promotion_token = self._get_promotion_token()
        login_url = self.request.build_absolute_uri(
            reverse('user-account-reg')
        )
        promotion_link = '%s?promotion_token=%s' % (
            login_url,
            promotion_token.token,
        )

        short_link_ret = WeixinService.get_short_url(promotion_link)
        if short_link_ret.get('errcode') == 0:
            promotion_link = short_link_ret.get('short_url', promotion_link)

        return promotion_link, promotion_token.token

    def _get_qr_code_link(self, token):
        register_link = settings.MOBILE_REGISTER_LINK
        company_name = self.request.user.userprofile.company_name
        name = self.request.user.userprofile.name
        username = '{0}{1}'.format(company_name, name)

        qr_code_link = '{0}?username={1}&promotion_token={2}'.format(
            register_link,
            username,
            token
        )

        short_link_ret = WeixinService.get_short_url(qr_code_link)
        if short_link_ret.get('errcode') == 0:
            qr_code_link = short_link_ret.get('short_url', qr_code_link)

        return qr_code_link

    @method_decorator(cache_response(cache_time=180))
    def get(self, request):
        promotion_link, token = self._get_promotion_link()
        qr_code_link = self._get_qr_code_link(token)

        return render(
            request,
            self.template_name,
            {
                'promotion_link': promotion_link,
                'token': token,
                'qr_code_link': qr_code_link,
            },
        )


class PromotionRecordList(LoginRequiredMixin, ListView):
    context_object_name = 'promotion_point_records'
    template_name = 'promotion_record_list.html'
    model = PromotionPointRecord

    no_permission_tpl = 'no_promotion_perms.html'

    def get_queryset(self):
        user = self.request.user
        promotion_point_records = self.model.objects.select_related(
            'register_user',
        ).filter(
            promotion_user=user,
            verify_status=1,
        ).order_by('-id')
        return promotion_point_records


class PromotionRecordJson(LoginRequiredMixin, PaginatedJSONListView):
    model = PromotionPointRecord
    context_object_name = 'data'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        promotion_point_records = self.model.objects.select_related(
            'register_user',
        ).filter(
            promotion_user=user,
            verify_status=1,
        ).order_by('-id')
        return promotion_point_records

    def get_dict_data(self, data):
        dict_data = [
            {
                'id': record.id,
                'register_username': record.register_user.username,
                'register_company_name': record.register_user.first_name,
                'point': record.point,
                'coin': record.coin,
                'promotion_date': record.promotion_date.strftime('%Y-%m-%d %H:%M'),
            }
            for record in data
        ]
        return dict_data

    def get_context_data(self, *args, **kwargs):
        context = super(PromotionRecordJson, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        dict_data = self.get_dict_data(data)
        context['data'] = dict_data
        context['status'] = 'ok'
        context['msg'] = 'ok'
        return context


class SavePromotionClick(LoginRequiredMixin, View):

    def get(self, request, token):
        user = request.user
        today = get_today()

        promotion_token = get_object_or_none(
            PromotionToken,
            promotion_user=user,
            token=token,
        )
        if not promotion_token:
            return JsonResponse({
                'status': 'token_error',
                'msg': 'token 不存在',
            })

        click_record = get_object_or_none(
            PromotionClickRecord,
            user=user,
            click_date=today,
        )
        if click_record:
            click_record.click_times += 1
        else:
            click_record = PromotionClickRecord(
                user=user,
            )
        click_record.save()

        return JsonResponse({
            'status': 'ok',
            'msg': u'记录成功',
        })
