# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from app.partner.models import RecoResumeTask
from app.special_feed.feed_utils import FeedUtils


def main():
    reco_task_query = RecoResumeTask.objects.select_related(
        'feed',
        'resume',
    ).filter(
        action=1,
    )

    for rt in reco_task_query:
        feed_obj_id = rt.feed.feed_obj_id
        resume_id = rt.upload_resume.resume_id

        FeedUtils.add_feed_result(
            feed_obj_id,
            resume_id,
            source='talent_partner',
        )
        print feed_obj_id, 'success'


if __name__ == '__main__':
    main()
