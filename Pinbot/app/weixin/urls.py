# coding: utf-8
from django.conf.urls import patterns, url
from .views.weixin_views import (
    Index,
    Authorization,
    FeedNotify
)

urlpatterns = patterns(
    '',
    url(
        '^$',
        Index.as_view(),
        name='weixin-index',
    ),
    url(
        '^/authorization$',
        Authorization.as_view(),
        name='weixin-authorize',
    ),
    url(
        '^/feed_notify',
        FeedNotify.as_view(),
        name='weixin-feed-notify',
    ),


)
