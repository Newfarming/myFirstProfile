# coding: utf-8

from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404

from .mixin import (
    ResumeInfoMixin,
    CommentInfoMixin,
    ContactInfoMixin,
    QueryAPIMixin,
)
from ..forms import (
    category_forms,
)

from transaction.models import (
    ResumeBuyRecord,
    BuyResumeCategory,
)
from resumes.models import (
    UserWatchResume,
)
from jobs.models import (
    SendCompanyCard,
)

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    CSRFExemptMixin,
)
from pin_utils.django_utils import (
    get_int,
    JsonResponse,
)


class ResumeCenter(LoginRequiredMixin, TemplateView):
    template_name = 'resume_center/resume_center.html'


class ResumeBuyRecordList(
        LoginRequiredMixin,
        PaginatedJSONListView,
        CommentInfoMixin,
        ContactInfoMixin,
        QueryAPIMixin,
        ResumeInfoMixin):

    context_object_name = 'data'
    paginate_by = 10

    def query_mark(self):
        all_mark = (
            'invite_interview',
            'break_invite',
            'next_interview',
            'send_offer',
            'entry',
            'no_will',
            'eliminate',
            'pending',
            'unmark',
            'interview_stage',
            'unconfirm',
            'entry_stage',
        )
        mark = self.request.GET.get('mark', '')
        if mark not in all_mark:
            return {}
        if mark == 'unmark':
            return {'resume_mark': None, 'status': 'LookUp'}
        if mark == 'interview_stage':
            return {
                'resume_mark__current_mark__code_name__in': ['unconfirm', 'break_invite', 'invite_interview', 'next_interview', 'join_interview']
            }
        if mark == 'invite_interview':
            return {
                'resume_mark__current_mark__code_name__in': ['invite_interview', 'next_interview', 'join_interview']
            }
        if mark == 'entry_stage':
            return {
                'resume_mark__current_mark__code_name__in': ['entry', 'send_offer'],
            }
        return {'resume_mark__current_mark__code_name': mark}

    def query_category(self):
        category = self.request.GET.get('category', '')
        if not category:
            return {}
        return {'resume_categories__category_name': category}

    def get_resume_id_str(self):
        user = self.request.user
        resume_id_list = list(ResumeBuyRecord.objects.filter(
            user=user,
        ).values_list('resume_id', flat=True))
        resume_id_str = ','.join(resume_id_list)
        return resume_id_str

    def get_query_cond(self):
        query_cond = {}
        query_cond.update(self.query_mark())
        query_cond.update(self.query_category())
        query_cond.update(self.query_api())
        return query_cond

    def get_queryset(self):
        user = self.request.user
        query_cond = self.get_query_cond()

        queryset = ResumeBuyRecord.objects.select_related(
            'resume_mark',
            'resume_mark__current_mark',
            'interview_alarm',
        ).filter(
            user=user,
            **query_cond
        ).order_by('-id')
        return queryset

    def get_interview_info(self, record):
        if not hasattr(record, 'interview_alarm'):
            return {}

        interview_alarm = record.interview_alarm
        ret = {
            'id': interview_alarm.id,
            'interview_count': interview_alarm.interview_count,
            'interview_time': interview_alarm.interview_time.strftime('%Y-%m-%d %H:%M'),
        }
        return ret

    def get_dict_data(self, data):
        dict_data = [
            {
                'id': record.id,
                'op_time': record.op_time.strftime('%Y-%m-%d %H:%M'),
                'status': record.status,
                'status_display': record.get_status_display(),
                'feed_id': record.feed_id,
                'resume_id': record.resume_id,
                'current_mark_display': record.resume_mark.current_mark.name if hasattr(record, 'resume_mark') else '',
                'current_mark': record.resume_mark.current_mark.code_name if hasattr(record, 'resume_mark') else '',
                'mark_time': record.resume_mark.mark_time.strftime('%Y-%m-%d %H:%M') if hasattr(record, 'resume_mark') else '',
                'interview': self.get_interview_info(record),
            }
            for record in data
        ]
        return dict_data

    def get_context_data(self, *args, **kwargs):
        context = super(ResumeBuyRecordList, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])

        user = self.request.user
        resume_id_list = [record.resume_id for record in data]
        buy_resume_id_list = [record.resume_id for record in data if record.status == 'LookUp']

        contact_info_mapper = self.get_contact_info_mapper(buy_resume_id_list)
        resume_info_mapper = self.get_resume_info_mapper(resume_id_list)
        comment_info_mapper = self.get_comment_info_mapper(user, resume_id_list)

        dict_data = self.get_dict_data(data)
        for record in dict_data:
            resume_id = record['resume_id']
            record['contact_info'] = contact_info_mapper.get(resume_id, {})
            record['resume'] = resume_info_mapper.get(resume_id, {})
            record['comment_info'] = comment_info_mapper.get(resume_id, [])

        context['data'] = dict_data
        context['status'] = 'ok'
        context['msg'] = 'ok'
        return context


class CreateBuyRecordCategory(CSRFExemptMixin, LoginRequiredMixin, View):

    form_cls = category_forms.CreateBuyRecordCategoryForm

    def post(self, request):
        form = self.form_cls(request.JSON)

        if form.is_valid():
            user = request.user
            category = form.save(commit=False)
            category.user = user
            category.save()

            return JsonResponse({
                'status': 'ok',
                'msg': '创建成功',
                'data': {
                    'id': category.id
                }
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class UpdateBuyRecordCategory(CSRFExemptMixin, LoginRequiredMixin, View):

    form_cls = category_forms.UpdateBuyRecordCategoryForm

    def post(self, request, category_id):
        user = request.user
        category = get_object_or_404(
            BuyResumeCategory,
            id=category_id,
            user=user
        )
        form = self.form_cls(request.JSON, instance=category)

        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'ok',
                'msg': '更新成功',
                'data': {
                    'id': category.id
                }
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class DeleteBuyRecordCategory(LoginRequiredMixin, View):

    def get(self, request, category_id):
        user = request.user
        BuyResumeCategory.objects.filter(
            user=user,
            id=category_id,
        ).delete()
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class BaseCategoryResume(CSRFExemptMixin, LoginRequiredMixin, View):

    def action(self, category, resume_list):
        pass

    def post(self, request, category_id):
        record_id_list = request.JSON.get('record_id', [])
        record_id_list = [get_int(i) for i in record_id_list if get_int(i)]

        if not record_id_list:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择需要分类的简历',
            })

        user = request.user
        category = get_object_or_404(
            BuyResumeCategory,
            user=user,
            id=category_id,
        )

        resume_list = list(ResumeBuyRecord.objects.filter(
            id__in=record_id_list,
            user=user,
        ))
        self.action(category, resume_list)

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class CategoryResume(BaseCategoryResume):

    def action(self, category, resume_list):
        ret = category.resumes.add(*resume_list)
        return ret


class RemoveCategoryResume(BaseCategoryResume):

    def action(self, category, resume_list):
        ret = category.resumes.remove(*resume_list)
        return ret


class ResumeSide(LoginRequiredMixin, View):

    def get_mark_count(self):
        user_id = self.request.user.id
        query = ResumeBuyRecord.objects.raw(
            '''
            SELECT
            `transaction_resumebuyrecord`.`id`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` IN ("invite_interview", "next_interview", "join_interview") THEN 1 ELSE 0 END
            ) AS `invite_interview`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "next_interview" THEN 1 ELSE 0 END
            ) AS `next_interview`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "send_offer" THEN 1 ELSE 0 END
            ) AS `send_offer`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "entry" THEN 1 ELSE 0 END
            ) AS `entry`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "eliminate" THEN 1 ELSE 0 END
            ) AS `eliminate`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "no_will" THEN 1 ELSE 0 END
            ) AS `no_will`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "break_invite" THEN 1 ELSE 0 END
            ) AS `break_invite`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "unconfirm" THEN 1 ELSE 0 END
            ) AS `unconfirm`,
            SUM(
            CASE WHEN `system_resumemarksetting`.`code_name` = "pending" THEN 1 ELSE 0 END
            ) AS `pending`,
            SUM(
            CASE WHEN `transaction_resumebuyrecord`.`status` = "LookUp" AND `transaction_downloadresumemark`.`id` is NULL THEN 1 ELSE 0 END
            ) AS `unmark`,
            count(*) AS `total`
            FROM `transaction_resumebuyrecord`
            LEFT OUTER JOIN `transaction_downloadresumemark`
            ON ( `transaction_resumebuyrecord`.`id` = `transaction_downloadresumemark`.`buy_record_id` )
            LEFT OUTER JOIN `system_resumemarksetting`
            ON ( `transaction_downloadresumemark`.`current_mark_id` = `system_resumemarksetting`.`id` )
            WHERE `transaction_resumebuyrecord`.`user_id` = %s
            ''',
            [user_id]
        )[0]
        record = {
            'total': query.total,
            'invite_interview': query.invite_interview,
            'next_interview': query.next_interview,
            'send_offer': query.send_offer,
            'entry': query.entry,
            'eliminate': query.eliminate,
            'no_will': query.no_will,
            'pending': query.pending,
            'break_invite': query.break_invite,
            'unconfirm': query.unconfirm,
            'unmark': query.unmark,
        }
        record = {
            key: get_int(value)
            for key, value in record.items()
        }
        return record

    def get_resume_categories(self):
        user_id = self.request.user.id
        category_query = BuyResumeCategory.objects.raw(
            '''
            SELECT `transaction_buyresumecategory`.`id`,
            `transaction_buyresumecategory`.`category_name`,
            COUNT(`transaction_buyresumecategory_resumes`.`buyresumecategory_id`) AS `resume_num`
            FROM `transaction_buyresumecategory`
            LEFT OUTER JOIN `transaction_buyresumecategory_resumes`
            ON (`transaction_buyresumecategory`.`id` = `transaction_buyresumecategory_resumes`.`buyresumecategory_id`)
            WHERE `transaction_buyresumecategory`.`user_id` = %s
            GROUP BY `transaction_buyresumecategory`.`id`
            ''',
            [user_id]
        )
        categories = [
            {
                'id': category.id,
                'category_name': category.category_name,
                'resume_num': category.resume_num,
            }
            for category in category_query
        ]
        return categories

    def get_watch_count(self):
        user = self.request.user
        count = UserWatchResume.objects.filter(
            user=user,
            type=1,
        ).count()
        return count

    def get_send_card_count(self):
        user = self.request.user
        count = SendCompanyCard.objects.filter(
            send_user=user,
        ).count()
        return count

    def get(self, request):
        mark_count = self.get_mark_count()
        categories = self.get_resume_categories()
        watch_count = self.get_watch_count()
        send_card_count = self.get_send_card_count()

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'mark_count': mark_count,
                'categories': categories,
                'watch_count': watch_count,
                'send_card_count': send_card_count,
            }
        })
