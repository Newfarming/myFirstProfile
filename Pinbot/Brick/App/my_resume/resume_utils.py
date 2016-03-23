# coding: utf-8

import bson
import celery
import datetime
import logging

from .models import (
    Resume,
    SearchTag,
)

from Brick.BCelery.celery_app import app
from Brick.App.job_hunting.templatetags.job_tags import (
    cn_display,
)

from resumes.resume_utils import PinbotResumeUtils

from Brick.Utils.mongo_utils import Mongo
from Brick.Utils.django_utils import (
    get_oid,
)
from Brick.RecoCelery.app import app as reco_celery_app

logger = logging.getLogger('brick.exception')


class ResumeUtils(object):

    @classmethod
    def get_resume(cls, user):
        resume_set = Resume.objects.select_related(
            'job_category',
        ).filter(
            user=user
        )
        if not resume_set:
            resume = Resume(
                user=user,
            )
            resume.resume_id = str(bson.ObjectId())
            resume.save()
        else:
            resume = resume_set[0]
        return resume


class SyncResume(object):

    TIME_FORMAT = '%Y-%m'

    @classmethod
    def is_valid_resume(cls, resume):
        phone = resume.phone
        email = resume.email
        works = resume.works.all()
        educations = resume.educations.all()
        valid_resume = (phone and email and works and educations)
        return True if valid_resume else False

    @classmethod
    def get_sync_resume_data(cls, resume):
        resume_data = {
            'contact_info': {
                'name': resume.name,
                'gender': resume.gender,
                'phone': resume.phone,
                'email': resume.email,
                'qq': resume.qq,
                'age': resume.age,
                'school': resume.school,
                'major': resume.major,
                'residence': resume.residence,
                'homepage': resume.homepage,
                'degree': resume.degree,
                'identity_id': resume.identity_id,
                'political_landscape': resume.political_landscape,
                'work_years': str(resume.work_years),
                'birthday': resume.birthday.strftime(cls.TIME_FORMAT),
                'resume_id': resume.id,
            },
            'job_target': {
                'job_category': resume.job_category.name,
                'job_hunting_state': resume.job_hunting_state,
                'expectation_area': ','.join(city.city.name for city in resume.expectation_area.all()),
                'target_salary': resume.target_salary,
            },
            'current_job': {
                'current_salary': resume.current_salary,
            },
            'trainings': [
                {
                    'certificate': train.certificate,
                    'course': train.course,
                    'start_time': train.start_time.strftime(cls.TIME_FORMAT),
                    'end_time': train.end_time.strftime(cls.TIME_FORMAT),
                    'instituation': train.instituation,
                    'location': train.location,
                    'train_desc': train.train_desc,
                }
                for train in resume.trainings.all()
            ],
            'other_info': {
                'content': resume.other_info,
                'title': '',
            },
            'educations': [
                {
                    'start_time': edu.start_time.strftime(cls.TIME_FORMAT),
                    'end_time': edu.end_time.strftime(cls.TIME_FORMAT),
                    'school': edu.school,
                    'degree': edu.degree,
                    'major': edu.major,
                }
                for edu in resume.educations.all()
            ],
            'works': [
                {
                    'start_time': work.start_time.strftime(cls.TIME_FORMAT),
                    'end_time': work.end_time.strftime(cls.TIME_FORMAT),
                    'position_title': work.position_title,
                    'duration': str(work.duration),
                    'min_salary': work.min_salary,
                    'max_salary': work.max_salary,
                    'salary': str(work.max_salary),
                    'position_category': work.position_category,
                    'company_category': work.company_category,
                    'industry_category': work.industry_category,
                    'company_name': work.company_name,
                    'job_desc': work.job_desc,
                    'company_scale': '',
                }
                for work in resume.works.all()
            ],
            'projects': [
                {
                    'start_time': project.start_time.strftime(cls.TIME_FORMAT),
                    'end_time': project.end_time.strftime(cls.TIME_FORMAT),
                    'project_name': project.project_name,
                    'job_title': project.job_title,
                    'project_desc': project.project_desc,
                    'company_name': project.company_name,
                    'responsible_for': project.responsible_for,
                }
                for project in resume.projects.all()
            ],
            'professional_skill': [
                {
                    'skill_desc': skill.skill_desc,
                    'proficiency': skill.proficiency,
                    'month': skill.month,
                }
                for skill in resume.professional_skills.all()
            ],
            'self_evaluation': resume.self_evaluation,
            'research_perf': resume.research_perf,
            'hobbies': resume.hobbies,
            'work_years': str(resume.work_years),
            'marital_status': resume.marital_status,
            'address': resume.address,
            'created_at': resume.create_time,
            'updated_time': resume.update_time,
            'resume_id': resume.resume_id,
            'brick_user': resume.user.username,
            'source': 'brick',
        }
        return resume_data

    @classmethod
    def sync(cls, user):
        resume = ResumeUtils.get_resume(user)
        if not cls.is_valid_resume(resume):
            return False

        resume_data = cls.get_sync_resume_data(resume)
        result = PinbotResumeUtils.save(resume_data)
        return result


class SaveResumeTag(object):

    WORK_YEARS_META = {
        2: '0-1',
        3: '1-3',
        4: '3-5',
        5: '5-8',
        6: '8-15',
    }

    @classmethod
    def save_search_tag(cls, tag, resume):
        citys = ','.join(tag['city'])
        tags = ','.join(tag['tags'])
        company_domains = ','.join(tag['company_domains'])

        SearchTag.objects.filter(
            resume=resume,
            active=True,
        ).update(
            active=False,
        )
        search_tag = SearchTag(
            resume=resume,
            gender=tag['gender'],
            citys=citys,
            category=tag['category'],
            degree=tag['degree'],
            tags=tags,
            work_years=tag['work_years'],
            salary_lowest=tag['salary_lowest'],
            company_domains=company_domains,
        )
        search_tag.save()
        return search_tag

    @classmethod
    def get_search_tag(cls, tag, resume):
        tag_query = resume.search_tags.filter(active=True)

        if not tag_query:
            search_tag = cls.save_search_tag(tag, resume)
            return search_tag

        search_tag = tag_query[0]
        same_tag = (
            search_tag.gender == tag['gender']
            and set(search_tag.citys.split(',')) == set(tag['city'])
            and search_tag.category == tag['category']
            and search_tag.degree == tag['degree']
            and set(search_tag.tags.split(',')) == set(tag['tags'])
            and search_tag.work_years == tag['work_years']
            and search_tag.salary_lowest == tag['salary_lowest']
            and set(search_tag.company_domains.split(',')) == set(tag['company_domains'])
        )
        if same_tag:
            return search_tag
        search_tag = cls.save_search_tag(tag, resume)
        return search_tag

    @classmethod
    def get_search_tag_dict(cls, user, resume):
        now = datetime.datetime.now()
        resume_oid = get_oid(resume.resume_id)

        tag = {
            'user_id': user.id,
            'resume_id': resume_oid,
            'resume_mysql_id': resume.id,
            'gender': cn_display(resume.gender),
            'city': list(resume.expectation_area.all().select_related('city').values_list('city__name', flat=True)),
            'category': resume.job_category.name,
            'degree': cn_display(resume.degree),
            'tags': list(resume.position_tags.all().select_related('position_tag').values_list('position_tag__name', flat=True)),
            'work_years': cls.WORK_YEARS_META.get(resume.work_years, '1-3'),
            'salary_lowest': resume.salary_lowest,
            'company_domains': list(resume.prefer_fields.all().select_related('category').values_list('category__category', flat=True)),
            'update_time': now,
            'has_recommend': False,
            'is_active': True,
        }
        return tag

    @classmethod
    def send_reco_task(cls, tag, search_tag):
        tag['tag_id'] = search_tag.id
        mongo = Mongo
        result = mongo.recruiting.talent_card.find_one(
            {'tag_id': tag['tag_id']},
        )
        if not result:
            user_id = tag['user_id']
            mongo.recruiting.talent_card.update(
                {'user_id': user_id},
                {'$set': {'is_active': False}},
                upsert=False,
                multi=True,
            )
            result_oid = mongo.recruiting.talent_card.insert(tag)
        else:
            result['update'] = True
            mongo.recruiting.talent_card.save(result)
            result_oid = result['_id']

        result = reco_celery_app.send_task(
            'reco_job_es',
            kwargs={
                'talent_card_id': str(result_oid),
            },
            queue='for_reco_job',
        )
        reco_celery_app.send_task(
            'reco_job_es',
            kwargs={
                'talent_card_id': str(result_oid),
                'calc_type': 'complex',
            },
            queue='for_reco_job',
        )

        try:
            result.get(timeout=5)
        except celery.exceptions.TimeoutError:
            username = search_tag.resume.user.username
            tag_id = search_tag.id
            warn_msg = '{username} search tag id {tag_id} get recommend job timeout'.format(
                username=username,
                tag_id=tag_id,
            )
            logger.error(warn_msg, exc_info=True)
            return False
        return True


asyn_sync_resume = app.task(name='sync-pinbot-resume')(SyncResume.sync)
