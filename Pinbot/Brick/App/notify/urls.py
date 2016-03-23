# coding: utf-8

from django.conf.urls import patterns, url

from .views import (
    NotifyList,
    MarkNotifyRead,
    DebugWebSocket,
    NotifyIndex,
)

urlpatterns = patterns(
    '',
    url(
        '^$',
        NotifyIndex.as_view(),
        name='notify-index',
    ),
    url(
        '^notify_list/$',
        NotifyList.as_view(),
        name='notify-list',
    ),
    url(
        '^mark_notify_read/(?P<notify_id>\d+)/$',
        MarkNotifyRead.as_view(),
        name='notify-mark-notify-read',
    ),
    url(
        '^mark_all_read/$',
        MarkNotifyRead.as_view(),
        name='notify-mark-all-read',
    ),
    url(
        '^debug_websocket/$',
        DebugWebSocket.as_view(),
    ),
)
