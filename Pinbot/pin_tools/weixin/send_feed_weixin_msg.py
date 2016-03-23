# coding:utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

import datetime

from feed.models import (
    EmailFeedData,
    Feed2,
)
from app.weixin.models import (
    WeixinUser
)
from app.weixin.runtime.weixin_utils import (
    WeixinService
)
from pin_utils.weixin.wx_utils import (
    WxUtils
)


def get_feed_data(send_user):

    username = send_user.user.username
    weixin_openid = send_user.openid

    user_pub_feeds = EmailFeedData.objects(
        email=username,
        is_send=False,
    ).select_related()

    total_num = 0
    keyword_list = []
    feed_id = None
    for pub_feed in user_pub_feeds:
        feed_id = pub_feed.feed.id

        feed = Feed2.objects(id=feed_id, deleted=False).first()
        if not feed:
            continue

        resumes_count = len(pub_feed.resumes)
        total_num += resumes_count

        keywords = feed.title if feed.title else feed.keywords
        if total_num > 1 or len(user_pub_feeds) > 1:
            keywords = '{0}({1})'.format(
                keywords,
                resumes_count
            )

        keyword_list.append(keywords.replace(u'，', ','))

    keyword_list = ', '.join(keyword_list).split(',')
    if len(keyword_list) > 3:
        keyword_list[3] = '...'
    keywords = ','.join(keyword_list[:4])

    feed_data = {}
    feed_data['openid'] = weixin_openid
    feed_data['username'] = username
    feed_data['reco_num'] = 0
    feed_data['feed_id'] = str(feed_id)
    feed_data['title'] = keywords
    feed_data['reco_num'] = total_num
    feed_data['display_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return feed_data


def send_feed_msg():

    need_send_email = EmailFeedData.objects(
        is_send=False,
    ).distinct('email')

    weixin_users = WeixinUser.objects.filter(
        user__username__in=need_send_email
    )
    for send_user in weixin_users:
        feed_data = get_feed_data(send_user)
        feed_id = feed_data.get('feed_id')
        title = feed_data['title']
        reco_num = feed_data['reco_num']
        display_time = feed_data['display_time']

        send_data = WeixinService.get_feed_notify_msg_tpl()
        send_data['first']['value'] = "聘宝刚刚为您推荐了{0}封简历，优质候选人不能等，请尽快查阅简历".format(feed_data['reco_num'])
        send_data['keyword1']['value'] = title
        send_data['keyword2']['value'] = reco_num
        send_data['keyword3']['value'] = display_time
        send_data['remark']['value'] = "小宝提示：手机上每个职位定制只能浏览最多5封简历哦，请返回PC上查看全部的简历推荐."

        urls = WeixinService.get_recommand_url().split('?from=')
        url = '{0}{1}/?from={2}'.format(urls[0], feed_id, urls[1])

        if reco_num == 0:
            send_data['first']['value'] = "小宝遗憾的通知您，以下职位暂时没有合适的人才匹配：",
            send_data['remark']['value'] = "不要气馁！小宝秘籍在此：你可以尝试修改定制内容，可能会有惊喜哦！"
            url = WeixinService.get_customize_url()

        ret = WxUtils.send_tpl_msg(
            openid=feed_data.get('openid'),
            tpl_id=WeixinService.get_template_msg_id(),
            data=send_data,
            url=url
        )

        if ret.get('errcode') == 0:
            print '%s,(openid:%s) send weixin msg success' % (send_user.user.username, feed_data.get('openid'))
        else:
            print '%s,(openid:%s) send weixin msg error' % (send_user.user.username, feed_data.get('openid'))

if __name__ == '__main__':
    send_feed_msg()
