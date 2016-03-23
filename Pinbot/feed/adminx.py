# coding: utf-8

import xadmin

from . import models


class FeedAdmin(object):

    def queryset(self):
        queryset = super(FeedAdmin, self).queryset()
        queryset = queryset.filter(feed_type=1)
        return queryset

    list_display = [
        'user',
        'title',
        'keywords',
        'expect_area',
        'show_company_name',
        'job_type',
        'deleted',
        'add_time',
        'fast_find',
        'expire_time',
        'last_click_time',
        'feed_expire_status',
        'feed_expire_time',
        'reco_results',
    ]

    list_filter = [
        'user',
        'keywords',
        'expect_area',
        'job_type',
        'deleted',
        'add_time',
        'expire_time',
        'feed_expire_time',
        'last_click_time',
        'feed_type',
    ]

    search_fields = [
        'user__username',
    ]

    list_select_related = (
        'user',
    )


class UserFeedAdmin(object):

    list_display = [
        'user',
        'feed',
        'user_charge_pkg',
        'is_deleted',
        'add_time',
    ]


xadmin.site.register(models.Feed, FeedAdmin)
