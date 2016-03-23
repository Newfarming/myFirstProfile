# coding: utf-8

import xadmin

from models import (
    PromotionPointRecord,
    PromotionToken,
    PromotionClickRecord,
)


class PromotionPointsRecordAdmin(object):
    list_display = (
        'promotion_user',
        'register_user',
        'point',
        'coin',
        'promotion_date',
    )
    list_filter = (
        'promotion_user',
        'register_user',
    )


class PromotionTokenAdmin(object):
    list_display = (
        'promotion_user',
        'token',
        'create_date',
    )
    list_filter = (
        'promotion_user',
        'token',
    )


class PromotionClickRecordAdmin(object):
    list_display = (
        'user',
        'company',
        'click_times',
        'click_date',
    )
    list_filter = (
        'user',
        'click_date',
    )


xadmin.site.register(PromotionPointRecord, PromotionPointsRecordAdmin)
xadmin.site.register(PromotionToken, PromotionTokenAdmin)
xadmin.site.register(PromotionClickRecord, PromotionClickRecordAdmin)
