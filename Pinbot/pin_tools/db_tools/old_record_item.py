# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from django.contrib.contenttypes.models import ContentType

from app.vip.models import (
    UserOrder,
    ItemRecord,
    UserVip,
    WithdrawRecord,
)


def main():
    user_orders = UserOrder.objects.filter(
        itemrecord=None,
    )
    uservip_ctype = ContentType.objects.get_for_model(UserVip)
    item_objects = {}
    item_objects[uservip_ctype.id] = UserVip.objects.select_related(
        'vip_role'
    ).in_bulk(
        [i.item_object_id for i in user_orders if i.item_content_type_id == uservip_ctype.id]
    )

    withdraw_ctype = ContentType.objects.get_for_model(WithdrawRecord)
    item_objects[withdraw_ctype.id] = WithdrawRecord.objects.in_bulk(
        [i.item_object_id for i in user_orders if i.item_content_type_id == withdraw_ctype.id]
    )

    bulk_item_records = []
    apply_vip_orders = []
    withdraw_orders = []

    for i in user_orders:
        try:
            item = item_objects[i.item_content_type_id][i.item_object_id]
        except KeyError:
            print 'error item id {0}'.format(i.item_object_id)
            continue
        bulk_item_records.append(
            ItemRecord(
                num=1,
                total_price=i.order_price,
                order=i,
                item=item,
            )
        )
        if i.item_content_type_id == uservip_ctype.id:
            apply_vip_orders.append(i.id)
        if i.item_content_type_id == withdraw_ctype.id:
            withdraw_orders.append(i.id)

    ItemRecord.objects.bulk_create(bulk_item_records)
    UserOrder.objects.filter(
        id__in=withdraw_orders,
    ).update(
        order_desc='提现',
        order_type=5,
    )
    UserOrder.objects.filter(
        id__in=apply_vip_orders,
    ).update(
        order_desc='申请会员',
        order_type=6,
    )
    print 'success'


if __name__ == '__main__':
    main()
