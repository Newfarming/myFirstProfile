# coding: utf-8

import datetime

from feed.models import (
    FeedResult,
)
from pin_utils.django_utils import get_today


def add_read_rate(day_num, user_feeds):
    start_date = get_today() - datetime.timedelta(days=day_num)
    user_feeds_id = [user_feed.feed.id for user_feed in user_feeds]
    all_feed_count = FeedResult.objects.filter(
        feed__in=user_feeds_id,
        published=True,
        display_time__gt=start_date,
    ).count()

    if all_feed_count == 0:
        return {
            'all_feed_count': 0,
            'all_read_feed_count': 0,
            'read_rate': 0,
        }
    all_read_feed_count = FeedResult.objects.filter(
        feed__in=user_feeds_id,
        user_read_status="read",
        display_time__gt=start_date,
    ).count()

    read_rate = "{:.2f}%".format(100 * (float(all_read_feed_count) / float(all_feed_count)))

    return {
        'all_feed_count': all_feed_count,
        'all_read_feed_count': all_read_feed_count,
        'read_rate': read_rate,
    }
