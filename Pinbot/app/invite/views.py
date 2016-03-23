# coding: utf-8

import shortuuid

from django.db import transaction
from django.views.generic import View
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

from .models import (
    InviteCodeApply,
    InviteCode,
)
from .forms import InviteCodeApplyForm

from pin_utils.django_utils import (
    JsonResponse,
    get_object_or_none,
    error_email,
)
from pin_utils.mixin_utils import (
    StaffRequiredMixin,
    MaliceMixin,
)
from pin_utils.email.send_mail import (
    asyn_send_mail,
)


class ApplyInviteCode(View, MaliceMixin):

    MALICE_IP_PREFIX = 'APPLY_CODE_IP_'
    EXPIRE_SECOND = 60 * 60 * 24
    MAX_ERROR_TIMES = 5

    template = 'apply_code.html'

    def get(self, request):
        host = request.get_host()
        if host == 'www.pinbot.me':
            return redirect('http://qz.pinbot.me')

        form = InviteCodeApplyForm()
        return render(
            request,
            self.template,
            {'form': form},
        )

    def post(self, request):
        form = InviteCodeApplyForm(request.POST, request=request)

        if form.is_valid():
            if self.malice_ip():
                return JsonResponse({
                    'status': 'malice_ip',
                    'msg': '提交太频繁了！休息一下再试吧',
                })
            form.save()
            result = {
                'status': 'ok',
                'msg': '申请已提交',
            }
        else:
            result = {
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            }
        return JsonResponse(result)


class CheckApplyEmail(View):

    def get(self, request):
        email = request.GET.get('email', '')
        if error_email(email):
            return JsonResponse({
                'status': 'form_error',
                'msg': '请输入正确的邮箱！',
            })

        has_apply = get_object_or_none(
            InviteCodeApply,
            email=email,
        )
        if has_apply:
            return JsonResponse({
                'status': 'has_apply',
                'msg': '你的邮箱已经申请过！',
            })
        return JsonResponse({
            'status': 'ok',
            'msg': '可以使用',
        })


class ApplyOperation(StaffRequiredMixin, View):

    success_email_tpl = 'apply_beta_success_email.html'
    success_email_subject = '【聘宝求职版】你的内测申请已通过'

    fail_email_tpl = 'apply_fail_email.html'
    fail_email_subject = '【聘宝求职版】感谢支持，咱们公测时再见！'

    def make_apply_fail(self, apply_info):
        if apply_info.status == 'success':
            result = {
                'result': 'success',
                'new_data': {'status': u'不能修改'},
                'new_html': {'status': u'不能修改'},
            }
            return result

        apply_info.status = 'fail'
        apply_info.save()

        email = apply_info.email
        html = render_to_string(
            self.fail_email_tpl,
            {
                'request': self.request,
            },
        )
        asyn_send_mail.delay(email, self.fail_email_subject, html)
        result = {
            'result': 'success',
            'new_data': {'status': u'申请失败'},
            'new_html': {'status': u'申请失败'},
        }
        return result

    def make_apply_success(self, apply_info):
        if apply_info.status == 'fail':
            result = {
                'result': 'success',
                'new_data': {'status': u'不能修改'},
                'new_html': {'status': u'不能修改'},
            }
            return result

        with transaction.atomic():
            if not apply_info.invite_code:
                code = shortuuid.ShortUUID().random(length=10)
                invite_code = InviteCode()
                invite_code.code = code
                invite_code.save()
                apply_info.invite_code = invite_code.code
            apply_info.status = 'success'
            apply_info.save()

        email = apply_info.email
        html = render_to_string(
            self.success_email_tpl,
            {
                'code': apply_info.invite_code,
                'request': self.request,
            },
        )
        asyn_send_mail.delay(email, self.success_email_subject, html)
        result = {
            'result': 'success',
            'new_data': {'status': u'邀请码已发送'},
            'new_html': {'status': u'邀请码已发送'},
        }
        return result

    def post(self, request, apply_id):
        apply_info = get_object_or_none(
            InviteCodeApply,
            id=apply_id,
        )
        operation = request.POST.get('operation')
        if not apply_info or operation not in ('success', 'fail'):
            return JsonResponse({
                'result': 'success',
                'new_data': {'apply_verify': u'数据有误'},
                'new_html': {'apply_verify': u'数据有误'},
            })

        if operation == 'success':
            result = self.make_apply_success(apply_info)

        else:
            result = self.make_apply_fail(apply_info)

        return JsonResponse(result)


class RedirectApplyCode(View):

    def get(self, request):
        return redirect('invite-apply-code')
