# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from feed.models import (
    Feed,
    Feed2,
)
from pin_utils.django_utils import get_oid

start_time = datetime.datetime(2015, 11, 17)


def main():
    mysql_feeds = Feed.objects.filter(
        feed_type=1,
        deleted=False,
        update_time__gt=start_time,
    )

    for feed in mysql_feeds:
        feed_oid = get_oid(feed.feed_obj_id)
        keywords = feed.keywords
        analyze_titles = feed.analyze_titles

        Feed2.objects.filter(id=feed_oid).update(
            set__keywords=keywords,
            set__analyze_titles=analyze_titles
        )
        print feed.feed_obj_id, 'update success'


if __name__ == '__main__':
    main()
