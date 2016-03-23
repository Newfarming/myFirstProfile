# coding: utf-8

import json
from django.test import TestCase, Client


class TestResumeCenterList(TestCase):

    fixtures = [
        'user.json',
        'markresumebuyrecord.json',
        'user.json',
        'markresumebuyrecord.json',
        'resumemarksetting.json',
        'resumemarkrelation.json',
        'userwatchresume.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDown(self):
        self.c.logout()

    def test_buy_record(self):
        url = '/resume/buy_record/list/'
        res = self.c.get(url)

        self.assertEqual(res.status_code, 200)
        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')
        self.assertTrue(json_content['data'])

    def test_follow_list(self):
        url = '/resume/follow/list/'
        res = self.c.get(url)

        self.assertEqual(res.status_code, 200)
        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')
        self.assertTrue(json_content['data'])


class TestResumeCategory(TestCase):

    fixtures = [
        'user.json',
        'markresumebuyrecord.json',
        'user.json',
        'markresumebuyrecord.json',
        'resumemarksetting.json',
        'resumemarkrelation.json',
        'userwatchresume.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDown(self):
        self.c.logout()

    def test_category_resume(self):
        url = '/resume/category/create/'
        res = self.c.post(
            url,
            json.dumps({'category_name': 'test'}),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 200)
        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')

        # test category resume
        category_id = json_content['data']['id']
        category_url = '/resume/category_resume/%s/' % category_id
        res = self.c.post(
            category_url,
            json.dumps({'record_id': [12]}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')
