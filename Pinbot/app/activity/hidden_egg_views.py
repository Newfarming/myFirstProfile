# coding: utf-8

import logging
import random
import datetime

from django.views.generic.base import View
from django.core.cache import cache
from django.db import transaction

from notifications import notify

from .models import (
    EasterEgg,
    EggRecord,
    CloseEasterRecord,
)

from app.pinbot_point.point_utils import point_utils
from app.weixin.runtime.weixin_utils import (
    WeixinService,
    WeixinRedPackService
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    StaffRequiredMixin,
    CSRFExemptMixin
)
from pin_utils.django_utils import (
    JsonResponse,
    get_tomorrow,
    get_today,
    get_object_or_none,
    str2bool
)

logger = logging.getLogger('django')


class FindEgg(LoginRequiredMixin, View):

    find_egg_key = 'FIND_EGG_USER_LIST'
    gift_pool_key = 'EGG_GIFT_POOL'
    grant_gift_key = 'EGG_GRANT_GIFT'

    def init_egg(self):
        self.all_easter_egg = list(EasterEgg.objects.filter(is_active=True))
        self.real_gift = [i.code_name for i in self.all_easter_egg if i.egg_type == 2]
        self.weighted_meta = [(i.code_name, i.amount) for i in self.all_easter_egg]
        self.gift_mapper = {i.code_name: i for i in self.all_easter_egg}
        return self.all_easter_egg

    def get_expire_time(self):
        now = datetime.datetime.now()
        tomorrow = get_tomorrow()
        expire_time = (tomorrow - now).total_seconds()
        return expire_time

    def has_find_egg(self):
        username = self.request.user.username
        find_egg_user_list = cache.get(self.find_egg_key, [])
        return True if username in find_egg_user_list else False

    def set_gift_pool(self, gift_pool):
        expire_time = self.get_expire_time()
        cache.set(self.gift_pool_key, gift_pool, expire_time)
        return True

    def set_find_egg_user_cache(self):
        username = self.request.user.username
        find_egg_user_list = cache.get(self.find_egg_key, [])

        find_egg_user_list.append(username)
        expire_time = self.get_expire_time()
        cache.set(self.find_egg_key, find_egg_user_list, expire_time)
        return True

    def send_egg_notify(self, gift):
        user = self.request.user
        gift_name = self.gift_mapper[gift].name

        if gift in ('pinbot_point_10', 'pinot_point_10'):
            verb = '砸彩蛋收获的{0}已赠送到你的账户中（<a class="c0091fa" href="/payment/point_record/">查看详情</a>）。'.format(gift_name)
        elif gift in ('hongbao_1', 'hongbao_3', 'hongbao_5', 'hongbao_8'):
            verb = '恭喜砸中{0}，红包已通过服务号发送。<a class="c0091fa" href="#"> </a>'.format(gift_name)
        else:
            verb = '恭喜砸中{0}，请到（<a class="c0091fa" href="/payment/point_record/">个人设置</a>）中填写收货地址，奖品将在每周五进行统一寄送。'.format(gift_name)

        ret = notify.send(
            user,
            recipient=user,
            verb=verb,
            user_role='hr',
            notify_type='egg_find_point',
        )
        return ret

    def grant_gift(self, gift):
        user = self.request.user
        gift_type = 1 if gift in self.real_gift else 0

        with transaction.atomic():
            record = EggRecord(
                user=user,
                egg=self.gift_mapper[gift]
            )

            # 抽到聘点直接发送给用户, 领奖状态改成已经领奖
            if gift in ('pinbot_point_10', 'pinot_point_10'):
                point_utils.egg_point(user)
                record.claim_status = 2

            # 如果是虚拟奖品，领奖状态改成已经领奖
            if not gift_type:
                record.claim_status = 2

            # 实物奖品添加通知
            if gift_type:
                self.send_egg_notify(gift)

            record.save()
        return record

    def weighted_choice(self, all_gift):
        '''
        reference:
        http://blog.csdn.net/handsomekang/article/details/40542817
        '''
        weighted_choice = [i for i in self.weighted_meta if i[0] in all_gift]
        total = sum(w for _, w in weighted_choice)
        n = random.uniform(0, total)
        for x, w in weighted_choice:
            if n < w:
                break
            n -= w
        return x

    def get_gift(self):
        gift_pool = cache.get(self.gift_pool_key, {})
        if not gift_pool:
            return False

        all_gift = [gift for gift, amount in gift_pool.items() if amount > 0]
        if not all_gift:
            return False

        gift = self.weighted_choice(all_gift)

        # 管理员不给实质奖品
        if gift in self.real_gift and self.request.user.is_staff:
            return False

        if gift in self.real_gift:
            gift_pool[gift] -= 1

        self.set_gift_pool(gift_pool)
        self.set_find_egg_user_cache()
        gift_record = self.grant_gift(gift)
        return gift_record

    def send_redpack(self, gift):
        ret = {
            'status': 'ok',
            'msg': 'ok'
        }
        if not gift:
            ret['status'] = 'ok'
            ret['msg'] = '没有微信红包'
            logger.debug('no redpack')
            return ret

        if not gift.egg.code_name.startswith('hongbao_'):
            ret['status'] = 'ok'
            ret['msg'] = '没有微信红包'
            logger.debug('no redpack')
            return ret

        user = self.request.user
        if not WeixinService.is_bind(user=user):
            ret['status'] = 'unbind'
            ret['msg'] = '您还未绑定微信服务号'

        gift_amount = gift.egg.price

        send_ret = WeixinRedPackService.send_feed_redpack(
            user=user,
            act_name='彩蛋红包',
            total_amount=gift_amount
        )
        if not send_ret:
            ret['status'] = 'redpack_send_fail'
            ret['msg'] = '红包发放失败!'

        ret['msg'] = '红包已经发送至聘宝招聘版服务号!'
        ret['status'] = 'redpack_send_success'
        gift.claim_status = 2
        gift.claim_time = datetime.datetime.now()
        gift.save()

        logger.info(
            'redpack for user: {username}  send status: {ret}'.format(
                username=user.username,
                ret=ret
            )
        )

        return ret

    def get(self, request):
        self.init_egg()

        if self.has_find_egg():
            return JsonResponse({
                'status': 'has_find',
                'msg': 'has_find_egg',
            })

        gift = self.get_gift()
        if not gift:
            return JsonResponse({
                'status': 'no_gift',
                'msg': 'sorry! no more gift',
            })
        # 尝试自动发送微信红包
        ret = self.send_redpack(
            gift=gift
        )

        gift_type = 1 if gift.egg.code_name in self.real_gift else 0
        return JsonResponse({
            'status': ret['status'],
            'msg': ret['msg'],
            'gift': gift.egg.code_name,
            'gift_type': gift_type,
            'gift_id': gift.id
        })


class GetGiftPool(StaffRequiredMixin, View):

    gift_pool_key = 'EGG_GIFT_POOL'

    def get(self, request):
        gift_pool = cache.get(self.gift_pool_key, {})
        return JsonResponse(gift_pool)


class CloseEaster(LoginRequiredMixin, View):

    def get(self, request):
        username = request.user.username
        today = get_today()
        tomorrow = get_tomorrow()

        has_close = CloseEasterRecord.objects.filter(
            username=username,
            close_time__gte=today,
            close_time__lt=tomorrow,
        ).exists()

        if not has_close:
            CloseEasterRecord.objects.create(
                username=username,
            )

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class GiftUserNeed(CSRFExemptMixin, LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        data = request.JSON
        need_status = data.get('need_status')
        gift_id = data.get('gift_id')

        gift_obj = get_object_or_none(EggRecord, id=gift_id, user=user)
        if not gift_obj:
            return JsonResponse({
                'status': 'error',
                'msg': '没找到彩蛋记录',
            })

        need_status = str2bool(need_status)
        gift_obj.user_need = need_status
        gift_obj.save()

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })
