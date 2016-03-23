# coding: utf-8

import datetime

from resumes.models import (
    ResumeData
)

from pin_utils.django_utils import (
    get_oid,

)
from app.crm.common import (
    CandidateMixin
)


class CandidateDetailsManage(object):
    # 候选人详情管理类
    @classmethod
    def get_resume_info(self, resume_id):

        ret = ResumeData.objects.filter(id=get_oid(resume_id)).first()
        return ret


class JobStatusManage(CandidateMixin):
    # 求职状态管理类

    def update_status(self, resume_id, job_status, admin=''):

        admin_time = datetime.datetime.now()
        ResumeData.objects.filter(
            id=get_oid(resume_id)
        ).update(
            set__job_target__job_hunting_state=job_status,
            set__admin=admin,
            set__admin_time=admin_time,
        )

        candidate_obj = self.get_candidate_by_resume_id(resume_id)
        candidate_obj.has_contact = True
        candidate_obj.save()

        return True
