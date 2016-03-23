# coding: utf-8

from django.views.generic import View
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db import transaction

from .mixin import (
    ResumeInfoMixin,
    ContactInfoMixin,
    QueryAPIMixin,
    CommentInfoMixin,
)

from resumes.models import (
    UserWatchResume,
    ResumeData,
    ContactInfoData,
    Comment,
)

from transaction.models import (
    ResumeBuyRecord,
    InterviewAlarm,
    UserResumeFeedback,
)
from transaction.forms import (
    InterviewMarkForm,
    UpdateInterviewAlarmForm,
)
from transaction.mark_views import MarkChoiceMixin
from jobs.models import SendCompanyCard
from app.special_feed.feed_utils import FeedUtils
from app.partner.partner_utils import PartnerCoinUtils, UploadResumeUtils

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.django_utils import (
    get_oid,
    JsonResponse,
    get_object_or_none,
)


class FollowResumeList(
        LoginRequiredMixin,
        PaginatedJSONListView,
        QueryAPIMixin,
        ContactInfoMixin,
        CommentInfoMixin,
        ResumeInfoMixin):

    context_object_name = 'data'
    paginate_by = 6

    def get_resume_id_str(self):
        user = self.request.user
        resume_id_list = list(UserWatchResume.objects.filter(
            user=user,
        ).values_list('resume_id', flat=True))
        resume_id_str = ','.join(resume_id_list)
        return resume_id_str

    def get_query_cond(self):
        query_cond = {}
        query_cond.update(self.query_api())
        return query_cond

    def get_queryset(self):
        user = self.request.user
        query_cond = self.get_query_cond()
        queryset = UserWatchResume.objects.filter(
            user=user,
            type=1,
            **query_cond
        ).order_by('-id')
        return queryset

    def add_resume_info(self, records):
        resume_id_list = [i.resume_id for i in records]
        resume_info_mapper = self.get_resume_info_mapper(resume_id_list)
        for record in records:
            record.resume = resume_info_mapper.get(record.resume_id, {})
        return records

    def get_buy_resume_id_list(self, resume_id_list):
        user = self.request.user
        buy_resume_id_list = list(ResumeBuyRecord.objects.filter(
            user=user,
            resume_id__in=resume_id_list,
            status='LookUp',
        ).values_list('resume_id', flat=True))
        return buy_resume_id_list

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(FollowResumeList, self).get_context_data(*args, **kwargs)
        follow_resume_records = context.get('data', [])
        follow_resume_records = self.add_resume_info(follow_resume_records)
        resume_id_list = [record.resume_id for record in follow_resume_records]
        buy_resume_id_list = self.get_buy_resume_id_list(resume_id_list)
        contact_info_mapper = self.get_contact_info_mapper(buy_resume_id_list)
        comment_info_mapper = self.get_comment_info_mapper(user, resume_id_list)

        ret = [
            {
                'id': i.id,
                'feed_id': i.feed_id,
                'add_time': i.add_time.strftime('%Y-%m-%d %H:%M'),
                'keywords': i.keywords,
                'resume': i.resume,
                'resume_id': i.resume_id,
            }
            for i in follow_resume_records
        ]

        for record in ret:
            resume_id = record['resume_id']
            record['contact_info'] = contact_info_mapper.get(resume_id, {})
            record['comment_info'] = comment_info_mapper.get(resume_id, {})

        context['data'] = ret
        context['status'] = 'ok'
        context['msg'] = 'ok'
        return context


class ResumeDetail(View, MarkChoiceMixin):

    def get_feed_result(self):
        resume_id = self.kwargs.get('resume_id', '')
        feed_id = self.request.GET.get('feed_id', '')
        feed_result = FeedUtils.get_feed_result(feed_id, resume_id)
        return feed_result

    def get_resume(self):
        resume_id = self.kwargs.get('resume_id', '')
        resume_oid = get_oid(resume_id)
        if not resume_oid:
            raise Http404
        resume = ResumeData.objects.filter(id=resume_oid).first()

        if not resume:
            raise Http404
        return resume

    def get_resume_buy_record(self):
        resume_id = self.kwargs.get('resume_id', '')
        user = self.request.user
        buy_record_query = ResumeBuyRecord.objects.select_related(
            'resume_mark',
            'resume_mark__current_mark',
            'interview_alarm',
        ).prefetch_related(
            'resume_mark__mark_logs',
            'resume_mark__mark_logs__mark',
            'resume_mark__mark_logs__user',
        ).filter(
            user=user,
            resume_id=resume_id,
        )
        if not buy_record_query:
            return None

        buy_record = buy_record_query[0]
        return buy_record

    def get_contact_info(self):
        resume_id = self.kwargs.get('resume_id', '')
        contact_info = get_object_or_none(
            ContactInfoData,
            resume_id=resume_id,
        )
        return contact_info

    def get_send_company_card(self):
        resume_id = self.kwargs.get('resume_id', '')
        user = self.request.user
        company_card_query = SendCompanyCard.objects.filter(
            resume_id=resume_id,
            send_user=user
        )
        if not company_card_query:
            return None
        send_company_card = company_card_query[0]
        return send_company_card

    def get_resume_comments(self):
        resume_id = self.kwargs.get('resume_id', '')
        comments = Comment.objects.filter(
            type=1,
            resume_id=resume_id,
        )
        return comments

    def self_upload_resume(self):
        user = self.request.user
        resume_id = self.kwargs.get('resume_id', '')
        return True if UploadResumeUtils.is_self_upload(user, resume_id) else False

    def get_watch_record(self):
        user = self.request.user
        resume_id = self.kwargs.get('resume_id', '')
        watch_resume_query = UserWatchResume.objects.filter(
            resume_id=resume_id,
            user=user,
        )
        watch_resume = watch_resume_query[0] if watch_resume_query else None
        return watch_resume

    def is_user_feed(self):
        user = self.request.user
        feed_id = self.request.GET.get('feed_id', '')
        return FeedUtils.is_user_feed(user, feed_id)

    def get_resume_mark(self, buy_record):
        if not buy_record:
            return None

        mark_choices = self.get_mark_choices(buy_record)
        return mark_choices

    def get_feedback(self):
        user = self.request.user
        resume_id = self.kwargs.get('resume_id', '')

        feedback_query = UserResumeFeedback.objects.select_related(
            'feedback_info',
            'feedback_info__type',
        ).filter(
            resume_id=resume_id,
            user=user,
        )

        if not feedback_query:
            return None

        feedback = feedback_query[0]
        return feedback

    def check_partner_resume(self):
        resume_id = self.kwargs.get('resume_id', '')
        feed_id = self.request.GET.get('feed_id', '')
        ret = PartnerCoinUtils.check_resume(feed_id, resume_id)
        return ret

    def read_feed_result(self, feed_result):
        if not feed_result:
            return False

        request = self.request
        feed_id = self.request.GET.get('feed_id', '')
        resume_id = self.kwargs.get('resume_id', '')

        if request.user.is_staff and feed_result.feed.username != request.user.username:
            read_user = 'admin'
        else:
            read_user = 'user'
        ret = FeedUtils.read_feed(request, feed_id, resume_id, read_user=read_user)
        return ret

    def get(self, request, resume_id, resume_score=None):
        ret = {}
        ret['resume'] = self.get_resume()

        if request.user.is_authenticated():
            ret['feed_result'] = self.get_feed_result()
            ret['send_company_card'] = self.get_send_company_card()
            ret['resume_comments'] = self.get_resume_comments()
            ret['contact_info'] = self.get_contact_info()
            ret['resume_buy_record'] = self.get_resume_buy_record()
            ret['self_upload_resume'] = self.self_upload_resume()
            ret['watch_record'] = self.get_watch_record()
            ret['is_user_feed'] = self.is_user_feed()
            ret['feed'] = ret['is_user_feed']
            ret['resume_mark'] = self.get_resume_mark(ret['resume_buy_record'])
            ret['feedback'] = self.get_feedback()

            self.check_partner_resume()
            self.read_feed_result(ret['feed_result'])

        return render(
            request,
            'resume/detail.html',
            ret,
        )


class SendInterview(LoginRequiredMixin, View):

    def save_interview_alarm(self, buy_record, interview_time):
        if not hasattr(buy_record, 'interview_alarm'):
            interview_alarm = InterviewAlarm(
                buy_record=buy_record,
                interview_time=interview_time,
            )
        else:
            interview_alarm = buy_record.interview_alarm
            interview_alarm.interview_time = interview_time
        interview_alarm.interview_count += 1
        interview_alarm.save()
        return interview_alarm

    @transaction.atomic
    def post(self, request, record_id):
        form = InterviewMarkForm(
            request.POST,
            request=request,
            record_id=record_id
        )

        if form.is_valid():
            mark_record = form.save()
            buy_record = mark_record.buy_record
            interview_time = form.cleaned_data['interview_time']
            self.save_interview_alarm(buy_record, interview_time)
            return JsonResponse({
                'status': 'ok',
                'msg': '安排面试成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': form.get_first_errors(),
                'errors': form.errors,
            })


class ChangeInterviewTime(LoginRequiredMixin, View):

    def post(self, request, record_id):
        user = request.user
        interview_alarm = get_object_or_404(
            InterviewAlarm,
            buy_record__user=user,
            id=record_id,
        )
        form = UpdateInterviewAlarmForm(request.POST, instance=interview_alarm)

        if form.is_valid():
            interview_alarm = form.save(commit=False)
            interview_alarm.has_alarm = False
            interview_alarm.save()

            return JsonResponse({
                'status': 'ok',
                'msg': '修改成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': form.get_first_errors(),
                'errors': form.errors,
            })
