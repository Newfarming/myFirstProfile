# coding: utf-8

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import Http404
from django.db.models import Q, Max

from .models import (
    ChatMessage,
    Chat,
)
from .chat_utils import (
    ChatUtils,
)
from Brick.App.job_hunting.models import (
    RecommendJob,
    CompanyCardJob,
)

from Brick.Utils.mixin_utils import (
    LoginRequiredMixin,
    MaliceMixin,
)
from Brick.Utils.AjaxView import PaginatedJSONListView
from Brick.Utils.django_utils import (
    JsonResponse
)


class ChatDetail(LoginRequiredMixin, View):

    template_name = 'brick_chat_detail.html'

    def get(self, request, chat_id):
        user = request.user
        chat = Chat.objects.select_related(
            'resume',
            'job',
            'feed',
        ).filter(
            id=chat_id
        ).filter(
            Q(hr=user) | Q(job_hunter=user)
        )

        if chat:
            return render(
                request,
                self.template_name,
                {
                    'chat': chat[0],
                },
            )
        else:
            raise Http404


class ChatMsgList(LoginRequiredMixin, PaginatedJSONListView):

    model = ChatMessage
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        chat_id = self.kwargs.get('chat_id', '0')
        user = self.request.user
        chat = Chat.objects.filter(
            id=chat_id
        ).filter(
            Q(hr=user) | Q(job_hunter=user)
        )
        if not chat:
            return []

        chat_messages = ChatMessage.objects.filter(
            chat=chat[0],
        ).filter(
            Q(sender=user) & Q(sender_delete=False) | Q(receiver=user) & Q(receiver_delete=False)
        ).values(
            'sender',
            'receiver',
            'msg',
            'send_time',
        ).order_by('-id')

        ChatMessage.objects.filter(
            chat=chat[0],
            receiver=user,
            receiver_delete=False
        ).update(
            receiver_read=True
        )

        return chat_messages

    def get_context_data(self, **kwargs):
        context = super(ChatMsgList, self).get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context


class SendMsg(LoginRequiredMixin, View, MaliceMixin):

    MAX_ERROR_TIMES = 3
    EXPIRE_SECOND = 60
    MALICE_IP_PREFIX = 'SEND_MSG_MALICE_IP'

    def post(self, request, chat_id):
        msg = self.request.POST.get('msg', '')

        if not msg:
            return JsonResponse({
                'status': 'msg_error',
                'msg': u'不能为空',
            })

        chat_id = self.kwargs['chat_id']
        user = self.request.user
        chat_query = Chat.objects.filter(
            id=chat_id
        ).filter(
            Q(hr=user) | Q(job_hunter=user)
        )
        if not chat_query:
            return JsonResponse({
                'status': 'data_error',
                'msg': u'数据有误',
            })

        if self.malice_ip():
            return JsonResponse({
                'status': 'malice_ip',
                'msg': '注册太频繁了，请稍后再试',
            })

        chat = chat_query[0]
        if user == chat.hr:
            receiver = chat.job_hunter
        else:
            receiver = chat.hr
        chat_message = ChatMessage(
            chat=chat,
            sender=user,
            receiver=receiver,
            msg=msg,
        )
        chat_message.save()
        return JsonResponse({
            'status': 'ok',
            'msg': u'发送成功',
            'data': {
                'send_time': chat_message.send_time.strftime('%Y-%m-%d %H:%M:%S'),
                'id': chat_message.id,
            },
        })


class ChatBox(LoginRequiredMixin, PaginatedJSONListView):

    template_name = 'brick_chat_box.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        chats = Chat.objects.select_related(
            'resume',
            'job',
            'feed',
        ).filter(
            Q(job_hunter=user) | Q(hr=user)
        ).values(
            'id',
            'job_hunter',
            'hr',
            'job__company__company_name',
            'job__title',
            'job__salary_low',
            'job__salary_high',
            'job__work_years',
            'job__degree',
            'create_time',
            'chat_type',
            'feed__company__company_name',
            'feed__title',
            'feed__salary_min',
            'feed__salary_max',
            'feed__work_years_min',
            'feed__work_years_max',
            'feed__deleted',
        ).order_by('-id')
        return chats


class HistoryList(LoginRequiredMixin, PaginatedJSONListView):

    template_name = 'brick_history_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        query_user = (
            Q(sender=user) & Q(sender_delete=False)
            | Q(receiver=user) & Q(receiver_delete=False)
        )
        lastest_chat_set = ChatMessage.objects.filter(
            query_user
        ).values(
            'chat',
        ).annotate(
            max_date=Max('send_time')
        )

        q_statement = Q()
        for p in lastest_chat_set:
            q_statement |= (Q(chat__exact=p['chat']) & Q(send_time=p['max_date']))
        last_chat = ChatMessage.objects.select_related(
            'chat'
        ).filter(
            q_statement
        ).filter(
            query_user
        ).values(
            'chat__id',
            'chat__job_hunter',
            'chat__hr',
            'chat__job__company__company_name',
            'chat__job__title',
            'chat__job__salary_low',
            'chat__job__salary_high',
            'chat__job__work_years',
            'chat__job__degree',
            'chat__create_time',
            'chat__chat_type',
            'chat__feed__company__company_name',
            'chat__feed__title',
            'chat__feed__salary_min',
            'chat__feed__salary_max',
            'chat__feed__work_years_min',
            'chat__feed__work_years_max',
            'chat__feed__degree',
            'msg',
            'receiver_read',
            'receiver',
        ).order_by('-id')
        return last_chat

    def get_context_data(self, **kwargs):
        context = super(HistoryList, self).get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context


class StartJobChat(LoginRequiredMixin, View):

    user_type = 'job_hunter'

    def get(self, request, job_id):
        user = request.user
        query_cond = {
            'id': job_id,
            'action': 'send',
            'company_action': 'download',
        }
        if self.user_type == 'job_hunter':
            query_cond['user'] = user
        if self.user_type == 'hr':
            query_cond['hr_user'] = user

        reco_job_query = RecommendJob.objects.filter(
            **query_cond
        )
        if not reco_job_query:
            raise Http404

        reco_job = reco_job_query[0]
        job = reco_job.job
        hr_user = reco_job.hr_user
        job_hunter = reco_job.user
        chat = ChatUtils.add_chat(
            job,
            hr_user,
            job_hunter,
            chat_type='feed'
        )
        return redirect(
            'chat-detail',
            chat_id=chat.id,
        )


class StartCardJobChat(LoginRequiredMixin, View):

    user_type = 'job_hunter'

    def get(self, request, card_job_id):
        user = request.user
        query_cond = {
            'id': card_job_id,
            'status': 'accept',
        }
        if self.user_type == 'job_hunter':
            query_cond['user'] = user
        card_job_query = CompanyCardJob.objects.filter(
            **query_cond
        )
        if not card_job_query:
            raise Http404

        card_job = card_job_query[0]
        job = card_job.job
        hr_user = card_job.job.user
        job_hunter = card_job.user
        chat = ChatUtils.add_chat(job, hr_user, job_hunter)
        return redirect(
            'chat-detail',
            chat_id=chat.id,
        )
