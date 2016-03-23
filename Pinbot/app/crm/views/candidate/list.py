# coding: utf-8

import json

from django.views.generic import ListView, View
from django.contrib.auth.models import User
from django.db.models import Count

from feed.models import (
    FeedResult,
)
from resumes.models import (
    ContactInfoData,
)
from transaction.models import (
    UserResumeFeedback,
    ResumeBuyRecord,
)
from app.crm.models import (
    CandidateTag,
)
from app.crm.common import (
    CandidateListMixin,
    AdminListMixin,
)

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    get_oid,
    get_int,
    JsonResponse,
)
from pin_utils.parse_utils import (
    ParseUtils,
)


class CandidateList(
        StaffRequiredMixin,
        ListView,
        CandidateListMixin,
        AdminListMixin):
    '''
    候选人列表
    '''
    template_name = 'candidate/list.html'
    context_object_name = 'candidate_list'
    paginate_by = 20

    def get_work_years(self):
        work_years_min = get_int(self.request.GET.get('work_years_min', ''))
        work_years_max = get_int(self.request.GET.get('work_years_max', ''))

        work_years = ''
        if work_years_min and not work_years_max:
            work_years_max = 20
            work_years = '%s,%s' % (work_years_min, work_years_max)
        if not work_years_min and work_years_max:
            work_years_min = 0
            work_years = '%s,%s' % (work_years_min, work_years_max)
        if work_years_min and work_years_max:
            work_years = '%s,%s' % (work_years_min, work_years_max)
        return work_years

    def get_api_query(self):
        api_param = {}
        keywords = self.request.GET.get('resume_keywords', '')
        if keywords:
            api_param['keywords'] = keywords

        city = self.request.GET.get('city', '')
        if city:
            api_param['current_area'] = city

        expect_city = self.request.GET.get('expect_city', '')
        if expect_city:
            api_param['expectation_area'] = expect_city

        hunting_state = self.request.GET.get('job_hunting_state', '')
        if hunting_state in ('求职', '观望', '稳定', '应届'):
            api_param['job_hunting_state'] = hunting_state

        work_years = self.get_work_years()
        if work_years:
            api_param['work_years'] = work_years

        search_fields = self.request.GET.getlist('search_fields', [])
        if search_fields:
            api_param['search_fields'] = ','.join(search_fields)

        if not api_param:
            return {}

        api_param['size'] = 200
        api_param['has_contact_info'] = 'yes'
        result = ParseUtils.search_resume(api_param)
        resume_data = result.get('data', {}).get('results', [])

        if not resume_data:
            return {}

        query = {
            'resume_id__in': [i['id'] for i in resume_data if i.get('id')]
        }
        return query

    def get_db_query(self):
        query = {}
        source = self.request.GET.get('source', '')
        if source in ('51job', 'zhilian', 'talent_partner', 'brick'):
            query['source'] = source

        has_contact = self.request.GET.get('has_contact', '')
        if has_contact in ('0', '1'):
            query['candidate__has_contact'] = True if get_int(has_contact) else False

        admin_id = get_int(self.request.GET.get('admin_id', ''))
        if admin_id:
            query['candidate__admin__id'] = admin_id

        tag_list = self.request.GET.getlist('tag_list', [])
        if tag_list:
            query['candidate__tags__id__in'] = tag_list

        return query

    def get_request_query(self):
        query = {}
        query.update(self.get_api_query())
        query.update(self.get_db_query())

        return query

    def get_queryset(self):
        query = self.get_request_query()

        self.queryset = ContactInfoData.objects.select_related(
            'candidate',
            'candidate__admin',
        ).filter(
            **query
        ).exclude(
            phone=None
        ).order_by('-id')
        return self.queryset

    def add_accu_status(self, candidate_list):
        resume_id_list = [i.resume_id for i in candidate_list]
        accu_resumes = list(UserResumeFeedback.objects.filter(
            resume_id__in=resume_id_list,
            check_status='pass',
            feedback_info__id__in=[220, 221, 222],
        ).values_list('resume_id', flat=True))

        for candidate in candidate_list:
            if candidate.resume_id in accu_resumes:
                candidate.has_accu = True
            else:
                candidate.has_accu = False

        return candidate_list

    def get_tag_list(self):
        tag_list = list(CandidateTag.objects.filter(
            display=True,
        ).values(
            'id',
            'name',
        ))
        return tag_list

    def add_download_count(self, candidate_list):
        resume_id_list = [i.resume_id for i in candidate_list]
        resume_buy_records = ResumeBuyRecord.objects.filter(
            resume_id__in=resume_id_list
        ).values('resume_id').annotate(download_count=Count('resume_id'))

        buy_record_mapper = {
            i['resume_id']: i['download_count']
            for i in resume_buy_records
        }
        for i in candidate_list:
            i.download_count = buy_record_mapper.get(i.resume_id, 0)
        return candidate_list

    def add_reco_count(self, candidate_list):
        resume_oid_list = [get_oid(i.resume_id) for i in candidate_list if get_oid(i.resume_id)]
        feed_results = FeedResult.objects.filter(
            is_recommended=True,
            published=False,
            resume__in=resume_oid_list,
            resume_source__ne='talent_partner',
        ).only(
            'resume',
        ).order_by('-job_related').no_cache().no_dereference()
        reco_list = [str(i.resume.id) for i in feed_results]
        reco_mapper = {
            key: reco_list.count(key)
            for key in reco_list
        }
        for i in candidate_list:
            i.reco_count = reco_mapper.get(i.resume_id, 0)

    def get_context_data(self, **kwargs):
        context = super(CandidateList, self).get_context_data(**kwargs)
        candidate_list = context['candidate_list']

        self.add_candidate_extra_info(candidate_list)
        self.add_accu_status(candidate_list)
        self.add_download_count(candidate_list)
        self.add_reco_count(candidate_list)

        context['paginate_query'] = self.queryset
        context['q_args_json'] = json.dumps(dict(self.request.GET.lists()))
        context['admin_list'] = self.get_admin_list()
        context['tag_list'] = self.get_tag_list()

        return context


class AdminList(StaffRequiredMixin, View):

    def get(self, request):
        admin_list = list(User.objects.filter(
            is_staff=True,
        ).values(
            'id',
            'username'
        ))

        admin_list = [{'username': '不限', 'id': -1}] + admin_list

        return JsonResponse({
            'status': 'ok',
            'data': admin_list,
        })
