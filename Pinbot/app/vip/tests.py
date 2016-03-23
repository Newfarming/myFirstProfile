# coding: utf-8

import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import (
    UserVip,
    VipRoleSetting,
)
from .runtime.self_service import (
    SelfService,
    SelfServiceUtils,
)

from app.pinbot_point.point_utils import (
    point_utils,
)
from app.pinbot_point.models import (
    PointRecord,
)

from pin_utils.package_utils import PackageUtils
from pin_utils.django_utils import (
    get_previous_monday,
)


class TestRenewService(TestCase):

    fixtures = [
        'user.json',
        'userchargepackage.json',
        'feedservice.json',
        'feed.json',
        'userfeed.json',
        'uservip.json',
        'viprolesetting.json',
        'auth_group.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')

    def tearDonw(self):
        self.c.logout()

    def test_expire_uservip(self):
        uservip = UserVip.objects.get(user__username='runforever@163.com')
        PackageUtils.update_uservip_package(uservip)

        expire_time = uservip.expire_time
        user = uservip.user
        has_feed = user.feed_set.filter(expire_time=expire_time).exists()
        self.assertTrue(has_feed)

    def test_disable_uservip(self):
        api = reverse('vip-disable', args=(2,))
        ret = self.c.post(api)

        self.assertEqual(ret.status_code, 200)
        json_content = json.loads(ret.content)
        self.assertEqual(json_content['result'], 'success')

        experience_uservip = UserVip.objects.filter(
            user__username='runforever@163.com',
            vip_role__code_name='experience_user',
            is_active=True,
        ).exists()

        self.assertTrue(experience_uservip)


class TestWeekPoint(TestCase):

    fixtures = (
        'user.json',
        'pointrule.json',
        'uservip.json',
        'viprolesetting.json',
    )

    def setUp(self):
        user_vip_query = UserVip.objects.select_related(
            'user',
        ).filter(
            user__username='runforever@163.com',
            is_active=True,
        )

        self.user_vip = user_vip_query[0]
        self.user = self.user_vip.user

        self.user = User.objects.get(username='runforever@163.com')
        pinbot_point = point_utils._get_pinbot_point(self.user)
        pinbot_point.point = 100
        pinbot_point.save()

        point_utils.consume_download_point(self.user)
        point_utils.consume_download_point(self.user)
        point_utils.consume_download_point(self.user)

        previous_monday = get_previous_monday()
        PointRecord.objects.filter(
            user=self.user,
        ).update(
            record_time=previous_monday,
        )

    def tearDown(self):
        pinbot_point = point_utils._get_pinbot_point(self.user)
        pinbot_point.point = 0
        pinbot_point.save()

        PointRecord.objects.filter(
            user=self.user,
        ).delete()

    def test_week_point(self):
        _, point = point_utils.week_point(self.user, vip_user=self.user_vip)
        self.assertEqual(30, point)


class TestSelfService(TestCase):

    fixtures = [
        'user.json',
        'userchargepackage.json',
        'feedservice.json',
        'feed.json',
        'userfeed.json',
        'uservip.json',
        'viprolesetting.json',
        'auth_group.json',
        'pointrule.json',
    ]

    def test_active_self_service(self):
        '''
        测试自助套餐生效
        '''
        user = User.objects.get(username='runforever@163.com')
        product = VipRoleSetting.objects.get(id=5)
        self_srv = SelfService(
            service_name='self_service',
            product=product,
            user=user,
        )
        self_srv.create_service()
        self_srv.active_service()

        pinbot_point = point_utils._get_pinbot_point(user)
        self.assertEqual(pinbot_point.point, 600)


class TestDeactiveSelfService(TestCase):

    fixtures = [
        'user.json',
        'userchargepackage.json',
        'feedservice.json',
        'feed.json',
        'userfeed.json',
        'uservip.json',
        'viprolesetting.json',
        'auth_group.json',
        'pointrule.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='runforever@163.com')
        product = VipRoleSetting.objects.get(id=5)
        self_srv = SelfService(
            service_name='self_service',
            product=product,
            user=self.user,
        )
        self.user_vip = self_srv.create_service()
        self_srv.active_service()

    def tearDown(self):
        SelfServiceUtils.set_experience_user(self.user)

    def test_deactive_user(self):
        result, point = point_utils.deduction_self_point(self.user, self.user_vip)
        self.assertEqual(point, -600)
        self.assertEqual(result, 'success')
