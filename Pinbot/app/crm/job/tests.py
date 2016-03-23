# coding: utf-8

import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestCompany(TestCase):

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

    def test_add_remark(self):
        url = reverse('crm-add-feed-remark')
        res = self.c.post(url, {'feed': 235725, 'remark_type': 2, 'remark': 'heheheheheh'})
        self.assertEqual(res.status_code, 200)

        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')
