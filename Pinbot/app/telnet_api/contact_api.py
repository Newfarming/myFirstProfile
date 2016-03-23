# coding: utf-8

import logging

from django.views.generic.base import View

from .forms import contact_forms

from pin_utils.mixin_utils import (
    SpiderTokenRequiredMixin,
    CSRFExemptMixin,
)
from pin_utils.django_utils import (
    JsonResponse,
)

logger = logging.getLogger('django')


class UpdateContactInfo(
        CSRFExemptMixin,
        SpiderTokenRequiredMixin,
        View):

    STAFF = True
    form_cls = contact_forms.ContactInfoForm

    def post(self, request):
        form = self.form_cls(request.POST)

        if form.is_valid():
            form.save()
            ret = {
                'status': 'ok',
                'msg': 'ok',
            }
        else:
            ret = {
                'status': 'form_error',
                'msg': u'表单错误',
                'errors': form.errors,
            }
        logger.info(
            """
            update_contact_api: user {0} request_data {1} ret {2}
            """.format(self.request.user.username, request.POST, ret)
        )
        return JsonResponse(ret)
