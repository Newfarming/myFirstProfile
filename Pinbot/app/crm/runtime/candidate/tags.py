# coding: utf-8

from resumes.models import (
    ResumeData,
    ContactInfoData
)
from app.crm.models import (
    CandidateTag
)
from pin_utils.django_utils import (
    get_object_or_none,
    get_oid
)
from app.crm.common import (
    CandidateMixin
)


class SystemTagsManage():
    # 系统标签管理

    @classmethod
    def add_tag(self, name):

        ret = CandidateTag(
            name=name
        )
        ret.save()
        return ret.id

    @classmethod
    def del_tag(self, tag_id):

        CandidateTag.objects.filter(id=tag_id).delete()
        return True

    @classmethod
    def get_tags(self):
        
        return CandidateTag.objects.filter(
            display=True
        )


class CandidateTagsManage(CandidateMixin):
    """候选人标签管理"""

    def add_tag(self, resume_id, tag_names, tag_ids):

        # 写入mongodb数据
        tag_list = [{'name': tag_name} for tag_name in tag_names]

        ResumeData.objects.filter(
            id=get_oid(resume_id)
        ).update(
            add_to_set__tags=tag_list
        )

        # 写入mysql数据
        candidate_obj = self.get_candidate_by_resume_id(resume_id=str(resume_id))
        candidate_obj.tags.clear()
        candidate_obj.tags.add(*tag_ids)
        candidate_obj.has_contact = True
        candidate_obj.save()
        return True

    def del_tag(self, resume_id, tag_names, tag_ids):

        # 写入mongodb数据
        tag_list = [{'name': tag_name}for tag_name in tag_names]

        ResumeData.objects(
            id=get_oid(resume_id)
        ).update(
            pull_all__tags=tag_list
        )

        # 写入mysql数据
        candidate_obj = self.get_candidate_by_resume_id(resume_id=str(resume_id))
        candidate_obj.tags.remove(*tag_ids)
        candidate_obj.save()

        return True

    def get_tags(self, resume_id):

        candidate_obj = self.get_candidate_by_resume_id(resume_id=str(resume_id))
        return candidate_obj.tags.all()