# coding: utf-8

import datetime

from django.views.generic import View
from django.shortcuts import (
    get_object_or_404,
)
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from app.crm.forms.candidate import (
    CandidateRemarkForm,
)
from app.crm.models import (
    CandidateRemark,
    Candidate,
    CompanyCardSendRecord,
)

from app.crm.common import (
    CandidateMixin,
)

from feed.models import (
    Feed,
)
from resumes.models import (
    ContactInfoData,
)
from app.special_feed.feed_utils import (
    FeedUtils,
)

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    JsonResponse,
    error_email,
    get_object_or_none,
    get_int,
)
from pin_utils.email.send_mail import (
    asyn_send_mail,
)


class EditRemark(StaffRequiredMixin, View, CandidateMixin):
    '''
    编辑备注
    '''
    def get_remark(self, remark_id):
        if not remark_id:
            return None

        remark = get_object_or_404(
            CandidateRemark,
            id=remark_id,
        )
        return remark

    def post(self, request, remark_id=None):
        contact_id = request.POST.get('contact_id', '')
        candidate = self.get_candidate(contact_id)
        remark = self.get_remark(remark_id)
        form = CandidateRemarkForm(request.POST) if not remark else CandidateRemarkForm(request.POST, instance=remark)

        if form.is_valid():
            remark = form.save(commit=False)
            remark.admin = request.user
            remark.candidate = candidate
            candidate.has_contact = True
            candidate.save()
            remark.save()
            return JsonResponse({
                'status': 'ok',
                'remark_id': remark.id,
                'remark_admin': remark.admin.username,
                'remark_time': remark.remark_time.strftime('%Y-%m-%d %H:%M:%S'),
                'remark_type': remark.get_remark_type_display(),
                'remark_desc': remark.desc,
                'msg': '保存成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class DeleteRemark(StaffRequiredMixin, View, CandidateMixin):

    def post(self, request):

        remark_id = request.POST.get('remark_id')
        CandidateRemark.objects.filter(
            id=remark_id
        ).delete()
        return JsonResponse({
            'status': 'ok',
            'msg': 'deleted',
        })


class SendJobCard(StaffRequiredMixin, View, CandidateMixin):
    '''
    发送公司名片
    '''

    def send_email(self, email, feed_id_list, candidate):
        admin = self.request.user

        feed_query = Feed.objects.select_related(
            'user',
            'company',
        ).filter(
            id__in=feed_id_list,
        )

        for feed in feed_query:
            CompanyCardSendRecord.objects.create(
                job=feed,
                operator=admin,
                candidate=candidate,
            )
            subject = '%s职位介绍' % feed.user.first_name if not feed.company else feed.company.company_name
            content = render_to_string(
                'candidate/job_card_email.html',
                {'feed': feed},
            )
            asyn_send_mail.delay(
                email,
                subject,
                content,
            )
        return True

    def post(self, request):
        email = request.POST.get('email', '')
        if error_email(email):
            return JsonResponse({
                'status': 'form_error',
                'msg': '邮件格式错误',
            })

        feed_id_list = request.POST.get('feed_id_list', '').split(',')
        if not feed_id_list:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择要发送的职位',
            })

        contact_id = get_int(self.request.POST.get('contact_id', ''))
        candidate = self.get_candidate(contact_id)

        self.send_email(email, feed_id_list, candidate)
        candidate.has_contact = True
        candidate.save()

        return JsonResponse({
            'status': 'ok',
            'msg': '发送成功',
        })


class AssignCandidate(StaffRequiredMixin, View):
    '''
    分配管理员
    '''

    def assign_contact(self, admin, contact_id_list):
        contact_query = ContactInfoData.objects.select_related(
            'candidate',
        ).filter(
            id__in=contact_id_list,
        )
        for contact in contact_query:
            if hasattr(contact, 'candidate'):
                candidate = contact.candidate
                candidate.admin = admin
            else:
                candidate = Candidate(
                    contact_info=contact,
                    admin=admin,
                )
            candidate.save()
        return True

    def post(self, request):
        admin_id = request.POST.get('admin_id', 0)
        admin = get_object_or_none(
            User,
            id=get_int(admin_id),
            is_staff=True,
        )

        contact_id_list = request.POST.get('contact_id_list', '')
        contact_id_list = contact_id_list.split(',')
        if not contact_id_list:
            return JsonResponse({
                'status': 'contact_error',
                'msg': '请选择联系人信息',
            })

        self.assign_contact(admin, contact_id_list)

        admin_name = '' if admin is None else admin.username

        return JsonResponse({
            'status': 'ok',
            'msg': '分配成功',
            'admin_name': admin_name
        })


class SearchJob(StaffRequiredMixin, View):
    '''
    搜索职位（定制信息）
    '''

    def get(self, request):
        query_str = request.GET.get('q', '')
        if not query_str:
            return JsonResponse({
                'status': 'ok',
                'msg': 'ok',
                'data': [],
            })

        now = datetime.datetime.now()
        feed_query = Feed.objects.select_related(
            'user',
            'company',
        ).filter(
            user__first_name__contains=query_str,
            deleted=False,
            feed_expire_time__lt=now,
        ).order_by('-id')
        data = [
            {
                'id': f.id,
                'title': f.title,
                'username': f.user.username,
                'company_name': f.company.company_name if f.company else f.user.first_name,
                'keywords': f.keywords,
                'expect_area': f.expect_area,
                'feed_expire_time': f.feed_expire_time.strftime('%Y-%m-%d'),
                'feed_obj_id': f.feed_obj_id,
                'salary': f.get_salary(),
            }
            for f in feed_query
        ]
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': data,
        })


class AddFeed(StaffRequiredMixin, View, CandidateMixin):
    '''
    加入定制
    '''

    def post(self, request):
        resume_id = request.POST.get('resume_id', '')
        feed_id = request.POST.get('feed_id', '')
        username = request.user.username

        feed_result = FeedUtils.add_feed_result(
            feed_id,
            resume_id,
            admin=username,
        )

        if not feed_result:
            result = {
                'status': 'data_error',
                'msg': '数据有误',
            }
        else:
            candidate = self.get_candidate_by_resume_id(resume_id)
            candidate.has_contact = True
            candidate.save()

            result = {
                'status': 'ok',
                'msg': '加入成功',
            }
        return JsonResponse(result)
