# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from resumes.models import (
    ContactInfoData,
    ResumeData,
)
from feed.models import (
    FeedResult,
)

from pin_utils.django_utils import (
    get_oid,
)


def main():
    resume_sid_list = list(ContactInfoData.objects.filter(
        source='brick',
    ).values_list(
        'resume_id',
        flat=True,
    ))
    resume_oid_list = [get_oid(i) for i in resume_sid_list]

    ResumeData.objects.filter(
        id__in=resume_oid_list
    ).update(
        set__source='brick',
    )
    FeedResult.objects.filter(
        resume__in=resume_oid_list
    ).update(
        set__feed_source='brick',
    )


if __name__ == '__main__':
    main()
