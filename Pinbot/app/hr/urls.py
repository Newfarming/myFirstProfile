# coding: utf-8

from django.conf.urls import patterns, url
from .views import (
    Login,
    Register,
    WeixinAuth,
    ValidToken,
    UnbindWeixinOpenid,
    QRcodeBind,
    QRcodeRedPack

)
from .backend_views import BackendLogin
from . import admin_views

urlpatterns = patterns(
    '',
    url(
        r'^register/$',
        Register.as_view(),
        name='hr-reg',
    ),
    url(
        r'^login/$',
        Login.as_view(),
        name='hr-login',
    ),
    url(
        r'^weixin_auth/$',
        WeixinAuth.as_view(),
        name='hr-weixin-auth',
    ),
    url(
        r'^valid_token/(?P<user>\d+)/(?P<token>.+)/$',
        ValidToken.as_view(),
        name='hr-valid-token',
    ),
    url(
        r'^backend_login/$',
        BackendLogin.as_view(),
        name='hr-backend-login',
    ),
    url(
        r'^unbind_weixin/$',
        UnbindWeixinOpenid.as_view(),
        name='hr-unbind-weixin',
    ),
    url(
        r'^active_user/(?P<username>.+)/$',
        admin_views.AdminActiveUser.as_view(),
        name='hr-admin-active-user',
    ),
    url(
        r'^qrcode_bind/$',
        QRcodeBind.as_view(),
        name='hr-qrcode-bind',
    ),
    url(
        r'^qrcode_redpack/$',
        QRcodeRedPack.as_view(),
        name='hr-qrcode-redpack',
    ),

)
