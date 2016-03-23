# coding: utf-8

import urllib
import requests
from hashlib import md5
from collections import OrderedDict

from alipay_config import AlipayConfig

from Pinbot.settings import DEBUG


class AlipayUtils(object):

    @classmethod
    def _convert_str_encode(cls, pay_option, encoding='utf-8'):
        '''
       将unicode编码转换成utf-8编码
        '''
        for key, value in pay_option.iteritems():
            if not value:
                continue
            if isinstance(value, unicode):
                pay_option[key] = value.encode(encoding)
        return pay_option

    @classmethod
    def _get_url_params(cls, pay_option):
        '''
        使用OrderedDict将url参数按字母顺序排序
        去除空的字段和sign, sign_type字段
        '''
        url_params = OrderedDict(
            sorted(
                [
                    item for item in pay_option.iteritems()
                    if item[1] and item[0] not in ('sign', 'sign_type')
                ],
                key=lambda x: x[0]
            )
        )
        return url_params

    @classmethod
    def _get_sign(cls, url_params):
        '''
        md5加密url参数和key
        '''
        key = AlipayConfig.ALIPAY_KEY
        prestr = '&'.join('%s=%s' % item for item in url_params.iteritems())
        sign = md5(prestr + key).hexdigest()
        return sign

    @classmethod
    def submit_order_url(
            cls,
            order,
            return_url=AlipayConfig.ALIPAY_RETURN_URL,
            notify_url=AlipayConfig.ALIPAY_NOTIFY_URL,
            order_price=0,
            extra_common_param=''
    ):
        '''
        构造支付宝即时到账链接
        '''
        total_fee = order.total_price if not order_price else order_price
        pay_option = dict([
            ('service', 'create_direct_pay_by_user'),
            ('payment_type', '1'),

            ('_input_charset', AlipayConfig.ALIPAY_INPUT_CHARSET),
            ('partner', AlipayConfig.ALIPAY_PID),
            ('seller_email', AlipayConfig.ALIPAY_SELLER_EMAIL),
            ('return_url', return_url),
            ('notify_url', notify_url),
            ('show_url', ''),

            ('out_trade_no', order.order_id),
            ('subject', order.subject_name()),
            ('body', order.order_detail()),
            ('total_fee', total_fee if not DEBUG else 0.1),
            ('extra_common_param', extra_common_param)
        ])

        pay_option = cls._convert_str_encode(
            pay_option,
            encoding=AlipayConfig.ALIPAY_INPUT_CHARSET,
        )

        url_params = cls._get_url_params(pay_option)
        url_params['sign'] = cls._get_sign(url_params)
        url_params['sign_type'] = AlipayConfig.ALIPAY_SIGN_TYPE
        submit_url = AlipayConfig.ALIPAY_GATEWAY + urllib.urlencode(url_params)

        return submit_url

    @classmethod
    def verify_alipay_notify(cls, url_data):
        '''
        验证支付宝支付成功的返回信息
        两个步骤：
           1. 验证签名
           2. 查询此notify是否在支付宝中有效
        '''
        # 验证签名
        alipay_sign = url_data.get('sign')
        alipay_url_params = cls._get_url_params(url_data)
        sign = cls._get_sign(alipay_url_params)

        if sign != alipay_sign:
            return False

        # 查询信息是否在支付宝中有效
        check_params = {
            'partner': AlipayConfig.ALIPAY_PID,
            'notify_id': url_data.get('notify_id')
        }
        result = requests.get(
            AlipayConfig.ALIPAY_NOTIFY_GATEWAY,
            params=check_params
        )
        if result.text.lower().strip() == 'true':
            return True

        return False


if __name__ == '__main__':
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

    from app.payment.models import PaymentOrder
    order = PaymentOrder.objects.filter()[0]
    print AlipayUtils.submit_order_url(order)
