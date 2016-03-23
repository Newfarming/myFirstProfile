# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User

from models import PointRule, PinbotPoint, PointRecord
from point_utils import point_utils

from pin_utils.django_utils import get_object_or_none


class TestPointUtils(TestCase):

    def setUp(self):
        self.test_rule = PointRule(
            rule_name='TEST RULE',
            point_rule='partner_upload',
            rule_type='add',
            record_type='partner',
            point=20,
            total_max_point=60,
            days_max_point=20,
            description=u'上传简历获得点数',
            remark=u'上传点数规则设置',
        )
        self.test_rule.save()

        self.reduce_rule = PointRule(
            rule_name='REDUCE RULE',
            point_rule='accu_resume',
            rule_type='consume',
            record_type='partner',
            point=-10,
            total_max_point=-60,
            days_max_point=-40,
            description=u'举报简历扣除点数',
            remark=u'举报简历扣除点数',
        )
        self.reduce_rule.save()
        self.user = User.objects.create_user(
            "runforever@163.com",
            "123456",
        )

    def tearDown(self):
        PinbotPoint.objects.filter(
            user=self.user,
        ).delete()
        PointRecord.objects.filter(
            user=self.user,
        ).delete()

    def test_partner_upload(self):
        '''
         test add point
        '''
        result, point = point_utils.partner_upload(self.user)
        self.assertEqual(result, 'success')
        self.assertEqual(point, 20)
        pinbot_point = get_object_or_none(
            PinbotPoint,
            user=self.user,
        )
        self.assertEqual(pinbot_point.point, 20)

    def test_max_partner_upload(self):
        '''
        test add max point
        '''
        result, point = point_utils.partner_upload(self.user)
        result, point = point_utils.partner_upload(self.user)
        result, point = point_utils.partner_upload(self.user)
        result, point = point_utils.partner_upload(self.user)

        self.assertEqual(result, 'over_total_max')
        self.assertEqual(point, 0)

        pinbot_point = get_object_or_none(
            PinbotPoint,
            user=self.user,
        )
        self.assertEqual(pinbot_point.point, 60)

    def test_accu_resume(self):
        '''
        测试简历扣除
        '''
        result, point = point_utils.partner_upload(self.user)
        self.assertEqual(result, 'success')
        self.assertEqual(point, 20)

        pinbot_point = point_utils._get_pinbot_point(self.user)
        self.assertEqual(pinbot_point.point, 20)

        result, point = point_utils.accu_resume(self.user)
        self.assertEqual(result, 'success')
        self.assertEqual(point, -10)

        pinbot_point = point_utils._get_pinbot_point(self.user)
        self.assertEqual(pinbot_point.point, 10)
