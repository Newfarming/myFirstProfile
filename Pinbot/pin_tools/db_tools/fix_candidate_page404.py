# coding: utf-8

'''
修复crm中，出现重复的候选人信息，但是一个是404，一个是正常状态的bug
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from resumes.models import (
    ResumeData,
    ContactInfoData,
)
from pin_utils.django_utils import(
    get_oid
)


def update_contactinfo_data():

    all_repeat_data = ContactInfoData.objects.raw(
        """
        select id,name,phone,source,email,count(*) from resumes_contactinfo
        where phone is not null
        group by name,phone,email,source having count(*) > 1
        """
    )
    for data in all_repeat_data:
        piece_repeat_data = ContactInfoData.objects.filter(
            name=data.name,
            phone=data.phone,
            email=data.email,
            source=data.source,
        )
        for repeat_data in piece_repeat_data:
            resume_id = get_oid(repeat_data.resume_id)
            if resume_id and not ResumeData.objects.filter(
                id=resume_id
            ):
                ContactInfoData.objects.filter(
                    resume_id=repeat_data.resume_id
                ).delete()

if __name__ == '__main__':
    update_contactinfo_data()
    print 'deleted the error data'
