# coding: utf-8

from django.views.generic import View, ListView
from django.shortcuts import render, redirect

from ..runtime.mail_manage import (
    MailTagsManage
)

from pin_utils.django_utils import (
    JsonResponse,
    get_object_or_none,
    get_int,
    get_float,
)
from pin_utils.mixin_utils import (
    CSRFExemptMixin,
    StaffRequiredMixin
)


class AddTag(StaffRequiredMixin, CSRFExemptMixin, View):
    """添加标签"""
    template_name = 'add_tag.html'

    def get(self, request):
        return render(
            request,
            self.template_name
        )

    def post(self, request):
        form = MailTagsManage(request.POST, request=request)
        if form.is_valid():
            tag_obj = form.add_tag()
            result = {
                'status': 'ok',
                'tag_id': tag_obj.tag_id,
                'tag_name': tag_obj.tag_name,
            }
        else:
            result = {
                'status': 'form_error',
                'msg': form.get_first_errors(),
            }
        return JsonResponse(result)


class EditTag(StaffRequiredMixin, View, MailTagsManage):
    """编辑标签"""
    template_name = 'edit_tag.html'

    def get(self, request, tag_id):

        tag_obj = self.get_tag(id=tag_id)

        return render(
            request,
            self.template_name,
            {
                'tag_obj': tag_obj,
            }
        )

class DeleteTag(StaffRequiredMixin, CSRFExemptMixin, View):
    """删除标签"""

    def post(self, request):
        tag_id = request.POST['tag_id']
        mtm = MailTagsManage()
        if mtm.delete_tablabel(tag_id):
            result = {
                'status': 'ok'
            }
        else:
            result = {
                'status': 'form_error',
            }
        print result
        return JsonResponse(result)