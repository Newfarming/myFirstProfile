# coding: utf-8

import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.http import HttpResponse

from Pinbot.settings import LOGIN_URL

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from transaction.models import UserChargePackage
from points.views import get_total_points
from Pinbot.forms import CaptchaForm
from app.pinbot_point.point_utils import point_utils

from .django_utils import JsonResponse


class LoginRequiredMixin(object):

    def is_token_auth(self):
        request = self.request
        user = None
        token = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')

        user = request.POST.get('user', request.GET.get('user'))
        token = request.POST.get('token', request.GET.get('token'))

        # 格式不对的token会导致报错，忽略掉
        try:
            if not (user and token) and basic_auth:
                auth_method, auth_string = basic_auth.split(' ', 1)

                if auth_method.lower() == 'basic':
                    auth_string = auth_string.strip().decode('base64')
                    user, token = auth_string.split(':', 1)

            if not (user and token):
                return False

            user = authenticate(pk=user, token=token)
        except:
            return False

        if user:
            login(request, user)
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() or self.is_token_auth():
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

        if request.is_ajax():
            return JsonResponse({
                'status': 'no_auth',
                'msg': '请先登录',
            })

        return redirect('{0}?next={1}'.format(LOGIN_URL, request.path))


class PackageRequiredMixin(object):
    no_permission_tpl = ''

    def check_package(self, request, *args, **kwargs):
        user_charges_pkgs = UserChargePackage.objects.filter(
            user=request.user,
            pay_status='finished',
        )

        if user_charges_pkgs:
            return True
        return False

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_package(request, *args, **kwargs):
            return render(
                request,
                self.no_permission_tpl,
                {},
            )
        return super(PackageRequiredMixin, self).dispatch(request, *args, **kwargs)


class CSRFExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class StaffRequiredMixin(object):

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class ResumePointsRequired(object):
    need_point = 10

    def get_pkg_points(self, user):
        total_points = 0
        user_pkgs = UserChargePackage.objects.filter(user=user, package_type=1)
        user_charges_pkgs = user_pkgs.filter(
            resume_end_time__gte=datetime.datetime.now(), pay_status='finished')
        for user_charges_pkg in user_charges_pkgs:
            total_points += user_charges_pkg.rest_points + \
                user_charges_pkg.re_points
        return total_points

    def get_user_points(self, user):
        return get_total_points(user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        pkg_point, pinbot_point = point_utils.get_user_point(request.user)
        total_points = pkg_point + pinbot_point
        if total_points >= self.need_point:
            return super(ResumePointsRequired, self).dispatch(request, *args, **kwargs)
        else:
            json_data = {
                'data': 3,
                'status': False,
                'error_dict': u'3.点数不够',
                'msg': '聘点不足%s点' % self.need_point
            }
            return JsonResponse(json_data)


class MaliceMixin(object):

    MAX_ERROR_TIMES = 3
    EXPIRE_SECOND = 60 * 10
    MALICE_IP_PREFIX = ''
    MALICE_USER_PREFIX = ''

    def get_expire_time(self):
        expire_time = datetime.timedelta(
            seconds=self.EXPIRE_SECOND).total_seconds()
        return expire_time

    def get_malice_key(self, prefix, value):
        return '%s%s' % (prefix, value)

    def malice_ip(self):
        ip = self.request.environ['REMOTE_ADDR']
        malice_key = self.get_malice_key(self.MALICE_IP_PREFIX, ip)
        malice_times = cache.get(malice_key, 1)
        expire_time = self.get_expire_time()
        if malice_times > self.MAX_ERROR_TIMES:
            cache.set(malice_key, malice_times, expire_time)
            return True
        else:
            malice_times += 1
            cache.set(malice_key, malice_times, expire_time)
            return False

    def clean_malice(self):
        ip = self.request.environ['REMOTE_ADDR']
        malice_key = self.get_malice_key(self.MALICE_IP_PREFIX, ip)
        cache.delete(malice_key)
        return True


class AjAxValidCaptcha(object):
    form = CaptchaForm
    METHOD = ''

    def valid_captcha(self):
        form = CaptchaForm(
            self.request.GET if self.METHOD == 'GET' else self.request.POST)

        if form.is_valid():
            result = {
                'status': 'success',
                'msg': u'验证码正确',
            }
        else:
            result = {
                'status': 'form_error',
                'msg': u'验证码错误'
            }
        captcha_key = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(captcha_key)
        result['captcha_url'] = captcha_url
        result['captcha_0'] = captcha_key
        return result


class NotMaliceGroupUser(object):
    malice_group = ''
    redirect_url = ''

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name=self.malice_group):
            return redirect(
                self.redirect_url
            )
        return super(NotMaliceGroupUser, self).dispatch(request, *args, **kwargs)


class GroupRequiredMixin(object):

    group_name = 'new_vip'
    redirect_url = ''

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser and not user.groups.filter(name=self.group_name):
            return redirect(
                self.redirect_url
            )
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)


class SpiderTokenRequiredMixin(LoginRequiredMixin):

    STAFF = False
    permission = 'spider_msg'

    def dispatch(self, request, *args, **kwargs):
        has_token_auth = self.is_token_auth()
        user = request.user
        is_staff = self.STAFF and request.user.is_staff
        has_permission = user.user_permissions.filter(codename=self.permission).exists()

        if has_token_auth and (is_staff or has_permission):
            return super(SpiderTokenRequiredMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponse(status=401)
