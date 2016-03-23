# coding: utf-8

from django.contrib.auth.models import (
    User
)

from django.utils.decorators import method_decorator
from pin_utils.cache_response import cache_response
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.urlresolvers import reverse
from django.views.generic import View
from forms import (
    AccountRegisterForm,
    AccountCompanyForm,
    AccountMyInfoForm,
    AccountMyPasswordForm,
    AccountMyRecvInfoForm,
    UserProfileForm
)
from .models import (
    NewIndustryBookin
)
from jobs.models import (
    Industry,
    CompanyCategory
)

from users.runtime.account import (
    PinbotAccount
)
from app.promotion_point.promotion_utils import PromotionUtils
from app.vip.runtime.self_service import(
    SelfService
)
from app.vip.vip_utils import VipRoleUtils
from pin_utils.email.email_code import (
    EmailCode
)
from pin_utils.sms.sms_code import (
    SmsCode,
    asyn_send_sms_code
)
from pin_utils.django_utils import (
    user_add_group,
    JsonResponse,
    error_phone,
    get_valid_next_url,
    get_int
)
from pin_utils.email.send_mail import (
    asyn_send_mail,
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    MaliceMixin,
    CSRFExemptMixin
)
from app.weixin.runtime.weixin_utils import (
    WeixinService
)


class ValidNotifyEmail(View):
    template = 'client_active_email_notify.html'

    def get(self, request, uidb64, activation_key):
        if uidb64 is not None and activation_key is not None:
            uid = get_int(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, id=uid)
            ret = default_token_generator.check_token(
                user,
                activation_key
            )
            if ret:
                user_profile = user.get_profile()
                user_profile.is_email_bind = True
                user_profile.guide_switch = True
                user_profile.save()
                # 开始登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                return render(
                    request,
                    self.template,
                    {
                        'status': 'ok',
                        'msg': u'绑定接收邮箱成功',
                    },
                )

        return render(
            request,
            self.template,
            {
                'status': 'error',
                'msg': u'无效的激活链接',
            }
        )


class SendVaildNotifyMailMixin(object):
    email_template = 'client_notify_email.html'
    change_notify_email_template = 'change_notify_email.html'
    subject = '聘宝验证接收邮箱'
    change_email_subject = '聘宝更换接收邮箱验证码'
    valid_url_name = 'user-valid-notify-email'

    def send_active_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        email = user.userprofile.user_email
        valid_url = self.request.build_absolute_uri(
            reverse(self.valid_url_name, args=(uid, token))
        )
        html = render_to_string(
            self.email_template,
            {
                'valid_url': valid_url,
            }
        )
        asyn_send_mail.delay(email, self.subject, html)
        return True

    def send_change_email_code(self, new_email, code):
        html = render_to_string(
            self.change_notify_email_template,
            {
                'code': code,
            }
        )
        asyn_send_mail.delay(new_email, self.change_email_subject, html)
        return True


class IndustryBookin(CSRFExemptMixin, LoginRequiredMixin, View):

    def post(self, request):
        payload = request.JSON
        bookin_type = get_int(payload.get('bookin_type'))
        if bookin_type not in [1, 2]:
            return JsonResponse({
                'status': 'error',
                'msg': '报名失败,参数错误',
            })

        userprofile = request.user.userprofile
        bookin = NewIndustryBookin(
            user=userprofile,
            type=bookin_type
        )

        bookin.save()
        if bookin:
            return JsonResponse({
                'status': 'ok',
                'msg': '报名成功',
            })

        return JsonResponse({
            'status': 'error',
            'msg': '报名失败,请重试',
        })


class Register(View, SendVaildNotifyMailMixin):
    '''
    注册View
    '''
    template = 'register_edit_info.html'
    email_template = 'client_active_email.html'
    form_obj = AccountRegisterForm

    def get(self, request):
        token = request.GET.get('promotion_token', '')
        industry_list = Industry.objects.all()
        field_list = CompanyCategory.objects.all()
        return render(
            request,
            self.template,
            {
                'industry_list': industry_list,
                'field_list': field_list,
                'promotion_token': token
            },
        )

    def extra_save(self, user_profile):
        user = user_profile.user
        user_add_group(user, 'new_vip')

        return True

    def active_experience_service(self, user):
        experience_service = VipRoleUtils.get_experience_vip()
        srv_meta = {
            'service_name': 'self_service',
            'product': experience_service,
            'user': user,
        }
        experience_srv = SelfService(**srv_meta)
        srv = experience_srv.create_service()

        ret = experience_srv.active_service() if srv else False
        return ret

    def post(self, request):

        post_data = request.JSON
        form = self.form_obj(post_data, request=request)
        if form.is_valid():
            user_profile = form.save()
            user = user_profile.user
            self.extra_save(user_profile)

            # 激活账号
            user.is_active = True
            user_profile.guide_switch = True
            user_profile.is_phone_bind = True

            with transaction.atomic():
                user.save()
                user_profile.save()

                # 激活体验服务
                self.active_experience_service(user)

                # 记录推广注册信息
                PromotionUtils.register_promotion(request, user)
                PromotionUtils.promotion_success(user)

            # 开始登录
            user.backend = 'users.runtime.auth_backend.AuthPhoneBackend'
            login(request, user)

            self.send_active_email(user)
            return JsonResponse({
                'status': 'ok',
                'msg': u'注册成功',
                'username': user.username,
                'redirect_url': reverse('special-feed-page')
            })

        else:
            return JsonResponse({
                'status': 'error',
                'msg': form.get_first_errors(),
                'errors': form.errors,
            })


class SendSmsCode(CSRFExemptMixin, View, MaliceMixin):

    MALICE_IP_PREFIX = 'send_sms_ip_'
    EXPIRE_SECOND = 60 * 10
    MAX_ERROR_TIMES = 5

    def is_can_send(self, mobile, action_name):
        account = PinbotAccount.get_profile(phone=mobile, is_phone_bind=True)
        if action_name == 'AccountReg' and account:
            return False

        if action_name == 'ChangePwd' and not account:
            return False

        return True

    """发送短信验证码请求"""
    def post(self, request):
        post_data = request.JSON
        action_name = post_data.get('action_name')
        mobile = post_data.get('mobile')
        if not self.is_can_send(
            mobile=mobile,
            action_name=action_name
        ):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '手机号错误!',
                    'errors': {
                        "code": [
                            '手机号错误!'
                        ]
                    }
                }
            )

        if self.malice_ip():
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '发送验证短信失败,每天每个手机号不得发送超过5次!',
                    'errors': {
                        "code": [
                            '发送验证短信失败,每天每个手机号不得发送超过5次!'
                        ]
                    }
                }
            )

        asyn_send_sms_code.delay(mobile=mobile, action_name=action_name)

        return JsonResponse(
            {
                'status': 'ok',
                'msg': '发送验证短成功'
            }
        )


class VaildSmsCode(View):
    """短信验证码验证"""
    def post(self, request):
        post_data = request.JSON
        action_name = post_data.get('action_name')
        code = post_data.get('code')
        mobile = post_data.get('mobile')

        ret = SmsCode.vaild_sms_code(
            code=code,
            mobile=mobile,
            action_name=action_name
        )
        if not ret:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '验证码错误',
                    'errors': {
                        "code": [
                            '验证码错误',
                        ]
                    }
                }
            )

        return JsonResponse(
            {
                'status': 'ok',
                'msg': '验证短信成功'
            }
        )


class Login(View, MaliceMixin):

    """用户登陆"""
    MAX_ERROR_TIMES = 10
    EXPIRE_SECOND = 60 * 5
    MALICE_IP_PREFIX = 'login_ip:'

    def post(self, request):

        if self.malice_ip():
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '错误次数太多，请稍后再试',
                    'errors': {
                        "username": [
                            '错误次数太多，请稍后再试'
                        ]
                    }
                }
            )

        post_data = request.JSON
        username = post_data.get('username')
        password = post_data.get('password')

        next_url = post_data.get('next', reverse('special-feed-page'))

        if not error_phone(username) and not PinbotAccount.is_phone_bind(mobile=username):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '手机号未绑定,不能登录',
                    'errors': {
                        "username": [
                            '手机号未绑定,不能登录'
                        ]
                    }
                }
            )

        user = authenticate(
            username=username,
            password=password
        )
        if not user:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '登陆失败，用户名或密码错误',
                    'errors': {
                        "username": [
                            '登陆失败，用户名或密码错误'
                        ]
                    }
                }
            )

        if not hasattr(user, 'userprofile'):
            return JsonResponse({
                'status': 'error',
                'msg': '请使用新的企业邮箱重新注册聘宝企业端',
                'errors': {
                    "username": [
                        '请使用新的企业邮箱重新注册聘宝企业端',
                    ]
                }
            })

        redirect_url = get_valid_next_url(next_url)
        login(request, user)
        self.clean_malice()

        industrys = user.company_set.all().values_list('category__industry__code_name', flat=True)
        user_industry = industrys[0] if len(industrys) > 0 else ''

        if user_industry == 'medicine':
            redirect_url = reverse('new_field_attent')

        return JsonResponse(
            {
                'status': 'ok',
                'msg': '登陆成功',
                'username': user.username,
                'redirect_url': redirect_url,
                'user_industry': user_industry
            }
        )


class ChangMobile(LoginRequiredMixin, View):
    """更换手机号"""
    def post(self, request):
        post_data = request.JSON
        user = request.user
        password = post_data.get('password')
        code = post_data.get('code')
        mobile = post_data.get('mobile')
        if PinbotAccount.is_phone_bind(mobile=mobile):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '手机号已绑定,不能继续绑定',
                    'errors': {
                        "phone": [
                            '手机号已绑定,不能继续绑定'
                        ]
                    }
                }
            )

        user_profile = user.userprofile
        if not user_profile:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '账号错误',
                    'errors': {
                        "phone": [
                            '账号错误'
                        ]
                    }
                }
            )

        if not SmsCode.vaild_sms_code(
            code=code,
            mobile=mobile,
            action_name='ChangeMobile'
        ):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '短信验证码错误',
                    'errors': {
                        "code": [
                            '短信验证码错误'
                        ]
                    }
                }
            )
        user = authenticate(
            username=user.username,
            password=password
        )

        if not user:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '用户名或密码错误',
                    'errors': {
                        "password": [
                            '用户名或密码错误'
                        ]
                    }
                }
            )

        ret = PinbotAccount.update_user_mobile(
            user=user,
            mobile=mobile
        )
        if not ret:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '更换手机号失败,请重试或者联系管理员'
                }
            )
        return JsonResponse(
            {
                'status': 'ok',
                'msg': '更换手机号成功'
            }
        )


class FindPwdByMobile(View):
    """根据手机号找回密码"""
    template = 'password_reset_by_mobile.html'

    def get(self, request):
        return render(
            request,
            self.template,
            {

            },
        )

    def post(self, request):
        post_data = request.JSON
        mobile = post_data.get('mobile')
        code = post_data.get('code')
        password = post_data.get('password')
        re_password = post_data.get('re_password')

        if not error_phone(mobile) and not PinbotAccount.is_phone_bind(mobile=mobile):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '手机号未绑定,不能登录',
                    'errors': {
                        "phone": [
                            '手机号未绑定,不能登录'
                        ]
                    }
                }
            )

        if password != re_password:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '前后密码不一致',
                    'errors': {
                        "password": [
                            '前后密码不一致'
                        ]
                    }
                }
            )

        if not SmsCode.vaild_sms_code(
            mobile=mobile,
            code=code,
            action_name='ChangePwd'
        ):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '短信验证码错误',
                    'errors': {
                        "code": [
                            '短信验证码错误'
                        ]
                    }
                }
            )
        user_profile = PinbotAccount.get_profile(phone=mobile, is_phone_bind=True)
        if not user_profile:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '账号错误',
                    'errors': {
                        "phone": [
                            '账号错误'
                        ]
                    }
                }
            )

        if not PinbotAccount.change_user_pwd(
            user_id=user_profile.user.id,
            password=password
        ):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '修改密码错误,请重试或者联系管理员!'
                }
            )

        return JsonResponse(
            {
                'status': 'ok',
                'msg': '修改密码成功!'
            }
        )


class SendEmailCode(LoginRequiredMixin, View, SendVaildNotifyMailMixin):

    def post(self, request):
        user = request.user
        post_data = request.JSON
        password = post_data.get('password')
        email = post_data.get('email')
        user = authenticate(
            username=user.username,
            password=password
        )
        if not user:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '修改接收邮箱失败,用户名或密码错误',
                    'errors': {
                        "email": [
                            '修改接收邮箱失败,用户名密码错误'
                        ]
                    }
                }
            )

        code = EmailCode.generation_code(
            username=user.username,
            action_name='CHANGE_NOTIFY_EMAIL'
        )
        self.send_change_email_code(
            new_email=email,
            code=code
        )

        return JsonResponse(
            {
                'status': 'ok',
                'msg': '邮箱验证码发送成功'
            }
        )


class ChangeNotifyEmail(LoginRequiredMixin, View):
    """更换通知接收邮箱"""
    def post(self, request):
        user = request.user
        post_data = request.JSON
        password = post_data.get('password')
        email = post_data.get('email')
        code = post_data.get('code')
        if PinbotAccount.is_email_bind(email=email):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '该邮箱已绑定,无法继续绑定该邮箱!',
                    'errors': {
                        "email": [
                            '该邮箱已绑定,无法继续绑定该邮箱!',
                        ]
                    }
                }
            )

        if not EmailCode.vaild_sms_code(
            username=user.username,
            code=code,
            action_name='CHANGE_NOTIFY_EMAIL'
        ):
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '验证码错误!',
                    'errors': {
                        "code": [
                            '验证码错误!'
                        ]
                    }
                }
            )

        user = authenticate(
            username=user.username,
            password=password
        )

        if not user:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': '密码错误!',
                    'errors': {
                        "password": [
                            '密码错误!'
                        ]
                    }
                }
            )

        PinbotAccount.update_user_notify_email(
            user=user,
            email=email,
        )
        return JsonResponse(
            {
                'status': 'ok',
                'msg': '修改接收邮箱成功!'
            }
        )


class NotifyEmailIsBind(LoginRequiredMixin, View):

    @method_decorator(cache_response())
    def get(self, request):
        user = request.user

        # 兼容没有userprofile的情况
        if not hasattr(user, 'userprofile'):
            return JsonResponse({
                'status': 'ok',
                'msg': '',
                'is_bind': False,
                'notify_email': user.username,
            })

        user_profile = user.userprofile

        return JsonResponse(
            {
                'status': 'ok',
                'msg': '',
                'is_bind': user_profile.is_email_bind,
                'notify_email': user_profile.user_email,
            }
        )


class BindNotifyEmail(LoginRequiredMixin, View):
    """绑定接收邮箱界面"""
    template = 'bind_notify_email.html'

    def get(self, request):
        user_profile = request.user.userprofile
        return render(
            request,
            self.template,
            {
                'user_profile': user_profile
            },
        )


class ReSendBindNotifyEmail(LoginRequiredMixin, View, SendVaildNotifyMailMixin):

    """重新发送绑定接收邮箱"""

    def get(self, request):
        user = request.user
        self.send_active_email(user=user)
        return JsonResponse(
            {
                'status': 'ok',
                'msg': '重新发送成功',
            }
        )


class ChangeCompanyInfo(LoginRequiredMixin, View):

    def post(self, request):
        form = AccountCompanyForm(request.JSON)
        if form.is_valid():
            user_profile = request.user.userprofile
            user_profile.company_name = form.cleaned_data['company_name']
            user_profile.url = form.cleaned_data['company_url']
            user_profile.save()

            return JsonResponse(
                {
                    'status': 'ok',
                    'msg': '编辑企业信息成功',
                }
            )

        return JsonResponse({
            'status': 'error',
            'msg': form.get_first_errors(),
            'errors': form.errors,
        })


class ChangeMyInfo(LoginRequiredMixin, View):

    def post(self, request):
        print request.JSON
        form = AccountMyInfoForm(request.JSON)

        if form.is_valid():
            user_profile = request.user.userprofile
            user_profile.name = form.cleaned_data['realname']
            user_profile.qq = form.cleaned_data['qq']
            user_profile.save()
            return JsonResponse(
                {
                    'status': 'ok',
                    'msg': '修改个人信息成功',
                }
            )
        return JsonResponse({
            'status': 'error',
            'msg': form.get_first_errors(),
            'errors': form.errors,
        })


class ChangeMyPassword(LoginRequiredMixin, View):

    def post(self, request):
        form = AccountMyPasswordForm(request.JSON)
        if form.is_valid():
            user = request.user
            if not authenticate(
                username=user.username,
                password=form.cleaned_data['old_password']
            ):
                return JsonResponse(
                    {
                        'status': 'error',
                        'msg': '旧密码错误',
                    }
                )

            user.set_password(form.cleaned_data['confirm_password'])
            user.save()
            return JsonResponse(
                {
                    'status': 'ok',
                    'msg': '修改密码成功',
                }
            )
        return JsonResponse({
            'status': 'error',
            'msg': form.get_first_errors(),
            'errors': form.errors,
        })


class ChanageMyRecvInfo(LoginRequiredMixin, View):

    def post(self, request):
        form = AccountMyRecvInfoForm(request.JSON)
        if form.is_valid():
            user_profile = request.user.userprofile
            user_profile.province = form.cleaned_data['province']
            user_profile.city = form.cleaned_data['city']
            user_profile.area = form.cleaned_data['area']
            user_profile.street = form.cleaned_data['street']
            user_profile.recv_name = form.cleaned_data['recv_name']
            user_profile.recv_phone = form.cleaned_data['recv_phone']
            user_profile.save()
            return JsonResponse(
                {
                    'status': 'ok',
                    'msg': '修改收货信息成功',
                }
            )
        return JsonResponse({
            'status': 'error',
            'msg': form.get_first_errors(),
            'errors': form.errors,
        })


class UserProfile(LoginRequiredMixin, View):

    def get(self, request):
        user_profile = request.user.userprofile
        form = UserProfileForm(
            {
                "company_name": user_profile.company_name,
                "email": request.user.email,
                "phone": user_profile.phone,
                "url": user_profile.url,
                "qq": user_profile.qq,
                "name": user_profile.name,
                "notify_email": user_profile.user_email,
                "is_email_bind": user_profile.is_email_bind,
                "is_phone_bind": user_profile.is_phone_bind,
                "province": user_profile.province,
                "city": user_profile.city,
                "street": user_profile.street,
                "area": user_profile.area,
                "postcode": user_profile.postcode,
                "recv_phone": user_profile.recv_phone,
                "recv_name": user_profile.recv_name,
            }
        )

        return render(request, "users/user.html", {'form': form})


class WeixinIsBind(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        ret = WeixinService.is_bind(user=user)
        nickname = '' if not ret else ret.nickname
        ret = True if WeixinService.is_bind(user=user) else False

        return JsonResponse(
            {
                'status': 'ok',
                'msg': '',
                'is_bind': ret,
                'nickname': nickname,
            }
        )
