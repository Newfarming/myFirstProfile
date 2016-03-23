# coding: utf-8

from django.shortcuts import (
    render,
)
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse

from .forms import (
    RegisterUserForm,
    ChangePasswordForm,
    ResetPasswordForm,
    CheckUserInForm,
    LoginForm,
)
from .models import (
    UserToken,
    UserProfile,
)
from .account_utils import (
    SendMailMixin,
)

from Brick.App.my_resume.resume_utils import (
    ResumeUtils,
)

from Brick.Utils.django_utils import (
    JsonResponse,
    get_object_or_none,
    error_email,
)
from Brick.Utils.mixin_utils import (
    LoginRequiredMixin,
    MaliceMixin,
)


class CheckUserIn(View):
    '''
    检查用户输入的用户名是否是pinbot用户
    如果是pinbot用户并且密码正确则返回允许登录状态
    如果pinbot不存在该用户名则注册用户，返回注册成功的结果
    如果是pinbot用户并且密码错误则提示用户名密码不存在
    '''
    template = 'account_check_in.html'

    def get(self, request):
        return render(
            request,
            self.template,
            {},
        )

    def post(self, request):
        form = CheckUserInForm(request.POST, request=request)
        if form.is_valid():
            result = form.check_in_result()
        else:
            result = {
                'status': 'form_error',
                'msg': form.get_first_errors(),
            }
        return JsonResponse(result)


class Register(View, SendMailMixin, MaliceMixin):

    '''
    注册View
    '''

    MAX_ERROR_TIMES = 10
    EXPIRE_SECOND = 60 * 3
    MALICE_IP_PREFIX = 'REGISTER_MALICE_IP'

    template = 'account_register.html'

    def get(self, request):
        return render(
            request,
            self.template,
            {}
        )

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            if self.malice_ip():
                return JsonResponse({
                    'status': 'malice_ip',
                    'msg': '注册太频繁了，请稍后再试',
                })

            user_profile = form.save()
            user = user_profile.user
            self.send_active_email(user)

            return JsonResponse({
                'status': 'ok',
                'msg': u'注册成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors
            })


class Login(View, MaliceMixin):

    MAX_ERROR_TIMES = 10
    EXPIRE_SECOND = 60 * 3
    MALICE_IP_PREFIX = 'LOGIN_MALICE_IP_'

    template = 'account_login.html'

    def get(self, request):
        return render(
            request,
            self.template,
            {}
        )

    def get_login_redirect_url(self):
        resume = ResumeUtils.get_resume(self.request.user)
        select_tag_url = reverse('resume-index')
        job_index_url = reverse('job-index')

        if not resume.gender:
            return '%s#/%s/' % (select_tag_url, 'select_gender')
        if not resume.expectation_area.all():
            return '%s#/%s/' % (select_tag_url, 'select_city')
        if not resume.position_tags.all() or not resume.job_category:
            return '%s#/%s/' % (select_tag_url, 'select_position_category')
        if not resume.work_years:
            return '%s#/%s/' % (select_tag_url, 'select_work_years')
        if not resume.degree:
            return '%s#/%s/' % (select_tag_url, 'select_degree')
        if not resume.salary_lowest:
            return '%s#/%s/' % (select_tag_url, 'select_salary')
        if not resume.prefer_fields.all():
            return '%s#/%s/' % (select_tag_url, 'select_field')

        return job_index_url

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data['username']
            password = form_data['password']
            auth_user = authenticate(username=username, password=password)

            if self.malice_ip():
                return JsonResponse({
                    'status': 'malice_ip',
                    'msg': '提交太频繁了，请稍后再试',
                })

            try:
                brick_user_profile = auth_user.brick_user_profile if auth_user else None
            except UserProfile.DoesNotExist:
                brick_user_profile = None

            if not brick_user_profile:
                return JsonResponse({
                    'status': 'not_exist',
                    'msg': '邮箱或密码错误！',
                })

            if not brick_user_profile.is_active:
                return JsonResponse({
                    'status': 'not_active',
                    'msg': '该账户未激活',
                })

            login(self.request, auth_user)
            self.clear_malice()
            return JsonResponse({
                'status': 'ok',
                'msg': '登录成功',
                'redirect_url': self.get_login_redirect_url(),
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class SendActiveEmail(View, SendMailMixin, MaliceMixin):

    MALICE_IP_PREFIX = 'send_mail_ip_'
    METHOD = 'GET'
    EXPIRE_SECOND = 60
    MAX_ERROR_TIMES = 5

    def get(self, request, email):
        user_profile = get_object_or_none(
            UserProfile,
            user__username=email,
        )
        if not user_profile:
            return JsonResponse({
                'status': 'not_found_user',
                'msg': u'用户不存在！',
            })

        if self.malice_ip():
            return JsonResponse({
                'status': 'malice',
                'msg': u'操作太频繁啦，稍后再试试！'
            })

        user = user_profile.user
        mail_result = self.send_active_email(user)
        return JsonResponse({
            'status': 'ok',
            'msg': u'发送成功！',
            'mail_result': mail_result,
        })


class ValidActiveEmail(View):

    template = 'account_active_user.html'

    def get(self, request, activation_key):
        user_token = get_object_or_none(
            UserToken,
            token=activation_key,
            active=True,
            token_type='register',
        )

        if user_token and user_token.user.brick_user_profile.is_active:
            return render(
                request,
                self.template,
                {
                    'status': 'already_active',
                    'msg': u'您已激活邮箱，请继续登陆',
                }
            )
        if not user_token:
            return render(
                request,
                self.template,
                {
                    'status': 'token_error',
                    'msg': u'无效的激活链接',
                }
            )

        user = user_token.user

        if not default_token_generator.check_token(
                user,
                user_token.token):
            return render(
                request,
                self.template,
                {
                    'status': 'token_expire',
                    'msg': u'链接已失效',
                    'user': user,
                }
            )

        with transaction.atomic():
            user.is_active = True
            user_token.active = False
            user.brick_user_profile.is_active = True
            user.save()
            user_token.save()
            user.brick_user_profile.save()

        return render(
            request,
            self.template,
            {
                'status': 'success',
                'msg': u'激活成功',
            },
        )


class ChangePassword(LoginRequiredMixin, View):
    template = 'account_my_pinbot.html'

    def get(self, request):
        return render(
            request,
            self.template,
            {}
        )

    def post(self, request):
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.change_user_password()
            return JsonResponse({
                'status': 'ok',
                'msg': u'密码修改成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'data': {
                    'errors': form.errors,
                },
            })


class SendResetPasswordEmail(SendActiveEmail):
    MALICE_RESET_PREFIX = 'send_reset_mail_ip_'
    url_name = 'account-reset-password'
    token_type = 'reset'
    email_template = 'account_active_email.html'
    subject = '聘宝-找回密码'


class ResetPassword(View):

    template = 'account_reset_password.html'

    def get(self, request, token):
        user_token = get_object_or_none(
            UserToken,
            token=token,
            active=True,
            token_type='reset',
        )

        if not user_token:
            return render(
                request,
                self.template,
                {
                    'status': 'token_error',
                    'msg': u'无效的链接',
                }
            )
        return render(
            request,
            self.template,
            {},
        )

    def post(self, request, token):
        user_token = get_object_or_none(
            UserToken,
            token=token,
            active=True,
            token_type='reset',
        )

        if not user_token:
            return JsonResponse({
                'status': 'token_error',
                'msg': u'无效的链接',
            })

        user = user_token.user
        if not default_token_generator.check_token(
                user,
                user_token.token):
            return JsonResponse({
                'status': 'token_expire',
                'msg': u'链接已失效',
            })

        form = ResetPasswordForm(request.POST, user=user)
        if form.is_valid():

            with transaction.atomic():
                form.change_user_password()
                user_token.active = False
                user_token.save()

            return JsonResponse({
                'status': 'ok',
                'msg': u'修改成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class CheckRegisterEmail(View):

    def get(self, request):
        username = self.request.GET.get('username', '')

        if error_email(username):
            return JsonResponse({
                'status': 'form_error',
                'msg': '邮件格式错误',
            })

        user = get_object_or_none(
            User,
            username=username
        )

        if not user:
            return JsonResponse({
                'status': 'ok',
                'msg': '可以使用',
            })

        try:
            brick_profile = user.brick_user_profile
        except UserProfile.DoesNotExist:
            brick_profile = None

        if brick_profile:
            return JsonResponse({
                'status': 'user_exists',
                'msg': '该邮箱已存在，请直接',
            })

        if user and not brick_profile:
            return JsonResponse({
                'status': 'company_user',
                'msg': '你已是企业版用户，输入邀请码即可',
            })

        return JsonResponse({
            'status': 'ok',
            'msg': '可以使用',
        })
