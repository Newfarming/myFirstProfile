# coding: utf-8

from jobs.models import Job

from pin_utils.django_utils import (
    get_object_or_none,
)


class JobUtils(object):

    @classmethod
    def bind_job(cls, user, feed, job_id):
        job = get_object_or_none(
            Job,
            id=job_id,
            user=user,
        )
        if not job:
            return False
        feed.bind_job = job
        feed.save()
        return True

    @classmethod
    def delete_job(cls, feed):
        if not feed.bind_job:
            return False
        feed.bind_job.deleted = True
        feed.bind_job.save()
        return True
