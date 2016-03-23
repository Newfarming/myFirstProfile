# coding: utf-8

import base64
import json

from django.test import TestCase, Client


class TestUpdateContactAPI(TestCase):

    fixtures = (
        'user.json',
        'contactinfodata.json',
        'userprofile.json',
    )

    def setUp(self):
        self.c = Client()
        ret = self.c.post('/hr/login/', {
            'username': 'runforever@163.com',
            'password': '199o1113',
        })
        json_ret = json.loads(ret.content)
        token = json_ret['auth_info']['token']
        user = json_ret['auth_info']['user']
        authorization_string = str(user) + ':' + str(token)
        self.encode_authorization = 'Basic %s' % base64.b64encode(authorization_string)

    def test_update_contact(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

        test_case = [
            {
                'resume_id': '550df8ed1d936620eae72161',
                'source': 'zhilian',
                'name': 'chenchao',
                'email': 'runforever@163.com',
                'phone': '18042412008',
                'source_id': 'JR226098827R90250001000',
            },
            {
                'resume_id': '550df8ed1d936620eae72161',
                'source': 'zhilian',
                'name': 'chenchao',
                'email': 'runforever@163.com',
                'phone': '18042412008(手机)',
                'source_id': 'JR226098827R90250001000',
            },
            {
                'resume_id': '550df8ed1d936620eae72161',
                'source': 'zhilian',
                'name': 'chenchao',
                'email': 'runforever@163.com',
                'phone': '18042412007',
                'source_id': 'JR226098827R90250001000',
            }
        ]

        for case in test_case:
            reps = self.c.post(
                '/telnetapi/contactinfo/update/',
                case,
                HTTP_AUTHORIZATION=self.encode_authorization
            )
            self.assertEqual(reps.status_code, 200)
            json_content = json.loads(reps.content)
            self.assertEqual(json_content['status'], 'ok')
