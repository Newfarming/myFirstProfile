# coding: utf-8

from dateutil.relativedelta import relativedelta

from .service import BaseService
from ..models import RenewRecord

from pin_utils.package_utils import PackageUtils


class RenewService(BaseService):
    '''
    自助服务续期服务
    '''

    service_name = 'renew_service'

    def __init__(self, *args, **kwargs):
        super(RenewService, self).__init__(*args, **kwargs)
        self.user_vip = kwargs.get('user_vip')
        self.service = self.product
        self.duration = kwargs.get('duration')
        self.price = kwargs.get('price')

    def create_service(self):
        self.service = RenewRecord.objects.create(
            user_vip=self.user_vip,
            duration=self.duration,
            price=self.price,
        )
        return self.service

    def renew_user_vip(self):
        self.user_vip = self.service.user_vip
        self.user_vip.total_price += self.service.price
        self.user_vip.expire_time += relativedelta(
            months=self.service.duration
        )
        self.user_vip.save()
        return self.user_vip

    def active_service(self):
        self.renew_user_vip()
        PackageUtils.update_uservip_package(self.user_vip)
        return self.service
