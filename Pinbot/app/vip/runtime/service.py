# coding: utf-8

from app.vip.models import (
    UserManualService,
    UserVip,
)
from pin_utils.django_utils import (
    get_object_or_none
)
from app.pinbot_point.point_utils import (
    CoinUtils
)

service_map_model = {
    'manual_service': UserManualService,
    'self_service': UserVip,
}


class BaseService(object):

    def __init__(self, **data):
        self.data = data
        self.source = data.get('source')
        self.dest = data.get('dest')
        self.event = data.get('event')
        self.service_class = data.get('service_class')
        self.order_id = data.get('order_id')
        self.product = data.get('product')
        self.product_type = data.get('product_type')
        self.item_num = data.get('item_num')
        self.user = data.get('user')
        self.service_id = data.get('service_id')
        self.service_name = data.get('service_name')
        self.payment_terms = data.get('payment_terms')
        self.is_insurance = data.get('is_insurance')
        self.order_price = data.get('order_price')

        if self.dest != self.service_name:
            return False

    def do_str_to_fun(self):
        method_to_call = getattr(self, self.event)
        return method_to_call()

    def change_service_status(self, status):
        model = service_map_model.get(self.service_name)
        service_obj = get_object_or_none(model, id=self.service_id)

        service_obj.status = status
        service_obj.save()
        return True

    def get_service_status(self):
        model = service_map_model.get(self.service_name)
        service_obj = get_object_or_none(model, id=self.service_id)
        return service_obj.status

    def refund_service(self):
        return self.change_service_status(
            status='refund'
        )

    def debit_coin(self, user, coin_num):
        point_utils = CoinUtils()
        point_utils.add_point(
            user=user,
            point=-coin_num,
            record_type='pkg',
            detail='金币购买服务'
        )
        return True

    def process(self, **data):
        return self.do_str_to_fun()

    def close_service(self):
        return True

    def delete_service(self):
        return True

    def cancel_service(self):
        return True
