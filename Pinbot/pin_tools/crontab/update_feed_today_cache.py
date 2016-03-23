# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from app.special_feed.feed_utils import FeedCacheUtils


def main():
    FeedCacheUtils.update_today_cache()


if __name__ == '__main__':
    main()
