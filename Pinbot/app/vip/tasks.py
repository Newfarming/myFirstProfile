# coding: utf-8

import datetime
from dateutil.relativedelta import relativedelta

from .models import (
    UserVip,
    UserManualService,
)

from .runtime.self_service import SelfServiceUtils

from app.pinbot_point.point_utils import (
    point_utils
)

from pin_utils.django_utils import (
    get_today,
)
from pin_utils.package_utils import PackageUtils

from pin_celery.celery_app import app


class VipPointTask(object):

    def vip_point_task(self):
        now = datetime.datetime.now()
        manual_srv_list = list(UserManualService.objects.filter(
            is_active=True,
            expire_time__gt=now,
        ).values_list(
            'user_id',
            flat=True,
        ))

        user_vips = UserVip.objects.select_related(
            'user',
            'vip_role',
        ).filter(
            user_id__in=manual_srv_list,
            is_active=True,
            vip_role__code_name='experience_user',
            custom_point__gt=0,
            expire_time__gt=now,
        )
        for user_vip in user_vips:
            point_utils.week_point(user_vip.user, vip_user=user_vip)
        return 'add %s vip point done' % user_vips.count()


class ExpireManualService(object):

    @classmethod
    def expire_manual_service(cls):
        now = datetime.datetime.now()
        update_count = UserManualService.objects.filter(
            expire_time__lt=now,
            is_active=True,
        ).exclude(
            status='finished',
        ).update(
            status='expired',
        )
        return update_count


class ExpireSelfService(object):

    @classmethod
    def expire_self_service(cls):
        now = datetime.datetime.now()

        user_vip_query = UserVip.objects.select_related(
            'user'
        ).filter(
            is_active=True,
            expire_time__lt=now,
        )

        for user_vip in user_vip_query:
            user = user_vip.user
            SelfServiceUtils.set_experience_user(user)

        return user_vip_query.count()


class RenewExperienceUser(object):

    @classmethod
    def renew(cls):
        today = get_today()
        expire_time = today + datetime.timedelta(days=15)

        user_vip_query = UserVip.objects.select_related(
            'user',
        ).filter(
            is_active=True,
            vip_role__code_name='experience_user',
            expire_time__lt=expire_time,
        )

        for user_vip in user_vip_query:
            user_vip.expire_time += relativedelta(
                months=3
            )
            user_vip.save()
            PackageUtils.update_uservip_package(user_vip)

        return user_vip_query.count()


# 自助服务每周添加聘点
point_task = VipPointTask()
asyn_vip_point_task = app.task(
    name='vip-point-task'
)(point_task.vip_point_task)

# 省心服务过期任务
expire_manual_service = app.task(
    name='expire-manual-service'
)(ExpireManualService.expire_manual_service)

# 自助服务过期任务
expire_self_service = app.task(
    name='expire-self-service'
)(ExpireSelfService.expire_self_service)

# 体验用户自动续期
renew_experience_user = app.task(
    name='renew-experience-user'
)(RenewExperienceUser.renew)
