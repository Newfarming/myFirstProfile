# coding: utf-8

from django.views.generic import View

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    get_oid,
    JsonResponse,
)

from FeedCelery.celery_utils import CeleryUtils


class AdminSendRecoTask(StaffRequiredMixin, View):

    def get(self, request, feed_id):
        feed_id = str(get_oid(feed_id))
        if not feed_id:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的定制数据',
            })

        ret = CeleryUtils.admin_send_reco_task(feed_id)

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'task_id': ret.task_id,
        })
