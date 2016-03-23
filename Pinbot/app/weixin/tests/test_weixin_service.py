# coding: utf-8

from django.test import TestCase
from app.weixin.runtime.weixin_utils import (
    WeixinService
)


class TestWeixinService(TestCase):

    def setUp(self):
        pass

    def test_create_menu(self):
        self.assertTrue(WeixinService.create_menu())

    def test_get_access_token(self):
        self.assertIsNotNone(WeixinService.get_base_access_token())

    def test_get_feed_notify_msg_tpl(self):
        self.assertIsNotNone(WeixinService.get_feed_notify_msg_tpl())

    def test_get_recommand_url(self):
        self.assertIsNotNone(WeixinService.get_recommand_url())

    def test_get_template_msg_id(self):
        self.assertIsNotNone(WeixinService.get_template_msg_id())
