# coding: utf-8

import datetime

from models import PromotionToken, PromotionPointRecord
from app.pinbot_point.point_utils import (
    coin_utils
)


class PromotionUtils(object):

    @classmethod
    def register_promotion(cls, request, register_user):
        token = request.REQUEST.get('promotion_token', '').strip() or request.JSON.get('promotion_token', '')
        promotion_token_query = PromotionToken.objects.filter(
            token=token
        )

        if not promotion_token_query:
            return False

        promotion_token = promotion_token_query[0]
        promotion_record = PromotionPointRecord(
            register_user=register_user,
            promotion_user=promotion_token.promotion_user,
        )
        promotion_record.save()
        return promotion_record

    @classmethod
    def promotion_success(cls, register_user):
        '''
        用户推广注册成功
        '''
        promotion_record_query = PromotionPointRecord.objects.select_related(
            'promotion_user',
        ).filter(
            register_user=register_user,
            verify_status=0,
        )

        if not promotion_record_query:
            return False

        promotion_record = promotion_record_query[0]
        promotion_user = promotion_record.promotion_user
        now = datetime.datetime.now()

        # 注册用户奖励金币
        coin_utils.promotion(register_user)
        # 推广用户奖励金币
        _, coin = coin_utils.promotion(promotion_user)

        if coin > 0:
            promotion_record.verify_status = 1
            promotion_record.coin = coin
        else:
            promotion_record.verify_status = 2

        promotion_record.promotion_date = now
        promotion_record.save()
        return promotion_record
