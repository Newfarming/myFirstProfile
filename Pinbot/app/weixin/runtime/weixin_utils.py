# coding: utf-8

import logging
import xml.etree.ElementTree as ET
import hashlib
import time
from datetime import datetime, timedelta

import requests
import ujson
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User


from app.weixin.models import (
    WeixinUser
)
from feed.models import (
    UserFeed2
)
from app.activity.models import (
    EggRecord
)
from pin_utils.django_utils import (
    get_object_or_none
)
from app.weixin.settings.weixin_settings import (
    CHAT_MAP,
    EVENT_KEY_MAP,
    RECOMMAND_URL,
    CUSTOMIZE_URL,
    FEED_NOTIFY_MSG_TEMPLATE
)
from app.payment.runtime.pay_utils import (
    PaymentService
)
from app.payment.models import (
    WeixinPackRecord
)


logger = logging.getLogger('django')

WEIXIN_APP_ID = settings.WEIXIN_APP_ID
WEIXIN_APP_SECERT = settings.WEIXIN_APP_SECERT
WEIXIN_APP_TOKEN = settings.WEIXIN_TOKEN
WEIXIN_ACCESS_TOKEN_EXPIRE_TIME = settings.WEIXIN_ACCESS_TOKEN_EXPIRE_TIME
WEIXIN_MENU = settings.WEIXIN_MENU
WEIXIN_OAUTH_REDIRECT_URL = settings.WEIXIN_OAUTH_REDIRECT_URL
WEIXIN_TEMPLATE_MSG_ID = settings.WEIXIN_TEMPLATE_MSG_ID


class WeixinMsgService(object):

    msg_tpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"

    def __init__(self, recv_body):
        self.parse_msg(recv_body)
        self.recv_msg = self.msg.get('Content')
        self.openid = self.msg.get('FromUserName')
        self.server_user = self.msg.get('ToUserName')
        self.msg_type = self.msg.get('MsgType')
        self.msg_event = self.msg.get('Event')
        self.event_key = self.msg.get('EventKey', '')

    def process_msg(self):
        if self.msg_type == 'text':
            return self.process_text_msg()

        if self.msg_type == 'event':
            return self.process_event_msg()

    def process_text_msg(self):

        self.reply_msg = EVENT_KEY_MAP.get('KEY_HELP').get('welcome_str')
        reply_doc = CHAT_MAP.get(self.recv_msg)
        if not reply_doc:
            return self.reply_content(
                content=self.reply_msg
            )
        if reply_doc.get('type') == 'show_text':
            self.reply_msg = reply_doc.get('welcome_str')

        if reply_doc.get('type') == 'show_text_fun':
            self.reply_msg = reply_doc.get('fun_name')

        if reply_doc.get('type') == 'reply_text_fun':
            self.reply_msg = self.do_str_to_fun(
                fun_name=reply_doc.get('fun_name')
            )

        return self.reply_content(
            content=self.reply_msg
        )

    def get_event_action(self, eventkey):
        actions = {
            '1': 'qr_bind',
            '2': 'get_red_pack'
        }
        return actions.get(eventkey[:1])

    def process_event_msg(self):

        self.reply_msg = CHAT_MAP.get('subscribe').get('welcome_str')

        if self.msg_type == 'event' and self.msg_event == 'SCAN':
            event_key = self.event_key
            event_key_action = self.get_event_action(event_key)
            uid_key = event_key[1:]

            if event_key_action == 'qr_bind':
                ret = WeixinService.qrcode_bind_user(
                    uid_key=uid_key,
                    openid=self.openid
                )
                self.reply_msg = CHAT_MAP.get('subscribe').get(ret['msg'])
                if ret['status'] == 'ok':
                    self.reply_msg = self.reply_msg % (ret.get('username'))

            if event_key_action == 'get_red_pack':

                ret = WeixinService.qrcode_get_red_pack(
                    uid_key=uid_key,
                    openid=self.openid
                )
                self.reply_msg = CHAT_MAP.get('get_red_pack').get(ret['msg'])

        if self.msg_type == 'event' and self.msg_event == 'subscribe':
            self.reply_msg = CHAT_MAP.get('subscribe').get('welcome_str')
            if self.event_key and 'qrscene' in self.event_key:

                event_key = self.event_key[8:]
                event_key_action = self.get_event_action(event_key)
                uid_key = event_key[1:]

                if event_key_action == 'qr_bind':
                    ret = WeixinService.qrcode_bind_user(
                        uid_key=uid_key,
                        openid=self.openid
                    )
                    self.reply_msg = CHAT_MAP.get('subscribe').get(ret['msg'])
                    if ret['status'] == 'ok':
                        self.reply_msg = self.reply_msg % (ret.get('username'))

                if event_key_action == 'get_red_pack':
                    ret = WeixinService.qrcode_get_red_pack(
                        uid_key=uid_key,
                        openid=self.openid
                    )
                    self.reply_msg = CHAT_MAP.get('get_red_pack').get(ret['msg'])

            WeixinService.update_weixin_user(
                openid=self.openid,
                is_subscribe=True
            )

        if self.msg_type == 'event' and self.msg_event == 'unsubscribe':
            WeixinService.update_weixin_user(
                openid=self.openid,
                is_subscribe=False
            )

        if self.msg_type == 'event' and self.msg_event == 'CLICK':

            ret = EVENT_KEY_MAP.get(self.event_key)
            self.reply_msg = self.do_str_to_fun(
                fun_name=ret.get('fun_name')
            )

        return self.reply_content(
            content=self.reply_msg
        )

    def parse_msg(self, recv_body):

        root = ET.fromstring(recv_body.decode('utf-8'))
        self.msg = {}
        for child in root:
            self.msg[child.tag] = child.text

    def do_str_to_fun(self, **kwargs):
        method_to_call = getattr(self, kwargs.get('fun_name'))
        return method_to_call()

    def reply_content(self, content):

        msg = self.msg_tpl % (
            self.openid,
            self.server_user,
            str(int(time.time())),
            'text',
            content
        )
        return msg

    def click_help(self):
        return EVENT_KEY_MAP.get('KEY_HELP').get('welcome_str')

    def click_view_job(self):
        weixin_user = WeixinService.get_weixin_user(
            openid=self.openid
        )
        ret = EVENT_KEY_MAP.get('KEY_VIEW_JOB').get('welcome_str')

        if weixin_user:
            # todo get commend info
            ret = EVENT_KEY_MAP.get('KEY_VIEW_JOB').get('success_str')

            feed_list = UserFeed2.objects.filter(
                username=weixin_user.user.username,
                is_deleted=False,
            ).order_by('-add_time').select_related()[:5]

            if len(feed_list) == 0:
                ret = EVENT_KEY_MAP.get('KEY_VIEW_JOB').get('no_data')
                return ret

            desc_list = []
            count = 0
            for feed_obj in feed_list:
                count += 1
                desc_list.append('{0}、<a href="{1}{2}/">{3}</a>, {4}, {5}'.format(
                    count,
                    RECOMMAND_URL,
                    str(feed_obj.feed.id),
                    feed_obj.feed.title if feed_obj.feed.title else feed_obj.feed.keywords,
                    feed_obj.feed.expect_area.replace(',', '/'),
                    feed_obj.feed.talent_level.replace(',', '/'))
                )
            ret = ret % (
                '\n\n'.join(desc_list)
            )

        return ret

    def click_bind_account(self):

        weixin_user = WeixinService.get_weixin_user(
            openid=self.openid
        )
        if not weixin_user:
            ret = EVENT_KEY_MAP.get('KEY_BIND_ACCOUNT').get('welcome_str')
        else:
            ret = EVENT_KEY_MAP.get('KEY_BIND_ACCOUNT').get('success_str')
            ret = ret % (weixin_user.user.username)
        return ret

    def click_contact_us(self):
        return EVENT_KEY_MAP.get('KEY_CONTACT_US').get('welcome_str')


class WeixinService(object):

    @classmethod
    def get_feed_notify_msg_tpl(self):
        return FEED_NOTIFY_MSG_TEMPLATE

    @classmethod
    def get_customize_url(self):
        return CUSTOMIZE_URL

    @classmethod
    def get_recommand_url(self):
        return RECOMMAND_URL

    @classmethod
    def get_template_msg_id(self):
        return WEIXIN_TEMPLATE_MSG_ID

    @classmethod
    def get_base_access_token(self):

        # 获取基础access_token
        access_token = cache.get('weixin_access_token')
        if (not access_token) or (not self.vaild_base_access_token(access_token)):
            access_token = self.update_base_access_token()

        return access_token

    @classmethod
    def grant_base_access_token(self):

        response_json = self._get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": WEIXIN_APP_ID,
                "secret": WEIXIN_APP_SECERT,
            }
        )
        return response_json

    @classmethod
    def update_base_access_token(self):
        # 更新基础access_token
        token_doc = self.grant_base_access_token()
        access_token = token_doc.get('access_token')
        cache.set(
            'weixin_access_token',
            access_token,
            WEIXIN_ACCESS_TOKEN_EXPIRE_TIME
        )
        cache.set(
            'weixin_access_token_expires_at',
            token_doc.get('expires_in'),
            WEIXIN_ACCESS_TOKEN_EXPIRE_TIME
        )
        return access_token

    @classmethod
    def vaild_base_access_token(self, access_token):
        response_json = self._get(
            url="https://api.weixin.qq.com/cgi-bin/getcallbackip",
            params={
                "access_token": access_token,
            }
        )

        if response_json.get('errcode') is None:
            return True
        return False

    @classmethod
    def create_qrcode(self, data):
        """
        创建二维码
        详情请参考 http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html
        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """

        data = self._transcoding_dict(data)
        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/qrcode/create',
            data=data
        )

    @classmethod
    def show_qrcode(self, ticket):
        """
        通过ticket换取二维码
        详情请参考 http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html
        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        """

        return requests.get(
            url='https://mp.weixin.qq.com/cgi-bin/showqrcode',
            params={
                'ticket': ticket
            }
        )

    @classmethod
    def create_menu(self):

        menu_data = self._transcoding_dict(WEIXIN_MENU)
        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/menu/create',
            data=menu_data
        )

    @classmethod
    def check_signature(self, signature, timestamp, nonce):
        tmp_str = hashlib.sha1(''.join(sorted([WEIXIN_APP_TOKEN, timestamp, nonce]))).hexdigest()
        if not signature or not timestamp or not nonce:
            return False

        if tmp_str == signature:
            return True
        return True

    @classmethod
    def get_oauth_redirect(self, next_url, grant_type):
        oauth_redirect_url = WEIXIN_OAUTH_REDIRECT_URL % (next_url)
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=STATE#wechat_redirect' % (
            WEIXIN_APP_ID,
            oauth_redirect_url,
            grant_type
        )
        return url

    @classmethod
    def get_redpack_amout(self, user):
        ret = EggRecord.objects.filter(
            user=user,
            egg__code_name__contains='hongbao_',
            claim_status=1,
            create_time__gte=datetime.now() - timedelta(days=1)
        )

        if ret.count() > 1 or not ret:
            return False
        else:
            return ret[0]

    @classmethod
    def qrcode_get_red_pack(self, uid_key, openid):
        uid = cache.get(uid_key)
        user = get_object_or_none(User, id=uid)
        weixin_user = WeixinService.get_weixin_user(openid=openid)

        ret = {
            'status': 'error',
            'msg': 'fail_str'
        }

        if not user:
            return ret

        if weixin_user:
            if weixin_user.user.id != user.id:
                return ret

        if not self.is_bind(user=user):
            WeixinService.bind_weixin_openid(user, openid)
            WeixinService.update_weixin_userinfo(openid)

        egg_obj = self.get_redpack_amout(user=user)

        if not egg_obj:
            return ret

        if egg_obj.egg.price > 0:
            WeixinRedPackService.send_feed_redpack(
                user=user,
                act_name='彩蛋红包',
                total_amount=egg_obj.egg.price
            )
            ret['status'] = 'ok'
            ret['msg'] = 'success_str'
            egg_obj.claim_status = 2
            egg_obj.claim_time = datetime.now()
            egg_obj.save()
            cache.delete(uid_key)
            logger.info(
                'redpack for user: {username}  send status: {ret}'.format(
                    username=user.username,
                    ret=ret
                )
            )

        return ret

    @classmethod
    def qrcode_bind_user(self, uid_key, openid):
        uid = cache.get(uid_key)
        user = get_object_or_none(User, id=uid)
        weixin_user = WeixinService.get_weixin_user(openid=openid)
        ret = {
            'status': 'error',
            'msg': 'fail_str'
        }

        if not user:
            ret['status'] = 'error'
            ret['msg'] = 'fail_str'
            return ret

        if self.is_bind(user):
            if weixin_user:
                if weixin_user.user.id == user.id:
                    ret['status'] = 'ok'
                    ret['msg'] = 'success_str'
                    ret['username'] = user.username
                else:
                    ret['status'] = 'error'
                    ret['msg'] = 'has_bind'
        else:
            if weixin_user:
                if weixin_user.user.id != user.id:
                    ret['status'] = 'error'
                    ret['msg'] = 'has_bind'
                    return ret
            WeixinService.bind_weixin_openid(user, openid)
            WeixinService.update_weixin_userinfo(openid)
            ret['status'] = 'ok'
            ret['msg'] = 'success_str'
            ret['username'] = user.username

        return ret

    @classmethod
    def process_request_msg(self, recv_body):

        """
        处理微信客户端发起的请求
        :param body:
        :return:
        """

        weixin_msg = WeixinMsgService(recv_body=recv_body)
        return weixin_msg.process_msg()

    @classmethod
    def get_openid(self, code):
        """
        获取用户openid
        详情请参考 http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
        :param appid: 微信app id
        :param secret: 微信app secret
        :code: code(五分钟内失效)
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        ret = self._get(
            url='https://api.weixin.qq.com/sns/oauth2/access_token',
            params={
                'appid': WEIXIN_APP_ID,
                'secret': WEIXIN_APP_SECERT,
                'code': code,
                'grant_type': 'authorization_code'
            }
        )
        if ret.get('errcode') == -1:
            return False
        return ret

    @classmethod
    def get_user_info(self, openid, lang='zh_CN'):
        """
        获取用户基本信息
        详情请参考 http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
        :param openid: 用户 ID
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """

        return self._get(
            url='https://api.weixin.qq.com/cgi-bin/user/info',
            params={
                'access_token': self.get_base_access_token(),
                'openid': openid,
                'lang': lang,
            }
        )

    @classmethod
    def update_weixin_userinfo(self, openid):

        weixin_userinfo = self.get_user_info(
            openid=openid
        )
        if weixin_userinfo.get('errcode'):
            return False

        WeixinUser.objects.filter(
            openid=openid
        ).update(
            **weixin_userinfo
        )
        return True

    @classmethod
    def update_weixin_user(self, openid, **kwargs):

        WeixinUser.objects.filter(
            openid=openid
        ).update(
            **kwargs
        )

        return True

    @classmethod
    def unbind_weixin_openid(self, user):

        ret = WeixinUser.objects.filter(
            user=user,
        ).delete()

        return ret

    @classmethod
    def is_bind(self, user):
        ret = get_object_or_none(WeixinUser, user=user)
        return ret

    @classmethod
    def bind_weixin_openid(self, user, openid):

        if not openid:
            return False

        if self.is_bind(user):
            return False
        weixin_user_obj = get_object_or_none(WeixinUser, openid=openid)

        if weixin_user_obj:
            weixin_user_obj.is_bind = True
            weixin_user_obj.save()
        else:
            weixin_user = WeixinUser(
                user=user,
                openid=openid,
            )
            weixin_user.save()

        return True

    @classmethod
    def create_weixin_user(self, user, weixin_user):

        weixin_user = WeixinUser(
            user=user,
            openid=weixin_user.get('openid'),
            nickname=weixin_user.get('nickname'),
            sex=weixin_user.get('sex'),
            city=weixin_user.get('city'),
            province=weixin_user.get('province'),
            country=weixin_user.get('country'),
            headimgurl=weixin_user.get('headimgurl'),
            privilege=weixin_user.get('privilege'),
        )
        weixin_user.save()
        return True

    @classmethod
    def get_weixin_user(self, openid):
        # 检查系统是否已经存在open_id,并返回 weixin user
        user_obj = get_object_or_none(WeixinUser, openid=openid)
        return user_obj

    @classmethod
    def get_weixin_user_by_uid(self, user):
        return get_object_or_none(WeixinUser, user=user)

    @classmethod
    def send_template_message(self, openid, template_id, data, url='', topcolor='#FF0000'):
        """
        发送模版消息
        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html
        :param openid: 用户 ID
        :param template_id: 模板ID
        :param data: 模板消息数据 (dict形式)，示例如下：
        {
            "first": {
               "value": "恭喜你购买成功！",
               "color": "#173177"
            },
            "keynote1":{
               "value": "巧克力",
               "color": "#173177"
            },
            "keynote2": {
               "value": "39.8元",
               "color": "#173177"
            },
            "keynote3": {
               "value": "2014年9月16日",
               "color": "#173177"
            },
            "remark":{
               "value": "欢迎再次购买！",
               "color": "#173177"
            }
        }
        :param url: 跳转地址 (默认为空)
        :param topcolor: 顶部颜色RGB值 (默认 '#FF0000' )
        :return: 返回的 JSON 数据包
        """

        unicode_data = {}
        if data:
            unicode_data = self._transcoding_dict(data)

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/template/send',
            data={
                'touser': openid,
                "template_id": template_id,
                "url": url,
                "topcolor": topcolor,
                "data": unicode_data
            }
        )

    @classmethod
    def _request(self, method, url, **kwargs):
        """
        向微信服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        if "params" not in kwargs:
            kwargs["params"] = {
                "access_token": self.get_base_access_token(),
            }
        if isinstance(kwargs.get("data", ""), dict):
            body = ujson.dumps(kwargs["data"], ensure_ascii=False)
            # body = body.encode('utf8')
            kwargs["data"] = body

        try:
            r = requests.request(
                method=method,
                url=url,
                **kwargs
            )
        except (requests.ConnectionError, requests.exceptions.Timeout):
            logger.error('weixin api error, url: {0}, param: {1}'.format(
                url,
                kwargs,
            ), exc_info=True)
            return {}

        response_json = r.json()
        return response_json

    @classmethod
    def _get(self, url, **kwargs):
        """
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        return self._request(
            method="get",
            url=url,
            **kwargs
        )

    @classmethod
    def _post(self, url, **kwargs):
        """
        使用 POST 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        return self._request(
            method="post",
            url=url,
            **kwargs
        )

    @classmethod
    def _transcoding(self, data):
        """
        编码转换
        :param data: 需要转换的数据
        :return: 转换好的数据
        """
        if not data:
            return data

        result = None
        if isinstance(data, str):
            result = data.decode('utf-8')
        else:
            result = data
        return result

    @classmethod
    def _transcoding_list(self, data):
        """
        编码转换 for list
        :param data: 需要转换的 list 数据
        :return: 转换好的 list
        """
        if not isinstance(data, list):
            raise ValueError('Parameter data must be list object.')

        result = []
        for item in data:
            if isinstance(item, dict):
                result.append(self._transcoding_dict(item))
            elif isinstance(item, list):
                result.append(self._transcoding_list(item))
            else:
                result.append(item)
        return result

    @classmethod
    def _transcoding_dict(self, data):

        """
        编码转换 for dict
        :param data: 需要转换的 dict 数据
        :return: 转换好的 dict
        """
        if not isinstance(data, dict):
            raise ValueError('Parameter data must be dict object.')

        result = {}
        for k, v in data.items():
            k = self._transcoding(k)
            if isinstance(v, dict):
                v = self._transcoding_dict(v)
            elif isinstance(v, list):
                v = self._transcoding_list(v)
            else:
                v = self._transcoding(v)
            result.update({k: v})
        return result

    @classmethod
    def get_short_url(cls, long_url):
        """
        创建短链接
        详情请参考 https://mp.weixin.qq.com/wiki/10/165c9b15eddcfbd8699ac12b0bd89ae6.html
        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        :return
          errcode  0 表示成功
          errmsg
          short_url
        """
        data = {
            'action': 'long2short',
            'long_url': long_url
        }
        data = cls._transcoding_dict(data)
        return cls._post(
            url='https://api.weixin.qq.com/cgi-bin/shorturl',
            data=data
        )


class WeixinRedPackService(object):

    @classmethod
    def send_feed_redpack(self, user, total_amount, act_name='聘宝任务系统'):
        weixin_user = WeixinService.get_weixin_user_by_uid(
            user=user
        )
        if not weixin_user:
            logger.info(
                'redpack for user: {username}  create_weixin_pack_result: {ret}'.format(
                    username=user.username,
                    ret='no weixin_user'
                )
            )
            return False
        openid = weixin_user.openid

        ret = PaymentService.create_weixin_pack(
            openid=openid,
            total_amount=total_amount,
            act_name=act_name
        )
        logger.info(
            'redpack for user: {username}  create_weixin_pack_result: {ret}'.format(
                username=user.username,
                ret=ret
            )
        )

        # 这里根据返回的结果，如果是因为访问频率过高，
        # 或者是一分钟内同时发给一个用户而导致的失败，
        # 就不记录到后台,如果是因为微信平台不能确认是否发放成功，
        # 或者是账户的余额不足的时候，那么就不再重试调用接口。

        error_code = ret.get('err_code')
        if error_code == 'FREQ_LIMIT':
            ret_status = False
            return ret_status
        else:
            ret_status = True

        result_code = ret.get('result_code')
        if result_code == 'FAIL':
            logger.warning(
                'redpack for {user} result:{return_msg}'.format(
                    user=user.username,
                    return_msg=ret.get('return_msg')
                )
            )

        weixin_pack_record = WeixinPackRecord(
            user=weixin_user,
            amount=total_amount,
            send_status=ret_status,
            send_msg=ret.get('return_msg')
        )
        weixin_pack_record.save()

        return ret_status
