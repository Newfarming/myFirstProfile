# coding: utf-8

from ..models import UserVip

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)


class SelfServiceList(LoginRequiredMixin, PaginatedJSONListView):

    context_object_name = 'data'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        queryset = UserVip.objects.select_related(
            'user',
            'vip_role',
        ).filter(
            user=user,
        ).order_by('-id')
        return queryset

    def get_json_data(self, context):
        data = context.get('data', [])
        json_data = [
            {
                'id': user_vip.id,
                'name': user_vip.vip_role.vip_name,
                'pinbot_point': user_vip.vip_role.pinbot_point,
                'feed_count': user_vip.vip_role.feed_count,
                'active_time': user_vip.active_time.strftime('%Y-%m-%d %H:%M'),
                'expire_time': user_vip.expire_time.strftime('%Y-%m-%d %H:%M'),
                'is_active': user_vip.is_active,
            }
            for user_vip in data
        ]
        return json_data

    def get_context_data(self, *args, **kwargs):
        context = super(SelfServiceList, self).get_context_data(*args, **kwargs)
        context['data'] = self.get_json_data(context)
        return context
