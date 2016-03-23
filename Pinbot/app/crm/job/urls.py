# coding: utf-8

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(
        '^detail/(?P<feed_id>\d+)/$',
        views.JobDetail.as_view(),
        name='crm-job-detail',
    ),
    url(
        '^recruit_num/(?P<feed_id>\d+)/$',
        views.ChangeRecruitNum.as_view(),
        name='crm-job-recruit-num',
    ),
    url(
        '^feed_remark/$',
        views.AddFeedRemark.as_view(),
        name='crm-add-feed-remark',
    ),
)
