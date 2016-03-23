# coding: utf-8

import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestMarkResume(TestCase):

    fixtures = [
        'user.json',
        'uservip.json',
        'viprolesetting.json',
        'markresumebuyrecord.json',
        'resumemarksetting.json',
        'resumemarkrelation.json',
        'userprofile.json',
        'pointrule.json',
    ]

    def test_mark_resume(self):
        c = Client()
        login_result = c.login(username='runforever@163.com', password='199o1113')
        self.assertTrue(login_result)

        url = reverse('transaction-mark-resume', args=(12, ))

        res = c.post(url, {'code_name': 'entry'})
        self.assertEqual(res.status_code, 200)
        json_content = json.loads(res.content)
        self.assertEqual(json_content['status'], 'ok')
