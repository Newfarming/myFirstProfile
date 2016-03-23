# coding: utf-8

import xadmin

from models import (
    PinbotPoint,
    PointRecord,
    PointRule,
    CoinRecord,
)


class PinbotPointAdmin(object):
    list_display = (
        'user',
        'point',
        'coin',
    )

    list_filter = (
        'user',
    )


class PointRecordAdmin(object):
    list_display = (
        'user',
        'record_time',
        'record_type',
        'detail',
        'point',
    )

    list_filter = (
        'user',
    )


class PointRuleAdmin(object):
    list_display = (
        'rule_name',
        'point_rule',
        'rule_classify',
        'rule_type',
        'record_type',
        'point',
        'total_max_point',
        'days_max_point',
    )

    list_filter = (
        'rule_type',
        'record_type',
    )


class CoinRecordAdmin(object):

    list_display = (
        'user',
        'record_type',
        'desc',
        'coin',
        'record_time',
        'point_rule',
    )

    list_filter = (
        'user',
    )


xadmin.site.register(PointRule, PointRuleAdmin)
xadmin.site.register(PinbotPoint, PinbotPointAdmin)
xadmin.site.register(PointRecord, PointRecordAdmin)
xadmin.site.register(CoinRecord, CoinRecordAdmin)
