# coding: utf-8

import logging

from .app import app

django_log = logging.getLogger('django')


class CeleryUtils(object):

    @classmethod
    def user_feed_task(cls, feed_id):
        reco_task = app.send_task(
            'reco_talent',
            kwargs={'feed_id': feed_id}
        )
        crawl_task = app.send_task(
            'crawl_resumes',
            kwargs={
                'feed_str_id_list': [feed_id],
            }
        )
        django_log.info(
            'celery_reco_task feed_id {0} reco_task_id {1} crawl_task_id {2}'.format(
                feed_id,
                reco_task.task_id,
                crawl_task.task_id,
            )
        )
        return reco_task

    @classmethod
    def admin_feed_task(cls, username):
        app.send_task(
            'crawl_resumes',
            kwargs={
                'username_list': [
                    username,
                ]
            }
        )

    @classmethod
    def admin_send_reco_task(cls, feed_id):
        task_ret = app.send_task(
            'reco_talent',
            kwargs={
                'feed_id': feed_id,
                'notify': False,
                'pub_with_calc': False,
            }
        )
        django_log.info(
            'celery_admin_reco_task feed_id {0} reco_task_id {1}'.format(
                feed_id,
                task_ret.task_id,
            )
        )
        return task_ret
