# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from django.contrib.auth.models import User

from users.models import UserProfile
from feed.models import Feed2, UserFeed2, FeedResult

from pin_utils.django_utils import get_oid


def get_feed_oid_list(user):
    feed_id_list = list(user.feed_set.all().values_list('feed_obj_id', flat=True))
    feed_oid_list = [get_oid(feed_id) for feed_id in feed_id_list if get_oid(feed_id)]
    return feed_oid_list


def remove_feed_results(feed_oid_list):
    FeedResult.objects.filter(feed__in=feed_oid_list).delete()


def remove_mongo_user_feed(username, feed_oid_list):
    UserFeed2.objects.filter(username=username, feed__in=feed_oid_list).delete()


def remove_mongo_feed(username, feed_oid_list):
    Feed2.objects.filter(username=username, id__in=feed_oid_list).delete()


def remove_company(user):
    user.company_set.all().delete()


def remove_user_charge_pkg(user):
    user.userchargepackage_set.all().delete()


def remove_userprofile(user):
    UserProfile.objects.filter(user=user).delete()


def remove_user_feed(user):
    user.userfeed_set.all().delete()


def remove_feed(user):
    user.feed_set.all().delete()


def remove_user(user):
    User.objects.filter(id=user.id).delete()


def main():
    userprofile_query = UserProfile.objects.select_related(
        'user',
    ).filter(
        source=2,
        user__is_active=False,
    )

    for userprofile in userprofile_query:
        user = userprofile.user
        username = user.username
        feed_oid_list = get_feed_oid_list(user)

        print 'username %s start remove' % username

        remove_feed_results(feed_oid_list)
        print 'remove feed results success'

        remove_mongo_user_feed(username, feed_oid_list)
        print 'remove mongo user feed success'

        remove_mongo_feed(username, feed_oid_list)
        print 'remove mongo feed success'

        remove_company(user)
        print 'remove company success'

        remove_user_feed(user)
        print 'remove user feed success'

        remove_feed(user)
        print 'remove feed success'

        remove_user_charge_pkg(user)
        print 'remove user charge pkg'

        remove_userprofile(user)
        print 'remove user profile'

        remove_user(user)
        print 'remove user'


if __name__ == '__main__':
    main()
