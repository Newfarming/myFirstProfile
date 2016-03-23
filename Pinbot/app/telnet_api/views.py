# coding: utf-8

from notifications import notify
from tokenapi.tokens import token_generator
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
)

from feed.models import Feed
from resumes.models import ResumeData
from pin_utils.django_utils import JsonResponse
from pin_utils.mixin_utils import (
    SpiderTokenRequiredMixin,
    CSRFExemptMixin,
)


class SendNotify(SpiderTokenRequiredMixin, View):

    def get(self, request):

        user_id = request.GET.get('user')
        resume_buy_result = request.GET.get('status')
        resume_id = request.GET.get('resume_id')
        feed_id = request.GET.get('feed_id')

        resume = ResumeData.objects(id=resume_id)
        resume_works = resume[0].works if resume else None
        latest_job = resume_works[0].position_title if resume_works else "查看详情"

        feed_query = Feed.objects.filter(feed_obj_id=feed_id)
        feed_title = feed_query[0].title if feed_query else None

        if feed_title:
            notify_verb = '简历下载完成：{feed_title}(<a class="c0091fa" href="/resumes/display/{resume_id}/?feed_id={feed_id}">{notify_text}</a>)'.format(
                feed_title=feed_title,
                resume_id=resume_id,
                feed_id=feed_id,
                notify_text=latest_job
            )
        else:
            notify_verb = '简历下载完成：(<a class="c0091fa" href="/resumes/display/{resume_id}/?feed_id={feed_id}">{notify_text}</a>)'.format(
                resume_id=resume_id,
                feed_id=feed_id,
                notify_text=latest_job
            )
        user_query = User.objects.filter(id=int(user_id))

        if not user_query:
            return JsonResponse({
                'status': 0
            })
        if resume_buy_result == '1':
            notify.send(
                user_query[0],
                recipient=user_query[0],
                verb=notify_verb,
                user_role='hr',
                notify_type='resume_download_finished'
            )
            return JsonResponse({
                'status': 'ok'
            })
        return JsonResponse({
            'status': 'not notify'
        })


class GetToken(CSRFExemptMixin, View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return JsonResponse({
                'status': 'error',
                'msg': 'error user'
            })

        if not user.user_permissions.filter(codename='spider_msg').exists():
            return JsonResponse({
                'status': 'error',
                'msg': 'no permission'
            })

        login(request, user)
        auth_info = {
            'token': token_generator.make_token(user),
            'user': user.pk,
        }

        return JsonResponse({
            'status': 'ok',
            'msg': 'success',
            'username': username,
            'auth_info': auth_info
        })
