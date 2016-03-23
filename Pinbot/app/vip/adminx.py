# coding: utf-8

import xadmin

from .models import (
    VipRoleSetting,
    UserVip,
    UserOrder,
    WithdrawRecord,
    PackageItem,
    PinbotPoint,
    Coin,
    ItemRecord,
    UserManualService
)
from service_utils import (
    ServiceUtils
)


class VipRoleSettingAdmin(object):

    list_display = (
        'vip_name',
        'code_name',
        'feed_count',
        'pinbot_point',
        'price',
        'service_time',
        'allow_apply',
        'auto_active',
        'attract_info',
        'level',
        'agreement',
        'index',
    )


class UserVipAdmin(object):

    list_display = (
        'user',
        'vip_role',
        'custom_point',
        'custom_feed',
        'is_active',
        'create_time',
        'active_time',
        'expire_time',
        'apply_vip_user',
        'disable_vip_user',
        'admin_order_page',
    )

    list_select_related = (
        'user',
        'vip_role',
    )

    list_editable = (
        'expire_time',
    )

    list_filter = (
        'user',
        'vip_role',
        'is_active',
        'has_sign',
        'active_time',
    )
    search_fields = (
        'user__username',
    )


class UserOrderAdmin(object):

    list_display = (
        'order_id',
        'order_type',
        'order_desc',
        'user',
        'order_price',
        'actual_price',
        'create_time',
        'pay_time',
        'payment_terms',
        'order_status',
        'offline_pay',
        'refund',
    )

    list_editable = (
        'order_price',
    )

    list_filter = (
        'user',
        'order_id',
        'item_content_type',
        'create_time',
        'pay_time',
        'payment_terms',
        'order_status',
    )

    search_fields = (
        'order_id',
        'user__username',
    )


class WithdrawRecordAdmin(object):

    list_display = (
        'user',
        'create_time',
        'verify_time',
        'current_coin',
        'money',
        'verify_status',
        'verify_remark',
        'operation',
    )

    list_filter = (
        'user',
        'verify_status',
        'create_time',
    )

    list_editable = (
        'verify_remark',
    )
    search_fields = (
        'user__username',
    )


class PackageItemAdmin(object):

    list_display = (
        'product_name',
        'code_name',
        'price',
        'status',
        'salary_range',
        'service_month',
        'candidate_num',
        'desc',
        'is_commend'
    )


class PinbotPointAdmin(object):

    list_display = (
        'product_name',
        'code_name',
        'price',
        'status',
        'desc',
    )


class CoinAdmin(object):

    list_display = (
        'product_name',
        'code_name',
        'price',
        'status',
        'desc',
    )


class ItemRecordAdmin(object):

    list_display = (
        'order',
        'total_price',
        'item',
        'num',
    )


class UserManualServiceAdmin(object):

    def item_desc(self, instance):
        return instance.item.get_desc
    item_desc.short_description = '套餐配置'

    def order_pay_fee(self, instance):
        order = ServiceUtils.get_service_order(
            service=instance
        )
        return order.order_price
    order_pay_fee.short_description = '套餐支付金额'

    list_display = (
        'user',
        'item_desc',
        'order_pay_fee',
        'create_time',
        'active_time',
        'expire_time',
        'is_active',
        'has_sign',
        'is_insurance',
        'status',
        'apply_vip_user',
        'refund',
        'finished',
        'invalid',
    )
    list_editable = (
        'has_sign',
        'active_time',
        'expire_time',
    )

    list_filter = (
        'user',
        'is_active',
        'has_sign',
        'active_time',
        'expire_time',
    )

    search_fields = (
        'user__username',
    )

xadmin.site.register(UserOrder, UserOrderAdmin)
xadmin.site.register(UserVip, UserVipAdmin)
xadmin.site.register(UserManualService, UserManualServiceAdmin)
xadmin.site.register(WithdrawRecord, WithdrawRecordAdmin)
xadmin.site.register(ItemRecord, ItemRecordAdmin)
xadmin.site.register(VipRoleSetting, VipRoleSettingAdmin)
xadmin.site.register(PackageItem, PackageItemAdmin)
xadmin.site.register(PinbotPoint, PinbotPointAdmin)
xadmin.site.register(Coin, CoinAdmin)
