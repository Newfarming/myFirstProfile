# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import (
    RecommendJobList,
    JobOperation,
    JobSend,
    MyJobList,
    JobIndex,
    DeleteMyJob,
    CardJobList,
    CardJobAction,
    DeleteCardJob,
    JobDetail,
    JobCardDetail,
    MarkRecommendJobRead,
    LeaveMessage,
    FavourCompany,
)

urlpatterns = patterns(
    '',
    url(
        '^$',
        JobIndex.as_view(),
        name='job-index',
    ),
    url(
        '^recommend_job_list/$',
        RecommendJobList.as_view(),
        name='job-recommend-job-list',
    ),
    url(
        '^contact_consultant/$',
        login_required(TemplateView.as_view(
            template_name='job_consultant.html'
        )),
        name='job-contanct-consulant',
    ),
    url(
        '^my_job/$',
        login_required(TemplateView.as_view(
            template_name='job_my_job.html'
        )),
        name='job-my-job',
    ),
    # 收藏
    url(
        '^favorite/(?P<job_id>\d+)/$',
        JobOperation.as_view(
            action='favorite',
            msg='收藏成功',
        ),
        name='job-favorite-job',
    ),
    # 取消收藏
    url(
        '^dislike/(?P<job_id>\d+)/$',
        JobOperation.as_view(
            action='dislike',
            msg='屏蔽成功',
        ),
        name='job-dislike-job',
    ),
    # 投递
    url(
        '^send/(?P<job_id>\d+)/$',
        JobSend.as_view(),
        name='job-send-job',
    ),
    url(
        '^my_job_list/(?P<action>(favorite|send))/$',
        MyJobList.as_view(),
        name='job-my-job-list',
    ),
    # 删除 “我的投递/我的收藏”
    url(
        '^delete/(?P<job_id>\d+)/$',
        DeleteMyJob.as_view(),
        name='job-delete-my-job',
    ),
    url(
        '^card_job_list/$',
        CardJobList.as_view(),
        name='job-card-job-list',
    ),
    # 感兴趣
    url(
        '^card_accept/(?P<card_id>\d+)/$',
        CardJobAction.as_view(
            action='accept',
            msg='已通知企业',
        ),
        name='job-card-accept',
    ),
    # 不感兴趣
    url(
        '^card_reject/(?P<card_id>\d+)/$',
        CardJobAction.as_view(
            action='reject',
            msg='已通知企业',
        ),
        name='job-card-reject',
    ),
    # 删除职位卡片
    url(
        '^card_delete/(?P<card_id>\d+)/$',
        DeleteCardJob.as_view(
            action='True',
            msg='删除成功',
        ),
        name='job-card-delete',
    ),
    url(
        '^job_detail/(?P<job_id>\d+)/$',
        JobDetail.as_view(),
        name='job-detail',
    ),
    url(
        '^job_card_detail/(?P<job_card_id>\d+)/$',
        JobCardDetail.as_view(),
        name='job-card-detail',
    ),
    url(
        '^mark_job_read/$',
        MarkRecommendJobRead.as_view(),
        name='job-mark-job-read',
    ),
    url(
        '^leave_message/$',
        LeaveMessage.as_view(),
        name='job-leave-message',
    ),
    url(
        '^favour_company/(?P<company_id>\d+)/$',
        FavourCompany.as_view(),
        name='job-favour-company',
    ),
)
