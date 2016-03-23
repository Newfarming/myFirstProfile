# coding: utf-8

import datetime

from django.db.models import Max

from .models import (
    UserVip,
    VipRoleSetting,
    UserOrder,
    Mission,
    WithdrawRecord,
)

from pin_utils.django_utils import (
    get_object_or_none,
)


class VipRoleUtils(object):

    @classmethod
    def get_vip_role(cls, user, role_type):
        role_type_meta = {
            'current_vip': {
                'is_active': True,
            },
            'apply_vip': {
                'apply_status': 'applying',
            },
            'unsign_vip': {
                'apply_status': 'success',
                'is_active': False,
                'has_sign': False,
                'vip_role__agreement': True,
            },
        }
        query_cond = role_type_meta[role_type]
        user_vip_query = UserVip.objects.select_related(
            'vip_role',
        ).filter(
            user=user,
            **query_cond
        ).order_by('-id')
        return user_vip_query[0] if user_vip_query else None

    @classmethod
    def get_current_vip(cls, user):
        return cls.get_vip_role(user, 'current_vip')

    @classmethod
    def get_apply_vip(cls, user):
        return cls.get_vip_role(user, 'apply_vip')

    @classmethod
    def get_highest_vip_level(cls):
        highest_level = VipRoleSetting.objects.all().aggregate(Max('level'))
        return highest_level['level__max']

    @classmethod
    def is_upgrade(cls, user, order):
        apply_count = UserVip.objects.filter(
            apply_status='success',
            user=user,
        ).count()
        if apply_count > 1 and order:
            return True
        if apply_count >= 1 and not order:
            return True
        return False

    @classmethod
    def get_unsign_vip(cls, user):
        return cls.get_vip_role(user, 'unsign_vip')

    @classmethod
    def get_experience_vip(cls):
        vip_role = get_object_or_none(
            VipRoleSetting,
            code_name='experience_user',
        )
        return vip_role


class UserOrderUtils(object):

    @classmethod
    def get_order_by_item(cls, item):
        order = get_object_or_none(
            UserOrder,
            item_object_id=item.id,
        )
        return order


class MissionUtils(object):

    @classmethod
    def start_mission(cls, user, mission_type):
        mission = get_object_or_none(
            Mission,
            user=user,
            mission_type=mission_type,
        )
        if not mission:
            mission = Mission(
                user=user,
                mission_type=mission_type
            )
            mission.save()
        return mission

    @classmethod
    def finish_mission(cls, user, mission_type):
        mission = get_object_or_none(
            Mission,
            user=user,
            mission_type=mission_type,
            mission_status='start'
        )
        if not mission:
            return False

        now = datetime.datetime.now()
        mission.mission_status = 'finish'
        mission.finish_time = now
        mission.save()
        return mission


class WithdrawUtils(object):

    @classmethod
    def get_withdraw_status(cls, user):
        '''
        1. 没有提现记录
        3. 有提现记录，未提现成功
        4. 提现失败
        5. 提现成功
        6. 金币小于等于0
        '''
        pinbot_point = user.pinbotpoint
        if pinbot_point.coin <= 0:
            return {
                'type': 6,
                'coin': pinbot_point.coin,
                'alreadyTakeOut': 0,
                'takeTime': '',
                'reason': '金币不足',
            }

        now = datetime.datetime.now()
        withdraw_record_query = WithdrawRecord.objects.filter(
            user=user,
            create_time__year=now.year,
            create_time__month=now.month,
        ).order_by('-id')

        if not withdraw_record_query:
            return {
                'type': 1,
                'coin': pinbot_point.coin,
            }

        withdraw_record = withdraw_record_query[0]
        if withdraw_record.verify_status == 0:
            return {
                'type': 3,
                'coin': pinbot_point.coin,
                'takeTime': withdraw_record.create_time.strftime('%Y-%m-%d %H:%M'),
                'alreadyTakeOut': withdraw_record.money,
            }

        if withdraw_record.verify_status == 1:
            return {
                'type': 5,
                'coin': pinbot_point.coin,
                'takeTime': withdraw_record.create_time.strftime('%Y-%m-%d %H:%M'),
                'alreadyTakeOut': withdraw_record.money,
            }

        if withdraw_record.verify_status == 2:
            withdraw_record = withdraw_record_query[0]
            return {
                'type': 4,
                'coin': pinbot_point.coin,
                'takeTime': withdraw_record.create_time.strftime('%Y-%m-%d %H:%M'),
                'alreadyTakeOut': withdraw_record.money,
                'reason': withdraw_record.verify_remark,
            }
