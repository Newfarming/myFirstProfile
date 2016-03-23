# coding: utf-8

import datetime
import shortuuid


def create_order_id(length=6):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    uuid = shortuuid.ShortUUID().random(length=length)
    order_id = '%s-%s' % (timestamp, uuid)
    return order_id
