# coding: utf-8

import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import Permission
from django.db import transaction

from app.vip.models import (
    UserVip,
    VipRoleSetting
)
from pin_utils.django_utils import (
    get_object_or_none,
    get_today,
)
from app.pinbot_point.point_utils import (
    point_utils,
)
from app.vip.vip_utils import (
    VipRoleUtils,
)
from pin_utils.package_utils import (
    PackageUtils,
)
from app.vip.runtime.service import (
    BaseService
)


class SelfService(BaseService):

    service_name = 'self_service'

    def __init__(self, **data):
        super(SelfService, self).__init__(**data)

    def process(self, **data):
        return self.do_str_to_fun()

    def create_service(self):
        self_service = self.add_user_vip_record(
            user=self.user
        )
        if not self_service:
            return False

        self.service_id = self_service.id
        self.change_service_status(
            status='applying'
        )

        return self_service

    def active_service(self):
        # 金币兑换
        if self.payment_terms == 'coin':
            self.debit_coin(self.user, self.order_price)

        # 失效当前生效的自助套餐
        SelfServiceUtils.set_experience_user(self.user)

        # 生效新购买的自助套餐
        self_service = get_object_or_none(UserVip, id=self.service_id)
        self.update_user_vip(self_service)
        self.update_vip_pkg(self_service)
        self.update_vip_perms(self_service)
        self.update_self_point(self_service)
        self.update_vip_point(self_service)
        self.change_service_status(
            status='success'
        )

        return True

    def invalid_service(self):
        return True

    def update_guide_switch(self, user):
        current_vip = VipRoleUtils.get_current_vip(user)
        if current_vip:
            return False
        user.userprofile.guide_switch = True
        user.userprofile.save()
        return user

    def add_user_vip_record(self, user, with_manual=False):
        if with_manual:
            product_id = get_object_or_none(VipRoleSetting, code_name='experience_user').id
        else:
            product_id = self.product.id

        self.current_vip = VipRoleUtils.get_current_vip(user)

        self.vip_role = get_object_or_none(
            VipRoleSetting,
            id=product_id,
            allow_apply=True,
        )

        if not self.vip_role:
            return False

        user_vip = UserVip(
            user=user,
            vip_role=self.vip_role,
            total_price=self.vip_role.price,
        )
        user_vip.save()
        return user_vip

    def get_current_active_service(self, user):
        current_active_service = UserVip.objects.select_related(
            'vip_role',
        ).filter(
            user=user,
            is_active=True
        )
        if current_active_service:
            return current_active_service[0]
        else:
            return None

    def has_active_service(self, user):
        has_active_service = UserVip.objects.filter(
            user=user,
            is_active=True
        ).exists()

        return has_active_service

    def update_user_vip(self, user_vip, admin=False):
        user_vip.apply_status = 'success'
        user = user_vip.user

        if user_vip.vip_role.auto_active or admin:
            UserVip.objects.filter(
                user=user,
                is_active=True,
            ).update(
                is_active=False,
            )

            service_time = user_vip.vip_role.service_time
            now = datetime.datetime.now()
            today = get_today()
            expire_time = today + relativedelta(months=service_time)

            user_vip.is_active = True
            user_vip.active_time = now
            user_vip.expire_time = expire_time

        user_vip.save()
        return user_vip

    def update_vip_pkg(self, user_vip, admin=False):
        vip_role = user_vip.vip_role
        user = user_vip.user

        vip_feed_pkg = PackageUtils.get_vip_feed_pkg(user)
        if user_vip.vip_role.auto_active or admin:
            feed_count = vip_role.feed_count if not user_vip.custom_feed else user_vip.custom_feed
            add_count = feed_count - vip_feed_pkg.extra_feed_num
            if add_count > 0:
                vip_feed_pkg.rest_feed += add_count
                vip_feed_pkg.extra_feed_num += add_count
            vip_feed_pkg.pay_status = 'finished'
            vip_feed_pkg.feed_end_time = user_vip.expire_time

        vip_feed_pkg.save()
        return vip_feed_pkg

    def update_vip_point(self, user_vip, admin=False):
        if user_vip.vip_role.auto_active or admin:
            point_utils.vip_point(user_vip.user, vip_user=user_vip)

    def update_self_point(self, user_vip):
        user = user_vip.user
        point_utils.self_service_point(user, user_vip)

    def is_can_buy_self_service(self, user, vip_role_level):
        '''
        之前的逻辑是低等级套餐只能升级，
        现在逻辑改成可以购买重复的套餐
        '''
        return True

    def update_vip_perms(self, user_vip, admin=False):
        if user_vip.vip_role.auto_active or admin:
            user = user_vip.user
            taocv_perm = get_object_or_none(
                Permission,
                codename='visit_taocv',
            )
            feed_perm = get_object_or_none(
                Permission,
                codename='visit_feed',
            )
            user.user_permissions.add(taocv_perm, feed_perm)
            return True
        return False

    def delete_service(self):
        pass

    def close_service(self):
        return self.change_service_status(
            status='closed'
        )

    def cancel_service(self):
        return self.change_service_status(
            status='applying'
        )


class SelfServiceUtils(object):

    @classmethod
    def active_experience_service(self, user):
        experience_service = VipRoleUtils.get_experience_vip()
        if not experience_service:
            return False

        srv_meta = {
            'service_name': 'self_service',
            'product': experience_service,
            'user': user,
        }
        experience_srv = SelfService(**srv_meta)
        srv = experience_srv.create_service()
        ret = experience_srv.active_service() if srv else False
        return ret

    @classmethod
    def get_current_active_service(cls, user):
        current_active_service = UserVip.objects.select_related(
            'vip_role',
        ).filter(
            user=user,
            is_active=True
        )
        if current_active_service:
            return current_active_service[0]
        else:
            return None

    @classmethod
    def pinbot_vip(cls, user):
        now = datetime.datetime.now()
        pinbot_vip_query = UserVip.objects.filter(
            is_active=True,
            expire_time__gt=now,
            user=user,
        ).exclude(
            vip_role__code_name='experience_user',
        )
        if not pinbot_vip_query:
            return False

        pinbot_vip = pinbot_vip_query[0]
        return pinbot_vip

    @classmethod
    @transaction.atomic
    def set_experience_user(cls, user):
        '''
        将用户设置成体验用户
        如果用户有正在使用的自助套餐，将正在使用的自助套餐失效，将用户设置成体验用户
        '''

        # 失效用户当前正在使用的套餐
        user_vip_query = UserVip.objects.select_related(
            'user',
            'vip_role',
        ).filter(
            user=user,
            is_active=True,
        ).exclude(
            vip_role__code_name='experience_user',
        )

        if user_vip_query:
            user_vip = user_vip_query[0]
            user_vip.custom_feed = 0
            user_vip.custom_point = 0
            user_vip.is_active = False
            user_vip.save()
            point_utils.deduction_self_point(user, user_vip)

        PackageUtils.expire_uservip_package(user)

        # 体验用户生效
        experience_vip_query = UserVip.objects.select_related(
            'user',
            'vip_role',
        ).filter(
            vip_role__code_name='experience_user',
            user=user,
        )
        if experience_vip_query:
            experience_vip = experience_vip_query[0]
        else:
            experience_service = VipRoleUtils.get_experience_vip()
            experience_vip = UserVip(
                user=user,
                vip_role=experience_service,
                apply_status='success',
            )

        experience_vip.is_active = True
        experience_vip.expire_time
        experience_vip.expire_time += relativedelta(
            months=3
        )
        experience_vip.custom_feed = 0
        experience_vip.custom_point = 0
        experience_vip.save()
        PackageUtils.set_uservip_pkg_feed(experience_vip)

        return experience_vip
