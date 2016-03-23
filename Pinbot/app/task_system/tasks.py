# coding: utf-8

from pin_celery.celery_app import app
from app.weixin.runtime.weixin_utils import WeixinRedPackService


class WEIXIN_SEND_REDPACK_FAIL(Exception):
    pass


@app.task(bind=True, name='weixin_send_redpack')
def send_weixin_redpack(self, user, total_amount, act_name='聘宝任务系统'):
    result = WeixinRedPackService.send_feed_redpack(
        user=user,
        total_amount=total_amount,
        act_name=act_name,
    )
    if not result:
        raise self.retry(countdown=70, max_retries=3, exc=WEIXIN_SEND_REDPACK_FAIL)
    return result
