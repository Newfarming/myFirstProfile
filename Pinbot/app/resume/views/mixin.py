# coding: utf-8

import itertools

from resumes.models import (
    ResumeData,
    Comment,
    ContactInfoData,
)

from resumes.helper import mongo_to_dict

from pin_utils.django_utils import (
    str2datetime,
    get_oid,
)
from pin_utils.parse_utils import (
    ParseUtils,
)


class ResumeInfoMixin(object):

    def get_latest_edu(self, resume):
        edus = resume.get('educations', [{}])
        sort_edus = sorted([i for i in edus if i], key=lambda x: str2datetime(x.get('start_time')), reverse=True)
        return sort_edus[:1]

    def get_resume_info_mapper(self, resume_id_list):
        resume_id_list = [get_oid(resume_id) for resume_id in resume_id_list if get_oid(resume_id)]
        resume_info_query = ResumeData.objects.filter(
            id__in=resume_id_list,
        )

        resume_dict_list = []
        for i in resume_info_query:
            work_years = i.get_work_years()
            resume_dict = mongo_to_dict(i, [])
            resume_dict['work_years'] = work_years
            resume_dict_list.append(resume_dict)

        resume_info_mapper = {
            str(resume['id']): {
                'id': resume.get('id', ''),
                'works': resume.get('works', [{}])[:1],
                'gender': resume.get('gender', ''),
                'age': resume.get('age', ''),
                'job_target': resume.get('job_target', {}),
                'address': resume.get('address', ''),
                'work_years': resume.get('work_years', 0),
                'educations': self.get_latest_edu(resume),
                'self_evaluation': resume.get('self_evaluation', ''),
                'is_secret': resume.get('is_secret', False),
                'last_contact': resume.get('last_contact', ''),
                'hr_evaluate': resume.get('hr_evaluate', ''),
            }
            for resume in resume_dict_list
        }
        return resume_info_mapper


class CommentInfoMixin(object):

    def get_comment_info_mapper(self, user, resume_id_list):
        comment_query = list(Comment.objects.filter(
            user=user,
            resume_id__in=resume_id_list,
        ).values(
            'resume_id',
            'content',
            'comment_time',
        ).order_by('resume_id'))

        comment_info_mapper = {
            key: sorted(list(group), key=lambda x: x['comment_time'], reverse=True)[:1]
            for key, group in itertools.groupby(comment_query, lambda x: x['resume_id'])
        }
        return comment_info_mapper


class ContactInfoMixin(object):

    def get_contact_info_mapper(self, resume_id_list):
        contact_info_query = ContactInfoData.objects.filter(
            resume_id__in=resume_id_list,
        ).values(
            'resume_id',
            'name',
            'phone',
            'email',
            'qq',
            'status',
        )
        contact_info_mapper = {
            contact_info['resume_id']: contact_info
            for contact_info in contact_info_query
        }
        return contact_info_mapper


class QueryAPIMixin(object):

    keywords_param = 'keywords'
    fields_param = 'search_fields'
    resume_id_key = 'resume_id__in'

    def get_resume_id_str(self):
        return ''

    def get_resume_size(self, resume_id_str):
        size = len(resume_id_str.split(',')) or 1
        return size

    def query_api(self):
        keywords = self.request.GET.get(self.keywords_param, '')
        fields = self.request.GET.get(self.fields_param, '')

        if not keywords:
            return {}

        if fields not in ('position_title', 'company_name', 'name', 'school', 'all'):
            return {}

        resume_id_str = self.get_resume_id_str()
        query_size = self.get_resume_size(resume_id_str)
        search_params = {
            'size': query_size,
            'start': 0,
            'keywords': keywords,
            'search_fields': fields,
            'ids_list': resume_id_str
        }
        if fields == 'all':
            search_params.pop('search_fields', None)

        search_result = ParseUtils.search_resume(search_params)
        resume_data = search_result.get('data', {}).get('results', [])
        search_id_list = [i['id'] for i in resume_data if i.get('id')]
        return {
            self.resume_id_key: search_id_list,
        }
