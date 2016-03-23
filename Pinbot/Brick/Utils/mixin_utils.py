# coding: utf-8

import datetime

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from Brick.forms import CaptchaForm


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CSRFExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class StaffRequiredMixin(object):

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class MaliceMixin(object):

    MAX_ERROR_TIMES = 3
    EXPIRE_SECOND = 60 * 10
    MALICE_IP_PREFIX = ''
    MALICE_USER_PREFIX = ''

    def get_expire_time(self):
        expire_time = datetime.timedelta(seconds=self.EXPIRE_SECOND).total_seconds()
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

    def clear_malice(self):
        ip = self.request.environ['REMOTE_ADDR']
        malice_key = self.get_malice_key(self.MALICE_IP_PREFIX, ip)
        cache.delete(malice_key)
        return True


class AjAxValidCaptcha(object):
    form = CaptchaForm
    METHOD = ''

    def valid_captcha(self):
        form = CaptchaForm(self.request.GET if self.METHOD == 'GET' else self.request.POST)

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
