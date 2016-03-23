# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (
    Register,
    SendActiveEmail,
    ValidActiveEmail,
    ChangePassword,
    SendResetPasswordEmail,
    ResetPassword,
    CheckRegisterEmail,
    Login,
)


urlpatterns = patterns(
    '',
    url(
        '^register/$',
        Register.as_view(),
        name='account-register',
    ),
    url(
        '^login/$',
        Login.as_view(),
        name='account-login',
    ),
    url(
        '^send_active_email/(?P<email>.+)/$',
        SendActiveEmail.as_view(),
        name='account-send-active-email',
    ),
    url(
        '^valid_active_email/(?P<activation_key>.+)/$',
        ValidActiveEmail.as_view(),
        name='account-valid-active-email',
    ),
    url(
        '^my_pinbot/$',
        ChangePassword.as_view(),
        name='account-my-pinbot',
    ),
    url(
        '^send_reset_email/(?P<email>.+)/$',
        SendResetPasswordEmail.as_view(),
        name='account-send-reset-email',
    ),
    url(
        '^reset_email/(?P<token>.+)/$',
        ResetPassword.as_view(),
        name='account-reset-password',
    ),
    url(
        '^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='account-logout',
    ),
    url(
        '^check_register_email/$',
        CheckRegisterEmail.as_view(),
        name='account-check-register-email',
    ),
    url(
        '^forget_password/$',
        TemplateView.as_view(
            template_name='account_forget_password.html',
        ),
        name='account-forget-password',
    ),
    url(
        '^forget_password_email/$',
        TemplateView.as_view(
            template_name='account_forget_password_email.html',
        ),
        name='account-forget-password-email',
    ),
    url(
        '^active_email/$',
        TemplateView.as_view(
            template_name='account_active_email.html',
        ),
        name='account-active-email',
    ),
)
