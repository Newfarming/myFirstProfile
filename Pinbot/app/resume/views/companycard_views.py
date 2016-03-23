# coding: utf-8

import datetime

from .mixin import (
    ResumeInfoMixin,
    CommentInfoMixin,
    ContactInfoMixin,
    QueryAPIMixin,
)

from jobs.models import (
    SendCompanyCard,
)
from transaction.models import ResumeBuyRecord

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)


class CompanyCardList(
        LoginRequiredMixin,
        PaginatedJSONListView,
        CommentInfoMixin,
        ContactInfoMixin,
        QueryAPIMixin,
        ResumeInfoMixin):

    context_object_name = 'data'
    paginate_by = 10

    def get_resume_id_str(self):
        user = self.request.user
        resume_id_list = list(SendCompanyCard.objects.filter(
            send_user=user,
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
        queryset = SendCompanyCard.objects.select_related(
            'job',
        ).filter(
            send_user=user,
            **query_cond
        ).order_by('-id')
        return queryset

    def get_buy_resume_id_list(self, resume_id_list):
        user = self.request.user
        buy_resume_id_list = list(ResumeBuyRecord.objects.filter(
            user=user,
            resume_id__in=resume_id_list,
            status='LookUp',
        ).values_list('resume_id', flat=True))
        return buy_resume_id_list

    def get_feedback_display(self, record):
        now = datetime.datetime.now()
        send_time = record.send_time
        feedback_status = record.feedback_status

        if feedback_status == 3 or (feedback_status == 0 and (now - send_time).days > 7):
            feedback = u'候选人无回复'
        else:
            feedback = record.get_feedback_status_display()
        return feedback

    def get_dict_data(self, data):
        dict_data = [
            {
                'id': record.id,
                'resume_id': record.resume_id,
                'feed_id': record.feed_id,
                'has_download': record.has_download,
                'download_status': record.download_status,
                'send_status': record.send_status,
                'send_status_display': record.get_send_status_display(),
                'send_time': record.send_time.strftime('%Y-%m-%d %H:%M'),
                'feedback_status': record.feedback_status,
                'feedback_status_display': self.get_feedback_display(record),
                'feedback_time': record.feedback_time.strftime('%Y-%m-%d %H:%M'),
            }
            for record in data
        ]
        return dict_data

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyCardList, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        user = self.request.user

        resume_id_list = [record.resume_id for record in data]
        buy_resume_id_list = self.get_buy_resume_id_list(resume_id_list)
        contact_info_mapper = self.get_contact_info_mapper(buy_resume_id_list)
        resume_info_mapper = self.get_resume_info_mapper(resume_id_list)
        comment_info_mapper = self.get_comment_info_mapper(user, resume_id_list)

        dict_data = self.get_dict_data(data)
        for record in dict_data:
            resume_id = record['resume_id']
            record['resume'] = resume_info_mapper.get(resume_id, {})
            record['comment'] = comment_info_mapper.get(resume_id, [])
            record['contact_info'] = contact_info_mapper.get(resume_id, {})

        context['data'] = dict_data
        context['status'] = 'ok'
        context['msg'] = 'ok'
        return context
