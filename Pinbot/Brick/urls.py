# coding: utf-8

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

import xadmin
xadmin.autodiscover()

from app.invite.views import (
    ApplyInviteCode,
)

admin.autodiscover()

import notifications

urlpatterns = patterns(
    '',
    url(
        r'^$',
        ApplyInviteCode.as_view(),
        name='brick-index',
    ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
    url(r'^account/', include('Brick.App.account.urls')),
    url(r'^job/', include('Brick.App.job_hunting.urls')),
    url(r'^my_resume/', include('Brick.App.my_resume.urls')),
    url(r'^notify/', include('Brick.App.notify.urls')),
    url(r'^chat/', include('Brick.App.chat.urls')),
    url(r'^invite/', include('app.invite.urls')),
    url(r'^email/', include('app.sendemail.urls')),
    url(
        '^default/$',
        login_required(
            TemplateView.as_view(template_name='index.html'),
        ),
    ),
    url(
        '^notfound/$',
        login_required(
            TemplateView.as_view(template_name='404.html'),
        ),
    ),
    url(
        '^error/$',
        login_required(
            TemplateView.as_view(template_name='500.html'),
        ),
    ),
    # third part app
    url(r'^inbox/notifications/', include(notifications.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler500 = "Brick.views.handler500"
