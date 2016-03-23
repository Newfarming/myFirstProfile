# coding: utf-8

import json
import requests

from django.views.generic import View
from django.shortcuts import render

from ..runtime.mail_manage import (
    MailTemplateManage,
    MailTagsManage
)
from ..email_utils import (
    UselessEmailUtils
)

from pin_utils.django_utils import (
    JsonResponse
)

from pin_utils.email.send_mail import (
    sendcloud_bat_mail
)
from pin_utils.mixin_utils import (
    CSRFExemptMixin,
    StaffRequiredMixin
)


class SendSms(StaffRequiredMixin, View):

    def send_sms(self, mobile, send_key):

        template = {
            '1': '【聘宝江湖深圳场】您已完成报名，由于现场席位有限，报名信息需等待人工审核，通过之后聘宝将以短信告知您。感谢您的参与，了解活动请戳 http://www.pinbot.me/activity/rccbz/',
            '2': '【聘宝江湖深圳场】我们很高兴的通知您，您的报名信息已通过审核。活动即将开始，期待您的准时到来。参会地点：地点： 深圳南山区软件产业基地4栋B座1楼10-13号 飞马旅ONSTAGE    参会时间：2015年12月18日  14:30  了解活动报名请戳：http://www.pinbot.me/activity/rccbz/',
            '3': '【聘宝江湖深圳场】活动将在明天下午14:30准时开始，为避免入场拥挤情况，请您提前15-30分钟入场。地点： 深圳南山区软件产业基地4栋B座1楼10-13号 飞马旅ONSTAGE   参会时间：2015年12月18日  14:30  了解活动报名请戳：http://www.pinbot.me/activity/rccbz/'
        }

        content = template.get(send_key)
        send_url = 'http://yunpian.com/v1/sms/send.json'
        param_doc = {
            'apikey': 'f0a698b6bb84ba82650053197ba5ebfa',
            'mobile': mobile,
            'text': content
        }

        rep = requests.post(
            url=send_url,
            data=param_doc
        )
        rep.json()

        ret = rep.json()
        ret['mobile'] = mobile
        ret['send_key'] = send_key

        return ret

    def get(self, request):

        mobile = request.REQUEST.get('mobile')
        send_key = request.REQUEST.get('send_key')

        send_ret = self.send_sms(
            mobile=mobile,
            send_key=send_key
        )
        return JsonResponse(send_ret)


class SendEmail(StaffRequiredMixin, CSRFExemptMixin, View):
    """发送邮件"""
    template_name = 'send_email.html'

    def get(self, request):
        mailTplManage = MailTemplateManage()
        mailTagsManage = MailTagsManage()
        all_tpl = mailTplManage.get_all_tpl()
        tags = mailTagsManage.get_all_tags()

        form = MailTemplateManage(request=request)
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'all_tpl': all_tpl,
                'tags': tags
            }
        )

    def post(self, request):
        mailTplManage = MailTemplateManage()
        json_data = json.loads(request.body)

        tpl_content = json_data['tpl_content']
        tag_id = json_data['tag_id']
        sendto = json_data['sendto']
        email_title = json_data['email_title']
        send_users = mailTplManage.get_send_target(**dict(json_data))

        if sendto != '':
            sendto_list = sendto.split(';')
            send_users.extend(sendto_list)

        useless_email = UselessEmailUtils.get_useless_email()

        for send_user in send_users:
            if send_user in useless_email:
                continue
            sendcloud_bat_mail.delay(send_user, email_title, tpl_content, label=tag_id)

        return JsonResponse({'message': 'ok'})
