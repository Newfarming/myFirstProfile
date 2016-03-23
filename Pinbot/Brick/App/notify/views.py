# coding: utf-8

from django.shortcuts import render
from django.views.generic.base import View

from Brick.Utils.AjaxView import PaginatedJSONListView
from Brick.Utils.mixin_utils import (
    LoginRequiredMixin,
)
from Brick.Utils.django_utils import (
    JsonResponse,
    get_int,
)


class NotifyIndex(LoginRequiredMixin, View):

    template_name = 'notify_index.html',

    def get(self, request):
        has_unread = self.request.user.notifications.unread().count()
        return render(
            request,
            self.template_name,
            {
                'has_unread': 'true' if has_unread else 'false',
            }
        )


class NotifyList(LoginRequiredMixin, PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 15
    user_role = ''

    def get_notify_list(self):
        user = self.request.user
        notify_type = self.request.GET.get('notify_type')
        if notify_type == 'unread':
            notify_list = user.notifications.filter(user_role=self.user_role).unread()
        elif notify_type == 'read':
            notify_list = user.notifications.filter(user_role=self.user_role).read()
        elif notify_type == 'all':
            notify_list = user.notifications.filter(user_role=self.user_role)
        elif notify_type in ('upload_resume', 'follow_resume', 'reco_resume_task'):
            notify_list = user.notifications.filter(
                user_role=self.user_role,
                notify_type='partner_%s' % notify_type
            )
        else:
            notify_list = user.notifications.unread()

        notify_list = notify_list.values('id', 'verb', 'timestamp', 'unread')
        return notify_list

    def get_queryset(self, *args, **kwargs):
        notify_list = self.get_notify_list()
        return notify_list


class MarkNotifyRead(LoginRequiredMixin, View):

    def get(self, request, notify_id=None):
        user = request.user
        bat_id = request.GET.getlist('bat_id', [])
        bat_id = [i for i in [get_int(i) for i in bat_id] if i]
        if notify_id:
            query = {'id': notify_id}
        if bat_id:
            query = {'id__in': bat_id}
        else:
            query = {}
        user.notifications.filter(**query).mark_all_as_read()
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class DebugWebSocket(View):

    def get(self, request):
        from ws4redis.publisher import RedisPublisher
        from ws4redis.redis_store import RedisMessage

        redis_publisher = RedisPublisher(
            facility='notify',
            users=('runforever@163.com',),
        )
        message = RedisMessage('Hello World')
        redis_publisher.publish_message(message)

        return JsonResponse({
            'status': 'ok',
        })
