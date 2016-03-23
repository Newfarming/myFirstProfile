# coding: utf-8

import datetime

from .models import (
    ContactInfoData,
    ResumeData,
)

from pin_utils.django_utils import (
    get_int,
    get_object_or_none,
    update_document,
    get_oid,
)


class PinbotResumeUtils(object):

    @classmethod
    def save_upload_contactinfo(cls, contact_dict, resume_id):
        contact_info = ContactInfoData(
            resume_id=resume_id,
            name=contact_dict.get('name', ''),
            qq=contact_dict.get('qq', ''),
            source=contact_dict.get('source', 'brick'),
            source_id=contact_dict.get('resume_id', ''),
            phone=contact_dict.get('phone', ''),
            email=contact_dict.get('email', ''),
            weibo=contact_dict.get('weibo', ''),
            identity_id=contact_dict.get('identity_id', ''),
        )
        contact_info.save()
        return contact_info

    @classmethod
    def save_upload_resume(cls, contact_dict, parse_resume):
        now = datetime.datetime.now()

        resume = ResumeData(
            id=get_oid(parse_resume.get('resume_id', '')),
            name=contact_dict.get('name', ''),
            email=contact_dict.get('email', ''),
            phone=contact_dict.get('phone', ''),
            age=get_int(contact_dict.get('age', 0)),
            gender=contact_dict.get('gender', ''),
            birthday=contact_dict.get('birthday', ''),
            residence=contact_dict.get('residence', ''),
            address=parse_resume.get('address', ''),
            work_years=parse_resume.get('work_years', ''),
            job_target=parse_resume.get('job_target', {}),
            educations=parse_resume.get('educations', []),
            works=parse_resume.get('works', []),
            projects=parse_resume.get('projects', []),
            trains=parse_resume.get('trains', []),
            professional_skills=parse_resume.get('professional_skills', []),
            self_evaluation=parse_resume.get('self_evaluation', ''),
            created_at=parse_resume.get('created_at', now),
            updated_at=parse_resume.get('updated_at', now),
            created_time=parse_resume.get('created_time', now),
            update_time=parse_resume.get('update_time', now.strftime('%Y-%m-%d')),
            source=parse_resume.get('source', ''),
            owner=parse_resume.get('owner', ''),
            last_contact=parse_resume.get('last_contact', ''),
            hr_evaluate=parse_resume.get('hr_evaluate', ''),
            source_id=parse_resume.get('source_id') or parse_resume.get('resume_id', ''),
            view_id=parse_resume.get('view_id') or parse_resume.get('resume_id', ''),
            url_id=parse_resume.get('url_id') or parse_resume.get('resume_id', ''),
            url='http://pinbot.me/resumes/display/{0}/'.format(parse_resume.get('resume_id', '')),
        )
        resume.save()
        return resume

    @classmethod
    def update_contact_info(cls, update_resume, contact_dict):
        contact_info = get_object_or_none(
            ContactInfoData,
            resume_id=str(update_resume.id)
        )
        if not contact_info:
            return None

        contact_info.name = contact_dict.get('name', '')
        contact_info.qq = contact_dict.get('qq', '')
        contact_info.phone = contact_dict.get('phone', '')
        contact_info.email = contact_dict.get('email', '')
        contact_info.weibo = contact_dict.get('weibo', '')
        contact_info.identity_id = contact_dict.get('identity_id', '')
        contact_info.source = contact_dict.get('source', '')

        contact_info.save()
        return contact_info

    @classmethod
    def update_resume_data(cls, update_resume, parse_resume, contact_dict):
        now = datetime.datetime.now()
        update_resume = update_document(
            update_resume,
            name=contact_dict.get('name', ''),
            email=contact_dict.get('email', ''),
            phone=contact_dict.get('phone', ''),
            gender=contact_dict.get('gender', ''),
            age=get_int(contact_dict.get('age', 0)),
            birthday=contact_dict.get('birthday', ''),
            residence=contact_dict.get('residence', ''),
            address=parse_resume.get('address', ''),
            work_years=parse_resume.get('work_years', ''),
            job_target=parse_resume.get('job_target', {}),
            educations=parse_resume.get('educations', []),
            works=parse_resume.get('works', []),
            projects=parse_resume.get('projects', []),
            trains=parse_resume.get('trains', []),
            professional_skills=parse_resume.get('professionals_skills', []),
            self_evaluation=parse_resume.get('self_evaluation', ''),
            other_info=parse_resume.get('other_info', {}),
            created_at=parse_resume.get('created_at', now),
            created_time=parse_resume.get('created_time', now),
            updated_at=parse_resume.get('updated_at', now),
            update_time=parse_resume.get('update_time', now.strftime('%Y-%m-%d')),
            source=parse_resume.get('source', ''),
            owner=parse_resume.get('owner', ''),
            last_contact=parse_resume.get('last_contact', ''),
            hr_evaluate=parse_resume.get('hr_evaluate', ''),
            source_id=parse_resume.get('source_id') or parse_resume.get('resume_id', ''),
            view_id=parse_resume.get('view_id') or parse_resume.get('resume_id', ''),
            url_id=parse_resume.get('url_id') or parse_resume.get('resume_id', ''),
            url='http://pinbot.me/resumes/display/{0}/'.format(parse_resume.get('resume_id', '')),
        )
        update_resume.save()
        return update_resume

    @classmethod
    def get_update_resume(cls, resume_id):
        resume_oid = get_oid(resume_id)
        if not resume_oid:
            return False

        update_resume = ResumeData.objects.filter(
            id=resume_oid,
        ).first()
        return update_resume

    @classmethod
    def update_resume(cls, update_resume, resume_data, contactinfo_data):
        resume = cls.update_resume_data(
            update_resume,
            resume_data,
            contactinfo_data,
        )
        contact_info = cls.update_contact_info(
            update_resume,
            contactinfo_data,
        )
        return resume, contact_info

    @classmethod
    def create_upload_resume(cls, resume_data, contact_data):
        upload_resume = cls.save_upload_resume(
            contact_data,
            resume_data,
        )
        upload_resume_id = str(upload_resume.id)
        upload_contactinfo = cls.save_upload_contactinfo(
            contact_data,
            upload_resume_id,
        )
        return upload_resume, upload_contactinfo

    @classmethod
    def save(cls, resume_data):
        contactinfo_data = resume_data.get('contact_info', {})
        update_resume_id = resume_data.get('resume_id', '')

        update_resume = cls.get_update_resume(update_resume_id)
        if update_resume:
            resume, contact_info = cls.update_resume(
                update_resume,
                resume_data,
                contactinfo_data,
            )
        else:
            resume, contact_info = cls.create_upload_resume(
                resume_data,
                contactinfo_data,
            )
        return resume, contact_info
