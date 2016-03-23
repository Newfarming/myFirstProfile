# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from views import(
    InterviewTerm,
    FeedBack,
)


urlpatterns = patterns(
    '',
    url(
        r'^$',
        login_required(
            TemplateView.as_view(template_name='tutorial.html'),
        ),
        name='tutorial',
    ),
    url(
        r'^interview_term/$',
        InterviewTerm.as_view(),
        name='interview-term',
    ),
    url(
        r'^feedback/$',
        FeedBack.as_view(),
        name='feedback',
    ),
)
