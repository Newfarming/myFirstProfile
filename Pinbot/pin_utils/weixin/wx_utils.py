# coding:utf-8

from app.weixin.runtime.weixin_utils import (
    WeixinService
)

from app.weixin.models import (
    MsgSendLog
)

class WxUtils(object):

    @classmethod
    def send_tpl_msg(cls, openid, tpl_id, data, url, msg_type=1):

        ret = WeixinService.send_template_message(
            openid=openid,
            template_id=tpl_id,
            data=data,
            url=url
        )

        weixin_user = WeixinService.get_weixin_user(openid=openid)

        msg_log = MsgSendLog(
            weixin_user=weixin_user,
            msg_type=msg_type,
            title=data['keyword1']['value'],
            reco_num=data['keyword2']['value'],
            display_time=data['keyword3']['value'],
            url=url,
            errcode=ret.get('errcode'),
            errmsg=ret.get('errmsg')
        )
        msg_log.save()
        return ret