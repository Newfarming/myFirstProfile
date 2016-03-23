# coding: utf-8

import datetime

from django.shortcuts import Http404
from django.contrib.auth.models import User

from .models import CRMClientInfo
from app.vip.models import (
    UserManualService,
    UserOrder,
)
from resumes.models import (
    ContactInfoData,
    ResumeData,
)
from app.crm.models import (
    Candidate,
)

from pin_utils.django_utils import (
    get_oid,
)


class CandidateMixin(object):

    def _generic_get_candidate(self, get_type, type_id):
        meta = {
            'contact': {
                'key': 'id',
            },
            'resume': {
                'key': 'resume_id',
            },
        }
        filter_key = meta[get_type]['key']
        filter_cond = {
            filter_key: type_id,
        }

        contact_query = ContactInfoData.objects.select_related(
            'candidate',
        ).filter(
            **filter_cond
        )
        if not contact_query:
            raise Http404

        contact = contact_query[0]
        if hasattr(contact, 'candidate'):
            candidate = contact.candidate
        else:
            candidate = Candidate(
                contact_info=contact,
            )
            candidate.save()
        return candidate

    def get_candidate(self, contact_id):
        candidate = self._generic_get_candidate('contact', contact_id)
        return candidate

    def get_candidate_by_resume_id(self, resume_id):
        resume_id = str(resume_id)
        candidate = self._generic_get_candidate('resume', resume_id)
        return candidate


class CandidateListMixin(object):

    def get_candidate_work(self, resume_data):
        if not resume_data:
            return {}
        return resume_data.get_latest_work_dict()

    def get_candidate_job_target(self, resume_data):
        if not resume_data:
            return {}
        return resume_data.get_job_target_dict()

    def add_candidate_extra_info(self, candidate_list):
        resume_oid_list = [get_oid(i.resume_id) for i in candidate_list if get_oid(i.resume_id)]
        resume_data = ResumeData.objects.filter(
            id__in=resume_oid_list,
        ).only(
            'job_target',
            'works',
            'address',
            'source',
            'update_time',
        )
        resume_data_dict = {
            str(r.id): r
            for r in resume_data
        }
        for candidate in candidate_list:
            resume_id = candidate.resume_id
            resume_data = resume_data_dict.get(resume_id)

            if not resume_data:
                continue

            candidate.work = self.get_candidate_work(
                resume_data,
            )
            candidate.job_target = self.get_candidate_job_target(
                resume_data,
            )
            candidate.address = resume_data.address
            candidate.update_time = resume_data.update_time
        return candidate_list


class AdminListMixin(object):

    def get_admin_list(self):
        admin_list = list(User.objects.filter(
            is_staff=True,
        ).values(
            'id',
            'username',
        ))
        return admin_list


def get_query_id_and_staff_desc(operate_type, request, **kwargs):

    def manual_service(request, **kwargs):
        is_continue = request.POST.get('pay_status')
        if is_continue == 'continue':
            staff_desc = '续期'
        else:
            staff_desc = '开通套餐'
        user_manual_service_id = int(kwargs.get('manual_service_id', '0'))
        return (user_manual_service_id, staff_desc)

    def finished_manual_service(*args, **kwargs):
        user_manual_service_id = int(kwargs.get('op_id', '0'))
        staff_desc = '关闭套餐'
        return (user_manual_service_id, staff_desc)

    def refunded(*args, **kwargs):
        order_id = kwargs.get('op_id')
        staff_desc = '退款'
        return (order_id, staff_desc)

    operate_type_dict = {
        'apply_manual_service': manual_service,
        'finished_manual_service': finished_manual_service,
        'refunded': refunded,
    }
    return operate_type_dict.get(operate_type)(request, **kwargs)


def get_user(operate_type, query_id):

    def get_user_by_manual_service_id(query_id):
        user_manual_service_query = UserManualService.objects.select_related(
            'user'
        ).filter(
            id=query_id
        )
        if not user_manual_service_query:
            return None
        return user_manual_service_query[0].user

    def get_user_by_order_id(query_id):
        user_order_query = UserOrder.objects.filter(
            order_id=query_id
        )
        if not user_order_query:
            return None
        return user_order_query[0].user

    operate_type_dict = {
        'apply_manual_service': get_user_by_manual_service_id,
        'finished_manual_service': get_user_by_manual_service_id,
        'refunded': get_user_by_order_id,
    }
    return operate_type_dict.get(operate_type)(query_id)


def record_last_operate(user, admin, staff_desc):
    admin_record, _ = CRMClientInfo.objects.get_or_create(
        client=user
    )
    admin_record.last_operate_admin=admin
    admin_record.last_time=datetime.datetime.now()
    admin_record.last_operate_staff=staff_desc
    admin_record.save()
    return True


def record_operate_admin(operate_type):
    def f_record_operate_admin(func):
        def f_record_operate_admin(*args, **kwargs):
            result = func(*args, **kwargs)
            if not result:
                return result
            admin = args[1].user
            query_id, staff_desc = get_query_id_and_staff_desc(operate_type, args[1], **kwargs)
            user = get_user(operate_type, query_id)
            record_last_operate(user, admin, staff_desc)
            return result
        return f_record_operate_admin
    return f_record_operate_admin
