# coding: utf-8

from app.vip.runtime.service import (
    BaseService
)
from app.pinbot_point.point_utils import (
    PointUtils
)


class PinbotPointService(BaseService):

    service_name = 'pinbot_point_service'

    def __init__(self, **data):

        super(PinbotPointService, self).__init__(**data)

    def process(self, **data):
        return self.do_str_to_fun()

    def create_service(self):
        return self.product

    def invaild_service(self):
        return True

    def active_service(self):
        point_utils = PointUtils()
        # 金币兑换
        if self.payment_terms == 'coin':
            self.debit_coin(self.user, int(self.order_price))

        point_utils.add_point(
            user=self.user,
            point=self.product.num,
            record_type='pkg',
            detail='聘点充值',
        )
        return True
