# coding: utf-8

import os
import requests
import random
import hashlib
from urllib import quote
import xml.etree.ElementTree as ET

from django.conf import settings
# =======【证书路径设置】=====================================
SSLCERT_PATH = os.path.join(settings.PROJECT_ROOT, 'Pinbot/cert/apiclient_cert.pem')
SSLKEY_PATH = os.path.join(settings.PROJECT_ROOT, 'Pinbot/cert/apiclient_key.pem')


class PaymentService(object):

    @classmethod
    def array_to_xml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.items():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    @classmethod
    def xml_to_array(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    @classmethod
    def create_noce_str(self, length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    @classmethod
    def format_biz_query_para_map(self, para_map, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(para_map)
        buff = []
        for k in slist:
            v = quote(para_map[k]) if urlencode else para_map[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    @classmethod
    def get_sign(self, obj):
        """生成签名"""
        # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        sgin_Str = self.format_biz_query_para_map(obj, False)
        # 签名步骤二：在string后加入KEY
        sgin_Str = "{0}&key={1}".format(sgin_Str, settings.WEIXIN_PAY_KEY)
        # 签名步骤三：MD5加密
        sgin_Str = hashlib.md5(sgin_Str).hexdigest()
        # 签名步骤四：所有字符转为大写
        result_ = sgin_Str.upper()
        return result_

    @classmethod
    def create_weixin_pack(self, openid, total_amount, act_name='提交定制'):
        total_amount = str(int(total_amount * 100))
        parmeter = {
            'nonce_str': self.create_noce_str(),
            'mch_billno': self.create_noce_str(28),
            'mch_id': settings.WEIXIN_MCHID,
            'wxappid': settings.WEIXIN_APP_ID,
            'send_name': '聘宝招聘版',
            're_openid': openid,
            'total_amount': total_amount,
            'total_num': '1',
            'wishing': '祝您招聘顺利',
            'act_name': act_name,
            'remark': ' ',
            'client_ip': '222.211.175.238'
        }

        sign = self.get_sign(parmeter)
        parmeter['sign'] = sign
        data = self.array_to_xml(parmeter)
        ret = requests.post(
            url='https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack',
            data=data,
            cert=(SSLCERT_PATH, SSLKEY_PATH)
        )
        ret = self.xml_to_array(ret.content)
        return ret
