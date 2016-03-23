# coding: utf-8

import datetime

from django.views.generic import View

from .view_mixin import AdvanceQueryMixin
from feed.models import Feed2
from feed.documents import FeedResultFilter

from pin_utils.django_utils import (
    get_int,
    get_oid,
    JsonResponse,
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)


class SaveFeedFilter(LoginRequiredMixin, View, AdvanceQueryMixin):

    def init_query(self):
        self.work_years = self.get_advance_work_years()
        self.degree = self.get_advance_degree()
        self.gender = self.get_advance_gender()
        self.age = self.get_advance_age()
        self.current_area = self.get_current_area()
        self.salary = self.get_advance_salary()

        has_query_advance = (
            self.work_years
            or self.degree
            or self.gender
            or self.age
            or self.current_area
            or self.salary
        )
        if not has_query_advance:
            return JsonResponse({
                'status': 'no_query',
                'msg': 'no query'
            })
        return None

    def init_query_match(self):
        title_match = get_int(self.request.GET.get('title_match', 0))
        self.match_type = 'intelligent' if title_match else 'extend'
        return self.match_type

    def get_feed(self):
        feed_id = self.kwargs.get('feed_id', '')
        feed_oid = get_oid(feed_id)

        if not feed_oid:
            return JsonResponse({
                'status': 'no_feed_id',
                'msg': 'no feed id',
            })

        username = self.request.user.username
        self.feed = Feed2.objects.filter(
            id=feed_oid,
            username=username,
        ).first()

        if not self.feed:
            return JsonResponse({
                'status': 'feed_not_found',
                'msg': 'feed not found',
            })
        return self.feed

    def save_feed_result_filter(self):
        now = datetime.datetime.now()
        username = self.request.user.username
        filters = {
            'work_years': self.work_years,
            'degree': self.degree,
            'gender': self.gender,
            'age': self.age,
            'current_area': self.current_area,
            'salary': self.salary,
            'match_type': self.match_type,
        }
        feed_result_filter = FeedResultFilter(
            add_time=now,
            username=username,
            filters=filters,
            feed=self.feed,
        )
        feed_result_filter.save()
        return feed_result_filter

    def get(self, request, feed_id):
        self.init_query()
        self.init_query_match()
        self.get_feed()
        feed_result_filter = self.save_feed_result_filter()

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'id': str(feed_result_filter.id)
            }
        })
