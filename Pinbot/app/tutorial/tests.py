# coding: utf-8

import json

from django.core.cache import cache
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestInterviewTerm(TestCase):

    def setUp(self):
        self.c = Client()
        cache.delete('feedback127.0.0.1')

    def test_feedback_sucess(self):

        data = json.dumps({"feedback_text": "测试数据", "contact_email": "test@test.com"})
        result = self.c.post(reverse('feedback'), data=data, content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content).get('status'), 'ok')

    def test_feedback_faile(self):

        data_no_text = json.dumps({"feedback_text": "", "contact_email": "test@test.com"})
        data_no_email = json.dumps({"feedback_text": "asdf", "contact_email": ""})

        result_no_text = self.c.post(reverse('feedback'), data=data_no_text, content_type='application/json')
        self.assertEqual(result_no_text.status_code, 200)
        self.assertEqual(json.loads(result_no_text.content).get('status'), 'error')

        result_no_email = self.c.post(reverse('feedback'), data=data_no_email, content_type='application/json')
        self.assertEqual(result_no_email.status_code, 200)
        self.assertEqual(json.loads(result_no_email.content).get('status'), 'error')
