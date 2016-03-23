# coding: utf-8

from django.conf.urls import patterns, url

from .views import (
    follow_views,
    center_views,
    companycard_views,
)

urlpatterns = patterns(
    '',
    url(
        r'^follow/list/$',
        follow_views.FollowResumeList.as_view(),
        name='resume-follow-list'
    ),
    url(
        r'^interview/send/(?P<record_id>.+)/$',
        follow_views.SendInterview.as_view(),
        name='resume-send-interview'
    ),
    url(
        r'^interview_time/change/(?P<record_id>.+)/$',
        follow_views.ChangeInterviewTime.as_view(),
        name='resume-send-interview'
    ),
    url(
        r'^center/$',
        center_views.ResumeCenter.as_view(),
        name='resume-center'
    ),
    url(
        r'^buy_record/list/$',
        center_views.ResumeBuyRecordList.as_view(),
        name='resume-buy-record'
    ),
    url(
        r'^send_record/list/$',
        companycard_views.CompanyCardList.as_view(),
        name='resume-buy-record'
    ),
    url(
        r'^category/create/$',
        center_views.CreateBuyRecordCategory.as_view(),
        name='resume-category-create'
    ),
    url(
        r'^category/update/(?P<category_id>\d+)/$',
        center_views.UpdateBuyRecordCategory.as_view(),
        name='resume-category-update'
    ),
    url(
        r'^category/delete/(?P<category_id>\d+)/$',
        center_views.DeleteBuyRecordCategory.as_view(),
        name='resume-category-update'
    ),
    url(
        r'^category_resume/(?P<category_id>\d+)/$',
        center_views.CategoryResume.as_view(),
        name='resume-category-resume'
    ),
    url(
        r'^category_resume/remove/(?P<category_id>\d+)/$',
        center_views.RemoveCategoryResume.as_view(),
        name='resume-remove-category-resume'
    ),
    url(
        r'^side/$',
        center_views.ResumeSide.as_view(),
        name='resume-side'
    ),
)
