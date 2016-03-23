# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from feed.models import (
    Feed,
    Feed2,
)


def main():
    mongo_feeds = Feed2.objects(
        __raw__={
            'title': {'$ne': ''},
            'feed_type': 1,
            'deleted': False,
        }
    )

    for mf in mongo_feeds:
        title = mf.title
        if not title:
            continue
        sid = str(mf.id)
        Feed.objects.filter(
            feed_obj_id=sid
        ).update(
            title=title
        )
        print title, sid, 'update success'


if __name__ == '__main__':
    main()
