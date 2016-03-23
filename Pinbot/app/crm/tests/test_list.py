# coding: utf-8

import json
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestList(TestCase):

    fixtures = [
        'user.json',
        'contactinfodata.json',
        'candidatetag.json',
        'feed.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDown(self):
        self.c.logout()

    def test_candidate_list(self):
        url = reverse('crm-candidate-list')
        res = self.c.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context['admin_list'])
        self.assertTrue(res.context['candidate_list'])
        self.assertTrue(res.context['tag_list'])

    def test_admin_list(self):
        url = reverse('crm-admin-list')
        res = self.c.get(url)

        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.content)
        self.assertEqual(json_data['status'], 'ok')
        self.assertTrue(json_data['data'])

    def test_search_job(self):
        url = reverse('crm-candidate-search-job')
        res = self.c.get(url, {'q': '浩泊'})
        json_data = json.loads(res.content)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(len(json_data['data']), 3)


class TestCandidateOperate(TestCase):

    fixtures = [
        'user.json',
        'contactinfodata.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDown(self):
        self.c.logout()

    def test_edit_remark(self):
        url = reverse('crm-candidate-edit-remark')
        res = self.c.post(url, {'contact_id': 52226, 'remark_type': 0, 'desc': 'heheheh'})

        json_data = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(json_data['remark_admin'], 'runforever@163.com')

    def test_assign_candidate(self):
        url = reverse('crm-candidate-assign-candidate')
        res = self.c.post(url, {'admin_id': '907', 'contact_id_list': '52225'})

        json_data = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['status'], 'ok')

    def test_add_feed(self):
        url = reverse('crm-candidate-add-feed')
        res = self.c.post(
            url,
            {
                'feed_id': '55c466148230dbbce21e1c4c',
                'resume_id': '55c1af6ac036980e206b9c80'
            }
        )
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.content)
        self.assertEqual(json_data['status'], 'ok')

    def test_send_email(self):
        url = reverse('crm-candidate-send-job-card')
        res = self.c.post(
            url,
            {
                'email': 'runforever@163.com',
                'feed_id_list': '3026',
                'contact_id': '52217',
            }
        )
        json_data = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['status'], 'ok')
