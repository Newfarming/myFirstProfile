# coding: utf-8

from django.conf.urls import patterns, include, url
from settings import MEDIA_ROOT
from django.views.generic import TemplateView

import xadmin
xadmin.autodiscover()

from users.account_views import (
    Register,
)


urlpatterns = patterns(
    '',
    url(
        r'^$',
        TemplateView.as_view(template_name='index.html'),
    ),
    (r'^signin/$', 'users.views.signin'),
    (r'^plugsignin/$', 'users.views.plugsignin'),
    url(
        r'^gotopinbot/$',
        'users.views.gotopinbot',
        name='goto-pinbot',
    ),
    (r'^who_am_i/$', 'users.views.who_am_i'),
    (r'^plugin_login/$', 'users.views.plugsignin'),
    (r'^plugin_logout/$', 'users.views.plugin_logout'),
    (r'^login/$', 'users.views.plugsignin'),
    url(
        r'^signup/$',
        Register.as_view(),
        name='pinbot-signup'
    ),
    (r'^signup_confirm/$', 'users.views.singnup_check'),
    (r'^complete_information', 'users.views.complete_information'),
    url(r'^signout', 'users.views.signout', name='pinbot-signout'),
    (r'^resumes/', include('resumes.urls', app_name='resumes')),
    (r'^users/', include('users.urls', app_name='users')),
    (r'^feed/', include('feed.urls', app_name='feed')),
    (r'transaction/', include('transaction.urls', app_name='transaction')),
    (r'xadmin/', include(xadmin.site.urls, app_name='xadmin')),
    (r'jobs/', include('jobs.urls', app_name='jobs')),
    (r'^statis/', include('statistics.urls', app_name='statistics')),
    (r'taocv/', include('taocv.urls', app_name='taocv')),
    url(r'^promotion_point/', include('app.promotion_point.urls', app_name='promotion_point')),
    url(r'^special_feed/', include('app.special_feed.urls', app_name='app.special_feed')),
    url(r'^payment/', include('app.payment.urls', app_name='app.payment')),
    url(r'^companycard/', include('jobs.urls', app_name='app.jobs')),
    url(r'^activity/', include('app.activity.urls', app_name='app.activity')),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^email/', include('app.sendemail.urls', app_name=u'app.sendemail')),
    url(r'^invite/', include('app.invite.urls', app_name='app.invite')),
    url(r'^notify/', include('Brick.App.notify.pinbot_urls', app_name='Brick.App.notify')),
    url(r'^chat/', include('Brick.App.chat.pinbot_urls', app_name='Brick.App.chat')),
    url(r'^crm/', include('app.crm.urls', app_name=u'app.crm')),
    url(r'^vip/', include('app.vip.urls', app_name='app.vip')),
    url(r'^tut/', include('app.tutorial.urls', app_name='app.tutorial')),
    url(r'^partner/', include('app.partner.urls', app_name='app.partner')),
    url(r'^weixin', include('app.weixin.urls', app_name='app.weixin')),
    url(r'^hr/', include('app.hr.urls', app_name='app.hr')),
    url(r'^resume/', include('app.resume.urls', app_name='app.resume')),
    url(r'^telnetapi/', include('app.telnet_api.urls', app_name='app.telnet_api')),
    url(r'^task/', include('app.task_system.urls', app_name='app.task_system')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(
        r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': MEDIA_ROOT,
        }
    ),
)
