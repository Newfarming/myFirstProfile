# coding: utf-8

from app.pinbot_point.point_utils import (
    CoinUtils
)

from app.vip.runtime.service import (
    BaseService
)


class CoinService(BaseService):

    service_name = 'coin_service'

    def __init__(self, **data):

        super(CoinService, self).__init__(**data)

    def process(self, **data):
        return self.do_str_to_fun()

    def create_service(self):
        return self.product

    def invaild_service(self):
        return True

    def active_service(self):
        coin_utils = CoinUtils()
        coin_utils.add_point(
            user=self.user,
            point=float(self.item_num),
            record_type='pkg',
            detail='金币充值',
        )
        return True
