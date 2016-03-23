# coding: utf-8

import mock
import json

from django.test import TestCase, Client

from FeedCelery.celery_utils import CeleryUtils


class TestSubmitFeed(TestCase):

    fixtures = [
        'user.json',
        'userprofile.json',
        'userchargepackage.json',
        'companycategory.json',
        'companycategoryprefer.json',
        'feedservice.json',
        'industry.json'
    ]

    @mock.patch.object(CeleryUtils, 'user_feed_task')
    def test_submit_feed(self, user_feed_task_mock):
        user_feed_task_mock.return_value = True

        data = json.dumps({'analyze_job_domain': [], 'categorys': [{'category': 'O2O', 'id': 7}, {'category': '移动互联网', 'id': 14}], 'company_prefer': [1], 'expect_area': '北京,上海', 'feed_id': '',
                           'job_desc': 'Python\nHtml\nJS', 'job_domain': [7], 'job_welfare': '不加班,不打卡', 'keywords': 'python', 'salary_max': 5000, 'salary_min': 3000, 'skill_required': '', 'talent_level': '中级,高级', 'title': 'Python开发'})

        api = '/special_feed/submit_feed/'
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')
        ret = self.c.post(api, content_type='application/json', data=data)

        self.assertEqual(ret.status_code, 200)
        json_content = json.loads(ret.content)
        self.assertEqual(json_content['status'], 'ok')

        # 清理测试数据
        feed_id = json_content['feed_id']
        self.c.get('/feed/delete/{0}/'.format(feed_id))


class TestShowFeedResult(TestCase):

    fixtures = [
        'user.json',
    ]

    def test_show_feed_result(self):
        api = '/special_feed/feed_list/568f24488230db780e7bc127/?start=0&latest=0&send=0&partner=0&title_match=1&extend_match=0&reco_time=15'
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

        ret = self.c.get(api)
        self.assertEqual(ret.status_code, 200)

        json_content = json.loads(ret.content)
        self.assertEqual(json_content['status'], 'ok')
