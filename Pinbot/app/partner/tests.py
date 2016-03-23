# coding: utf-8

import mock
import json

from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from .views import (
    EditResume,
)
from .partner_utils import (
    PartnerLevelUtils,
    PartnerCoinUtils,
)
from .models import (
    UserAcceptTask,
    UploadResume,
    RecoResumeTask,
)
from .tasks import CleanRecoTask

from feed.models import (
    Feed
)
from pin_utils.parse_utils import (
    ParseUtils,
)

from pin_utils.django_utils import (
    after7day
)


class TestLevel(TestCase):

    fixtures = [
        'user.json',
        'taskcoinrecord.json',
        'uploadresume.json',
        'useraccepttask.json',
        'feed.json',
        'usertaskresume.json',
        'pointrule.json',
        'partnerlevelmanage.json',
    ]

    def test_user_exp_state(self):
        level1_user = User.objects.get(username='runforever@163.com')
        level_utils = PartnerLevelUtils(level1_user)

        exp_state = level_utils.user_exp_state()
        self.assertEqual(exp_state.download_count, 1)
        self.assertEqual(exp_state.interview_count, 1)
        self.assertEqual(exp_state.taking_work_count, 1)

    def test_level_api(self):
        c = Client()
        login_result = c.login(username='runforever@163.com', password='199o1113')
        self.assertEqual(login_result, True)

        url = reverse('partner-level-state')
        res = c.get(url)
        self.assertEqual(res.status_code, 200)

        url = reverse('partner-extra-grant-form', args=(1,))
        res = c.get(url)
        self.assertEqual(res.status_code, 200)

        url = reverse('partner-extra-grant-taking-work', args=(1,))
        res = c.post(url, {'coin': 200})
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.content)
        self.assertEqual(result['result'], 'success')

    def test_empty_user(self):
        User.objects.create_user(
            'runforever_hehe@163.com',
            'runforever_hehe@163.com',
            '123456',
        )
        c = Client()
        c.login(username='runforever_hehe@163.com', password='123456')
        url = reverse('partner-level-state')
        res = c.get(url)
        self.assertEqual(res.status_code, 200)


class TestGetLevel(TestCase):

    fixtures = [
        'partnerlevelmanage.json',
        'user.json',
    ]

    @mock.patch.object(PartnerLevelUtils, 'user_exp_state')
    def test_get_max_level(self, user_exp_state_mock):

        class MockObj(object):
            pass

        exp_state = MockObj()
        exp_state.__dict__.update({
            'check_count': 200,
            'download_count': 100,
            'interview_count': 20,
            'taking_work_count': 10,
            'download_ratio': 0.5,
            'interview_ratio': 0.2,
            'taking_work_ratio': 0.5,
        })
        user_exp_state_mock.return_value = exp_state
        user = User.objects.get(username='runforever@163.com')
        level_utils = PartnerLevelUtils(user)

        download_level = level_utils.get_download_level()
        self.assertEqual(download_level['level'], 2)
        self.assertEqual(download_level['is_max_level'], True)

        interview_level = level_utils.get_interview_level()
        self.assertEqual(interview_level['is_max_level'], True)
        self.assertEqual(interview_level['level'], 4)

        taking_work_level = level_utils.get_taking_work_level()
        self.assertEqual(taking_work_level['is_max_level'], True)
        self.assertEqual(taking_work_level['level'], 3)


class TestExtraGrantUser(TestCase):

    fixtures = [
        'user.json',
        'taskcoinrecord.json',
        'uploadresume.json',
        'useraccepttask.json',
        'feed.json',
        'usertaskresume.json',
        'pointrule.json',
        'partnerlevelmanage.json',
    ]

    def setUp(self):
        self.group = Group.objects.create(name='malice_partner')

    @mock.patch.object(PartnerLevelUtils, 'get_download_level')
    @mock.patch.object(PartnerLevelUtils, 'get_interview_level')
    def test_extra_grant(self, get_interview_level_mock, get_download_level_mock):
        get_download_level_mock.return_value = {
            'bonus_coin': 20,
        }
        get_interview_level_mock.return_value = {
            'bonus_coin': 100,
        }
        coin = PartnerCoinUtils.extra_grant_task_user(
            '5301d9b3fb6dec344c92b790',
            '558287b58230dbc012df1322',
            'extra_download',
        )
        self.assertEqual(coin, 20)

        coin = PartnerCoinUtils.extra_grant_task_user(
            '5301d9b3fb6dec344c92b790',
            '558287b58230dbc012df1322',
            'extra_interview',
        )
        self.assertEqual(coin, 100)

    @mock.patch.object(PartnerLevelUtils, 'get_download_level')
    @mock.patch.object(PartnerLevelUtils, 'get_interview_level')
    def test_malice_extra_grant(self, get_interview_level_mock, get_download_level_mock):
        get_download_level_mock.return_value = {
            'bonus_coin': 20,
        }
        get_interview_level_mock.return_value = {
            'bonus_coin': 100,
        }

        user = User.objects.get(username='runforever@163.com')
        user.groups.add(self.group)

        coin = PartnerCoinUtils.extra_grant_task_user(
            '5301d9b3fb6dec344c92b790',
            '558287b58230dbc012df1322',
            'extra_download',
        )
        self.assertEqual(coin, 0)


class TestGrantUser(TestCase):

    fixtures = [
        'user.json',
        'uploadresume.json',
        'useraccepttask.json',
        'feed.json',
        'usertaskresume.json',
        'pointrule.json',
        'partnerlevelmanage.json',
    ]

    def setUp(self):
        self.group = Group.objects.create(name='malice_partner')

    def test_grant_task_user(self):
        coin = PartnerCoinUtils.download_resume(
            '5301d9b3fb6dec344c92b790',
            '558287b58230dbc012df1322',
        )
        self.assertEqual(coin, 10)

        coin = PartnerCoinUtils.check_resume(
            '5301d9b3fb6dec344c92b790',
            '558287b58230dbc012df1322',
        )
        self.assertEqual(coin, 5)

        coin = PartnerCoinUtils.check_resume(
            '5301d9b3fb6dec344c92b790',
            '558287b58230dbc012df1322',
        )
        self.assertEqual(coin, 0)

    def test_malice_user_grant(self):
        user = User.objects.get(username='runforever@163.com')
        user.groups.add(self.group)

        coin = PartnerCoinUtils.download_resume(
            '5301d9b3fb6dec344c92b790',
            '558287b58230dbc012df1322',
        )
        self.assertEqual(coin, 0)


class TestWebApi(TestCase):

    fixtures = [
        'user.json',
        'uploadresume.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDown(self):
        self.c.logout()

    def test_upload_resume_list(self):
        url = reverse('partner-upload-resume-list')
        res = self.c.get(url)
        self.assertEqual(res.status_code, 200)

    def test_accept_task_list(self):
        url = reverse('partner-accept-task-list')
        res = self.c.get(url)
        self.assertEqual(res.status_code, 200)


class TestAcceptTask(TestCase):

    fixtures = [
        'user.json',
        'uploadresume.json',
    ]

    def setUp(self):
        user = User.objects.create_user(
            'hhrunfor@163.com',
            'hhrunfor@163.com',
            '123456'
        )
        self.feed = Feed.objects.create(
            salary_min=1000,
            salary_max=21500,
            skill_required='fdsafdsakjfklsafjdsakfdj',
            expect_area='北京,成都，上海',
            talent_level='初级',
            job_type='fdsafdsf',
            keywords='fdsafjdkaslfj',
            title='fdasfjdkasfj',
            job_desc='fdsafjkdlsajfdklafj',
            feed_obj_id='55a878df8230dbfce1130553',
            user=user,
            feed_expire_time=after7day(),
            expire_time=after7day(),
        )

    def tearDown(self):
        User.objects.filter(username='hhrunfor@163.com').delete()

    def test_accept_task(self):
        c = Client()
        login_result = c.login(username='runforever@163.com', password='199o1113')
        self.assertEqual(login_result, True)

        url = reverse('partner-accept-task', args=(self.feed.id, 2))
        res = c.get(url)
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')

        has_accept = UserAcceptTask.objects.filter(
            feed=self.feed,
            user__username='runforever@163.com',
        ).exists()
        self.assertTrue(has_accept)


class TestCheckAcceptTask(TestCase):

    fixtures = [
        'user.json',
        'uploadresume.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')
        user = User.objects.create_user(
            'hhrunfor@163.com',
            'hhrunfor@163.com',
            '123456'
        )
        self.feed_area = Feed.objects.create(
            salary_min=1000,
            salary_max=21500,
            skill_required='fdsafdsakjfklsafjdsakfdj',
            expect_area='北京,，上海',
            talent_level='初级',
            job_type='fdsafdsf',
            keywords='fdsafjdkaslfj',
            title='fdasfjdkasfj',
            job_desc='fdsafjkdlsajfdklafj',
            feed_obj_id='55a878df8230dbfce1130553',
            user=user,
            feed_expire_time=after7day(),
            expire_time=after7day(),
        )

        self.feed_salary = Feed.objects.create(
            salary_min=1000,
            salary_max=1500,
            skill_required='fdsafdsakjfklsafjdsakfdj',
            expect_area='北京,成都，上海',
            talent_level='初级',
            job_type='fdsafdsf',
            keywords='fdsafjdkaslfj',
            title='fdasfjdkasfj',
            job_desc='fdsafjkdlsajfdklafj',
            feed_obj_id='55a878df8230dbfce1130553',
            user=user,
            feed_expire_time=after7day(),
            expire_time=after7day(),
        )

    def tearDown(self):
        User.objects.filter(username='hhrunfor@163.com').delete()
        self.c.logout()

    def test_check_accept_task(self):
        url = reverse('partner-check-accept-task', args=(self.feed_area.id, 2))
        res = self.c.get(url)
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'city_unfit')

        url = reverse('partner-check-accept-task', args=(self.feed_salary.id, 2))
        res = self.c.get(url)
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'salary_unfit')


class TestCleanTask(TestCase):

    fixtures = [
        'user.json',
        'uploadresume.json',
    ]

    def setUp(self):
        user = User.objects.create_user(
            'hhrunfor@163.com',
            'hhrunfor@163.com',
            '123456'
        )
        self.feed1 = Feed.objects.create(
            salary_min=1000,
            salary_max=21500,
            skill_required='fdsafdsakjfklsafjdsakfdj',
            expect_area='北京,成都，上海，广州',
            talent_level='初级',
            job_type='fdsafdsf',
            keywords='fdsafjdkaslfj',
            title='fdasfjdkasfj',
            job_desc='fdsafjkdlsajfdklafj',
            feed_obj_id='55a878df8230dbfce1130553',
            user=user,
            feed_expire_time=after7day(),
            expire_time=after7day(),
        )
        self.feed2 = Feed.objects.create(
            salary_min=1000,
            salary_max=1500,
            skill_required='fdsafdsakjfklsafjdsakfdj',
            expect_area='fdasfsf,fdsafda',
            talent_level='初级',
            job_type='fdsafdsf',
            keywords='fdsafjdkaslfj',
            title='fdasfjdkasfj',
            job_desc='fdsafjkdlsajfdklafj',
            feed_obj_id='55a878df8230dbfce1130553',
            user=user,
            feed_expire_time=after7day(),
            expire_time=after7day(),
            deleted=True,
        )
        self.feed3 = Feed.objects.create(
            salary_min=1000,
            salary_max=1500,
            skill_required='fdsafdsakjfklsafjdsakfdj',
            expect_area='fdasfsf,fdsafda',
            talent_level='初级',
            job_type='fdsafdsf',
            keywords='fdsafjdkaslfj',
            title='fdasfjdkasfj',
            job_desc='fdsafjkdlsajfdklafj',
            feed_obj_id='55a878df8230dbfce1130553',
            user=user,
            feed_expire_time=after7day(),
            expire_time=after7day(),
        )
        resume = UploadResume.objects.select_related('user').get(id=2)
        RecoResumeTask.objects.bulk_create([
            RecoResumeTask(
                feed=self.feed1,
                user=resume.user,
                upload_resume=resume,
            ),
            RecoResumeTask(
                feed=self.feed2,
                user=resume.user,
                upload_resume=resume,
            ),
            RecoResumeTask(
                feed=self.feed3,
                user=resume.user,
                upload_resume=resume,
            ),
        ])

    def tearDown(self):
        User.objects.filter(username='hhrunfor@163.com')

    def test_clean_task(self):
        c = Client()
        login_result = c.login(username='runforever@163.com', password='199o1113')
        self.assertEqual(login_result, True)

        url = reverse('partner-accept-task', args=(self.feed1.id, 2))
        res = c.get(url)
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')

        clean_task = CleanRecoTask()
        clean_task.clean_reco_task()

        reco_count = RecoResumeTask.objects.all().count()
        self.assertEqual(reco_count, 0)


class TestEditResume(TestCase):

    fixtures = [
        'user.json',
        'uploadresume.json',
    ]

    post_data = '{"name":"\xe9\x99\x88\xe8\xb6\x85","gender":"male","phone":"18042412008","email":"runforever@163.com","qq":"34564356","address":"\xe6\x88\x90\xe9\x83\xbd","work_years":3,"expect_work_place":"\xe6\x88\x90\xe9\x83\xbd","age":25,"expect_position":"web\xe5\xbc\x80\xe5\x8f\x91\xe5\x8f\x91\xe8\xbe\xbe\xe5\x8f\x91\xe7\x94\x9f\xe5\x9c\xb0\xe6\x96\xb9\xe5\x8f\x91\xe7\x94\x9f\xe7\x9a\x84","target_salary":11,"degree":"bachelor","self_evaluation":"\xe5\xbe\x88\xe5\xa5\xbd","works":[{"start_time":"2014.03","end_time":"2015.03","company_name":"\xe9\xa3\x8e\xe5\xa3\xb0\xe5\xa4\xa7","position_title":"\xe8\x8c\x83\xe5\xbe\xb7\xe8\x90\xa8","id":117,"job_desc":"\xe9\xa3\x8e\xe5\xa3\xb0\xe5\xa4\xa7","_index":1},{"start_time":"2012.11","end_time":"2013.08","company_name":"\xe5\x8c\x97\xe4\xba\xac\xe7\x9f\xa5\xe9\x81\x93\xe5\x88\x9b\xe5\xae\x87","position_title":"web\xe7\xa0\x94\xe5\x8f\x91\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xb8\x88","id":116,"job_desc":"python\xe5\xbc\x80\xe5\x8f\x91\xe4\xb9\x8b\xe7\xb1\xbb\xe7\x9a\x84","_index":0}],"educations":[{"major":"\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xb8\x88","degree":"\xe6\x9c\xac\xe7\xa7\x91","start_time":"2009.09","school":"\xe5\x90\x89\xe6\x9e\x97\xe5\xa4\xa7\xe5\xad\xa6","end_time":"2013.06","id":116},{"major":"\xe5\x8f\x91\xe7\x83\xa7\xe7\xa2\x9f","degree":"\xe7\xa1\x95\xe5\xa3\xab","start_time":"2014.02","school":"fsa","end_time":"2100.01","id":117}],"projects":[{"project_desc":"\xe6\x80\xa5\xe6\x80\xa5\xe6\x80\xa5\xe6\x80\xa5","start_time":"2014.02","project_name":"fsda","id":94,"end_time":"2015.02","_index":0},{"project_desc":"fdsafdsafasfdsa","start_time":"2012.04","project_name":"fdsafasf","id":95,"end_time":"2013.01","_index":0}],"skills":[{"proficiency":"\xe9\xa3\x8e\xe5\xa3\xb0\xe5\xa4\xa7","id":46,"skill_desc":"\xe5\xb7\x8d\xe5\xb3\xa8\xe5\xa5\x87\xe7\x83\xad\xe7\xbd\x91"}],"job_hunting_state":"\xe7\x9b\xae\xe5\x89\x8d\xe6\xad\xa3\xe5\x9c\xa8\xe6\x89\xbe\xe5\xb7\xa5\xe4\xbd\x9c","last_contact":2,"hr_evaluate":"\xe5\xbe\x88\xe4\xb8\x8d\xe9\x94\x99\xe5\x93\xa6","task_id":"0","id":2}'

    @mock.patch.object(ParseUtils, 'insert_resume')
    def test_edit_resume(self, insert_resume_mock):
        insert_resume_mock.return_value = True
        user = User.objects.get(username='runforever@163.com')
        request = RequestFactory()
        request.user = user
        request.body = self.post_data

        edit_resume_view = EditResume()
        edit_resume_view.request = request
        res = edit_resume_view.post(request, 2)
        self.assertEqual(res.status_code, 200)


class TestDumpContactInfo(TestCase):
    '''
    测试重复简历信息判断
    '''
    fixtures = [
        'user.json',
        'uploadresume.json',
        'contactinfodata.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDown(self):
        self.c.logout()

    def test_check_resume_phone(self):
        '''
        人才伙伴录入简历测试重复电话
        '''
        url = reverse('partner-check-exist-phone')
        res = self.c.get(url, {'info': '13444877754'})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'exist')

        res = self.c.get(url, {'info': '18042412008'})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'exist')

        res = self.c.get(url, {'id': 2, 'info': '18042412008'})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')

    def test_check_resume_email(self):
        '''
        人才伙伴录入简历测试重复Email
        '''
        url = reverse('partner-check-exist-email')

        res = self.c.get(url, {'info': 'dae@qq.com'})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'exist')

        res = self.c.get(url, {'info': 'runforever@163.com'})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'exist')

        res = self.c.get(url, {'id': 2, 'info': 'runforever@163.com'})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')
