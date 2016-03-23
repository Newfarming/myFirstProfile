# coding: utf-8

import datetime

from django.core.urlresolvers import resolve

from Pinbot.settings import (
    settings
)

from pin_utils.django_utils import (
    get_client_ip
)
from pin_utils.user_log import (
    UserLogService
)


class UserAccessMiddleware(object):
    """用户访问行为记录中间件"""
    def process_request(self, request):

        write_flag = False
        access_url = request.path
        app_name = resolve(access_url).app_name
        app_allows = settings.USER_ACCESS_MIDDLEWARE_CONFIG['enable'].get(app_name)

        if not app_allows:
            return

        for url in app_allows:
            if (url in access_url):
                write_flag = True
                break

        if write_flag:
            user_obj = request.user
            if user_obj.is_staff:
                return

            user_name = user_obj.username
            ip = get_client_ip(request)
            refer_url = request.META.get('HTTP_REFERER', '')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            if user_name != '':

                UserLogService.write_user_access_log(
                    access_url=access_url,
                    app_name=app_name,
                    user_name=user_name,
                    ip=ip,
                    refer_url=refer_url,
                    user_agent=user_agent,
                    access_time=datetime.datetime.now()
                )
