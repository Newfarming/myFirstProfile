# coding: utf-8

from django.http import Http404
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User

from transaction.models import (
    ResumeBuyRecord
)
from resumes.models import (
    ContactInfoData
)
from transaction.models import (
    UserResumeFeedback
)
from feed.models import (
    FeedResult,
    Feed2,
    Feed,
)
from pin_utils.mixin_utils import (
    StaffRequiredMixin
)
from app.crm.runtime.candidate.details import (
    CandidateDetailsManage,
    JobStatusManage,
)
from app.crm.runtime.candidate.tags import (
    CandidateTagsManage,
    SystemTagsManage
)
from pin_utils.django_utils import (
    get_oid,
    JsonResponse
)
from app.crm.common import (
    CandidateMixin
)


class UpdateJobStatus(StaffRequiredMixin, View):

    def post(self, request):

        resume_id = request.POST.get('resume_id', '')
        job_status = request.POST.get('job_status', '')
        admin = request.user.username

        jobManage = JobStatusManage()
        jobManage.update_status(
            resume_id=resume_id,
            job_status=job_status,
            admin=admin,
        )
        result = {
            'status': 'ok'
        }
        return JsonResponse(result)


class AddTag(StaffRequiredMixin, View):

    def post(self, request):
        resume_id = request.POST['resume_id']
        tag_names = request.POST.getlist('tag_names[]')
        tag_ids = request.POST.getlist('tag_ids[]')

        ctm = CandidateTagsManage()
        ctm.add_tag(
            tag_names=tag_names,
            tag_ids=tag_ids,
            resume_id=resume_id
        )
        result = {
            'status': 'ok'
        }
        return JsonResponse(result)


class DelTag(StaffRequiredMixin, View):

    def post(self, request):

        resume_id = request.POST['resume_id']
        tag_names = request.POST.getlist('tag_names[]')
        tag_ids = request.POST.getlist('tag_ids[]')

        ctm = CandidateTagsManage()
        ctm.del_tag(
            tag_names=tag_names,
            tag_ids=tag_ids,
            resume_id=resume_id
        )
        result = {
            'status': 'ok'
        }
        return JsonResponse(result)


class AddSysTag(StaffRequiredMixin, View):

    def post(self, request):

        name = request.POST['name']

        ret = SystemTagsManage.add_tag(
            name=name
        )
        result = {
            'status': 'ok',
            'sys_tag_id': ret
        }
        return JsonResponse(result)


class DelSysTag(StaffRequiredMixin, View):

    def post(self, request):

        tag_id = request.POST['tag_id']
        SystemTagsManage.del_tag(
            tag_id=tag_id,
        )
        result = {
            'status': 'ok'
        }
        return JsonResponse(result)


class ShowCandidate(StaffRequiredMixin, View, CandidateMixin):

    template_name = 'candidate/details.html'

    def get_candidate_job_target(self, resume_data):

        if not resume_data:
            return {}
        return resume_data.get_job_target_dict()

    def get_feed_hitstory(self, resume_id):

        feed_results = FeedResult.objects.filter(
            resume=get_oid(str(resume_id)),
            published=True,
            is_recommended=True,
        )

        feed_ids = [str(feed.feed.id) for feed in feed_results]

        buy_records = ResumeBuyRecord.objects.filter(
            feed_id__in=feed_ids
        )

        buy_record_ids = [str(buy_record.feed_id)
                          for buy_record in buy_records]

        feed_results_list = []

        for ret in feed_results:
            feed_doc = {}
            if not isinstance(ret.feed, Feed2):
                continue
            company_name_query = User.objects.filter(
                username=ret.feed.username
            ).first()
            company_name = " " if not company_name_query else company_name_query.first_name

            feed_doc['company_name'] = company_name
            feed_doc['admin'] = ret.admin
            feed_doc['job'] = ret.feed.keywords
            feed_doc['pub_time'] = ret.pub_time
            feed_doc['is_clicked'] = False
            feed_doc['is_down'] = False
            feed_doc['is_interview'] = False
            feed_doc['is_enter'] = False
            feed_id = str(ret.feed.id)

            if ret.click_count >= 1:
                feed_doc['is_clicked'] = True

            if feed_id in buy_record_ids:
                feed_doc['is_down'] = True
                feed_doc['is_clicked'] = True

            buy_record = ResumeBuyRecord.objects.filter(
                resume_id=str(ret.resume.id),
                user__username=ret.feed.username
            ).first()
            if hasattr(buy_record, 'resume_mark'):

                if buy_record.resume_mark.has_interview:
                    feed_doc['is_interview'] = True
                if buy_record.resume_mark.current_mark.code_name == 'entry':
                    feed_doc['is_enter'] = True

            feed_results_list.append(feed_doc)

        return feed_results_list

    def get_resume_info(self, resume_query, contract_name):

        # 封装候选人基本信息
        resume_query.name = contract_name
        resume_query.work_years = resume_query.get_work_years()
        resume_query.education = resume_query.get_educations_text()
        resume_query.highest_degree = resume_query.highest_degree()

        if resume_query.job_target:
            resume_query.job_status = resume_query.job_target.job_hunting_brief(
                resume_query.source)
            resume_query.job_salary = resume_query.job_target.salary
            resume_query.job_location = ','.join(
                resume_query.job_target.get_expectation_area_list())
            resume_query.job_career = resume_query.job_target.job_career
        else:
            resume_query.job_status = u'未知'
            resume_query.job_salary = u'未知'
            resume_query.job_location = u'未知'
            resume_query.job_career = u'未知'

        resume_query.job_target = self.get_candidate_job_target(
            resume_query,
        )
        # 如果没有求职目标,显示最后一次工作职位
        if not resume_query.job_career:
            resume_query.job_career = resume_query.get_latest_work_dict()[
                'position_title']

        return resume_query

    def get_reco_feed_results(self, resume_id):
        '''
        显示未发布的定制
        '''
        resume_oid = get_oid(resume_id)
        feed_results = FeedResult.objects.filter(
            is_recommended=True,
            published=False,
            resume=resume_oid,
            resume_source__ne='talent_partner',
        ).only(
            'id',
            'feed',
            'calc_time',
            'admin',
            'watch',
            'download',
        ).order_by('-calc_time').limit(30).no_cache().select_related()
        feed_results = [i for i in feed_results if hasattr(i.feed, 'username')]

        username_list = [i.feed.username for i in feed_results]
        users = list(User.objects.filter(
            username__in=username_list,
        ).values(
            'username',
            'first_name',
        ))
        company_mapper = {
            i['username']: i['first_name']
            for i in users
        }
        for fr in feed_results:
            fr.company_name = company_mapper.get(fr.feed.username, fr.feed.username)

        return feed_results

    def get_download_records(self, resume_id):
        buy_records = ResumeBuyRecord.objects.select_related(
            'user',
            'resume_mark',
            'resume_mark__current_mark',
        ).prefetch_related(
            'resume_mark__mark_logs',
            'resume_mark__mark_logs__resume_mark',
        ).filter(
            resume_id=str(resume_id),
            status='LookUp',
        ).order_by('-id')

        feed_obj_id_list = [i.feed_id for i in buy_records if i.feed_id]
        feed_query = Feed.objects.select_related(
            'user',
        ).filter(
            feed_obj_id__in=feed_obj_id_list,
        )
        job_mapper = {
            i.feed_obj_id: {
                'title': i.title if i.title else i.keywords,
                'id': i.id,
            }
            for i in feed_query
        }
        for r in buy_records:
            r.job = job_mapper.get(r.feed_id, {})

        return buy_records

    def get(self, request, resume_id):
        resume_query = CandidateDetailsManage.get_resume_info(str(resume_id))

        if not resume_query:
            raise Http404

        contract_query = ContactInfoData.objects.prefetch_related(
            'candidate__candidate_remarks',
            'candidate__candidate_remarks__admin',
            'candidate__send_records',
            'candidate__send_records__operator',
            'candidate__send_records__job',
            'candidate__send_records__job__user',
        ).filter(resume_id=str(resume_id))

        if not contract_query:
            raise Http404

        # 获取联系人信息
        contract_info = contract_query[0]

        # 获取简历信息
        resume_info = self.get_resume_info(
            resume_query=resume_query,
            contract_name=contract_info.name
        )

        candidate_info = self.get_candidate(contract_info.id)

        # 获取候选人标签信息
        ctm = CandidateTagsManage()
        candidate_tags = ctm.get_tags(str(resume_id))

        # 获取系统标签列表
        sys_tags = SystemTagsManage.get_tags()

        # 获取候选人举报信息记录
        feedbacks = UserResumeFeedback.objects.filter(
            resume_id=str(resume_id)
        )

        # 获取候选人推荐历史
        feed_results_list = self.get_feed_hitstory(resume_id=resume_id)

        # 未发布的推荐数据
        reco_feed_results = self.get_reco_feed_results(resume_id)

        # 简历下载记录
        download_records = self.get_download_records(resume_id)

        return render(
            request,
            self.template_name,
            {
                'contract': contract_info,
                'resume_info': resume_info,
                'feedbacks': feedbacks,
                'feed_results_list': feed_results_list,
                'sys_tags': sys_tags,
                'candidate_tags': candidate_tags,
                'candidate_tag_name_list': [tag.name for tag in candidate_tags],
                'candidate_info': candidate_info,
                'reco_feed_results': reco_feed_results,
                'download_records': download_records,
            }
        )
