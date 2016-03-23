# coding: utf-8

import datetime

from functools import partial

from django.db.models import Sum
from django.db import transaction

from .models import (
    PinbotPoint,
    PointRecord,
    PointRule,
    CoinRecord,
)
from transaction.models import (
    UserChargePackage
)

from pin_utils.django_utils import (
    get_object_or_none,
    get_monday,
    get_previous_monday,
    get_next_monday,
    get_int,
)


class PointUtils(object):
    '''
    聘点工具类
    function:
        add_point
        add_rule_point
        code_name
        add_pkg_point
        consume_download_point

    规约:
        success, add_point: 成功
        over_total_max, 0: 超过最大加点数
        over_today_max, 0: 超过今天最大加点数
        poor_point, 0: 点数不够
    '''
    RECORD_TYPE_META = {
        'download_resume': {
            'record_type': 'download_resume',
            'detail': u'下载简历',
        },
        'send_company_card': {
            'record_type': 'send_company_card',
            'detail': u'发送企业名片',
        }
    }

    def _get_pinbot_point(self, user):

        pinbot_point = get_object_or_none(
            PinbotPoint,
            user=user,
        )
        if not pinbot_point:
            pinbot_point = PinbotPoint(
                user=user,
            )
            pinbot_point.save()
        return pinbot_point

    def _get_user_package(self, user):
        now = datetime.datetime.now()
        user_pkgs = UserChargePackage.objects.filter(
            user=user,
            package_type=1,
            resume_end_time__gt=now,
            pay_status='finished',
        )
        return user_pkgs

    def get_user_point(self, user):
        now = datetime.datetime.now()
        pinbot_point = self._get_pinbot_point(user)
        user_pkgs = UserChargePackage.objects.filter(
            user=user,
            package_type=1,
            resume_end_time__gt=now,
            pay_status='finished',
        ).aggregate(
            total_rest_point=Sum('rest_points'),
            total_re_point=Sum('re_points'),
        )
        if not user_pkgs:
            pkg_point = 0
        else:
            total_rest_point = user_pkgs['total_rest_point'] or 0
            total_re_point = user_pkgs['total_re_point'] or 0
            pkg_point = total_rest_point + total_re_point
        return pkg_point, pinbot_point.point

    def consume_point(self, user, point, record_type):
        record_type_meta = self.RECORD_TYPE_META[record_type]
        record_type = record_type_meta['record_type']
        detail = record_type_meta['detail']
        pinbot_point = self._get_pinbot_point(user)
        consume_point = - abs(point)

        pkg_point, point = self.get_user_point(user)

        if pkg_point + point + consume_point < 0:
            return 'poor_point', 0

        user_pkgs = self._get_user_package(user)
        with transaction.atomic():
            need_point = consume_point
            for pkg in user_pkgs:
                rest_points, re_points = pkg.rest_points, pkg.re_points
                if rest_points + re_points < 0:
                    continue
                if rest_points + need_point >= 0:
                    pkg.rest_points += need_point
                    need_point = 0
                elif rest_points + need_point < 0 and rest_points + re_points + need_point >= 0:
                    need_point += rest_points
                    pkg.rest_points = 0
                    pkg.re_points += need_point
                    need_point = 0
                elif rest_points + re_points + need_point < 0:
                    need_point += (rest_points + re_points)
                    pkg.rest_points = 0
                    pkg.re_points = 0
                pkg.save()

            if need_point < 0:
                pinbot_point.point += need_point

            point_record = PointRecord(
                user=user,
                point=consume_point,
                record_type=record_type,
                detail=detail,
            )

            point_record.save()
            pinbot_point.save()
            return 'success', consume_point

    def consume_download_point(self, user, point=10):
        return self.consume_point(user, point, 'download_resume')

    def send_card_point(self, user, point=3):
        return self.consume_point(user, point, 'send_company_card')

    def add_point(self, user, point, record_type, detail, point_rule=''):
        pinbot_point = self._get_pinbot_point(user)

        with transaction.atomic():
            pinbot_point.point += point
            point_record = PointRecord(
                user=user,
                point=point,
                record_type=record_type,
                detail=detail,
                point_rule=point_rule,
            )
            pinbot_point.save()
            point_record.save()
            return 'success', point

    def _over_today_max_point(self, user, rule):
        return False

    def _over_total_max_point(self, user, rule):
        total_max_point = rule.total_max_point

        total_record = PointRecord.objects.filter(
            point_rule=rule.point_rule,
            user=user,
        ).aggregate(total_max_point=Sum('point'))

        total_max = total_record['total_max_point']
        if rule.rule_type == 'add':
            return True if total_max and total_max >= total_max_point else False
        else:
            return True if total_max and total_max <= total_max_point else False

    def add_rule_point(self, rule, user, *args, **kwargs):
        # 0 代表没有最大数限制
        if rule.total_max_point != 0 and self._over_total_max_point(user, rule):
            return 'over_total_max', 0

        point_rule = rule.point_rule
        detail = rule.description
        record_type = rule.record_type

        try:
            over_max = getattr(self, '_%s_over_max' % point_rule)(user, *args, **kwargs)
            if over_max:
                return 'over_total_max', 0
        except AssertionError:
            pass

        try:
            point = getattr(self, '_get_%s_point' % point_rule)(user, *args, **kwargs)
        except AssertionError:
            point = rule.point

        if not point:
            return 'not_add', 0

        point_result, point = self.add_point(
            user,
            point,
            record_type,
            detail,
            point_rule,
        )
        return point_result, point

    def __getattr__(self, point_rule):
        rule = get_object_or_none(
            PointRule,
            point_rule=point_rule,
        )
        assert rule, 'not found point rule'
        apply_rule_point = partial(self.add_rule_point, rule)
        return apply_rule_point

    def get_total_point(self, user, record_type):
        aggregate_record = PointRecord.objects.filter(
            user=user,
            record_type=record_type,
        ).aggregate(
            total_point=Sum('point'),
        )
        total_point = aggregate_record.get('total_point', 0)
        return total_point

    def get_user_pinbot_point(self, user):
        aggregate_record = PointRecord.objects.raw(
            '''
            SELECT
            `pinbot_point_pointrecord`.`id`,
            SUM(
            CASE WHEN `pinbot_point_pointrecord`.`record_type` = 'partner' AND `pinbot_point_pointrecord`.`point` > 0 THEN `pinbot_point_pointrecord`.`point` ELSE 0 END) AS `partner_point`,
            SUM(
            CASE WHEN `pinbot_point_pointrecord`.`record_type` = 'promotion' AND `pinbot_point_pointrecord`.`point` > 0 THEN `pinbot_point_pointrecord`.`point` ELSE 0 END) AS `promotion_point`,
            SUM(
            CASE WHEN `pinbot_point_pointrecord`.`record_type` = 'accu_return_point' AND `pinbot_point_pointrecord`.`point` > 0 THEN `pinbot_point_pointrecord`.`point` ELSE 0 END) AS `return_point`,
            SUM(
            CASE WHEN `pinbot_point_pointrecord`.`record_type` IN ('download_resume', 'send_company_card') THEN `pinbot_point_pointrecord`.`point` ELSE 0 END) AS `consume_point`,
            SUM(`pinbot_point_pointrecord`.`point`) AS `total_point`
            FROM `pinbot_point_pointrecord`
            WHERE `user_id` = %s
            ''' % user.id
        )[0]
        return aggregate_record

    def _vip_point_over_max(self, user, *args, **kwargs):
        vip_user = kwargs.get('vip_user')
        role_point = vip_user.vip_role.pinbot_point if not vip_user.custom_point else vip_user.custom_point
        pinbot_point = self._get_pinbot_point(user)
        return True if pinbot_point.point >= role_point else False

    def _get_vip_point_point(self, user, *args, **kwargs):
        vip_user = kwargs.get('vip_user')
        role_point = vip_user.custom_point
        pinbot_point = self._get_pinbot_point(user)
        if pinbot_point.point >= role_point:
            return 0
        return role_point - pinbot_point.point

    def _week_point_over_max(self, user, *args, **kwargs):
        has_grant = user.pointrecord_set.filter(
            record_time__gte=get_monday(),
            record_time__lt=get_next_monday(),
            point_rule='week_point',
        ).exists()
        return True if has_grant else False

    def _get_week_point_point(self, user, *args, **kwargs):
        '''
        每周给用户添加聘点
        每周一凌晨会给用户添加上一周使用的聘点
        添加逻辑

        计算出用户上一周消费的聘点（下载，企业名片发送和返点）
        消费聘点大于每周配置聘点则给用户反每周配置聘点
        消费聘点小于每周配置聘点则给用户返回消费聘点
        '''
        vip_user = kwargs.get('vip_user')
        role_point = vip_user.custom_point
        aggregate_record = user.pointrecord_set.filter(
            record_time__gte=get_previous_monday(),
            record_time__lt=get_monday(),
            record_type__in=['download_resume', 'accu_return_point', 'send_company_card'],
        ).aggregate(
            download_point=Sum('point'),
        )
        download_points = abs(get_int(aggregate_record.get('download_point', 0) or 0))

        if download_points >= role_point:
            return role_point

        return download_points

    def self_service_point(self, user, uservip):
        point = uservip.vip_role.pinbot_point
        if not point:
            return 'not_add', 0

        vip_name = uservip.vip_role.vip_name
        record_type = 'self_service_point'
        detail = '购买{0}添加聘点'.format(vip_name)
        point_rule = 'self_service_point'
        return self.add_point(user, point, record_type, detail, point_rule)

    def deduction_self_point(self, user, uservip):
        active_time = uservip.active_time
        expire_time = uservip.expire_time
        uservip_point = uservip.vip_role.pinbot_point

        record_type_list = (
            'download_resume',
            'accu_return_point',
            'send_company_card',
        )

        aggregate_record = user.pointrecord_set.filter(
            record_time__gte=active_time,
            record_time__lt=expire_time,
            record_type__in=record_type_list,
        ).aggregate(
            rest_point=Sum('point'),
        )
        download_point = get_int(aggregate_record.get('rest_point', 0) or 0)
        rest_point = download_point + uservip_point

        if rest_point <= 0:
            return 'not_add', 0

        pinbot_point = self._get_pinbot_point(user)
        current_point = pinbot_point.point

        rest_point = current_point if rest_point >= current_point else rest_point

        vip_name = uservip.vip_role.vip_name
        deduction_point = -rest_point
        record_type = 'deduction_self_point'
        detail = '{0}到期扣除聘点'.format(vip_name)
        point_rule = 'deduction_self_point'
        return self.add_point(user, deduction_point, record_type, detail, point_rule)


class WalletUtils(object):

    def __init__(self, classify=0):
        self.classify = classify

    def _get_pinbot_point(self, user):
        pinbot_point = get_object_or_none(
            PinbotPoint,
            user=user,
        )
        if not pinbot_point:
            pinbot_point = PinbotPoint(
                user=user,
            )
            pinbot_point.save()
        return pinbot_point

    def add_point(self, user, point, record_type, detail, point_rule=''):
        '''
        需要继承重写

        聘点实现的样例
        pinbot_point = self._get_pinbot_point(user)

        with transaction.atomic():
            pinbot_point.point += point
            point_record = PointRecord(
                user=user,
                point=point,
                record_type=record_type,
                detail=detail,
                point_rule=point_rule,
            )
            pinbot_point.save()
            point_record.save()
            return 'success', point
        '''
        return 'success', 0

    def _over_total_max_point(user, rule):
        '''
        需要继承重写

        聘点实现样例
        total_max_point = rule.total_max_point

        total_record = PointRecord.objects.filter(
            point_rule=rule.point_rule,
            user=user,
        ).aggregate(total_max_point=Sum('point'))

        total_max = total_record['total_max_point']
        if rule.rule_type == 'add':
            return True if total_max and total_max >= total_max_point else False
        else:
            return True if total_max and total_max <= total_max_point else False
        '''
        return False

    def add_rule_point(self, rule, user, *args, **kwargs):
        # 0 代表没有最大数限制
        if rule.total_max_point != 0 and self._over_total_max_point(user, rule):
            return 'over_total_max', 0

        point_rule = rule.point_rule
        detail = rule.description
        record_type = rule.record_type

        # 如果有自定义最大点数方法，使用自定义方法判断
        if hasattr(self, '_%s_over_max' % point_rule):
            over_max = getattr(self, '_%s_over_max' % point_rule)(user, *args, **kwargs)

            if over_max:
                return 'over_total_max', 0

        # 如果有自定义获得点数方法，使用自定义方法
        if hasattr(self, '_get_%s_point' % point_rule):
            point = getattr(self, '_get_%s_point' % point_rule)(user, *args, **kwargs)
        else:
            point = rule.point

        if not point:
            return 'not_add', 0

        point_result, point = self.add_point(
            user,
            point,
            record_type,
            detail,
            point_rule,
        )
        return point_result, point

    def __getattr__(self, point_rule):

        rule = get_object_or_none(
            PointRule,
            point_rule=point_rule,
            rule_classify=self.classify,
        )
        if not rule:
            return super(WalletUtils, self).__getattribute__(point_rule)

        apply_rule_point = partial(self.add_rule_point, rule)
        return apply_rule_point


class CoinUtils(WalletUtils):

    def _over_total_max_point(self, user, rule):
        total_max_point = rule.total_max_point

        total_record = CoinRecord.objects.filter(
            point_rule=rule.point_rule,
            user=user,
        ).aggregate(total_max_point=Sum('coin'))

        total_max = total_record['total_max_point']
        if rule.rule_type == 'add':
            return True if total_max and total_max >= total_max_point else False
        else:
            return True if total_max and total_max <= total_max_point else False

    def add_point(self, user, point, record_type, detail, point_rule=''):
        pinbot_point = self._get_pinbot_point(user)

        pinbot_point.coin += point
        coin_record = CoinRecord(
            user=user,
            coin=point,
            record_type=record_type,
            desc=detail,
            point_rule=point_rule,
        )
        pinbot_point.save()
        coin_record.save()
        return 'success', point

    def get_coin_statistic(self, user):
        aggregate_record = PointRecord.objects.raw(
            '''
            SELECT
            `pinbot_point_coinrecord`.`id`,
            SUM(
            CASE WHEN `pinbot_point_coinrecord`.`record_type` = 'partner' THEN `pinbot_point_coinrecord`.`coin` ELSE 0 END) AS `partner_coin`,
            SUM(
            CASE WHEN `pinbot_point_coinrecord`.`record_type` = 'promotion' AND `pinbot_point_coinrecord`.`coin` > 0 THEN `pinbot_point_coinrecord`.`coin` ELSE 0 END) AS `promotion_coin`,
            SUM(
            CASE WHEN `pinbot_point_coinrecord`.`record_type` = 'withdraw' THEN `pinbot_point_coinrecord`.`coin` ELSE 0 END) AS `consume_coin`,
            SUM(`pinbot_point_coinrecord`.`coin`) AS `total_coin`
            FROM `pinbot_point_coinrecord`
            WHERE `user_id` = %s
            ''' % user.id
        )[0]
        return aggregate_record

    def __generic_partner_over_max(self, user, *args, **kwargs):
        accept_task = kwargs.get('accept_task')
        resume = kwargs.get('resume')
        record_type = kwargs.get('record_type')
        has_grant = accept_task.task_coin_records.filter(
            upload_resume=resume,
            record_type=record_type,
        )
        return True if has_grant else False

    def _check_resume_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _download_resume_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _interview_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _taking_work_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _accusation_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _extra_download_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _extra_interview_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _extra_taking_work_over_max(self, user, *args, **kwargs):
        return self.__generic_partner_over_max(user, *args, **kwargs)

    def _get_accusation_point(self, user, *args, **kwargs):
        accept_task = kwargs.get('accept_task')
        resume = kwargs.get('resume')
        total_coin_record = accept_task.task_coin_records.filter(
            upload_resume=resume,
        ).aggregate(Sum('coin'))

        total_coin = total_coin_record['coin__sum'] or 0
        return -total_coin if total_coin > 0 else 0

    def _get_taking_work_point(self, user, *args, **kwargs):
        coin = kwargs.get('coin', 0)
        return coin if coin > 0 else 0

    def _get_extra_taking_work_point(self, user, *args, **kwargs):
        coin = kwargs.get('coin', 0)
        return coin if coin > 0 else 0

    def _get_extra_download_point(self, user, *args, **kwargs):
        coin = kwargs.get('coin', 0)
        return coin if coin > 0 else 0

    def _get_extra_interview_point(self, user, *args, **kwargs):
        coin = kwargs.get('coin', 0)
        return coin if coin > 0 else 0

    def withdraw_coin(self, user, coin):
        pinbot_point = self._get_pinbot_point(user)

        coin = - abs(coin)
        pinbot_point.coin += coin
        coin_record = CoinRecord(
            user=user,
            coin=coin,
            record_type='withdraw',
            desc='金币提现',
        )
        pinbot_point.save()
        coin_record.save()
        return 'success', coin


point_utils = PointUtils()
coin_utils = CoinUtils(1)
