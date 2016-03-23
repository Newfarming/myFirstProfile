# coding: utf-8

'''
修复只有mongo feed的feed数据，
将mysql的feed也加入到里面
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from django.contrib.auth.models import User

from feed.models import (
    Feed,
    Feed2,
    UserFeed,
)

from transaction.models import (
    UserChargePackage,
)

from jobs.models import (
    CompanyCategory,
)

from Brick.App.system.models import (
    CompanyCategoryPrefer,
)

from pin_utils.django_utils import (
    get_object_or_none,
)


def create_mysql_feed(mongo_feed, user):
    feed_id = str(mongo_feed.id)
    mysql_feed_query = Feed.objects.filter(
        feed_obj_id=feed_id
    )

    if mysql_feed_query:
        mysql_feed = mysql_feed_query
    else:
        mysql_feed = Feed(
            keywords=mongo_feed.keywords,
            talent_level=mongo_feed.talent_level,
            expect_area=mongo_feed.expect_area,
            job_desc=mongo_feed.job_desc,
            salary_min=mongo_feed.salary_min,
            salary_max=mongo_feed.salary_max,
            feed_type=mongo_feed.feed_type,
            job_welfare=','.join(mongo_feed.job_welfare) if mongo_feed.job_welfare else '',
            language=mongo_feed.language,
            degree=mongo_feed.degree,
            major=mongo_feed.major,
            job_type=mongo_feed.job_type,
            user=user,
            expire_time=mongo_feed.expire_time,
            feed_expire_time=mongo_feed.feed_expire_time,
            feed_obj_id=str(mongo_feed.id),
        )
    job_domain = [
        get_object_or_none(
            CompanyCategory,
            category=domain,
        )
        for domain in mongo_feed.job_domain
    ]
    prefer = [
        get_object_or_none(
            CompanyCategoryPrefer,
            name=name,
        )
        for name in mongo_feed.company_prefer
    ]
    mysql_feed.save()
    mysql_feed.job_domain.add(*job_domain)
    mysql_feed.company_prefer.add(*prefer)
    mysql_feed.save()
    return mysql_feed


def create_mysql_userfeed(mongo_feed, user, mysql_feed, feed_pkg):
    user_feed = UserFeed(
        user=user,
        add_time=mongo_feed.add_time,
    )
    user_feed.user_charge_pkg = feed_pkg
    user_feed.expire_time = feed_pkg.feed_end_time
    user_feed.feed = mysql_feed
    user_feed.save()
    return user_feed


def fix_mysql_feed(username):
    feed_id_list = Feed2.objects.filter(
        username=username,
        feed_type=1,
        deleted=False,
    )

    for feed in feed_id_list:
        mongo_feed = feed
        feed_oid = feed.id
        feed_id = str(feed_oid)

        expire_time = mongo_feed.expire_time
        username = mongo_feed.username

        user = get_object_or_none(
            User,
            username=username,
        )
        feed_pkg = get_object_or_none(
            UserChargePackage,
            feed_end_time=expire_time,
            user=user,
        )

        mysql_feed = create_mysql_feed(mongo_feed, user)
        create_mysql_userfeed(mongo_feed, user, mysql_feed, feed_pkg)
        print 'save %s success' % feed_id


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print '''
        run this script
        python fix_mysql_feed.py username
        '''

    username = sys.argv[1]
    fix_mysql_feed(username)
