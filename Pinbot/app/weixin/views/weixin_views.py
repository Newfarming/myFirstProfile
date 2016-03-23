# coding: utf-8

from app.weixin.runtime.weixin_utils import (
    WeixinService
)
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import (
    View,
)
from pin_utils.django_utils import (
    JsonResponse,
    get_object_or_none,
    error_weixin_code,
)
from pin_utils.mixin_utils import (
    StaffRequiredMixin,
    CSRFExemptMixin
)
from pin_utils.weixin.wx_utils import (
    WxUtils
)
from users.models import (
    User
)
from ..settings.weixin_settings import (
    REDIRECT_LOGIN_URL,
    REDIRECT_REG_URL,
    RECOMMAND_URL,
    CUSTOMIZE_URL,
    CUSTOMIZE_NEW_URL,
    FAVOURS_URL,

)


class Authorization(View):

    NEXT_URL_META = {
        'signin': REDIRECT_LOGIN_URL,
        'signup': REDIRECT_REG_URL,
        'recommand': RECOMMAND_URL,
        'favours': FAVOURS_URL,
        'customize': CUSTOMIZE_URL,
        'customize_new': CUSTOMIZE_NEW_URL,
    }

    def save_token_to_session(self, openid, access_token):
        if openid:
            self.request.session['openid'] = openid
            self.request.session['access_token'] = access_token
            return True
        return False

    def validate(self):

        signature = self.request.REQUEST.get('signature', '')
        timestamp = self.request.REQUEST.get('timestamp', '')
        nonce = self.request.REQUEST.get('nonce', '')

        return WeixinService.check_signature(
            signature=signature,
            timestamp=timestamp,
            nonce=nonce
        )

    def get(self, request):

        # if not self.validate():
        #     return HttpResponseBadRequest('Verify Failed')

        self.request = request

        code = self.request.REQUEST.get('code')
        next_url = self.request.REQUEST.get('next_url')

        if not error_weixin_code(code):
            return HttpResponseBadRequest('Verify Failed')

        user_base = WeixinService.get_openid(
            code=code
        )
        if not user_base:
            return HttpResponseBadRequest('Verify Failed')

        openid = user_base.get('openid')
        access_token = user_base.get('access_token')

        # save session
        self.save_token_to_session(
            openid=openid,
            access_token=access_token
        )

        # get weixin user sns info
        readlly_weixin_user = WeixinService.get_weixin_user(
            openid=openid
        )

        redirect_next_url = self.NEXT_URL_META.get(next_url, REDIRECT_LOGIN_URL)
        redirect_next_url = redirect_next_url[:redirect_next_url.find('?from=weixin')]
        if readlly_weixin_user:
            pinbot_user = readlly_weixin_user.user
            if pinbot_user.is_active:
                return redirect('{0}?is_bind=1&weixin_auth=1'.format(redirect_next_url))

        return redirect(redirect_next_url)


class FeedNotify(StaffRequiredMixin, View):

    def post(self, request):

        username = request.POST.get('username')
        feed_id = request.POST.get('feed_id')
        title = request.POST.get('title')
        reco_num = int(request.POST.get('reco_num'))
        # calc_num = request.POST.get('calc_num')
        display_time = request.POST.get('display_time')
        user = get_object_or_none(User, email=username)
        weixin_user = WeixinService.get_weixin_user_by_uid(user=user)
        if not weixin_user:
            return JsonResponse(
                {
                    'msg': 'not found weixin user',
                    'status': 'error'
                }
            )

        openid = weixin_user.openid

        send_data = WeixinService.get_feed_notify_msg_tpl()
        url = '{0}{1}/'.format(
            WeixinService.get_recommand_url(),
            feed_id
        )

        send_data['first']['value'] = "聘宝刚刚为您推荐了{0}封简历，优质候选人不能等，请尽快查阅简历".format(reco_num),
        send_data['remark']['value'] = "小宝提示：手机上每个职位定制只能浏览最多5封简历哦，请返回PC上查看全部的简历推荐."
        if reco_num == 0:
            send_data['first']['value'] = "小宝遗憾的通知您，以下职位暂时没有合适的人才匹配：",
            send_data['remark']['value'] = "不要气馁！小宝秘籍在此：你可以尝试修改定制内容，可能会有惊喜哦！"
            url = WeixinService.get_customize_url()

        send_data['keyword1']['value'] = title
        send_data['keyword2']['value'] = reco_num
        send_data['keyword3']['value'] = display_time

        ret = WxUtils.send_tpl_msg(
            openid=openid,
            tpl_id=WeixinService.get_template_msg_id(),
            data=send_data,
            url=url,
        )

        if ret.get('errcode') != 0:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': ret.get('errmsg')
                }
            )

        return JsonResponse(
            {
                'status': 'ok',
                'msg': 'success'
            }
        )


class Index(CSRFExemptMixin, View):

    def validate(self):

        signature = self.request.REQUEST.get('signature', '')
        timestamp = self.request.REQUEST.get('timestamp', '')
        nonce = self.request.REQUEST.get('nonce', '')

        return WeixinService.check_signature(
            signature=signature,
            timestamp=timestamp,
            nonce=nonce
        )

    def get(self, request):

        if self.validate():

            return HttpResponse(
                request.GET.get('echostr', ''),
                content_type="text/plain"
            )

        return HttpResponseBadRequest('Verify Failed')

    def post(self, request):

        if not self.validate():
            return HttpResponseBadRequest('Verify Failed')

        response = WeixinService.process_request_msg(
            recv_body=request.body
        )

        return HttpResponse(response, content_type="application/xml")
