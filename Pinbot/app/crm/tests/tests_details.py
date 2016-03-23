# coding: utf-8

import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from resumes.models import (
    ResumeData,
    ContactInfoData,
)
from resumes.resume_utils import (
    PinbotResumeUtils,
)
from app.crm.runtime.candidate.details import (
    CandidateDetailsManage,
    JobStatusManage
)
from app.crm.runtime.candidate.tags import (
    CandidateTagsManage,
    SystemTagsManage
)

resume_doc = {'job_target': {'salary': '11000', 'job_career': u'web\u5f00\u53d1\u53d1\u8fbe\u53d1\u751f\u5730\u65b9\u53d1\u751f\u7684', 'job_hunting_state': u'\u6211\u76ee\u524d\u5728\u804c\uff0c\u6b63\u8003\u8651\u6362\u4e2a\u73af\u5883', 'expectation_area': u'\u6210\u90fd'}, 'contact_info': {'degree': '\xe6\x9c\xac\xe7\xa7\x91', 'expect_position': u'web\u5f00\u53d1\u53d1\u8fbe\u53d1\u751f\u5730\u65b9\u53d1\u751f\u7684', 'phone': u'18042412008', 'qq': u'348453961', 'name': u'\u9648\u8d85', 'expect_work_place': u'\u6210\u90fd', 'gender': '\xe7\x94\xb7', 'age': 25L, 'job_hunting_state': u'\u6211\u76ee\u524d\u5728\u804c\uff0c\u6b63\u8003\u8651\u6362\u4e2a\u73af\u5883', 'self_evaluation': u'\u5f88\u597d', 'source': 'talent_partner', 'work_years': 3L, 'email': u'runforever@163.com'}, 'updated_at': datetime.datetime(2015, 8, 12, 11, 15, 57), 'expect_position': u'web\u5f00\u53d1\u53d1\u8fbe\u53d1\u751f\u5730\u65b9\u53d1\u751f\u7684', 'owner': u'runforever@163.com', 'resume_id': '55cb059f8230db2113606fc4', 'id': u'55cb059f8230db2113606fc4', 'last_contact': '\xe4\xb8\x80\xe4\xb8\xaa\xe6\x9c\x88\xe5\x86\x85', 'hr_evaluate': u'\u5f88\u4e0d\u9519\u54e6', 'expect_work_place': u'\u6210\u90fd', 'job_hunting_state': u'\u6211\u76ee\u524d\u5728\u804c\uff0c\u6b63\u8003\u8651\u6362\u4e2a\u73af\u5883', 'source': 'talent_partner', 'work_years': '3', 'email': u'runforever@163.com', 'current_job': {}, 'update_time': '2015-08-12', 'degree': '\xe6\x9c\xac\xe7\xa7\x91', 'educations': [{'start_time': '2009-09', 'major': u'\u8f6f\u4ef6\u5de5\u7a0b\u5e08', 'end_time': '2013-06', 'degree': u'\u672c\u79d1', 'school': u'\u5409\u6797\u5927\u5b66'}, {'start_time': '2014-02', 'major': u'\u53d1\u70e7\u789f', 'end_time': '2100-01', 'degree': u'\u7855\u58eb', 'school': u'fsa'}], 'phone': u'18042412008', 'address': u'\u6210\u90fd', 'projects': [{'project_desc': u'\u6025\u6025\u6025\u6025', 'start_time': '2014-02', 'project_name': u'fsda', 'end_time': '2015-02'}, {'project_desc': u'fdsafdsafasfdsa', 'start_time': '2012-04', 'project_name': u'fdsafasf', 'end_time': '2013-01'}], 'name': u'\u9648\u8d85', 'gender': '\xe7\x94\xb7', 'age': 25L, 'professional_skills': [{'proficiency': u'\u98ce\u58f0\u5927', 'skill_desc': u'\u5dcd\u5ce8\u5947\u70ed\u7f51'}], 'self_evaluation': u'\u5f88\u597d', 'works': [{'position_title': u'\u8303\u5fb7\u8428', 'start_time': '2014-03', 'job_desc': u'\u98ce\u58f0\u5927', 'end_time': '2015-03', 'company_name': u'\u98ce\u58f0\u5927'}, {'position_title': u'web\u7814\u53d1\u5de5\u7a0b\u5e08', 'start_time': '2012-11', 'job_desc': u'python\u5f00\u53d1\u4e4b\u7c7b\u7684', 'end_time': '2013-08', 'company_name': u'\u5317\u4eac\u77e5\u9053\u521b\u5b87'}], 'created_at': datetime.datetime(2015, 6, 18, 16, 56, 21)}


class TestCandidateDetailsRuntime(TestCase):
    fixtures = [
        'user.json',
        'resumebuyrecord.json',
        'downloadresumemark.json',
        'resumemarksetting.json',
        'sendcompanycard.json',
        'job.json',
        'company.json',
        'contactinfodata.json',
        'candidatetag.json',
        'candidate.json',
    ]

    def setUp(self):
        self.candidate_tag = CandidateTagsManage()
        self.sys_tag = SystemTagsManage()
        self.job_manage = JobStatusManage()
        self.resume_doc = resume_doc
        resume, _ = PinbotResumeUtils.save(resume_doc)
        self.resume = resume
        self.resume_id = str(resume.id)

    def tearDown(self):
        ResumeData.objects.filter(id=self.resume.id).delete()
        ContactInfoData.objects.filter(resume_id=self.resume_id).delete()

    def test_add_candidate_tag(self):
        ret = self.candidate_tag.add_tag(
            resume_id=self.resume_id,
            tag_ids=[1, 2, 3, 4],
            tag_names=['tag1', 'tag2', 'tag3', 'tag4']
        )
        self.assertTrue(ret)

    def test_get_candidate_info(self):
        ret = CandidateDetailsManage.get_resume_info(
            resume_id=self.resume_id
        )
        self.assertIsNotNone(ret, None)

    def get_candidate_tag(self):
        ret = self.candidate_tag.get_tags(self.resume_id)
        self.assertIsNotNone(ret, None)

    def test_del_candidate_tag(self):
        ret = self.candidate_tag.del_tag(
            resume_id=self.resume_id,
            tag_ids=[1, 2, 3, 4],
            tag_names=['tag1', 'tag2', 'tag3', 'tag4']
        )
        self.assertTrue(ret)

    def test_add_sys_tag(self):
        ret = self.sys_tag.add_tag(
            name='tag5'
        )
        self.assertTrue(ret)

    def test_get_sys_tags(self):
        ret = self.sys_tag.get_tags()
        self.assertIsNotNone(ret, None)

    def test_update_job_status(self):
        ret = self.job_manage.update_status(
            resume_id=self.resume_id,
            job_status='求职(已离职)'
        )
        self.assertTrue(ret)


class TestCandidateDeatilsView(TestCase):

    fixtures = [
        'user.json',
        'resumebuyrecord.json',
        'downloadresumemark.json',
        'resumemarksetting.json',
        'sendcompanycard.json',
        'job.json',
        'company.json',
        'contactinfodata.json',
        'candidatetag.json',
        'candidate.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')
        resume, _ = PinbotResumeUtils.save(resume_doc)
        self.resume = resume
        self.resume_id = str(resume.id)

    def tearDown(self):
        ResumeData.objects.filter(id=self.resume.id).delete()
        ContactInfoData.objects.filter(resume_id=self.resume_id).delete()
        self.c.logout()

    def test_update_job_status(self):

        url = reverse('crm-candidate-update-jobstatus')
        res = self.c.post(url, {'resume_id': self.resume_id,
                                'job_status': '求职(已离职)'
                                }
                          )
        self.assertEqual(res.status_code, 200)

    def test_add_candidate_tag(self):

        url = reverse('crm-candidate-add-tag')
        res = self.c.post(url, {'tag_ids': [1],
                                'tag_names': ['tag1'],
                                'resume_id': self.resume_id
                                }
                          )
        self.assertEqual(res.status_code, 200)

    def test_del_candidate_tag(self):

        url = reverse('crm-candidate-del-tag')
        res = self.c.post(url, {'tag_ids': [1],
                                'tag_names': ['tag1'],
                                'resume_id': self.resume_id
                                }
                          )
        self.assertEqual(res.status_code, 200)

    def test_add_sys_tag(self):

        url = reverse('crm-candidate-add-systag')
        res = self.c.post(url, {
            'name': 'tag6'
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_del_sys_tag(self):

        url = reverse('crm-candidate-del-systag')
        res = self.c.post(url, {
            'tag_id': '1'
            }
        )
        self.assertEqual(res.status_code, 200)
