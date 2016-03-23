# coding: utf-8

from django.conf.urls import patterns, url

from .views import SendNotify, GetToken
from . import contact_api


urlpatterns = patterns(
    '',
    url(
        '^gettoken/$',
        GetToken.as_view(),
        name='get-token',
    ),
    url(
        '^sendnotify/$',
        SendNotify.as_view(),
        name='send-notify',
    ),
    url(
        '^contactinfo/update/$',
        contact_api.UpdateContactInfo.as_view(),
        name='contactinfo-update',
    ),
)
