# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (
    ValidActiveEmail,
    SendActiveEmail,
    ValidBDUser
)

from .account_views import (
    Register,
    Login,
    VaildSmsCode,
    SendSmsCode,
    ChangMobile,
    ChangeNotifyEmail,
    ValidNotifyEmail,
    SendEmailCode,
    NotifyEmailIsBind,
    FindPwdByMobile,
    BindNotifyEmail,
    ReSendBindNotifyEmail,
    ChanageMyRecvInfo,
    ChangeCompanyInfo,
    ChangeMyInfo,
    ChangeMyPassword,
    UserProfile,
    WeixinIsBind,
    IndustryBookin
)

urlpatterns = patterns(
    'users.views',
    (r'^logout$', 'plugin_logout'),
    url(
        r'^login/$',
        'plugsignin',
    ),
    (r'^change_profile/source=ajax/$', 'profile_ajax'),
    (r'^change_profile/$', 'profile'),
    (r'^get_check_code_image/$', 'get_check_code_image'),
    (r'^resetpassword/$', 'my_password_reset'),
    (r'^resetpassword/(?P<uidb36>[0-9A-Za-z]+)?-(?P<token>.+)/$', 'my_password_confirm'),
    (r'^resetpassword/(?P<type>.+)/(?P<uidb36>[0-9A-Za-z]+)?-(?P<token>.+)/$', 'my_password_confirm'),
    (r'^reset_password_confirm/$', 'my_password_confirm'),
    (r'^password_confirm_ajax/$', 'password_confirm_ajax'),
    (r'^changepassword/$', 'change_password'),
    (r'^active/$', 'send_active_email'),
    (r'active/(?P<activation_key>.+)/$', 'activate'),
    (r'send_mail', 'send_mail'),
    (r'price', 'get_price'),
    (r'feature', 'get_feature'),
    url(
        '^valid_active_email/(?P<activation_key>.+)/$',
        ValidActiveEmail.as_view(),
        name='user-valid-active-email',
    ),
    # 激活成功
    url(
        '^valid_vip_email/(?P<activation_key>.+)/$',
        ValidActiveEmail.as_view(
            template='register_active_success.html'
        ),
        name='user-valid-vip-email',
    ),
    url(
        '^send_active_email/(?P<email>.+)/$',
        SendActiveEmail.as_view(),
        name='user-send-active-email',
    ),
    # 注册激活，再次发送邮件接口
    url(
        '^send_vip_active_email/(?P<email>.+)/$',
        SendActiveEmail.as_view(
            email_template='vip_active_email.html',
            valid_url_name='user-valid-vip-email',
        ),
        name='user-send-vip-active-email',
    ),
    url(
        '^register_success/$',
        TemplateView.as_view(template_name='client_register_success.html'),
        name='users-register-success',
    ),
    url(
        '^valid_bduser/(?P<token>.+)/$',
        ValidBDUser.as_view(),
        name='user-valid-bduser',
    ),
    url(
        '^vip_protocal/$',
        TemplateView.as_view(template_name='vip_protocal.html'),
        name='vip-protocal',
    ),
    # 注册后，激活页面（记得结尾加斜杠）
    url(
        r'^signup_activate/$',
        TemplateView.as_view(
            template_name='signup_activate.html'
        ),
        name='signup_activate',
    ),
    # 新账号机制
    # 注册
    url(
        '^account_register/$',
        Register.as_view(),
        name='user-account-reg',
    ),
    url(
        '^account_login/$',
        Login.as_view(),
        name='user-account-login',
    ),
    url(
        '^send_sms_code/$',
        SendSmsCode.as_view(),
        name='user-send-sms-code',
    ),
    url(
        '^vaild_sms_code/$',
        VaildSmsCode.as_view(),
        name='user-vaild-sms-code',
    ),
    url(
        '^change_mobile/$',
        ChangMobile.as_view(),
        name='user-change-mobile',
    ),
    url(
        '^change_pwd_by_mobile/$',
        FindPwdByMobile.as_view(),
        name='user-change-pwd-mobile',
    ),
    url(
        '^valid_notify_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<activation_key>.+)/$',
        ValidNotifyEmail.as_view(),
        name='user-valid-notify-email',
    ),
    url(
        '^send_email_code/$',
        SendEmailCode.as_view(),
        name='user-send-email-code',
    ),
    url(
        '^change_notify_email/$',
        ChangeNotifyEmail.as_view(),
        name='user-change-notify-email',
    ),
    url(
        'notify_email_is_bind/$',
        NotifyEmailIsBind.as_view(),
        name='user-notify-email-is-bind',
    ),
    url(
        'bind_notify_email/$',
        BindNotifyEmail.as_view(),
        name='user-bind-notify-email',
    ),
    url(
        'resend_bind_email/$',
        ReSendBindNotifyEmail.as_view(),
        name='user-resend-bind-email',
    ),
    url(
        'change_my_pwd/$',
        ChangeMyPassword.as_view(),
        name='user-change-my-pwd',
    ),
    url(
        'change_company_info/$',
        ChangeCompanyInfo.as_view(),
        name='user-change-company-info',
    ),
    url(
        'change_my_info/$',
        ChangeMyInfo.as_view(),
        name='user-change-my-info',
    ),
    url(
        'change_my_recv_info/$',
        ChanageMyRecvInfo.as_view(),
        name='user-change-my-recv-info',
    ),
    url(
        'profile/$',
        UserProfile.as_view(),
        name='user-profile',
    ),
    url(
        'weixin_isbind/$',
        WeixinIsBind.as_view(),
        name='user-weixin-isbind',
    ),
    url(
        'new_industry_bookin/$',
        IndustryBookin.as_view(),
        name='user-new-industry-bookin',
    )
)
