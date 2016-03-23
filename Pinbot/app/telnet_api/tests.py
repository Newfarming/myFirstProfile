# coding: utf-8

import base64
import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestSpiderMsg(TestCase):

    fixtures = [
        'user.json',
        'permission.json'
    ]

    def setUp(self):
        self.c = Client()
        self.token_url = reverse('get-token')
        self.sendnotify_url = reverse('send-notify')

    def test_gettoken_success(self):
        response = self.c.post(
            self.token_url,
            {
                'username': 'spider_msg_account',
                'password': "`~#@!spider",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('status'), 'ok')
        auth_info = json.loads(response.content).get('auth_info')

        return auth_info

    def test_gettoken_failed(self):
        response = self.c.post(
            self.token_url,
            {
                'username': 'wrong_user',
                'password': 'wrong_password',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('status'), 'error')
        self.assertEqual(json.loads(response.content).get('msg'), 'error user')

    def test_gettoken_nopermission(self):
        response = self.c.post(
            self.token_url,
            {
                'username': 'runforever@163.com',
                'password': '199o1113',
            }
        )
        self.assertEqual(json.loads(response.content).get('status'), 'error')
        self.assertEqual(json.loads(response.content).get('msg'), 'no permission')

    def test_notify(self):

        auth_info = self.test_gettoken_success()
        user_id = auth_info.get('user')
        token = auth_info.get('token')
        authorization_string = str(user_id) + ':' + str(token)
        encode_authorization = base64.b64encode(authorization_string)

        response = self.c.get(
            self.sendnotify_url,
            {
                'user': 907,
                'status': 0,
                'resume_id': '539fb9ca81af590468fad7ab',
            },
            HTTP_AUTHORIZATION='Basic ' + encode_authorization
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('status'), 'not notify')

        response = self.c.get(
            self.sendnotify_url,
            {
                'user': 907,
                'status': 1,
                'resume_id': '539fb9ca81af590468fad7ab',
            },
            HTTP_AUTHORIZATION='Basic ' + encode_authorization
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('status'), 'ok')
