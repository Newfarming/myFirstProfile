# coding: utf-8

from django.conf.urls import (
    patterns,
    url,
)

from views import (
    TaskStatus,
    TaskList,
    TaskStatusList,
    ReceiveReward,
    UserRealRewardAddress
)

urlpatterns = patterns(
    '',
    url(
        '^$',
        TaskList.as_view(),
        name='task-list',
    ),
    url(
        '^finished/$',
        TaskStatusList.as_view(),
        name='task-finished-list',
    ),
    url(
        '^receive_reward/$',
        ReceiveReward.as_view(),
        name='receive-reward',
    ),
    url(
        '^task_status/$',
        TaskStatus.as_view(),
        name='task-status',
    ),
    url(
        '^address/$',
        UserRealRewardAddress.as_view(),
        name='task-real-address',
    ),
)
