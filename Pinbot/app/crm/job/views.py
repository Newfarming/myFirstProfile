# coding: utf-8

from django.http import Http404
from django.views.generic import View
from django.shortcuts import render

from .forms import (
    CRMFeedRemarkForm,
)

from feed.models import (
    Feed,
)

from pin_utils.mixin_utils import (
    StaffRequiredMixin,
)
from pin_utils.django_utils import (
    get_int,
    JsonResponse,
)


class JobDetail(StaffRequiredMixin, View):

    template_name = 'job/detail.html'

    def get(self, request, feed_id):
        job_query = Feed.objects.select_related(
            'user',
            'user__userprofile',
            'company',
        ).prefetch_related(
            'crm_remarks',
            'crm_remarks__admin',
        ).filter(
            id=feed_id,
        )

        if not job_query:
            raise Http404

        job = job_query[0]

        return render(
            request,
            self.template_name,
            {
                'job': job,
            }
        )


class ChangeRecruitNum(StaffRequiredMixin, View):

    def get(self, request, feed_id):
        count = get_int(request.GET.get('recruit_num', ''))

        if not count:
            return JsonResponse({
                'status': 'count_error',
                'msg': '招聘数量必须大于0',
            })

        Feed.objects.filter(
            id=feed_id,
        ).update(
            recruit_num=count,
        )

        return JsonResponse({
            'status': 'ok',
            'msg': '修改成功',
        })


class AddFeedRemark(StaffRequiredMixin, View):

    def post(self, request):
        form = CRMFeedRemarkForm(request.POST)

        if form.is_valid():
            remark = form.save(commit=False)
            remark.admin = request.user
            remark.save()

            return JsonResponse({
                'status': 'ok',
                'msg': '添加成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })
