# coding: utf-8

from django.views.generic import ListView, View
from django.db import transaction

from Brick.App.job_hunting.models import (
    RecommendJob as ReceiveResume,
)
from Brick.App.notify.notify_utils import (
    NotifyUtils,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.django_utils import (
    JsonResponse,
)


class ReceiveJobList(LoginRequiredMixin, ListView):

    template_name = 'feed_receive_resume.html'
    context_object_name = 'receive_resumes'

    def get_queryset(self):
        feed_status = self.request.GET.get('feed_status', '')
        user = self.request.user
        query = {
            'hr_user': user,
            'action': 'send',
            'company_delete': False,
        }
        if feed_status == 'waiting':
            query['company_action'] = 'waiting'

        receive_list = ReceiveResume.objects.select_related(
            'resume',
            'resume__expectation_area',
            'resume__works',
            'resume__educations',
            'resume__user',
        ).filter(
            **query
        )
        return receive_list


class ResumeUnfit(LoginRequiredMixin, View):
    '''
    简历不合适
    '''

    def get(self, request, job_id):
        user = request.user

        receive_resume_query = ReceiveResume.objects.filter(
            hr_user=user,
            id=job_id,
            action='send',
            company_action='waiting',
        ).select_related(
            'job',
            'resume',
        )
        if receive_resume_query:
            with transaction.atomic():
                receive_resume = receive_resume_query[0]
                receive_resume.company_action = 'unfit'
                receive_resume.save()
                NotifyUtils.company_notify(receive_resume, 'fail')

        return JsonResponse({
            'status': 'ok',
            'msg': '操作成功',
        })
