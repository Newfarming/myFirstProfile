# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from feed.models import (
    Feed,
    UserFeed,
    Feed2,
    UserFeed2,
    FeedResult,
)

from transaction.models import UserChargePackage


def remove_feed_results(feed_oid_list):
    FeedResult.objects.filter(feed__in=feed_oid_list).delete()


def remove_mongo_user_feed(feed_oid_list):
    UserFeed2.objects.filter(feed__in=feed_oid_list).delete()


def remove_mongo_feed(feed_oid_list):
    Feed2.objects.filter(id__in=feed_oid_list, feed_type=2).delete()


def remove_user_feed(feed_id_list):
    UserFeed.objects.filter(feed__id__in=feed_id_list).delete()


def remove_feed(feed_id_list):
    Feed.objects.filter(id__in=feed_id_list).delete()


def remove_mysql():
    for i in xrange(160):
        feed_query = Feed.objects.filter(feed_type=2)[:1000]
        feed_id_list = [feed.id for feed in feed_query]

        remove_user_feed(feed_id_list)
        print 'remove user feed success'

        remove_feed(feed_id_list)
        print 'remove feed success'

    UserChargePackage.objects.filter(pkg_source=2).delete()
    print 'remove useless package success'


def remove_mongo():
    for i in xrange(160):
        feed_query = Feed2.objects.filter(feed_type=2)[:1000]
        feed_oid_list = [feed.id for feed in feed_query]

        remove_feed_results(feed_oid_list)
        print 'remove feed result success'

        remove_mongo_user_feed(feed_oid_list)
        print 'remove mongo user feed success'

        remove_mongo_feed(feed_oid_list)
        print 'remove mongo feed success'


def main():
    remove_mysql()
    remove_mongo()


if __name__ == '__main__':
    main()
