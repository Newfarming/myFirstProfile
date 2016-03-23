# coding:utf-8

import logging
import datetime as date_time
import hashlib
import random

from django.db import transaction
from django.shortcuts import render, redirect, render_to_response
from Pinbot import settings
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from users.veriry_code import Code
from django.contrib.auth.views import get_user_model
from django.utils.http import base36_to_int
from users.forms import PasswordChangeForm
from django.utils import timezone
from basic_service.models import *
from django.core.mail.message import EmailMessage
from django.utils.http import int_to_base36
from resumes.models import *
from users.models import *
from forms import RegisterForm
from jobs.models import CompanyCategory
from transaction.models import UserChargePackage

from app.promotion_point.promotion_utils import PromotionUtils
from app.vip.vip_utils import VipRoleUtils, UserOrderUtils
from app.vip.runtime.self_service import (
    SelfService,
)

from app.special_feed.feed_utils import FeedUtils
from jobs.job_utils import JobUtils
from pin_utils.django_utils import (
    JsonResponse,
    user_add_group,
    get_object_or_none,
    get_today,
    get_yesterday
)
from pin_utils.email.send_mail import (
    asyn_send_mail,
)
from pin_utils.mixin_utils import (
    MaliceMixin,
)
from Brick.App.account.models import (
    UserProfile as BrickUserProfile
)

mail_host_dict = {'sina': 'http://mail.sina.com.cn/',
                  '163': 'http://mail.163.com/',
                  'qq': 'http://mail.qq.com/',
                  '126': 'http://mail.126.com/',
                  'gmail': 'http://mail.google.com/'}

SHA1_RE = re.compile('^[a-f0-9]{40}$')
django_log = logging.getLogger('django')


@login_required
def gotopinbot(request):
    '''
    如果用户有taocv的权限进入taocv
    如果用户没有套餐没有申请vip进入注册vip申请页面
    如果用户有专属定制套餐直接跳定制套餐
    '''
    user = request.user
    if user.groups.filter(name='taocv'):
        return redirect("/taocv/")

    current_vip = VipRoleUtils.get_current_vip(user)
    use_feed = FeedUtils.has_use_feed(user)
    has_fill = JobUtils.has_fill_company(user)
    unsign_vip = VipRoleUtils.get_unsign_vip(user)

    if not current_vip and not use_feed and unsign_vip:
        order = UserOrderUtils.get_order_by_item(unsign_vip)
        return redirect('vip-alipay-result', order_id=order.id)

    if current_vip and not use_feed and not has_fill:
        return redirect('companycard-get')

    user_charges_pkgs = UserChargePackage.objects.filter(
        user=user,
        package_type__in=(1, 2),
        pay_status='finished',
    )

    if user_charges_pkgs:
        return redirect('special-feed-page')

    return redirect('vip-role-info')


def signout(request):
    logout(request)
    return redirect("/")


@csrf_exempt
def signin(request):
    p = request.GET.copy()
    next_url = p.get('next')
    if request.method == "GET":
        user = request.user
        if user and user.is_authenticated():
            if next_url:
                return redirect(next_url[0])
            else:
                industrys = user.company_set.all().values_list('category__industry__code_name', flat=True)
                user_industry = industrys[0] if len(industrys) > 0 else ''

                if user_industry == 'medicine':
                    redirect_url = reverse('new_field_attent')
                    return redirect(redirect_url)

                return redirect("/feed/")
        form = UserLoginForm()
        request.session['failed_count'] = 0
        return render(request, "pinbot_beta/login.html", {"form": form, 'code': False})
    else:
        next_url = None
        http_referer = request.META.get('HTTP_REFERER')
        if http_referer:
            result = urlparse.urlparse(http_referer)

            if result.path == '/signin/':
                params = urlparse.parse_qs(result.query, True)
                next_url = params.get('next')
                if next_url:
                    next_url = next_url[0]

        form = UserLoginForm(request.POST)
        message = ''
        failed_count = 0
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['email'].lower(), password=data['password'])

            if user is not None:
                try:
                    user_profile = user.userprofile
                except UserProfile.DoesNotExist:
                    user_profile = None

                try:
                    brick_user_profile = user.brick_user_profile
                except BrickUserProfile.DoesNotExist:
                    brick_user_profile = None

                if brick_user_profile and not user_profile:
                    message = 'brick user'
                    return render(request, "pinbot_beta/login.html", locals())

                if not brick_user_profile and not user_profile:
                    message = 'accout error'
                    return render(request, "pinbot_beta/login.html", locals())

                if user.is_active:
                    login(request, user)

                    if next_url:
                        return redirect(next_url)
                    return redirect('special-feed-page')
                else:
                    message = 'user not active'
            else:
                message = 'authenticate fail'
        else:
            message = 'input error'
            failed_count = failed_count + 1
        return render(request, "pinbot_beta/login.html", locals())


@csrf_exempt
def signin_old(request):
    p = request.GET.copy()
    next_url = p.get('next')
    if request.method == "GET":
        user = request.user

        if user and user.is_authenticated():
            if next_url:
                return redirect(next_url[0])
            else:
                return redirect("/feed/")
        form = UserLoginForm()
        request.session['failed_count'] = 0
        return render(request, "pinbot_beta/login.html", {"form": form, 'code': False})
    else:
        next_url = None
        http_referer = request.META.get('HTTP_REFERER')
        if http_referer:
            result = urlparse.urlparse(http_referer)

            if result.path == '/signin/':
                params = urlparse.parse_qs(result.query, True)
                next_url = params.get('next')
                if next_url:
                    next_url = next_url[0]

        form = UserLoginForm(request.POST)
        _code = request.POST.get('code') or u''
        _code = _code.encode('utf-8')
        failed_count = request.session.get('failed_count', 0)
        message = ''
        if failed_count < 3:
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(
                    username=data['email'].lower(), password=data['password'])
                user_profile = UserProfile.objects.filter(user=user)
                is_review = -1
                if len(user_profile) == 1:
                    is_review = user_profile[0].is_review

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        failed_count = 0
                        if next_url:
                            return redirect(next_url)
                        return redirect("/")
                    else:
                        if is_review == None or is_review == 0:
                            message = 'user not checked'
                        elif is_review == -1:
                            message = 'check failed'
                        else:
                            message = 'user not active'
                        failed_count = failed_count + 1
                else:
                    message = 'user not existed'
                    failed_count = failed_count + 1
            else:
                message = 'input error'
                failed_count = failed_count + 1
        else:
            if not _code:
                return render_to_response('pinbot_beta/login.html', {'status': 'error', 'message': 'code error', 'form': form})

            code = Code(request)
            if code.check(_code):
                # TODO This is only for proof of concept and very simple login.
                if form.is_valid():
                    data = form.cleaned_data
                    user = authenticate(
                        username=data['email'].lower(), password=data['password'])
                    user_profile = UserProfile.objects.filter(user=user)
                    is_review = -1
                    if len(user_profile) == 1:
                        is_review = user_profile[0].is_review

                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            failed_count = 0
                            return redirect("/users/profile")
                        else:
                            if is_review == None or is_review == -1:
                                message = 'user not reviewed'
                            else:
                                message = 'user not active'
                            failed_count = failed_count + 1
                    else:
                        message = 'user not existed'
                        failed_count = failed_count + 1
                else:
                    message = 'input error'
                    failed_count = failed_count + 1
            else:
                message = 'code error'
                failed_count = failed_count + 1

        request.session['failed_count'] = failed_count
        if failed_count >= 3:
            code = True
        else:
            code = False
        return render(request, "pinbot_beta/login.html", {'status': 'error', 'message': message, 'form': form, 'code': code})


@csrf_exempt
def plugsignin(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({'status': False, 'data': {}, 'error': {'type': 'method error', 'message': u'请使用POST方法'}}), 'application/json')
    else:
        username = request.POST.get("username", '').lower()
        password = request.POST.get("password", '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({'status': True, 'data': {'username': user.username}}), 'application/json')
            else:
                return HttpResponse(json.dumps({'status': False, 'data': {}, 'error': {'type': 'status error ', 'message': u'该用户未被激活'}}), 'application/json')
        else:
            return HttpResponse(json.dumps({'status': False, 'data': {}, 'error': {'type': 'not authenticated', 'message': u'用户名或密码错误,请重新输入'}}), 'application/json')


@login_required
def profile(request):
    user = request.user
    username = user.email
    user_setting_class = "curr"
    if request.method == "GET":
        try:
            profile = user.get_profile()
            form = UserProfileForm(
                {
                    "company_name": profile.company_name,
                    "email": user.email,
                    "phone": profile.phone,
                    "url": profile.url,
                    "qq": profile.qq,
                    "name": profile.name,
                    "notify_email": profile.user_email,
                    "is_email_bind": profile.is_email_bind,
                    "is_phone_bind": profile.is_phone_bind,
                    "province": profile.province,
                    "city": profile.city,
                    "street": profile.street,
                    "area": profile.area,
                    "postcode": profile.postcode,
                    "recv_phone": profile.recv_phone,
                    "recv_name": profile.recv_name,
                }
            )
        except Exception, IntegrityError:
            form = UserProfileForm({"name": user.get_full_name(),
                                    "email": user.email, "phone": "",
                                    "url": "", "street": "",
                                    "city": "", "province": "",
                                    "postcode": "", "area": "", "recv_phone": "", "recv_name": ""}
                                   )
        return render(request, "users/user.html", locals())
    else:
        form = UserProfileForm(request.JSON)

        if form.is_valid():
            form_data = form.cleaned_data
            company_name = form_data['company_name']
            url = form_data['url']
            qq = form_data['qq']
            name = form_data['name']
            province = form_data['province']
            city = form_data['city']
            street = form_data['street']
            postcode = form_data['postcode']
            recv_phone = form_data['recv_phone']
            recv_name = form_data['recv_name']
            area = form_data['area']

            if len(UserProfile.objects.filter(user=user)) >= 1:
                profile = UserProfile.objects.filter(user=user)[0]
                profile.company_name = company_name
                profile.url = url
                profile.qq = qq
                profile.name = name
                profile.province = province
                profile.city = city
                profile.street = street
                profile.area = area
                profile.postcode = postcode
                profile.recv_phone = recv_phone
                profile.recv_name = recv_name
                profile.save()
            else:
                user_profile = UserProfile()
                user_profile.user = user
                user_profile.user_email = username
                user_profile.company_name = company_name
                user_profile.url = url
                user_profile.qq = qq
                user_profile.name = name
                user_profile.province = province
                user_profile.city = city
                user_profile.street = street
                user_profile.postcode = postcode
                user_profile.recv_phone = recv_phone
                user_profile.recv_name = recv_name
                user_profile.save()
            return redirect("/users/profile/")
        else:
            return render(request, "users/user.html", {"status": 'error', 'email': user.email})


def signup(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        step = 1
        return render(request, "pinbot_beta/user/register.html", locals())
    else:
        form = UserProfileForm(request.POST)
        step = 1
        if form.is_valid():
            data = form.cleaned_data
            status = 'error'
            message = ''
            try:
                email = data['email'].lower()
                qq = data['qq']
                company_name = data.get('company_name', '')
                phone = data.get('phone', '')
                url = data.get('url', '')
                name = data.get('name', '')
                ip = ''
                password = 'pinbot'

                if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']

                user = User.objects.filter(email=email)
                if len(user) >= 1:
                    message = 'user existed'
                    return render(request, 'pinbot_beta/user/register.html', locals())

                user = User.objects.create_user(
                    email, email, password, first_name=company_name)
#                 send_check_email(user,True)
                # TODO This is only very simply registration and for proof of concept. In the future,
                # we should include more information, validation, sending
                # emails etc.
                user.first_name = company_name
                user.is_active = False
                user.save()
                PromotionUtils.register_promotion(request, user)

                if len(UserProfile.objects.filter(user_email=user.username)) == 1:
                    # 已经填写过信息 直接跳转到登录页面
                    step = 2
                    return render(request, "pinbot_beta/user/register.html", locals())
                else:
                    UserProfile.objects.create(
                        user=user, company_name=company_name, phone=phone, url=url, user_email=email, name=name, ip=ip, qq=qq)
                    step = 2
                    return render(request, "pinbot_beta/user/register.html", locals())
            except Exception, IntegrityError:
                form = UserRegistrationForm()
                return render(request, 'pinbot_beta/user/register.html', {'status': 'error', 'message': 'other_error', 'step': step})
        else:
            return render(request, 'pinbot_beta/user/register.html', {'status': 'error', 'message': 'input error', 'step': step})


@csrf_exempt
def complete_information(request):
    if request.method == "GET":
        return render(request, "complete.html")
    else:
        form = UserProfileForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                email = data['email'].lower()
                password = data['password']
                company_name = data.get('company_name', '')
                phone = data.get('phone', '')
                url = data.get('url', '')
                name = data.get('name', '')
                ip = ''
                if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']

                user = User.objects.filter(email=email)
                if user:
                    return render(request, 'complete.html', {'status': 'error', 'message': 'user existed', 'form': form})
                if not is_pass_valid(password):
                    return render(request, 'complete.html', {'status': 'error', 'message': 'password invalid', 'form': form})

                user = User.objects.create_user(
                    email, email, password, first_name=company_name)

                # TODO This is only very simply registration and for proof of concept. In the future,
                # we should include more information, validation, sending
                # emails etc.
                user.first_name = company_name
                user.is_active = False
                user.save()

                if len(UserProfile.objects.filter(user=user)) == 1:
                    # 已经填写过信息 直接跳转到登录页面
                    return redirect("/signin/")
                else:
                    UserProfile.objects.create(
                        user=user, company_name=company_name, phone=phone, url=url, user_email=email, name=name, ip=ip)
                    return render(request, "apply_success.html")
            except Exception, IntegrityError:
                form = UserRegistrationForm()
                return render(request, 'complete.html', {'status': 'error', 'message': 'input error', 'form': form})
        else:
            return render(request, 'complete.html', {'status': 'error', 'message': 'input error', 'form': form})


@csrf_exempt
def plugin_logout(request):
    """
    @summary:  chrome-extension logout.

    @author:  likaiguo.happy@gmail.com 2013-09-10
    """
    logout(request)
    return redirect("/signin/")


@login_required
def profile_ajax(request):
    if request.method == "POST":
        user = request.user
        form = UserProfileForm(request.POST)
        if form.is_valid():
            company_name = request.POST.get('company_name', '')
            phone = request.POST.get('phone', '')
            url = request.POST.get('url', '')
            qq = request.POST.get('qq', '')
            if len(UserProfile.objects.filter(user=user)) == 1:
                profile = UserProfile.objects.filter(user=user)[0]
                profile.company_name = company_name
                profile.phone = phone
                profile.url = url
                profile.qq = qq
                profile.save()
            else:
                UserProfile.objects.create(
                    user=user, company_name=company_name, phone=phone, url=url)
            return HttpResponse(json.dumps({'status': 'success'}))
        else:
            return HttpResponse(json.dumps({'status': 'error', 'message': 'input invalid'}))
    else:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'get method'}))


def who_am_i(request):
    user = request.user
    if user:
        return HttpResponse(json.dumps({'username': user.username.lower()}), 'application/json')
    else:
        return HttpResponse(json.dumps({'username': ''}), 'application/json', 'application/json')


def get_check_code_image(request):
    code = Code(request)
    code.type = "world"
    return code.display()


def add_user(email):
    if len(User.objects.filter(email=email)) >= 1:
        return False
    user = User.objects.create_user(email, email, password='123456')

    # TODO This is only very simply registration and for proof of concept. In the future,
    # we should include more information, validation, sending emails etc.
    user.is_active = False
    user.save()
    return True


@csrf_exempt
@login_required
def singnup_check(request):

    try:
        staff = request.user
        email = request.POST.get('email', None)
        key = request.POST.get('x-pinbot-admin-auth', None)
        check_status = request.POST.get('result', None)
        if not key:
            email = request.GET.get('email', None)
            key = request.GET.get('x-pinbot-admin-auth', None)
            check_status = request.GET.get('result', None)

        if key in settings.PINBOT_ADMIN:
            user = User.objects.filter(email=email)
            if user:
                user = user[0]

                if check_status == 'success':
                    result, message = send_check_email(user, True)
                    sys_user = User.objects.get(username="pinbot@hopperclouds.com")
                    assign = StaffCustomerAssgin(staff=staff,customer=user,operator=sys_user)
                    assign.save()
                else:
                    result, message = send_check_email(user, False)
                if result:
                    if check_status == 'success':
                        return HttpResponse(json.dumps({"status": "ok", 'data': '审核通过'}), 'application/json')
                    else:
                        return HttpResponse(json.dumps({"status": "error", 'data': '已拒绝'}), 'application/json')
                else:
                    return HttpResponse(json.dumps({"status": "error", "msg": 'no user:' + message}), 'application/json')
            else:
                return HttpResponse(json.dumps({"status": "error", "msg": 'no user:' + email}), 'application/json')
        else:
            return HttpResponse(json.dumps({"status": "error", "msg": "auth failed:" + key}), 'application/json')
    except Exception, IntegrityError:
        return HttpResponse(json.dumps({"status": "error", "msg": str(IntegrityError)}), 'application/json')

    return HttpResponse(json.dumps({"status": "error", "msg": 'unknownerror'}), 'application/json')


def send_active_email(user=None, site=settings.WEBSITE):
    if user:
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt + username).hexdigest()

        if len(UserProfile.objects.filter(user=user)) == 1:
            profile = user.get_profile()
            profile.activation_key = activation_key
            profile.save()
        else:
            UserProfile.objects.create(
                user=user, activation_key=activation_key, is_review=1)
        ctx_dict = {'activation_key': activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site}
        subject = render_to_string('users/active_email_subject.txt', ctx_dict)
        # Email subject *must not* contain newlines

        message = render_to_string('users/active_email.html', ctx_dict)
        subject = ''.join(subject.splitlines())
        send_email(subject=subject, message=message,
                   from_email=settings.DEFAULT_FROM_EMAIL, email=username)
        return True


def send_check_email(user, check_result=True, site=settings.WEBSITE):
    if user:
        username = user.username
        if check_result:
            email_subject = 'users/active_email_subject.txt'
            email_templete = 'users/active_email.html'

            c = {
                'email': username,
                'site_name': settings.WEBSITE,
                'uid': int_to_base36(user.pk),
                'token': default_token_generator.make_token(user),
            }

        else:
            email_subject = 'users/checkfail_email_subject.txt'
            email_templete = 'users/checkfail_email.html'

            c = {}

        if len(UserProfile.objects.filter(user=user)) == 1:
            profile = user.get_profile()
            # profile.activation_key = activation_key
            if check_result:
                profile.is_review = 1
            else:
                profile.is_review = -1
            profile.save()
        else:
            UserProfile.objects.create(user=user, is_review=1)

        subject = render_to_string(email_subject, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string(email_templete, c)
        result, message = send_email(
            subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, email=username)
        return result, message


def send_check_email_old(user, check_result=True, site=settings.WEBSITE):
    if user:
        activation_key = ''
        username = user.username
        try:
            if check_result:
                email_subject = 'users/active_email_subject.txt'
                email_templete = 'users/active_email.html'
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                if isinstance(username, unicode):
                    username = username.encode('utf-8')
                activation_key = hashlib.sha1(salt + username).hexdigest()

                if len(UserProfile.objects.filter(user=user)) == 1:
                    profile = user.get_profile()
                    profile.activation_key = activation_key
                    profile.is_review = 1
                    profile.save()
                else:
                    UserProfile.objects.create(
                        user=user, activation_key=activation_key, is_review=1)

            else:
                email_subject = 'users/checkfail_email_subject.txt'
                email_templete = 'users/checkfail_email.html'

                if len(UserProfile.objects.filter(user=user)) == 1:
                    profile = user.get_profile()
                    profile.is_review = -1
                    profile.save()
                else:
                    UserProfile.objects.create(user=user, is_review=0)

            ctx_dict = {'activation_key': activation_key,
                        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                        'site': site}
            subject = render_to_string(email_subject, ctx_dict)

            message = render_to_string(email_templete, ctx_dict)
            subject = ''.join(subject.splitlines())
            send_email(subject=subject, message=message,
                       from_email=settings.DEFAULT_FROM_EMAIL, email=username)
        except Exception, IntegrityError:
            return HttpResponse(json.dumps({"status": "error", "msg": "email send error"}), 'application/json')


from Pinbot.settings import MAIL_KEY, EMAIL_HOST_USER


@csrf_exempt
def send_mail(request):
    p = request.POST.copy()
    if request.META.get('HTTP_X_API_KEY') == MAIL_KEY:
        to = p.get('to', 'likaiguo.happy@163.com')
        to = to.split(',')
        from_email = p.get('from_email', EMAIL_HOST_USER)
        subject = p.get('subject', 'pinbot_test')
        content = p.get('content', '<a href="http://pinbot.me">pinbot</a>')
        msg = EmailMessage(subject, body=content, from_email=from_email, to=to)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        return HttpResponse('mail okay')
    else:
        return HttpResponse("KEY invalid")


@login_required
def feed_added_email(request, form,feed=None):
    username = request.user.username
    user = request.user
    if isinstance(username, unicode):
        username = username.encode('utf-8')
    ctx_dict = {'form': form}
    subject = render_to_string('email-template/rss_init_subject.txt')

    message = render_to_string('email-template/rss-init.html', ctx_dict)
    subject = ''.join(subject.splitlines())
    send_email(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, email=username)

    subject = render_to_string('email-template/feed_new_notify.txt',locals())

    message = render_to_string('email-template/feed_new_notify.html', locals())
    send_email(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, email='support@hopperclouds.com')
    subject = ''.join(subject.splitlines())
    return True


def send_email(subject, message, from_email, email):
    try:
        if not isinstance(email, tuple):
            to = list()
            to.append(email)
        else:
            to = email
        msg = EmailMessage(
            subject=subject, body=message, from_email=from_email, to=to)
        msg.content_subtype = "html"  # Main content is now text/html
        ret = msg.send()

        email_log = EmailSendLog()
        email_log.from_email = from_email
        email_log.send_time = date_time.datetime.now()
        email_log.subject = subject
        to_emails = ''
        for to_email in to:
            to_emails += ';' + to_email
        email_log.to_email = to_emails
        email_log.status = 'success'
        email_log.save()
    except Exception, IntegrityError:
        if not isinstance(email, tuple):
            to = list()
            to.append(email)
        else:
            to = email
        email_log = EmailSendLog()
        email_log.from_email = from_email
        email_log.send_time = date_time.datetime.now()
        email_log.subject = subject
        to_emails = ''
        for to_email in to:
            to_emails += ',' + str(to_email)
        email_log.to_email = to_emails
        email_log.status = 'fail'
        email_log.error_info = str(IntegrityError)
        email_log.save()
        django_log.error(str(IntegrityError))
        return False, str(IntegrityError)
    return True, ret


def activation_key_expired(user, activation_key):
    expiration_date = date_time.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    return activation_key == u"ALREADY_ACTIVATED" or (user.date_joined + expiration_date <= timezone.now())


def activate(request, activation_key):
    if SHA1_RE.search(activation_key):
        try:
            user_profile = UserProfile.objects.get(
                activation_key=activation_key)
            user = user_profile.user
        except:
            return render(request, 'users/reset.html', {'next_page': 'reset_form', 'status': False, 'message': 'actived'})
        if not activation_key_expired(user, user_profile.activation_key):
            user.is_active = True
            user.save()
            user_profile.activation_key = u"ALREADY_ACTIVATED"
            user_profile.save()
            return render_to_response('login.html', RequestContext(request, locals()))
        else:
            return render(request, 'users/reset.html', {'next_page': 'reset_form', 'status': False, 'message': ''})
    else:
        return render(request, 'users/reset.html', {'next_page': 'reset_form', 'status': False, 'message': ''})


def my_password_reset(request, is_admin_site=False,
                      template_name='users/reset.html',
                      email_template_name='users/password_reset_email.html',
                      subject_template_name='users/password_reset_subject.txt',
                      password_reset_form=PasswordResetForm,
                      token_generator=default_token_generator,
                      post_reset_redirect='users/reset.html',
                      from_email='pinbot@hopperclouds.com'):
    if request.method == "GET":
        step = 1
# return
# render(request,'users/reset.html',{'apply_reset':True,'code_error':False,'email_error':False})
        return render(request, 'pinbot_beta/user/password_reset.html', locals())
    else:
        step = 1
        _code = request.POST.get('code') or ''
        email = request.POST.get('email') or ''
        form = password_reset_form({'email': email})

        status = 'success'
        message = ''
        if not _code:
            # return
            # render(request,post_reset_redirect,{'apply_reset':True,'code_error':True,'email_error':False})
            status = 'error'
            message = 'code error'
            return render(request, 'pinbot_beta/user/password_reset.html', locals())
        code = Code(request)
        if code.check(_code):
            code = Code(request)
            user = User.objects.filter(email=email)
            if form.is_valid():
                if not user:
                    status = 'error'
                    message = 'user not exist'
                    return render(request, 'pinbot_beta/user/password_reset.html', locals())
                else:
                    user = user[0]
                    c = {
                        'email': email,
                        'site_name': settings.WEBSITE,
                        'uid': int_to_base36(user.pk),
                        'token': token_generator.make_token(user),
                    }
                    subject = render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    message = render_to_string(email_template_name, c)

                    asyn_send_mail.delay(email, subject, message)

                    try:
                        mail_host = email.split("@")[1].split('.')[0]
                        mail_host_url = mail_host_dict[mail_host]
                    except:
                        pass
                    step = 2
                    site = settings.WEBSITE_HOST
                    return render(request, 'pinbot_beta/user/password_reset.html', locals())
            else:
                status = 'error'
                message = 'input error'
                return render(request, 'pinbot_beta/user/password_reset.html', locals())
        else:
            status = 'error'
            message = 'code error'
            return render(request, 'pinbot_beta/user/password_reset.html', locals())


@csrf_exempt
def password_confirm_ajax(request, uidb36=None, token=None,
                          template_name='users/reset.html',
                          token_generator=default_token_generator,
                          set_password_form=SetPasswordForm,
                          post_reset_redirect="login.html"):
    UserModel = get_user_model()
    json_data = json.loads(request.body)
    uidb36 = request.session.get('uid', '')
    uid_int = base36_to_int(uidb36)
    new_password1 = json_data.get('new_password1')
    new_password2 = json_data.get('new_password2')
    user = UserModel._default_manager.get(pk=uid_int)

    form = set_password_form(
        user, {'new_password1': new_password1, 'new_password2': new_password2})
    if form.is_valid():
        form.save()
        if user.is_active == False:
            user.is_active = True
            user.save()
            PromotionUtils.promotion_success(user)
        return HttpResponse(json.dumps({"status": "ok", 'msg': ''}))
    else:
        return HttpResponse(json.dumps({"status": "error", "msg": "密码不一致"}))


@csrf_exempt
def my_password_confirm(request, type=None, uidb36=None, token=None,
                        template_name='users/reset.html',
                        token_generator=default_token_generator,
                        set_password_form=SetPasswordForm,
                        post_reset_redirect="login.html"):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    if request.method == "GET":
        if uidb36 is not None and token is not None:  # checked by URLconf
            try:
                uid_int = base36_to_int(uidb36)
                user = UserModel._default_manager.get(pk=uid_int)
                username = user.username
            except (ValueError, OverflowError, UserModel.DoesNotExist):
                user = None
            if user is not None and token_generator.check_token(user, token):
                validlink = True
                request.session.flush()
                request.session['uid'] = uidb36
            else:
                validlink = False
        else:
            validlink = False
        step = 3
        p = request.GET.copy()
        if type == 'activate':
            return render(request, 'pinbot_beta/user/password_reset.html', locals())
        else:
            return render(request, 'pinbot_beta/user/password_reset.html', locals())
    else:
        uidb36 = request.session.get('uid', '')
        uid_int = base36_to_int(uidb36)
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
#         password_form = ResetPasswordForm(request.POST)
        user = UserModel._default_manager.get(pk=uid_int)

        form = set_password_form(
            user, {'new_password1': new_password1, 'new_password2': new_password2})
        if form.is_valid():
            form.save()
            if user.is_active == False:
                user.is_active = True
                user.save()
                PromotionUtils.promotion_success(user)
            return redirect("/signin")
        else:
            step = 3
# return
# render(request,template_name,{'reset_form':True,'error':True,'validlink':True})
            return render(request, 'pinbot_beta/user/password_reset.html', locals())


@login_required
def change_password(request, template_name='users/user.html',
                    post_change_redirect='login.html',
                    current_app=None, extra_context=None):
    if request.method == "POST":
        form = PasswordChangeForm(request.JSON)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password', '')
            new_password1 = form.cleaned_data.get('new_password1', '')
            new_password2 = form.cleaned_data.get('new_password2', '')
            if old_password == '' or new_password1 == '' or new_password2 == '':
                return render(request, template_name, {'error_message': 'input empty', 'form': form})
            else:
                if new_password1 != new_password2:
                    return render(request, template_name, {'error_message': 'password confirm error', 'form': form})
                else:
                    if not request.user.check_password(old_password):
                        return render(request, template_name, {'error_message': 'old password error', 'form': form})
                    else:
                        request.user.set_password(new_password1)
                        request.user.save()
                        return redirect("/signout/")
        else:
            return render(request, template_name, {'error_message': 'input empty', 'form': form})
    else:
        return render(request, template_name)


@login_required
def change_password_ajax(request, template_name='users/user.html',
                         post_change_redirect='login.html',
                         current_app=None, extra_context=None):
    if request.method == "POST":
        form = PasswordChangeForm(request.JSON)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password', '')
            new_password1 = form.cleaned_data.get('new_password1', '')
            new_password2 = form.cleaned_data.get('new_password2', '')
            if old_password == '' or new_password1 == '' or new_password2 == '':
                return HttpResponse(json.dumps({"status": "error", "msg": "input empty"}))
            else:
                if new_password1 != new_password2:
                    return HttpResponse(json.dumps({"status": "error", "msg": "password confirm error"}))
                else:
                    if not request.user.check_password(old_password):
                        return render(request, template_name, {'error_message': 'old password error', 'form': form})
                        return HttpResponse(json.dumps({"status": "error", "msg": "old password error"}))
                    else:
                        request.user.set_password(new_password1)
                        request.user.save()
                        return render(request, 'login.html')
                        return HttpResponse(json.dumps({"status": "success", "msg": ""}))
            return HttpResponse(json.dumps({"status": "error", "msg": "invalid input"}))
    else:
        return HttpResponse(json.dumps({"status": "error", "msg": "get method"}))


@login_required
def email_send_frequency(request):
    user = request.user
    email = request.session['frequency']


def get_price(request):
    price_class = "on"
    loged_in = True
    if request.user.is_anonymous():
        loged_in = False
    return render(request, "pinbot_beta/price.html", locals())


def get_feature(request):
    feature_class = "on"
    loged_in = True
    if request.user.is_anonymous():
        loged_in = False
    return render(request, "pinbot_beta/feature.html", locals())


def is_pass_valid(password):
    return True


class SendActiveMailMixin(object):
    email_template = 'client_active_email.html'
    subject = '聘宝激活邮件'
    valid_url_name = 'user-valid-active-email'

    def send_active_email(self, user):
        token = default_token_generator.make_token(user)
        email = user.email
        valid_url = self.request.build_absolute_uri(
            reverse(self.valid_url_name, args=(token, ))
        )

        html = render_to_string(
            self.email_template,
            {
                'valid_url': valid_url,
            }
        )
        user.userprofile.activation_key = token
        user.userprofile.save()
        asyn_send_mail.delay(email, self.subject, html)
        return True


class Register(View, SendActiveMailMixin):

    '''
    注册View
    '''
    template = 'client_register.html'
    email_template = 'client_active_email.html'
    form_obj = RegisterForm

    def get(self, request):
        token = request.GET.get('promotion_token', '')
        return render(
            request,
            self.template,
            {
                'promotion_token': token,
            },
        )

    def extra_save(self, user_profile):
        user = user_profile.user
        user_add_group(user, 'partner')
        return True

    @transaction.atomic
    def post(self, request):
        form = self.form_obj(request.POST, request=request)
        if form.is_valid():
            user_profile = form.save()
            user = user_profile.user
            self.extra_save(user_profile)
            self.send_active_email(user)

            # 记录推广注册信息
            PromotionUtils.register_promotion(request, user)

            return JsonResponse({
                'status': 'ok',
                'msg': u'注册成功',
                'username': user.username,
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': form.get_first_errors(),
                'errors': form.errors,
            })


class VipRegister(Register):
    '''
    注册View
    '''
    template = 'register_edit_info.html'
    email_template = 'vip_active_email.html'
    form_obj = VipRegisterForm
    valid_url_name = 'user-valid-vip-email'

    def extra_save(self, user_profile):
        user = user_profile.user
        user_add_group(user, 'new_vip')
        return True

    def get(self, request):
        field_list = CompanyCategory.objects.all()
        promotion_token = request.GET.get('promotion_token', '')
        return render(
            request,
            self.template,
            {
                'field_list': field_list,
                'promotion_token': promotion_token,
            },
        )


class SendActiveEmail(View, SendActiveMailMixin, MaliceMixin):

    MALICE_IP_PREFIX = 'send_mail_ip_'
    METHOD = 'GET'
    EXPIRE_SECOND = 60 * 20

    def get(self, request, email):
        user = get_object_or_none(
            User,
            is_active=False,
            email=email,
        )
        if not user:
            return JsonResponse({
                'status': 'not_found_user',
                'msg': u'无效的用户',
            })

        if self.malice_ip():
            return JsonResponse({
                'status': 'malice',
                'msg': u'发送过于频繁，请稍后重试'
            })

        mail_result = self.send_active_email(user)
        return JsonResponse({
            'status': 'ok',
            'msg': u'发送成功',
            'mail_result': mail_result,
        })


class ValidActiveEmail(View):

    template = 'client_active_user.html'

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

    def get(self, request, activation_key):
        user_profile = get_object_or_none(
            UserProfile,
            activation_key=activation_key,
        )

        if user_profile and user_profile.user.is_active:
            return render(
                request,
                self.template,
                {
                    'status': 'already_active',
                    'msg': u'您已激活邮箱，请继续登陆',
                }
            )
        if not user_profile:
            return render(
                request,
                self.template,
                {
                    'status': 'token_error',
                    'msg': u'无效的激活链接',
                }
            )

        user = user_profile.user

        if not default_token_generator.check_token(
                user,
                user_profile.activation_key):
            return render(
                request,
                self.template,
                {
                    'status': 'token_expire',
                    'msg': u'链接已失效',
                    'user': user,
                }
            )

        user.is_active = True
        user_profile.guide_switch = True

        with transaction.atomic():
            user.save()
            user_profile.save()
            self.active_experience_service(user)

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return render(
            request,
            self.template,
            {
                'status': 'success',
                'msg': u'激活成功',
            },
        )


class ValidBDUser(View):

    template = 'client_reset_password.html'

    def get(self, request, token):
        user_profile = get_object_or_none(
            UserProfile,
            activation_key=token,
        )
        if not user_profile:
            return render(
                request,
                self.template,
                {
                    'status': 'token_error',
                    'msg': u'无效的激活链接',
                }
            )
        if user_profile and user_profile.user.is_active:
            return render(
                request,
                self.template,
                {
                    'status': 'already_active',
                    'msg': u'您已激活邮箱，请继续登陆',
                }
            )
        return render(
            request,
            self.template,
            {
                'username': user_profile.user.username,
            }
        )

    def post(self, request, token):
        user_profile = get_object_or_none(
            UserProfile,
            activation_key=token,
        )
        if not user_profile:
            return JsonResponse({
                'status': 'token_error',
                'msg': u'无效的激活链接',
            })

        if user_profile and user_profile.user.is_active:
            return JsonResponse({
                'status': 'already_active',
                'msg': u'您已激活邮箱，请继续登陆',
            })
        user = user_profile.user
        form = BDUserPasswordForm(request.POST, user=user)

        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'ok',
                'msg': '激活成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': form.get_first_errors(),
            })
