# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import hidden_egg_views as egg_views
from . import views

from views import (
    Questions,
    QuestionnaireFeedback
)

urlpatterns = patterns(
    '',
    url(
        r'^qixi2015/$',
        TemplateView.as_view(
            template_name='qixi2015.html'
        ),
        name='activity-qixi2015',
    ),
    url(
        '^find_egg/$',
        egg_views.FindEgg.as_view(),
        name='activity-find-egg',
    ),
    url(
        '^get_gift_pool/$',
        egg_views.GetGiftPool.as_view(),
        name='activity-gift-pool',
    ),
    url(
        '^close_easter/$',
        egg_views.CloseEaster.as_view(),
        name='activity-close-easter',
    ),
    url(
        '^user_need/$',
        egg_views.GiftUserNeed.as_view(),
        name='activity-gift-user-need',
    ),
    url(
        r'^rccbz/$',
        TemplateView.as_view(
            template_name='talented_reserve.html'
        ),
        name='activity-talented_reserve',
    ),
    url(
        r'^ndtc/$',
        views.NewPromotionView.as_view(
            template_name='promotion.html'
        ),
        name='activity-promotion',
    ),
    url(
        r'^questionnaire/$',
        login_required(TemplateView.as_view(
            template_name='questionnaire.html'
        )),
        name='activity-questionnaire',
    ),
    url(
        r'^questions/$',
        Questions.as_view(),
        name='activity-questions',
    ),
    url(
        r'^questionnaire_feedback/$',
        QuestionnaireFeedback.as_view(),
        name='activity-question_feedback',
    ),
    url(
        r'^yizhifu/$',
        TemplateView.as_view(
            template_name='orange-financial.html'
        ),
        name='orange-financial',
    ),
    url(
        r'^medicine/$',
        TemplateView.as_view(
            template_name='new_field.html'
        ),
        name='new_field',
    ),
    url(
        r'^medicine/success/$',
        login_required(TemplateView.as_view(
            template_name='new_field_attent.html'
        )),
        name='new_field_attent',
    ),
)
