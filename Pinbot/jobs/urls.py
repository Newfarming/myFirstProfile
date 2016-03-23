# coding:utf-8
'''
Created on 2013-11-25

@author: dell
'''
from django.conf.urls import patterns,url
from views import (
    CompanyCardGet,
    CompanySave,
    JobSave,
    JobDelete,
    Card,
    CompanyCardSend,
    InterestClick,
    CompanyCardGetJson,
    ResumeFilter,
    ResumeBuy,
    CompanyCardTask,
    DeleteCompanyCategory,
    )

urlpatterns = patterns('jobs.views',
    (r'^index/$', 'get_waitting'),
    url(
        r'^get/json/$',
        CompanyCardGetJson.as_view(),
        name='company-card-get-json'
    ),
    url(
        r'^company/save/$',
        CompanySave.as_view(),
        name='company-card-save'
    ),
    url(
        r'^job/save/$',
        JobSave.as_view(),
        name='company-card-job-save'
    ),
    url(
        r'^job/delete/(?P<job_id>\d+)/$',
        JobDelete.as_view(),
        name='company-card-job-delete'
    ),
    url(
        r'^job/preview/(?P<job_id>\d+)/$',
        Card.as_view(),
        name='company-card-job-preview'
    ),
    url(
        r'^card/send/$',
        CompanyCardSend.as_view(),
        name='company-card-job-send'
    ),
    url(
        r'^job/interest/$',
        InterestClick.as_view(),
        name='job-interest'
    ),
    url(
        r'^get/$',
        CompanyCardGet.as_view(),
        name='companycard-get'
    ),
    url(
        r'^resume/filter/$',
        ResumeFilter.as_view(),
        name='resume-filter'
    ),
    url(
        r'^resume/direct_buy/$',
        ResumeBuy.as_view(),
        name='resume-direct_buy-resume'
    ),
    url(
        r'^card/task/send/$',
        CompanyCardTask.as_view(),
        name='resume-direct_buy-resume'
    ),
    url(
        r'^delete_category/(?P<category_id>\d+)/$',
        DeleteCompanyCategory.as_view(),
        name='company-delete-category',
    ),
)
