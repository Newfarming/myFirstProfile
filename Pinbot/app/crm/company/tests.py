# coding: utf-8

import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestCompanyList(TestCase):

    fixtures = [
        'user.json',
        'userprofile.json',
        'company.json',
        'feed.json',
        'job.json',
        'sendcompanycard.json',
        'resumebuyrecord.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDown(self):
        self.c.logout()

    def test_company_list(self):
        url = reverse('crm-company-list')
        data = {'admin_id': '-1'}
        res = self.c.get(url, data=data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context['company_list'])

    def test_assign_admin(self):
        url = reverse('crm-company-assign')
        res = self.c.post(url, {'obj_id': 1, 'client': 907, 'admin': 907})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')

    def test_contact_download(self):
        url = reverse('crm-company-contact', args=(6134, ))
        res = self.c.get(url)
        self.assertEqual(res.status_code, 200)
        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')
