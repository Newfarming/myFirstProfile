# coding: utf-8

from django.conf.urls import patterns, url
from views import (
    PromotionLink,
    PromotionRecordList,
    SavePromotionClick,
    PromotionRecordJson,
)

urlpatterns = patterns(
    '',
    url(
        r'^link/$',
        PromotionLink.as_view(),
        name='promotion-link'
    ),
    url(
        r'^record_list/$',
        PromotionRecordList.as_view(),
        name='promotion-record-list'
    ),
    url(
        r'^record/list/$',
        PromotionRecordJson.as_view(),
        name='promotion-record-json-list'
    ),
    url(
        r'^save_click_record/(?P<token>.+)/$',
        SavePromotionClick.as_view(),
        name='promotion-save-click-record'
    ),
)
