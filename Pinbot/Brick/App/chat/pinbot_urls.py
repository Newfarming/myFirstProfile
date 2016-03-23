# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import (
    ChatBox,
    HistoryList,
    SendMsg,
    ChatDetail,
    ChatMsgList,
    StartJobChat,
    StartCardJobChat,
)


urlpatterns = patterns(
    '',
    url(
        '^$',
        login_required(TemplateView.as_view(
            template_name='pinbot_chat_box.html',
        )),
        name='chat-box',
    ),
    url(
        '^chat_box/$',
        ChatBox.as_view(),
        name='chat-chat-box',
    ),
    url(
        '^history_list/$',
        HistoryList.as_view(),
        name='chat-history-list',
    ),
    url(
        '^send_msg/(?P<chat_id>\d+)/$',
        SendMsg.as_view(),
        name='chat-send-msg',
    ),
    url(
        '^chat_msg_list/(?P<chat_id>\d+)/$',
        ChatMsgList.as_view(),
        name='chat-msg-list',
    ),
    url(
        '^chat_detail/(?P<chat_id>\d+)/$',
        ChatDetail.as_view(
            template_name='pinbot_chat_detail.html',
        ),
        name='chat-detail',
    ),
    url(
        '^start_job_chat/(?P<job_id>\d+)/$',
        StartJobChat.as_view(
            user_type='hr',
        ),
        name='chat-start-job-chat',
    ),
    url(
        '^start_card_job_chat/(?P<card_job_id>\d+)/$',
        StartCardJobChat.as_view(
            user_type='hr',
        ),
        name='chat-start-card-job-chat',
    ),
)
