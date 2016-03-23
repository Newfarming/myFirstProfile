# coding: utf-8

import sys

import datetime
from django.db import transaction

from ..models import (
    UserOrder,
    PackageItem,
    Coin,
    PinbotPoint,
    ItemRecord,
    VipRoleSetting,
    RenewRecord,
)
from pin_utils.order_utils import (
    create_order_id,
)
from pin_utils.django_utils import (
    get_object_or_none,
    str2bool
)
from app.pinbot_point.point_utils import (
    PointUtils
)
from . import (
    self_service,
    manual_service,
    coin,
    pinbot_point,
    renew_service,
)

ORDER_TYPE_MAP = {
    'self_service': 1,
    'manual_service': 2,
    'pinbot_point': 3,
    'coin': 4,
    'withdraw': 5,
    'renew_service': 7,
}

order_schema = {
    'service_list':
    {
        'self_service':
        {
            'dest': 'self_service',
            'class': self_service.SelfService,
            'order_events': {
                'create_order': 'create_service',
                'paid_order': 'active_service',
                'refund_order': '',
                'confirm_refund_order': '',
                'cancel_refund_order': '',
                'close_order': 'close_service',
                'delete_order': 'delete_service',
                'cancel_order': 'cancel_service'
            }
        },
        'manual_service':
        {
            'dest': 'self_service',
            'class': manual_service.ManualService,
            'order_events': {
                'create_order': 'create_service',
                'paid_order': 'active_service',
                'refund_order': 'refund_service',
                'confirm_refund_order': 'invalid_service',
                'cancel_refund_order': 'cancel_refund_service',
                'close_order': 'close_service',
                'delete_order': 'delete_service',
                'cancel_order': 'cancel_service'
            }
        },
        'coin':
        {
            'dest': 'coin_service',
            'class': coin.CoinService,
            'order_events': {
                'create_order': 'create_service',
                'paid_order': 'active_service',
                'refund_order': '',
                'confirm_refund_order': '',
                'cancel_refund_order': '',
                'close_order': '',
                'delete_order': '',
                'cancel_order': ''
            }
        },
        'pinbot_point':
        {
            'dest': 'pinbot_point_service',
            'class': pinbot_point.PinbotPointService,
            'order_events': {
                'create_order': 'create_service',
                'paid_order': 'active_service',
                'refund_order': '',
                'confirm_refund_order': '',
                'cancel_refund_order': '',
                'close_order': '',
                'delete_order': '',
                'cancel_order': ''
            }
        },
        'renew_service':
        {
            'dest': 'renew_service',
            'class': renew_service.RenewService,
            'order_events': {
                'create_renew_order': 'create_service',
                'paid_order': 'active_service',
                'refund_order': '',
                'confirm_refund_order': '',
                'cancel_refund_order': '',
                'close_order': 'close_service',
                'delete_order': 'delete_service',
                'cancel_order': 'cancel_service'
            }
        },
    },
    'source': 'order',
    'version': 1.0
}


class OrderManage(object):

    @classmethod
    def get_refund_info(self, service_id):
        ms = manual_service.ManualService()
        service = ms.get_service_info(
            service_id=service_id
        )
        service_price = service.item.price
        refund_rule = {
            'month1': {
                'refund_fee': 0,
                'refund_percent': '0%',
                'service_months': 1
            },
            'month2': {
                'refund_fee': service_price * 0.6,
                'refund_percent': '60%',
                'service_months': 2
            },
            'month3': {
                'refund_fee': service_price * 0.4,
                'refund_percent': '40%',
                'service_months': 3
            }
        }

        active_time = service.active_time
        now = datetime.datetime.now()
        service_diff_days = (now - active_time).days

        if service_diff_days <= 30:
            return refund_rule['month1']
        if service_diff_days > 30 and service_diff_days <= 60:
            return refund_rule['month2']
        if service_diff_days > 60 and service_diff_days <= 100:
            return refund_rule['month3']

        return None

    @classmethod
    def get_normal_item_price(self, product, user, order_price, is_insurance):
        if is_insurance:
            insurance_price = int(product.candidate_num) * 500
            order_price += insurance_price
        return order_price

    @classmethod
    def get_order_price(self, user, product, num, is_insurance):
        # 金币数据单独处理
        if product.get_product_type != 'coin':

            order_price = self.get_normal_item_price(
                product=product,
                order_price=product.price,
                is_insurance=is_insurance,
                user=user
            )
            return order_price

        num = int(num)
        order_price = 0
        product_price = product.price

        if (isinstance(product_price, (int, long, float, complex)) and
                product_price > 0 and
                num > 0):
            order_price = product_price * num

        return order_price

    @classmethod
    def create_protcol_data(self, **kwargs):
        service_name = kwargs.get('service_name')
        event = kwargs.get('event')
        protcol_data = {
            'source': 'order',
            'dest': kwargs.get('service_name'),
            'service_class': order_schema['service_list'][service_name]['class'],
            'event': order_schema['service_list'][service_name]['order_events'][event],
            'order_id': kwargs.get('order_id'),
            'product': kwargs.get('product'),
            'product_type': kwargs.get('product_type'),
            'item_num': kwargs.get('item_num'),
            'user': kwargs.get('user'),
            'service_id': kwargs.get('service_id'),
            'service_name': kwargs.get('service_name'),
            'payment_terms': kwargs.get('payment_terms'),
            'is_insurance': kwargs.get('is_insurance'),
            'order_price': kwargs.get('order_price')

        }
        return protcol_data

    @classmethod
    def get_item_record_by_order(self, order_id):

        item_record = ItemRecord.objects.filter(
            order__order_id=order_id
        ).first()
        return item_record

    @classmethod
    def before_create_order(self, user, product, product_type, num):

        # 省心用户不能购买自助服务
        if product_type == 'self_service':
            manual_srv = manual_service.ManualService()
            has_manual_service = manual_srv.has_active_service(
                user=user
            )
            if has_manual_service:
                return False

        # 成为自助会员才能购买聘点
        if product_type == 'pinbot_point':
            pinbot_vip = self_service.SelfServiceUtils.pinbot_vip(user)
            if not pinbot_vip:
                return False
        return True

    @classmethod
    def after_create_order(self, user, order, service, num):
        self.add_item_record(
            item=service,
            order_id=order.order_id,
            num=num,
            total_price=order.order_price
        )

    @classmethod
    def after_paid_order(self, user, order, service, num):
        pass

    @classmethod
    @transaction.atomic
    def create_order(self, user, pid, product_type, num, payment_terms, is_insurance=None):
        is_insurance = str2bool(str(is_insurance))

        product = self.get_product_object(
            pid=pid,
            product_type=product_type,
        )

        if not self.before_create_order(
            user=user,
            product_type=product_type,
            product=product,
            num=num
        ):
            return False

        if product.status != 'enable':
            return False

        order_price = self.get_order_price(
            product=product,
            num=num,
            is_insurance=is_insurance,
            user=user
        )
        order_type = ORDER_TYPE_MAP.get(product_type)

        order = UserOrder.objects.create(
            user=user,
            order_price=order_price,
            actual_price=order_price,
            item=product,
            payment_terms=payment_terms,
            order_desc=product.get_desc,
            is_insurance=is_insurance,
            order_type=order_type
        )

        order.order_id = create_order_id()
        order.save()

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event=sys._getframe().f_code.co_name,
            dest=product_type,
            order_id=order.order_id,
            product=product,
            product_type=product_type,
            item_num=num,
            user=user,
            is_insurance=is_insurance,
            order_price=order_price
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.process()

        self.after_create_order(
            user=user,
            order=order,
            service=service_result,
            num=num
        )
        return order

    @classmethod
    @transaction.atomic
    def create_renew_order(cls, user_vip, renew_month):

        user = user_vip.user
        vip_role = user_vip.vip_role
        order_price = user_vip.vip_role.month_price * renew_month
        num = 1
        order_desc = '{vip_name}, 续期{renew_month}个月, {feed_count}个定制, {pinbot_point}聘点/周'.format(
            vip_name=vip_role.vip_name,
            renew_month=renew_month,
            feed_count=vip_role.feed_count,
            pinbot_point=vip_role.pinbot_point,
        )

        protcol_data = cls.create_protcol_data(
            service_name='renew_service',
            event='create_renew_order',
            dest='renew_service',
            product=None,
            product_type='renew_service',
            item_num=num,
            user=user,
            is_insurance=False,
            order_price=order_price,
        )
        protcol_data['duration'] = renew_month
        protcol_data['price'] = order_price
        protcol_data['user_vip'] = user_vip

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.create_service()

        order = UserOrder.objects.create(
            user=user,
            order_price=order_price,
            actual_price=order_price,
            item=service_result,
            payment_terms='alipay',
            order_desc=order_desc,
            order_type=7,
        )

        order.order_id = create_order_id()
        order.save()

        cls.after_create_order(
            user=user,
            order=order,
            service=service_result,
            num=num,
        )

        return order

    @classmethod
    def befor_paid_order(self, user, item_record, payment_terms):
        item_num = item_record.num
        try:
            item_price = item_record.item.price
        except AttributeError:
            item_price = item_record.item.item.price

        order_price = item_num * item_price

        if payment_terms == 'coin':
            if not self.has_enough_coin(
                user=user,
                order_price=order_price,
            ):
                return False

        return True

    @classmethod
    def has_enough_coin(self, user, order_price):
        point_utils = PointUtils()
        point = point_utils._get_pinbot_point(user)
        user_coin = point.coin

        if user_coin < int(order_price):
            return False
        return True

    @classmethod
    @transaction.atomic
    def paid_order(self, order_id, user):
        order = self.get_order_info(
            order_id=order_id,
            user=user,
        )
        order.pay_time = datetime.datetime.now()
        order.save()

        item_record = self.get_item_record_by_order(order_id)
        product_type = item_record.item.get_product_type
        service_id = item_record.item.id

        if not self.befor_paid_order(
            user=user,
            item_record=item_record,
            payment_terms=order.payment_terms
        ):
            return False

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event='paid_order',
            dest=product_type,
            order_id=order.order_id,
            payment_terms=order.payment_terms,
            product=item_record.item,
            product_type=product_type,
            user=user,
            item_num=item_record.num,
            service_id=service_id,
            order_price=order.order_price
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.process()

        self.change_order_status(
            user=user,
            order_id=order_id,
            order_status='paid'
        )
        return service_result

    @classmethod
    def close_order(self, order_id, user):
        order = self.get_order_info(
            order_id=order_id,
            user=user,
        )

        item_record = self.get_item_record_by_order(order_id)
        product_type = item_record.item.get_product_type
        service_id = item_record.item.id

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event=sys._getframe().f_code.co_name,
            dest=product_type,
            order_id=order.order_id,
            payment_terms=order.payment_terms,
            product=item_record.item,
            product_type=product_type,
            user=user,
            item_num=item_record.num,
            service_id=service_id
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.process()

        self.change_order_status(
            user=user,
            order_id=order_id,
            order_status='closed'
        )
        return service_result

    @classmethod
    def cancel_order(self, order_id, user):
        order = self.get_order_info(
            order_id=order_id,
            user=user,
        )

        item_record = self.get_item_record_by_order(order_id)
        product_type = item_record.item.get_product_type
        service_id = item_record.item.id

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event=sys._getframe().f_code.co_name,
            dest=product_type,
            order_id=order.order_id,
            payment_terms=order.payment_terms,
            product=item_record.item,
            product_type=product_type,
            user=user,
            item_num=item_record.num,
            service_id=service_id
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.process()

        self.change_order_status(
            user=user,
            order_id=order_id,
            order_status='canceled'
        )
        return service_result

    @classmethod
    def delete_order(self, order_id, user):
        order = self.get_order_info(
            order_id=order_id,
            user=user,
        )

        item_record = self.get_item_record_by_order(order_id)
        product_type = item_record.item.get_product_type
        service_id = item_record.item.id

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event=sys._getframe().f_code.co_name,
            dest=product_type,
            order_id=order.order_id,
            payment_terms=order.payment_terms,
            product=item_record.item,
            product_type=product_type,
            user=user,
            item_num=item_record.num,
            service_id=service_id
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.process()

        self.change_order_status(
            user=user,
            order_id=order_id,
            order_status='deleted'
        )
        return service_result

    @classmethod
    @transaction.atomic
    def refund_order(self, user, order_id, service_id):
        order = self.get_order_info(
            order_id=order_id,
            user=user,
        )
        item_record = self.get_item_record_by_order(order_id)
        product_type = item_record.item.get_product_type
        service_id = item_record.item.id
        refund_info = self.get_refund_info(
            service_id=service_id
        )

        # 只允许人工服务退款
        if product_type != 'manual_service':
            return False

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event=sys._getframe().f_code.co_name,
            dest=product_type,
            order_id=order.order_id,
            payment_terms=order.payment_terms,
            product=item_record.item,
            product_type=product_type,
            user=user,
            item_num=item_record.num,
            service_id=service_id
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.process()

        self.change_order_status(
            user=user,
            order_id=order_id,
            order_status='refund'
        )

        return {
            'service_result': service_result,
            'refund_info': refund_info
        }

    @classmethod
    @transaction.atomic
    def confirm_refund_order(self, user, order_id):
        order = get_object_or_none(UserOrder, order_id=order_id)
        item_record = self.get_item_record_by_order(order_id)
        product_type = item_record.item.get_product_type
        service_id = item_record.item.id

        # 只允许人工服务退款
        if product_type != 'manual_service':
            return False

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event=sys._getframe().f_code.co_name,
            dest=product_type,
            order_id=order.order_id,
            product_type=product_type,
            user=user,
            service_id=service_id
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        result = service_obj.process()

        order.order_status = 'refunded'
        order.save()

        return result

    @classmethod
    @transaction.atomic
    def cancel_refund_order(self, order_id, user):
        order = self.get_order_info(
            order_id=order_id,
            user=user,
        )

        item_record = self.get_item_record_by_order(order_id)
        product_type = item_record.item.get_product_type
        service_id = item_record.item.id

        # 只允许人工服务退款
        if product_type != 'manual_service':
            return False

        # connect service
        protcol_data = self.create_protcol_data(
            service_name=product_type,
            event=sys._getframe().f_code.co_name,
            dest=product_type,
            order_id=order.order_id,
            payment_terms=order.payment_terms,
            product=item_record.item,
            product_type=product_type,
            user=user,
            item_num=item_record.num,
            service_id=service_id
        )

        service_obj = protcol_data.get('service_class')(**protcol_data)
        service_result = service_obj.process()
        self.change_order_status(
            user=user,
            order_id=order_id,
            order_status='paid'
        )
        return service_result

    @classmethod
    def add_item_record(self, item, order_id, num, total_price):
        order = get_object_or_none(UserOrder, order_id=order_id)
        item_record = ItemRecord(
            order=order,
            item=item,
            num=num,
            total_price=total_price
        )
        item_record.save()
        return True

    @classmethod
    def change_order_status(self, user, order_id, order_status):
        order = get_object_or_none(UserOrder, order_id=order_id)

        if order_status not in dict(UserOrder.ORDER_STATUS_META):
            return False

        if (order.user != user):
            return False

        order.order_status = order_status
        order.save()
        return True

    @classmethod
    def get_order_info(self, order_id, user=None):
        if user:
            order = get_object_or_none(
                UserOrder,
                order_id=order_id,
                user=user,
            )
        else:
            order = get_object_or_none(
                UserOrder,
                order_id=order_id,
            )
        return order

    @classmethod
    def get_order_list(self, user, order_status=None):
        search_dict = {}
        search_dict['user'] = user

        if order_status:
            search_dict['order_status'] = order_status

        order_list = UserOrder.objects.filter(
            **search_dict
        )
        return order_list

    @classmethod
    def get_product_object(self, pid, product_type):
        product_map = {
            'manual_service': PackageItem,
            'self_service': VipRoleSetting,
            'coin': Coin,
            'pinbot_point': PinbotPoint,
            'renew_service': RenewRecord,
        }

        product = get_object_or_none(
            product_map[product_type],
            id=pid
        )

        return product
