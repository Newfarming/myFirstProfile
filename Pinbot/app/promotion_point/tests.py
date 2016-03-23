# coding: utf-8

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from .promotion_utils import PromotionUtils


class TestPromotionUtils(TestCase):

    fixtures = [
        'promotiontoken.json',
        'pointrule.json',
        'user.json',
    ]

    def test_promotion_success(self):
        token = '7307b281225552ef082a688d9f0c1a01'
        request = RequestFactory()
        request = request.get('/signup/?promotion_token=%s' % token)
        register_user = User.objects.get(username='runforever_test5@163.com')
        register_result = PromotionUtils.register_promotion(request, register_user)
        self.assertTrue(register_result)

        PromotionUtils.promotion_success(register_user)
        self.assertTrue(register_result)
        self.assertEqual(register_user.pinbotpoint.coin, 5)
