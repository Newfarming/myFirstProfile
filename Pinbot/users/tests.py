# coding:utf-8

from django.core.cache import cache
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import json
import shortuuid


class AccountTest(TestCase):
    fixtures = [
        'user.json',
        'userprofile.json',
        'companycategory.json',
        'viprolesetting.json',
        'feed.json',
        'feedservice.json',
        'pointrule',
        'industry'
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(
            username='runforever@163.com',
            password='199o1113',
        )

    def tearDown(self):
        self.c.logout()

    def test_reg(self):
        phone = '18086808650'
        sms_code = shortuuid.ShortUUID(alphabet="0123456789").random(length=6)
        code_key = '{0}_{1}'.format(phone, 'AccountReg')
        cache.set(
            code_key,
            sms_code,
            7200
        )
        api = reverse('user-account-reg')
        c = Client()
        json_str = json.dumps({
            'user_email': '1619483@qq.com',
            'password': '123456shi',
            'company_name': 'fdsjakfdja',
            'phone': phone,
            'name': '石刚',
            'qq': '39245133',
            'code': sms_code,
            'select_fields': [1, 2, 3]
        })
        ret = c.post(api, data=json_str, content_type='application/json')
        content = json.loads(ret.content)
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(content.get('status'), 'ok')

    def test_login(self):
        api = reverse('user-account-login')
        c = Client()
        json_str = json.dumps({'username': 'runforever@163.com', 'password': '199o1113'})
        ret = c.post(api, data=json_str, content_type='application/json')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(json.loads(ret.content).get('status'), 'ok')

    def test_email_is_bind(self):
        api = reverse('user-notify-email-is-bind')
        login_url = reverse('user-account-login')
        c = Client()
        json_str = json.dumps({'username': 'runforever@163.com', 'password': '199o1113'})
        c.post(login_url, data=json_str, content_type='application/json')
        ret = c.get(api)
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(json.loads(ret.content).get('is_bind'), False)
