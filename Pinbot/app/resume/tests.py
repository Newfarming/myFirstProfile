# coding: utf-8

import json
import bson

from django.test import TestCase, Client

from resumes.resume_utils import PinbotResumeUtils
from resumes.models import ResumeData

from pin_utils.django_utils import (
    get_tomorrow,
)


class TestInviteInterview(TestCase):

    fixtures = (
        'user.json',
        'markresumebuyrecord.json',
        'resumemarksetting.json',
        'resumemarkrelation.json',
    )

    def test_invite_interview(self):
        c = Client()
        c.login(username='runforever@163.com', password='199o1113')

        url = '/resume/interview/send/12/'
        tomorrow = get_tomorrow()
        res = c.post(url, {
            'code_name': 'invite_interview',
            'interview_time': tomorrow.strftime('%Y-%m-%d %H:%M')
        })

        self.assertEqual(res.status_code, 200)
        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')


class TestResumeDisplay(TestCase):

    fixtures = (
        'user.json',
        'markresumebuyrecord.json',
        'resumemarksetting.json',
        'resumemarkrelation.json',
        'pointrule.json',
    )

    resume_data = '{"name":"\xe9\x99\x88\xe8\xb6\x85","gender":"male","phone":"18042412008","email":"runforever@163.com","qq":"34564356","address":"\xe6\x88\x90\xe9\x83\xbd","work_years":"3","expect_work_place":"\xe6\x88\x90\xe9\x83\xbd","age":25,"expect_position":"web\xe5\xbc\x80\xe5\x8f\x91\xe5\x8f\x91\xe8\xbe\xbe\xe5\x8f\x91\xe7\x94\x9f\xe5\x9c\xb0\xe6\x96\xb9\xe5\x8f\x91\xe7\x94\x9f\xe7\x9a\x84","target_salary":11,"degree":"bachelor","self_evaluation":"\xe5\xbe\x88\xe5\xa5\xbd","works":[{"start_time":"2014.03","end_time":"2015.03","company_name":"\xe9\xa3\x8e\xe5\xa3\xb0\xe5\xa4\xa7","position_title":"\xe8\x8c\x83\xe5\xbe\xb7\xe8\x90\xa8","id":117,"job_desc":"\xe9\xa3\x8e\xe5\xa3\xb0\xe5\xa4\xa7","_index":1},{"start_time":"2012.11","end_time":"2013.08","company_name":"\xe5\x8c\x97\xe4\xba\xac\xe7\x9f\xa5\xe9\x81\x93\xe5\x88\x9b\xe5\xae\x87","position_title":"web\xe7\xa0\x94\xe5\x8f\x91\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xb8\x88","id":116,"job_desc":"python\xe5\xbc\x80\xe5\x8f\x91\xe4\xb9\x8b\xe7\xb1\xbb\xe7\x9a\x84","_index":0}],"educations":[{"major":"\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xb8\x88","degree":"\xe6\x9c\xac\xe7\xa7\x91","start_time":"2009.09","school":"\xe5\x90\x89\xe6\x9e\x97\xe5\xa4\xa7\xe5\xad\xa6","end_time":"2013.06","id":116},{"major":"\xe5\x8f\x91\xe7\x83\xa7\xe7\xa2\x9f","degree":"\xe7\xa1\x95\xe5\xa3\xab","start_time":"2014.02","school":"fsa","end_time":"2100.01","id":117}],"projects":[{"project_desc":"\xe6\x80\xa5\xe6\x80\xa5\xe6\x80\xa5\xe6\x80\xa5","start_time":"2014.02","project_name":"fsda","id":94,"end_time":"2015.02","_index":0},{"project_desc":"fdsafdsafasfdsa","start_time":"2012.04","project_name":"fdsafasf","id":95,"end_time":"2013.01","_index":0}],"skills":[{"proficiency":"\xe9\xa3\x8e\xe5\xa3\xb0\xe5\xa4\xa7","id":46,"skill_desc":"\xe5\xb7\x8d\xe5\xb3\xa8\xe5\xa5\x87\xe7\x83\xad\xe7\xbd\x91"}],"job_hunting_state":"\xe7\x9b\xae\xe5\x89\x8d\xe6\xad\xa3\xe5\x9c\xa8\xe6\x89\xbe\xe5\xb7\xa5\xe4\xbd\x9c","last_contact":"2","hr_evaluate":"\xe5\xbe\x88\xe4\xb8\x8d\xe9\x94\x99\xe5\x93\xa6","task_id":"0","id":2}'

    def setUp(self):
        dict_data = json.loads(self.resume_data)
        dict_data['resume_id'] = str(bson.ObjectId())
        self.resume, self.contact_info = PinbotResumeUtils.save(dict_data)

    def tearDown(self):
        ResumeData.objects.filter(
            id=self.resume.id,
        ).delete()

    def test_resume_display(self):
        resume_id = str(self.resume.id)
        url = '/resumes/display/%s/' % resume_id

        c = Client()
        c.login(username='runforever@163.com', password='199o1113')
        res = c.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context['resume'])
