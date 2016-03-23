# coding: utf-8

import json
import datetime
from Pinbot.settings import ON_LINE_TIME

from django.db.models import Q, Count
from django.views.generic import ListView, View
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .forms import (
    CreateCRMClientInfoForm,
    UpdateCRMClientInfoForm,
)

from ..common import (
    CandidateListMixin,
    AdminListMixin,
)
from ..models import (
    CRMClientInfo,
    CRMDownloadResume,
)

from users.models import (
    UserProfile,
)
from transaction.models import (
    ResumeBuyRecord,
    UserMarkLog,
)
from resumes.models import (
    ContactInfoData,
)
from feed.models import (
    Feed,
)
from Brick.App.system.models import (
    ResumeMarkSetting,
)
from app.vip.models import (
    UserManualService,
    ItemRecord,
)

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    get_int,
    JsonResponse,
    get_object_or_none,
)
from pin_utils.csvexport_utils import (
    CSVExportUtils,
)
from transaction.models import UserChargePackage


class CompanyList(StaffRequiredMixin, ListView, AdminListMixin):
    '''
    公司列表
    '''
    template_name = 'company/list.html'
    context_object_name = 'company_list'
    paginate_by = 20

    def query_keywords(self):
        keywords = self.request.GET.get('keywords', '')
        if not keywords:
            return []

        return [
            Q(company_name__contains=keywords) | Q(user__username__contains=keywords)
        ]

    def query_admin(self):
        admin_id = get_int(self.request.GET.get('admin_id'))
        if admin_id == -1:
            return {}
        if not admin_id:
            return {'user__crm_client_info__admin_id': self.request.user.id}
        return {'user__crm_client_info__admin_id': admin_id}

    def query_cond(self):
        query_cond = {}
        query_cond.update(self.query_admin())
        return query_cond

    def get_queryset(self):
        keywords = self.query_keywords()
        query_cond = self.query_cond()

        self.queryset = UserProfile.objects.select_related(
            'user',
            'user__crm_client_info__admin',
        ).prefetch_related(
            'user__company_set',
        ).filter(
            *keywords
        ).filter(
            **query_cond
        ).order_by('-id')

        return self.queryset

    def add_company_job(self, company_list):
        user_id_list = [i.user_id for i in company_list]
        feed_query = Feed.objects.filter(
            user_id__in=user_id_list,
            deleted=False,
        ).values(
            'user__id'
        ).annotate(
            total=Count('user__id')
        )
        feed_mapper = {
            i['user__id']: i['total'] or 0
            for i in feed_query
        }
        for i in company_list:
            i.job_count = feed_mapper.get(i.user_id, 0)

        return company_list

    def add_download_count(self, company_list):

        user_id_list = [i.user_id for i in company_list]
        buy_record_query = ResumeBuyRecord.objects.filter(
            user_id__in=user_id_list,
            status='LookUp',
            crm_resume_info=None,
            resume_mark=None,
            op_time__gt=ON_LINE_TIME,
        ).values(
            'user__id'
        ).annotate(
            total=Count('user__id')
        )
        buy_record_mapper = {
            i['user__id']: i['total'] or 0
            for i in buy_record_query
        }
        for i in company_list:
            i.download_count = buy_record_mapper.get(i.user_id, 0)
        return company_list

    def add_is_active(self, company_list):

        now = datetime.datetime.now()
        user_id_list = [i.user_id for i in company_list]
        active_feed_count_list = Feed.objects.filter(
            user__id__in=user_id_list,
            feed_expire_time__gt=now,
            feed_type=1,
            expire_time__gt=now,
            deleted=False,
        ).values('user').annotate(
            active_count=Count('user')
        )

        active_feed_mapper = {
            x['user']: x['active_count']
            for x in active_feed_count_list
        }
        for i in company_list:
            i.active_count = active_feed_mapper.get(i.user_id, 0)
        return company_list

    def get_context_data(self, **kwargs):
        context = super(CompanyList, self).get_context_data(**kwargs)
        context['paginate_query'] = self.queryset

        company_list = context.get('company_list', [])
        self.add_company_job(company_list)
        self.add_download_count(company_list)
        self.add_is_active(company_list)

        context['q_args_json'] = json.dumps(dict(self.request.GET.lists()))
        context['admin_list'] = self.get_admin_list()
        return context


class AssignAdmin(StaffRequiredMixin, View):

    def post(self, request):
        obj_id = get_int(request.POST.get('obj_id', ''))
        client = get_object_or_none(
            CRMClientInfo,
            id=obj_id
        )
        form = CreateCRMClientInfoForm(request.POST) if not client else UpdateCRMClientInfoForm(request.POST, instance=client)

        if form.is_valid():
            crm_info = form.save()

            return JsonResponse({
                'status': 'ok',
                'msg': '分配成功',
                'admin_name': crm_info.admin.username
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class CompanyDetail(StaffRequiredMixin, View):

    template_name = 'company/detail.html'

    def get(self, request, uid):
        user_query = User.objects.select_related(
            'userprofile',
        ).prefetch_related(
            'company_set',
            'company_set__category',
        ).filter(
            id=uid,
        )
        if not user_query:
            raise Http404

        client = user_query[0]
        company_query = client.company_set.all()
        company = company_query[0] if company_query else None
        mark_choices = ResumeMarkSetting.objects.filter(
            display=True,
        )

        return render(
            request,
            self.template_name,
            {
                'client': client,
                'company': company,
                'mark_choices': mark_choices,
            }
        )


class CompanyDownload(StaffRequiredMixin, ListView, CandidateListMixin):
    template_name = 'company/download_list.html'
    context_object_name = 'download_list'
    need_contact = False
    paginate_by = 10

    def query_has_contact(self):
        if not self.need_contact:
            return {}

        return {
            'crm_resume_info': None,
            'resume_mark': None,
        }

    def query_job(self):
        job = self.request.GET.get('job', '')
        if not job:
            return {}
        return {'feed_id': job}

    def query_mark(self):
        mark = get_int(self.request.GET.get('mark', ''))
        if not mark:
            return {}
        return {'resume_mark__current_mark__id': mark}

    def query_mark_type(self):
        mark_type = self.request.GET.getlist('mark_type', [])
        if not mark_type:
            return {}
        return {'resume_mark__current_mark__code_name__in': mark_type}

    def query_cond(self):
        query_cond = {}
        query_cond.update(self.query_has_contact())
        query_cond.update(self.query_job())
        query_cond.update(self.query_mark())
        query_cond.update(self.query_mark_type())
        return query_cond

    def get_queryset(self):
        uid = self.kwargs.get('uid', 0)
        query_cond = self.query_cond()

        self.queryset = ResumeBuyRecord.objects.select_related(
            'user',
            'resume_mark',
            'resume_mark__current_mark',
            'resume_mark__mark_time',
        ).filter(
            user_id=uid,
            status='LookUp',
            op_time__gt=ON_LINE_TIME,
            **query_cond
        ).order_by(
            '-resume_mark__mark_time',
            '-id',
        )
        return self.queryset

    def add_contact_info(self, download_list):
        resume_id_list = [i.resume_id for i in download_list]

        contactinfo_query = ContactInfoData.objects.select_related(
            'candidate',
            'candidate__candidate_remarks',
        ).filter(
            resume_id__in=resume_id_list,
        )
        contactinfo_mapper = {
            i.resume_id: i
            for i in contactinfo_query
        }

        for record in download_list:
            record.contact = contactinfo_mapper.get(record.resume_id)
        return download_list

    def add_job_info(self, download_list):
        feed_id_list = [i.feed_id for i in download_list if i.feed_id]
        feed_query = Feed.objects.filter(
            feed_obj_id__in=feed_id_list,
        )
        feed_mapper = {
            i.feed_obj_id: i
            for i in feed_query
        }
        for i in download_list:
            i.feed = feed_mapper.get(i.feed_id)
        return download_list

    def get_context_data(self, **kwargs):
        context = super(CompanyDownload, self).get_context_data(**kwargs)
        context['paginate_query'] = self.queryset

        download_list = context.get('download_list', [])
        download_list = self.add_contact_info(download_list)
        download_list = self.add_candidate_extra_info(download_list)
        download_list = self.add_job_info(download_list)
        context['download_list'] = download_list
        return context


class ContactDownload(StaffRequiredMixin, View):

    def get(self, request, buy_resume_id):
        buy_resume = get_object_or_404(
            ResumeBuyRecord,
            id=buy_resume_id,
        )
        admin = request.user
        CRMDownloadResume.objects.get_or_create(
            buy_resume=buy_resume,
            admin=admin,
        )
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class CompanyJob(StaffRequiredMixin, ListView):
    template_name = 'company/job_list.html'
    context_object_name = 'job_list'
    all_job = True

    def query_deleted(self):
        if self.all_job:
            return {}
        return {'deleted': False}

    def query_cond(self):
        query_cond = {}
        query_cond.update(self.query_deleted())
        return query_cond

    def get_queryset(self):
        uid = self.kwargs.get('uid', 0)
        query_cond = self.query_cond()

        self.queryset = Feed.objects.prefetch_related(
            'crm_remarks',
            'crm_remarks__admin',
        ).filter(
            user_id=uid,
            **query_cond
        ).order_by('-id')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(CompanyJob, self).get_context_data(**kwargs)
        return context


class CancelAssign(StaffRequiredMixin, View):

    def post(self, request):
        client_id = get_int(request.POST.get('client_id'))
        CRMClientInfo.objects.filter(client__id=client_id).update(admin=None)
        return JsonResponse({
            'status': 'ok',
            'msg': '取消成功'
        })


class CompanyDownloadCSVExport(CompanyDownload):
    export_type = 'export_current_company'

    def add_comment_info(self, all_list):
        resume_id_list = [i.resume_id for i in all_list]

        commentinfo_query = ContactInfoData.objects.prefetch_related(
            'candidate__candidate_remarks',
        ).filter(
            resume_id__in=resume_id_list,
        )
        commentinfo_mapper = {
            i.resume_id: i
            for i in commentinfo_query
        }

        for record in all_list:
            record.comment = commentinfo_mapper.get(record.resume_id)
        return all_list

    def get_context_data(self, **kwargs):
        all_list = self.queryset
        all_list = self.add_contact_info(all_list)
        all_list = self.add_candidate_extra_info(all_list)
        all_list = self.add_job_info(all_list)
        all_list = self.add_comment_info(all_list)
        return all_list

    def get_attr_value(self, record, query):
        value = record
        attrs = query.split('__')
        for attr in attrs:
            if isinstance(value, dict):
                value = value.get(attr)
                continue
            if attr.startswith('query_all'):
                _, _, field = attr.split('_')
                return ','.join(value.values_list(field, flat=True))
            if not hasattr(value, attr):
                return None
            value = getattr(value, attr)
        return value

    def get_csv_data(self, resume_buy_record):
        fields = (
            'user__userprofile__company_name',
            'feed__title',
            'contact__name',
            'contact__phone',
            'contact__email',
            'job_target__hunting_status',
            'finished_time',
            'resume_mark__mark_time',
            'resume_mark__current_mark__name',
            'resume_mark__mark_logs__query_all_desc',
        )
        data = [
            [self.get_attr_value(record, attr_query) for attr_query in fields]
            for record in resume_buy_record
        ]

        return data

    def get(self, request, *args, **kwargs):
        label = (
            '公司', '职位名', '候选人', '电话', '邮箱',
            '求职状态', '简历购买完成时间', '标记时间', '阶段', '评论',
        )
        self.queryset = self.get_queryset()
        resume_buy_record_data = self.get_context_data()
        data = self.get_csv_data(resume_buy_record_data)
        response = CSVExportUtils.generate_csv_response(label, data)
        return response

    def query_cond(self):
        uid = self.kwargs.get('uid', 0)
        if self.export_type == 'export_current_company':
            return {'user_id': uid}
        if self.export_type == 'export_all_company':
            if uid == -1:
                return {}
            if not uid:
                return {'user__crm_client_info__admin_id': self.request.user.id}
            return {'user__crm_client_info__admin_id': uid}

    def query_mark_type(self):
        mark_type = self.request.GET.getlist('mark_type', '')
        if 'mark_type' in self.request.GET.keys() and not mark_type:
            return {'resume_mark__current_mark__code_name__in': []}
        if 'mark_type' not in self.request.GET.keys():
            return {}
        return {'resume_mark__current_mark__code_name__in': mark_type}

    def query_need_contact(self):
        need_contact = self.request.GET.get('need_contact', '')
        if need_contact:
            return {
                'crm_resume_info': None,
                'resume_mark': None,
            }
        return {}

    def query_time_slot(self):
        time = self.request.GET.get('time_slot', '')
        need_contact = self.request.GET.get('need_contact', '')
        if not time:
            return [{}, {}]
        time_start, _, time_end = time.split(' ')
        start_month, start_day, start_year = time_start.split('/')
        end_month, end_day, end_year = time_end.split('/')
        start_time = datetime.datetime(int(start_year), int(start_month), int(start_day))
        end_time = datetime.datetime(int(end_year), int(end_month), int(end_day))
        if not need_contact:
            return [{
                'op_time__gt': start_time,
                'op_time__lt': end_time,
            }, {}]
        return [{
            'resume_mark__mark_time__gt': start_time,
            'resume_mark__mark_time__lt': end_time,
        }, {
            'op_time__gt': start_time,
            'op_time__lt': end_time,
        }
        ]

    def get_queryset(self):

        query_cond = {}
        query_cond.update(self.query_cond())
        query_mark_type = self.query_mark_type()
        query_need_contact = self.query_need_contact()
        query_sign_time_slot, query_download_time_slot = self.query_time_slot()

        self.queryset = ResumeBuyRecord.objects.select_related(
            'user',
            'resume_mark',
            'resume_mark__current_mark',
        ).filter(
            status='LookUp',
            **query_cond
        ).filter(
            Q(**query_sign_time_slot) | Q(**query_download_time_slot)
        ).filter(
            Q(**query_mark_type) | Q(**query_need_contact)
        ).order_by('-id')
        return self.queryset


class CompanyArchives(StaffRequiredMixin, ListView, View, AdminListMixin):

    template_name = 'company/archives.html'
    context_object_name = 'company_archives_list'
    paginate_by = 20

    def query_keywords(self):
        keywords = self.request.GET.get('keywords', '')
        if not keywords:
            return []
        return [
            Q(user__userprofile__company_name__contains=keywords) | Q(user__username__contains=keywords)
        ]

    def query_admin(self):
        admin_id = get_int(self.request.GET.get('admin_id', -1))
        if admin_id == -1:
            return {}
        if not admin_id:
            return {'user__crm_client_info__admin_id': self.request.user.id}
        return {'user__crm_client_info__admin_id': admin_id}

    def query_appoint_user(self):
        user_id = get_int(self.request.GET.get('user_id', ''))
        if not user_id:
            return {}
        return {'user_id': user_id}

    def query_cond(self):
        query_cond = {}
        query_cond.update(self.query_admin())
        query_cond.update(self.query_appoint_user())
        return query_cond

    def get_queryset(self):
        key_words = self.query_keywords()
        query_cond = self.query_cond()

        self.queryset = UserManualService.objects.select_related(
            'user',
            'item',
            'user__userprofile',
            'user__crm_client_info__admin',
        ).filter(
            *key_words
        ).filter(
            **query_cond
        ).order_by('-id')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(CompanyArchives, self).get_context_data(**kwargs)
        context['paginate_query'] = self.queryset

        company_archives_list = context.get('company_archives_list', [])
        self.add_record_count(company_archives_list)
        self.add_feed_useage(company_archives_list)
        self.add_useage_data(company_archives_list)
        self.add_order_id(company_archives_list)

        context['admin_list'] = self.get_admin_list()

        return context

    def convert_dict_list_to_dict(self, dict_list, key):
        return {
            x.get('user'): x.get(key)
            for x in dict_list
        }

    def get_dict_mapper(self, dict_list):
        the_mapper = {}
        for x in dict_list:
            user_id = x['resume_mark__buy_record__user__id']
            code_name = x['mark__code_name']
            code_count = x['code_count']
            the_mapper[user_id] = the_mapper.get(user_id, {})
            the_mapper[user_id].update({code_name: code_count})
        return the_mapper

    def get_order_mapper(self, order_query):
        order_mapper = {
            record.item_object_id: record.order.order_id
            for record in order_query if record.item_object_id is not None
        }
        return order_mapper

    def add_record_count(self, company_archives_list):

        user_id_list = [x.user_id for x in company_archives_list]

        resume_buy_record_count_data = ResumeBuyRecord.objects.filter(
            user_id__in=user_id_list
        ).values('user').annotate(
            record_count=Count('user')
        )
        resume_buy_record_mapper = self.convert_dict_list_to_dict(
            resume_buy_record_count_data,
            'record_count'
        )
        for x in company_archives_list:
            x.record_count=resume_buy_record_mapper.get(x.user_id, 0)
        return company_archives_list

    def add_feed_useage(self, company_archives_list):

        user_id_list = [x.user_id for x in company_archives_list]

        user_feed_data = UserChargePackage.objects.filter(
            user_id__in=user_id_list,
            feed_package__name=u'会员定制'
        ).values(
            'extra_feed_num',
            'rest_feed',
            'user'
        )
        user_feed_data_mapper = {
            x.get('user'): '{used}/{total}'.format(
                used=x.get('extra_feed_num') - x.get('rest_feed'),
                total=x.get('extra_feed_num')
            )
            for x in user_feed_data
        }
        for x in company_archives_list:
            x.feed_usage=user_feed_data_mapper.get(x.user_id, '-')
        return company_archives_list

    def add_useage_data(self, company_archives_list):

        user_id_list = [x.user_id for x in company_archives_list]

        mark_data_dict_list_query = UserMarkLog.objects.select_related(
            'mark'
        ).filter(
            resume_mark__buy_record__user_id__in=user_id_list,
        ).values(
            'resume_mark__buy_record__user__id',
            'mark__code_name',
        ).annotate(code_count=Count('mark__code_name'))
        mark_data_mapper = self.get_dict_mapper(mark_data_dict_list_query)
        for x in company_archives_list:
            invite_interview = mark_data_mapper.get(x.user_id, {}).get('invite_interview', 0)
            next_interview = mark_data_mapper.get(x.user_id, {}).get('next_interview', 0)
            join_interview = mark_data_mapper.get(x.user_id, {}).get('join_interview', 0)
            x.interview = invite_interview + next_interview + join_interview
            x.send_offer = mark_data_mapper.get(x.user_id, {}).get('send_offer', 0)
            x.entry = mark_data_mapper.get(x.user_id, {}).get('entry', 0)
        return company_archives_list

    def add_order_id(self, company_archives_list):

        manual_service_id_list = [x.id for x in company_archives_list]
        order_query = ItemRecord.objects.select_related(
            'order',
        ).filter(
            item_content_type__name=u'人工服务',
            item_object_id__in=manual_service_id_list,
        )
        order_mapper = self.get_order_mapper(order_query)

        for x in company_archives_list:
            x.order_id=order_mapper.get(x.id)
        return company_archives_list
