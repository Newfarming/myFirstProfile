# coding: utf-8

import datetime

from collections import OrderedDict
from operator import __or__ as OR

from django.http import Http404
from django.shortcuts import render
from django.views.generic import View, ListView
from django.db import transaction
from django.db.models import Q

from .forms import MarkResumeForm
from .models import (
    ResumeBuyRecord,
    DownloadResumeMark,
    AdminMarkLog,
)

from resumes.models import (
    ContactInfoData,
    ResumeData,
)

from Brick.App.system.models import (
    ResumeMarkRelation,
)

from Pinbot.settings import MARK_TIME

from pin_utils.django_utils import (
    JsonResponse,
    get_oid,
    get_object_or_none,
    get_today,
)
from pin_utils.mixin_utils import (
    CSRFExemptMixin,
    LoginRequiredMixin,
    StaffRequiredMixin,
)


class MarkChoiceMixin(object):

    def classify_choices(self, mark_choices_list, classify):
        return [i for i in mark_choices_list if i.get('classify') == classify]

    def get_mark_choices(self, buy_record):
        if not hasattr(buy_record, 'resume_mark'):
            mark_choices_query = ResumeMarkRelation.objects.select_related(
                'mark'
            ).filter(
                parent=None,
                mark__display=True,
            ).order_by(
                '-mark__sort'
            )
        else:
            resume_mark = buy_record.resume_mark
            current_mark = resume_mark.current_mark

            if not current_mark.change and current_mark.end_status:
                return {}

            mark_choices_query = ResumeMarkRelation.objects.select_related(
                'mark'
            ).filter(
                parent=current_mark,
                mark__display=True,
            ).order_by(
                '-mark__sort'
            )

        mark_choices_list = [
            {
                'code_name': i.mark.code_name,
                'desc': i.mark.desc,
                'good_result': i.mark.good_result,
                'classify': i.mark.classify,
                'name': i.mark.name,
            }
            for i in list(mark_choices_query)
        ]
        stages = [
            u'面试阶段',
            u'入职阶段',
            u'约面不成功',
            u'面试不通过',
            u'入职遇到问题',
        ]
        all_choices = [
            {
                'name': s,
                'choices': self.classify_choices(mark_choices_list, i)
            }
            for i, s in enumerate(stages)
        ]
        mark_choices = OrderedDict()
        mark_choices['good'] = {
            'name': u'进展顺利',
            'choices': [
                {
                    'name': all_choices[i]['name'],
                    'choices': all_choices[i]['choices'],
                }
                for i in xrange(2) if all_choices[i]['choices']
            ],
            'is_good': True,
        }
        mark_choices['bad'] = {
            'name': u'遇到问题',
            'choices': [
                {
                    'name': all_choices[i]['name'],
                    'choices': all_choices[i]['choices'],
                }
                for i in xrange(2, 5) if all_choices[i]['choices']
            ],
            'is_good': False,
        }
        return mark_choices

    def get_buy_record(self, record_id):
        user = self.request.user
        # 管理员可以修改任何用户的记录
        if user.is_staff:
            buy_record_query = ResumeBuyRecord.objects.select_related(
                'resume_mark',
                'resume_mark__current_mark',
            ).prefetch_related(
                'resume_mark__mark_logs',
            ).filter(
                id=record_id,
                status='LookUp',
            )
        else:
            buy_record_query = ResumeBuyRecord.objects.select_related(
                'resume_mark',
                'resume_mark__current_mark',
            ).prefetch_related(
                'resume_mark__mark_logs',
            ).filter(
                user=user,
                id=record_id,
                status='LookUp',
            )

        if not buy_record_query:
            raise Http404

        buy_record = buy_record_query[0]

        if hasattr(buy_record, 'resume_mark') and buy_record.resume_mark.accu_status in (1, 2):
            raise Http404
        return buy_record


class MarkResume(CSRFExemptMixin, LoginRequiredMixin, View, MarkChoiceMixin):

    template_name = 'mark_resume.html'

    def get_mark_logs(self, buy_record):
        return [] if not hasattr(buy_record, 'resume_mark') else buy_record.resume_mark.mark_logs.all()

    def get_referer_url(self):
        request = self.request
        referer_url = request.META.get('HTTP_REFERER')
        current_path = request.path
        if not referer_url or referer_url == current_path:
            referer_url = '/transaction/bought'
        return referer_url

    def get(self, request, record_id):
        buy_record = self.get_buy_record(record_id)

        resume_id = buy_record.resume_id
        resume_oid = get_oid(resume_id)

        mark_choices = self.get_mark_choices(buy_record)
        mark_logs = self.get_mark_logs(buy_record)
        contact_info = get_object_or_none(
            ContactInfoData,
            resume_id=resume_id,
        )
        resume_info = ResumeData.objects.filter(
            id=resume_oid,
        ).first()
        referer_url = self.get_referer_url()

        return render(
            request,
            self.template_name,
            {
                'contact_info': contact_info,
                'resume_info': resume_info,
                'mark_choices': mark_choices,
                'mark_logs': mark_logs,
                'referer_url': referer_url,
                'buy_record': buy_record,
            },
        )

    @transaction.atomic
    def post(self, request, record_id):
        form = MarkResumeForm(
            request.POST,
            request=request,
            record_id=record_id
        )

        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'ok',
                'msg': '标记成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class MarkNotify(LoginRequiredMixin, View):

    def get(self, request):
        today = get_today()
        time_limit = today + datetime.timedelta(days=-2)

        if time_limit < MARK_TIME:
            has_mark = False
        else:
            user = request.user
            need_mark_query = ResumeBuyRecord.objects.filter(
                user=user,
                status='LookUp',
                finished_time__gt=MARK_TIME,
                finished_time__lte=time_limit,
            ).exclude(
                resume_mark__current_mark__end_status=True,
                resume_mark__accu_status__in=(0, 1, 2),
            )
            has_mark = True if need_mark_query else False
        return JsonResponse({
            'status': 'ok',
            'has_mark': has_mark,
            'redirect_url': '/transaction/unmark_resume/',
            'msg': 'ok',
        })


class ResumeBuyRecordList(LoginRequiredMixin, ListView):

    context_object_name = 'record_list'
    template_name = 'to_be_marked.html'

    query = 'all'

    def get_query_cond(self):
        query_meta = {
            'unmark': {
                'exclude': {
                    'resume_mark__current_mark__end_status': True,
                },
                'filter': {
                    'status': 'LookUP',
                    'finished_time__gt': MARK_TIME,
                },
                'select_related': [
                    'resume_mark',
                    'resume_mark__current_mark'
                ],
                'q_list': [],
                'order_by': [
                    '-id'
                ],
            },
            'all': {
                'exclude': {
                },
                'filter': {
                },
                'select_related': [],
                'q_list': [],
                'order_by': [
                    '-id'
                ],
            },
        }
        return query_meta[self.query]

    def query_unmark_cond(self, query_cond):
        mark_status = self.request.GET.get('mark_status')
        if mark_status == '1':
            query_cond['q_list'] = [Q(resume_mark=None), Q(resume_mark__accu_status=3)]
        return query_cond

    def get_queryset(self):
        user = self.request.user

        query_cond = self.get_query_cond()
        query_cond = self.query_unmark_cond(query_cond)
        query_cond['filter']['user'] = user

        queryset = ResumeBuyRecord.objects.select_related(
            *query_cond['select_related']
        ).filter(
            reduce(OR, query_cond['q_list'], Q()),
            **query_cond['filter']
        ).exclude(
            **query_cond['exclude']
        ).order_by(
            *query_cond['order_by']
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ResumeBuyRecordList, self).get_context_data(
            *args, **kwargs)
        record_list = context.get('record_list', [])

        for r in list(record_list):
            resume_id = r.resume_id
            resume_oid = get_oid(resume_id)
            resume_info = ResumeData.objects.filter(
                id=resume_oid
            ).first()
            contact_info = get_object_or_none(
                ContactInfoData,
                resume_id=resume_id,
            )
            r.resume_info = resume_info
            r.contact_info = contact_info
        return context


class AdminVerifyRemark(StaffRequiredMixin, View):

    def post(self, request, mark_id):
        remark = request.POST.get('remark', '').strip()

        if not remark:
            return JsonResponse({
                'result': 'success',
                'new_data': {'remark': '请填写备注'},
                'new_html': {'remark': '请填写备注'},
            })

        mark = get_object_or_none(
            DownloadResumeMark,
            id=mark_id,
        )
        if not mark:
            return JsonResponse({
                'result': 'success',
                'new_data': {'remark': '数据有误'},
                'new_html': {'remark': '数据有误'},
            })
        user = request.user
        admin_log = AdminMarkLog(
            resume_mark=mark,
            user=user,
            desc=remark,
        )
        admin_log.save()
        return JsonResponse({
            'result': 'success',
            'new_data': {'remark': '备注成功'},
            'new_html': {'remark': '备注成功'},
        })


class RecordMarkChoice(StaffRequiredMixin, View, MarkChoiceMixin):

    def get(self, request, record_id):
        buy_record = self.get_buy_record(record_id)
        mark_choices = self.get_mark_choices(buy_record)

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'choices': mark_choices
        })
