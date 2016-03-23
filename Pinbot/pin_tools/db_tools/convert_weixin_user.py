import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from app.weixin.runtime.weixin_utils import (
    WeixinService
)
from app.weixin.models import (
    WeixinUser
)


def update_weixin():

    weixin_users = WeixinUser.objects.all()
    for weixin_user in weixin_users:
        openid = weixin_user.openid
        weixin_user_doc = WeixinService.get_user_info(openid=openid)
        weixin_user_doc.pop('openid')
        print weixin_user_doc
        WeixinUser.objects.filter(
            openid=openid
        ).update(
            **weixin_user_doc
        )
        print 'weixin user info: %s update success' % (openid)


if __name__ == '__main__':
    update_weixin()
