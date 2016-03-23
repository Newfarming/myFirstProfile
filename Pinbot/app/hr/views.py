# coding: utf-8

import shortuuid

from django.conf import settings
from django.core.cache import cache
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
)
from django.db import transaction

from tokenapi.tokens import token_generator

from .forms import (
    LoginForm,
    RegisterForm,
)

from ..promotion_point.promotion_utils import PromotionUtils
from ..vip.runtime.self_service import SelfServiceUtils
from ..weixin.runtime.weixin_utils import (
    WeixinService
)

from users.views import SendActiveMailMixin

from pin_utils.django_utils import (
    JsonResponse,
    get_object_or_none,
)
from pin_utils.mixin_utils import (
    CSRFExemptMixin,
    MaliceMixin,
    LoginRequiredMixin,
)


class Register(CSRFExemptMixin, View, SendActiveMailMixin):

    '''
    注册View
    '''
    email_template = 'client_active_email.html'
    form_obj = RegisterForm

    def active_weixin_register(self, user):
        request = self.request
        openid = request.session.get('openid')
        if not openid:
            return False

        WeixinService.bind_weixin_openid(user, openid)
        ret = WeixinService.update_weixin_userinfo(openid)
        return ret

    @transaction.atomic
    def post(self, request):
        form = self.form_obj(request.POST, request=request)

        if form.is_valid():
            user_profile = form.save()
            user = user_profile.user

            self.active_weixin_register(user)

            user.is_active = True
            user_profile.is_phone_bind = True

            user.save()
            user_profile.save()
            # 激活体验用户
            SelfServiceUtils.active_experience_service(user)
            # 记录推广注册信息
            PromotionUtils.register_promotion(request, user)
            PromotionUtils.promotion_success(user)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            auth_info = {
                'token': token_generator.make_token(user),
                'user': user.pk,
            }

            return JsonResponse({
                'status': 'ok',
                'msg': u'注册成功',
                'username': user.username,
                'auth_info': auth_info,
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': form.get_first_errors(),
                'errors': form.errors,
            })


class Login(CSRFExemptMixin, View, MaliceMixin):

    MAX_ERROR_TIMES = 5
    EXPIRE_SECOND = 60 * 2
    MALICE_IP_PREFIX = 'malice_login_ip_'

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return JsonResponse({
                'status': 'form_error',
                'msg': form.get_first_errors(),
                'errors': form.errors,
            })

        form_data = form.cleaned_data

        username = form_data['username']
        password = form_data['password']

        user = authenticate(
            username=username,
            password=password,
        )

        if not user.is_active:
            return JsonResponse({
                'status': 'not_active',
                'msg': '用户未激活',
            })

        if not hasattr(user, 'userprofile'):
            return JsonResponse({
                'status': 'not_hr',
                'msg': '不是有效的HR用户，请更换邮箱注册HR用户',
            })

        if self.malice_ip():
            return JsonResponse({
                'status': 'malice_login',
                'msg': '登录错误次数过多，请稍后再试',
            })

        login(request, user)
        auth_info = {
            'token': token_generator.make_token(user),
            'user': user.pk,
        }
        openid = request.session.get('openid')
        WeixinService.bind_weixin_openid(user, openid)
        WeixinService.update_weixin_userinfo(openid)

        self.clean_malice()

        industrys = user.company_set.all().values_list('category__industry__code_name', flat=True)
        user_industry = industrys[0] if len(industrys) > 0 else ''

        return JsonResponse({
            'status': 'ok',
            'msg': '登录成功',
            'username': user.username,
            'auth_info': auth_info,
            'user_industry': user_industry
        })


class WeixinAuth(View):

    def get(self, request):
        session = request.session
        openid = session.get('openid')

        if not openid:
            return JsonResponse({
                'status': 'auth_fail',
                'msg': 'auth fail',
                'auth_info': {},
            })

        weixin_user = WeixinService.get_weixin_user(
            openid=openid
        )

        if weixin_user and weixin_user.user.is_active:
            industrys = weixin_user.user.company_set.all().values_list('category__industry__code_name', flat=True)
            user_industry = industrys[0] if len(industrys) > 0 else ''
            return JsonResponse({
                'status': 'ok',
                'msg': 'ok',
                'auth_info': {
                    'token': token_generator.make_token(weixin_user.user),
                    'user': weixin_user.user_id,
                },
                'username': weixin_user.user.username,
                'user_industry': user_industry
            })

        return JsonResponse({
            'status': 'auth_fail',
            'msg': 'auth fail',
            'auth_info': {}
        })


class ValidToken(View, MaliceMixin):

    MAX_ERROR_TIMES = 5
    EXPIRE_SECOND = 60 * 2
    MALICE_IP_PREFIX = 'malice_valid_token_ip_'

    def get(self, request, token, user):
        if self.malice_ip():
            return JsonResponse({
                'status': 'malice_check',
                'msg': '失败次数太多，请稍后尝试',
            })

        user = get_object_or_none(
            User,
            id=user,
        )
        if not user:
            return JsonResponse({
                'status': 'token_error',
                'msg': '无效token',
            })
        is_valid = token_generator.check_token(user, token)

        industrys = user.company_set.all().values_list('category__industry__code_name', flat=True)
        user_industry = industrys[0] if len(industrys) > 0 else ''

        if is_valid:
            self.clean_malice()
            return JsonResponse({
                'status': 'ok',
                'msg': '成功',
                'user_industry': user_industry
            })

        return JsonResponse({
            'status': 'token_error',
            'msg': '无效token',
        })


class UnbindWeixinOpenid(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        WeixinService.unbind_weixin_openid(user)

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class QRcodeBind(LoginRequiredMixin, View):

    def get(self, request):

        uid = str(request.user.id)
        uid_key = int(shortuuid.ShortUUID(alphabet="123456789").random(length=9))
        qr_uid_key = int('{:1d}{:9d}'.format(1, uid_key))

        res = WeixinService.create_qrcode(
            {
                "expire_seconds": settings.QRCODE_BIND_TOKEN_EXPIRE_TIME,
                "action_name": "QR_SCENE",
                "action_info": {
                    "scene": {
                        "scene_id": qr_uid_key
                    }
                }
            }
        )
        ticket = WeixinService.show_qrcode(
            res['ticket']
        )

        cache.set(
            uid_key,
            uid,
            settings.QRCODE_BIND_TOKEN_EXPIRE_TIME
        )

        return HttpResponse(ticket, mimetype="image/jpeg")


class QRcodeRedPack(View):

    def get(self, request):

        uid = str(request.user.id)
        uid_key = int(shortuuid.ShortUUID(alphabet="123456789").random(length=9))
        qr_uid_key = int('{:1d}{:9d}'.format(2, uid_key))

        res = WeixinService.create_qrcode(
            {
                "expire_seconds": settings.QRCODE_BIND_TOKEN_EXPIRE_TIME,
                "action_name": "QR_SCENE",
                "action_info": {
                    "scene": {
                        "scene_id": qr_uid_key
                    }
                }
            }
        )
        ticket = WeixinService.show_qrcode(
            res['ticket']
        )

        cache.set(
            uid_key,
            uid,
            settings.QRCODE_BIND_TOKEN_EXPIRE_TIME
        )

        return HttpResponse(ticket, mimetype="image/jpeg")