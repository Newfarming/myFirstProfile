# coding: utf-8

import json

from django.test import TestCase, Client


class TestLogin(TestCase):

    fixtures = [
        'user.json',
        'userprofile.json',
    ]

    def test_login(self):
        api = '/hr/login/'
        c = Client()
        ret = c.post(api, {'username': 'runforever@163.com', 'password': '199o1113'})

        self.assertEqual(ret.status_code, 200)
        json_content = json.loads(ret.content)
        self.assertEqual(json_content['status'], 'ok')

        ret = c.post(api, {'username': 'runforever@163.com', 'password': '199o111'})

        self.assertEqual(ret.status_code, 200)
        json_content = json.loads(ret.content)
        self.assertEqual(json_content['status'], 'form_error')

    def test_valid_token(self):
        api = '/hr/login/'
        c = Client()
        ret = c.post(api, {'username': 'runforever@163.com', 'password': '199o1113'})

        self.assertEqual(ret.status_code, 200)
        json_content = json.loads(ret.content)
        self.assertEqual(json_content['status'], 'ok')

        token = json_content['auth_info']['token']
        user_id = json_content['auth_info']['user']

        valid_api = '/hr/valid_token/{0}/{1}/'.format(user_id, token)
        ret = c.get(valid_api)
        self.assertEqual(ret.status_code, 200)
        json_content = json.loads(ret.content)
        self.assertEqual(json_content['status'], 'ok')

    def test_register(self):
        api = '/hr/register/'
        c = Client()
        ret = c.post(api, {
            'user_email': 'runforever_test4@163.com',
            'password': '199o1113',
            'company_name': 'fdsjakfdja',
            'phone': '18042412008',
            'name': 'alan'
        })

        self.assertEqual(ret.status_code, 200)
        json_content = json.loads(ret.content)
        self.assertEqual(json_content['status'], 'ok')
