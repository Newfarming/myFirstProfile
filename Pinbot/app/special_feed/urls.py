# coding: utf-8

from django.conf.urls import patterns, url

from .views import (
    SpecialFeedPage,
    SpecialFeedList,
    VerifyFeedList,
    PublishFeedResult,
    ResetFeedExpireTime,
    GetRestFeed,
    RenewalFeed,
)
from .edit_views import (
    EditFeed,
    SubmitFeed,
    AnalyzeJD,
    PredictionNum,
    PredictionSalary,
    PredictionRelated,
)
from . import admin_views
from . import statistic_views


urlpatterns = patterns(
    '',
    url(
        r'^page/$',
        SpecialFeedPage.as_view(template_name='re_feed_list.html'),
        name='special-feed-page'
    ),
    url(
        r'^feed_list/(?P<feed_id>\w+)',
        SpecialFeedList.as_view(),
        name='special-feed-list',
    ),
    url(
        r'^verify_list/(?P<feed_id>\w+)/$',
        VerifyFeedList.as_view(),
        name='special-verify-list'
    ),
    url(
        r'^publish_feed/$',
        PublishFeedResult.as_view(),
        name='special-publish-feed'
    ),
    url(
        r'^reset_feed_expire/(?P<feed_id>.+)/$',
        ResetFeedExpireTime.as_view(),
        name='special-reset-feed-expire'
    ),
    url(
        r'^get_rest_feed/$',
        GetRestFeed.as_view(),
        name='special-get-rest-feed'
    ),
    url(
        r'^renewal_feed/(?P<feed_id>.+)/$',
        RenewalFeed.as_view(),
        name='special-renewal-feed'
    ),
    url(
        r'^edit_feed/(?P<feed_id>.+)/$',
        EditFeed.as_view(),
        name='special-edit-feed'
    ),
    url(
        r'^edit_feed/$',
        EditFeed.as_view(),
        name='special-new-feed'
    ),
    url(
        r'^re_feed_list/$',
        SpecialFeedPage.as_view(template_name='re_feed_list.html'),
    ),
    url(
        '^analyze_jd/$',
        AnalyzeJD.as_view(),
        name='special-analyze-jd',
    ),
    url(
        '^analyze_salary/$',
        PredictionSalary.as_view(),
        name='special-prediction-salary',
    ),
    url(
        '^analyze_num/$',
        PredictionNum.as_view(),
        name='special-prediction-num',
    ),
    url(
        '^submit_feed/$',
        SubmitFeed.as_view(),
        name='special-submit-feed',
    ),
    url(
        '^analyze_related/$',
        PredictionRelated.as_view(),
        name='special-prediction-related',
    ),
    url(
        '^admin/send_reco_task/(?P<feed_id>.+)/$',
        admin_views.AdminSendRecoTask.as_view(),
        name='special-admin-send-task',
    ),
    url(
        '^statistic/save_feed_filter/(?P<feed_id>.+)/$',
        statistic_views.SaveFeedFilter.as_view(),
        name='special-statistic-save-filter',
    ),
)
