# coding: utf-8


class AlipayConfig(object):
    '''
    支付宝接口的通用配置
    '''

    ALIPAY_PID = '2088012894071031'
    ALIPAY_KEY = 'zufznjki4sm2ph9j9a4v6b8d4d1kqwoh'

    ALIPAY_SELLER_EMAIL = 'peaker@hopperclouds.com'

    ALIPAY_INPUT_CHARSET = 'utf-8'
    ALIPAY_SIGN_TYPE = 'MD5'

    ALIPAY_GATEWAY = 'https://mapi.alipay.com/gateway.do?'
    ALIPAY_NOTIFY_GATEWAY = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'

    ALIPAY_RETURN_URL = 'http://www.pinbot.me/payment/alipay_return/'
    ALIPAY_NOTIFY_URL = 'http://www.pinbot.me/payment/alipay_notify/'


try:
    from Pinbot.settings import ALIPAY_RETURN_URL
    AlipayConfig.ALIPAY_RETURN_URL = ALIPAY_RETURN_URL
except:
    pass
