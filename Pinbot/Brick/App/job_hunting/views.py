# coding: utf-8

import datetime
import logging

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.db import transaction
from django.shortcuts import render
from django.http import Http404
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.core.cache import cache

from .models import (
    RecommendJob,
    CompanyCardJob,
)
from .forms import (
    JobMessageForm,
)
from .job_utils import (
    JobUtils,
)
from .exception import CompanyCardInterestExeception
from Brick.App.my_resume.resume_utils import (
    ResumeUtils,
    SaveResumeTag,
    SyncResume,
)
from Brick.App.my_resume.models import (
    SearchTag,
)
from Brick.App.notify.notify_utils import (
    NotifyUtils,
)
from Brick.settings import (
    ACTIVE_URL,
    RESUME_URL,
    SEND_RESUME_URL,
    SUPPORT_EMAIL_LIST,
    RECO_MAX_COUNT,
)

from feed.models import (
    Feed,
    Feed2,
    FeedResult,
)
from jobs.models import (
    Company,
    UserFavourCompany,
)
from app.pinbot_point.point_utils import point_utils

from Brick.Utils.AjaxView import PaginatedJSONListView
from Brick.Utils.mixin_utils import (
    LoginRequiredMixin,
    MaliceMixin,
)
from Brick.Utils.django_utils import (
    get_object_or_none,
    JsonResponse,
    get_oid,
    get_int,
    get_today,
    get_tomorrow,
    get_http_url,
)
from Brick.Utils.email.send_mail import (
    asyn_send_mail,
    asyn_mg_mail,
)

logger = logging.getLogger('brick.exception')


class TagRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        self.resume = resume = ResumeUtils.get_resume(user)
        select_tag_url = reverse('resume-index')

        if not resume.gender:
            return redirect('%s#/%s/' % (select_tag_url, 'select_gender'))
        if not resume.expectation_area.all():
            return redirect('%s#/%s/' % (select_tag_url, 'select_city'))
        if not resume.position_tags.all() or not resume.job_category:
            return redirect('%s#/%s/' % (select_tag_url, 'select_position_category'))
        if not resume.work_years:
            return redirect('%s#/%s/' % (select_tag_url, 'select_work_years'))
        if not resume.degree:
            return redirect('%s#/%s/' % (select_tag_url, 'select_degree'))
        if not resume.salary_lowest:
            return redirect('%s#/%s/' % (select_tag_url, 'select_salary'))
        if not resume.prefer_fields.all():
            return redirect('%s#/%s/' % (select_tag_url, 'select_field'))

        return super(TagRequiredMixin, self).dispatch(request, *args, **kwargs)


class JobIndex(TagRequiredMixin, View):

    template = 'job_index.html'

    def get(self, request):
        user = self.request.user
        tag_dict = SaveResumeTag.get_search_tag_dict(user, self.resume)
        search_tag = SaveResumeTag.get_search_tag(tag_dict, self.resume)

        today = get_today()
        min_reco_time = today + datetime.timedelta(days=-9)
        has_reco_jobs = RecommendJob.objects.filter(
            user=user,
            delete=False,
            read_status='unread',
            action='',
            display=True,
            search_tag=search_tag,
            reco_index__gt=0,
            reco_time__gt=min_reco_time,
        ).exclude(
            job__company__key_points='',
        )
        if not has_reco_jobs:
            SaveResumeTag.send_reco_task(tag_dict, search_tag)

        return render(
            request,
            self.template,
            {}
        )


class LimitDailyRecoMixin(object):

    KEY_PRIFIX = 'DAILY_RECOMMEND_'
    MAX_COUNT = 3
    EXPIRE_TIME = 0

    def get_expire_time(self):
        if self.EXPIRE_TIME:
            return self.EXPIRE_TIME
        expire_time = (get_tomorrow() - get_today()).total_seconds()
        return expire_time

    def get_cache_key(self):
        username = self.request.user.username
        return '%s%s' % (self.KEY_PRIFIX, username)

    def add_reco_times(self, default_times=1):
        cache_key = self.get_cache_key()
        reco_times = cache.get(cache_key, 0)
        reco_times += default_times
        expire_time = self.get_expire_time()
        cache.set(cache_key, reco_times, expire_time)
        return reco_times

    def over_max_times(self):
        cache_key = self.get_cache_key()
        reco_times = cache.get(cache_key, 0)
        return True if reco_times >= self.MAX_COUNT else False


class RecommendJobList(
        LoginRequiredMixin,
        PaginatedJSONListView,
        LimitDailyRecoMixin):

    model = RecommendJob
    context_object_name = 'data'
    paginate_by = 1
    MAX_COUNT = RECO_MAX_COUNT

    def get_recommend_jobs(self, search_tag):
        user = self.request.user
        today = get_today()
        min_reco_time = today + datetime.timedelta(days=-9)
        recommend_jobs = self.model.objects.prefetch_related(
            'job__company__category',
        ).filter(
            user=user,
            delete=False,
            read_status='unread',
            action='',
            display=True,
            search_tag=search_tag,
            reco_index__gt=0,
            reco_time__gt=min_reco_time,
        ).exclude(
            job__company__key_points='',
        ).select_related(
            'job',
            'job__company',
        ).order_by(
            '-search_tag',
            '-reco_index',
            '-reco_time',
        ).values(
            'id',
            'job__expect_area',
            'job__job_desc',
            'job__deleted',
            'job__id',
            'succ_rate',
            'job__title',
            'job__salary_min',
            'job__salary_max',
            'job__work_years_min',
            'job__work_years_max',
            'job__degree',
            'job__job_desc',
            'job__skill_required',
            'job__company__company_name',
            'job__company__key_points',
            'job__company__desc',
            'job__company__pinbot_recommend',
            'job__company__key_points',
            'job__company__favour_count',
            'job__company__id',
            'job__company__company_stage',
            'job__company__url',
            'job__company__product_url',
            'job__company__category',
            'job__job_welfare',
        )
        return recommend_jobs

    def get_queryset(self, *args, **kwargs):
        if self.over_max_times():
            return []

        user = self.request.user
        search_tag_query = SearchTag.objects.filter(
            resume__user=user,
            active=True,
        )
        if not search_tag_query:
            return []
        search_tag = search_tag_query[0]
        recommend_jobs = self.get_recommend_jobs(search_tag)
        return recommend_jobs

    def get_resume_tag(self):
        resume = ResumeUtils.get_resume(self.request.user)
        resume_tag = {
            'job_category': resume.job_category.name if resume.job_category else '',
            'work_years': resume.work_years,
        }
        return resume_tag

    def get_context_data(self, **kwargs):
        context = super(RecommendJobList, self).get_context_data(**kwargs)
        data = context.get('data', [])

        user = self.request.user
        for job in data:
            company_id = job['job__company__id']
            has_favour = True if get_object_or_none(
                UserFavourCompany,
                company__id=company_id,
                user=user,
            ) else False
            job['has_favour'] = has_favour
            job['job__company__url'] = get_http_url(job['job__company__url'])
            job['job__company__product_url'] = get_http_url(job['job__company__product_url'])

            company_query = Company.objects.filter(
                id=company_id
            )

            if not company_query:
                job['company_category'] = []
                continue
            company = company_query[0]
            job['company_category'] = list(company.category.all().values_list('category', flat=True))
            job['job_welfare'] = [i for i in job['job__job_welfare'].split(',') if i]

        context['resume_tag'] = self.get_resume_tag()
        return context


class JobOperation(LoginRequiredMixin, View, LimitDailyRecoMixin):

    action = 'favorite'
    msg = '收藏成功'

    def extra_operation(self, job, recommend_job):
        return True

    def get(self, request, job_id):
        user = self.request.user
        now = datetime.datetime.now()

        recommend_job = get_object_or_none(
            RecommendJob,
            id=job_id,
            user=user,
        )
        if not recommend_job:
            return JsonResponse({
                'status': 'data_error',
                'msg': u'数据有误',
            })

        if self.action == 'send':
            resume = ResumeUtils.get_resume(user)
            if not SyncResume.is_valid_resume(resume):
                return JsonResponse({
                    'status': 'valid_resume',
                    'msg': '简历不全',
                    'redirect_url': '%s?send=True' % reverse('resume-show-resume'),
                    'operation': self.action,
                })

        job = recommend_job.job

        with transaction.atomic():
            need_add_times = (recommend_job.read_status == 'unread')
            recommend_job.read_status = 'read'
            recommend_job.action = self.action
            recommend_job.action_time = now
            recommend_job.company_action_time = now
            recommend_job.save()
            self.extra_operation(job, recommend_job)

            if need_add_times:
                self.add_reco_times()

        return JsonResponse({
            'status': 'ok',
            'msg': self.msg,
            'operation': self.action,
        })


class JobSend(JobOperation):
    action = 'send'
    msg = '投递成功'

    MAX_GRANT_COUNT = 10

    def need_grant_feed(self, job_manage):
        '''
        检查赠送爬取的定制数量是否大于最大赠送定制数MAX_GRANT_COUNT
        '''
        hr_user = job_manage.hr_user
        total_feed_count = Feed.objects.filter(
            deleted=False,
            display=True,
            user=hr_user,
        ).count()
        return False if total_feed_count > self.MAX_GRANT_COUNT else True

    def check_grant_feed(self, job_manage):
        hr_user = job_manage.hr_user
        total_feed_count = Feed.objects.filter(
            deleted=False,
            display=True,
            user=hr_user,
        ).count()

        if total_feed_count > self.MAX_GRANT_COUNT:
            hr_user.receive_jobs.filter(
                job__job_type=2
            ).update(
                display=False
            )
        return True

    def email_notify_user(self, feed, job_manage, resume):
        hr_user = feed.user
        email = hr_user.username
        if not hr_user.is_active:
            # 发送激活邮件
            token = default_token_generator.make_token(hr_user)
            hr_user.userprofile.activation_key = token
            hr_user.userprofile.save()

            html = render_to_string(
                'new_user_get_resume.html',
                {
                    'company_name': feed.company.company_name if feed.company else u'尊敬的客户',
                    'title': feed.title,
                    'active_url': ACTIVE_URL.format(token=token),
                },
            )
            asyn_send_mail.delay(
                email,
                '聘宝为您推荐合适的求职者',
                html,
            )
            asyn_mg_mail.delay(
                SUPPORT_EMAIL_LIST,
                u'聘宝为%s推荐合适的求职者' % hr_user.username,
                html,
            )
        else:
            # 发送新投递邮件
            html = render_to_string(
                'old_user_get_resume.html',
                {
                    'title': feed.title,
                    'resume_url': RESUME_URL.format(
                        resume_id=resume.resume_id,
                        job_id=job_manage.id,
                    ),
                    'send_resume_url': SEND_RESUME_URL,
                }
            )
            asyn_send_mail.delay(
                email,
                '你收到了新的简历投递',
                html,
            )
            asyn_mg_mail.delay(
                SUPPORT_EMAIL_LIST,
                u'新的投递%s' % hr_user.username,
                html,
            )
        return True

    def add_user_charge_pkg(self, feed):
        user_feed_query = feed.userfeed_set.all()

        if not user_feed_query:
            return False

        user_feed = user_feed_query[0]
        user_charge_pkg = user_feed.user_charge_pkg
        if not user_charge_pkg:
            return False

        user_charge_pkg.extra_feed_num += 1
        user_charge_pkg.save()
        return True

    def make_feed_display(self, job, job_manage):
        if job.display or job.feed_type == 1:
            return True

        if not self.need_grant_feed(job_manage):
            return True

        feed_oid = get_oid(job.feed_obj_id)
        mongo_feed = Feed2.objects.filter(
            id=feed_oid,
        ).first()

        job.display = True
        job.save()

        mongo_feed.display = True
        mongo_feed.save()
        self.add_user_charge_pkg(job)
        self.check_grant_feed(job_manage)
        return True

    def add_feed_result(self, job, user, resume):
        now = datetime.datetime.now()
        feed_oid = get_oid(job.feed_obj_id)
        resume_oid = get_oid(resume.resume_id)
        feed_result = FeedResult.objects.filter(
            feed=feed_oid,
            resume=resume_oid,
        )
        if feed_result:
            return False

        feed_result = FeedResult(
            feed=feed_oid,
            resume=resume_oid,
            is_recommended=True,
            published=True,
            display_time=now,
            feed_source='brick',
        )
        feed_result.save()
        return feed_result

    def extra_operation(self, job, job_manage):
        job_manage.company_action = 'waiting'
        job_manage.hr_user = job.user
        job_manage.save()

        user = self.request.user
        resume = ResumeUtils.get_resume(user)

        self.add_feed_result(job, user, resume)
        point_utils.send_resume(job_manage.hr_user)
        self.make_feed_display(job, job_manage)
        self.email_notify_user(job, job_manage, resume)
        NotifyUtils.send_resume_notify(job_manage)
        return True


class MyJobList(LoginRequiredMixin, PaginatedJSONListView):

    model = RecommendJob
    context_object_name = 'data'
    paginate_by = 3

    def get_queryset(self):
        job_action = self.kwargs['action']
        user = self.request.user
        my_jobs = self.model.objects.filter(
            user=user,
            action=job_action,
            delete=False,
            display=True,
        ).select_related(
            'job',
            'job__company',
        ).values(
            'id',
            'job__expect_area',
            'job__job_desc',
            'job__deleted',
            'job__id',
            'succ_rate',
            'job__title',
            'job__salary_min',
            'job__salary_max',
            'job__work_years_min',
            'job__work_years_max',
            'job__degree',
            'job__job_desc',
            'job__skill_required',
            'job__company__company_name',
            'job__company__key_points',
            'job__company__desc',
            'job__company__company_stage',
            'job__company__url',
            'job__company__product_url',
            'job__company__id',
            'action',
            'company_action',
            'action_time',
            'company_action_time',
            'id',
        ).order_by(
            '-action_time',
        )
        return my_jobs

    def get_context_data(self, **kwargs):
        context = super(MyJobList, self).get_context_data(**kwargs)
        data = context.get('data', [])

        for job in data:
            company_id = job['job__company__id']
            company_query = Company.objects.prefetch_related(
                'category'
            ).filter(
                id=company_id
            )

            if not company_query:
                job['company_category'] = []
                continue
            company = company_query[0]
            job['company_category'] = [i.category for i in company.category.all()]
        return context


class DeleteMyJob(View):

    def get(self, request, job_id):
        user = request.user
        with transaction.atomic():
            RecommendJob.objects.filter(
                user=user,
                id=job_id,
                company_action__in=['no_reply', 'unfit'],
            ).update(
                delete=True,
            )
        return JsonResponse({
            'status': 'ok',
            'msg': '删除成功',
        })


class LeaveMessage(LoginRequiredMixin, View, MaliceMixin):

    MAX_ERROR_TIMES = 5
    EXPIRE_SECOND = 60 * 60 * 24
    MALICE_IP_PREFIX = 'LEAVE_MSG_MALICE_IP'

    def post(self, request):
        form = JobMessageForm(request.POST)

        if form.is_valid():

            if self.malice_ip():
                return JsonResponse({
                    'status': 'malice',
                    'msg': u'操作太频繁啦，稍后再试试！'
                })

            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            return JsonResponse({
                'status': 'ok',
                'msg': '留言成功'
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class CardJobList(LoginRequiredMixin, PaginatedJSONListView):
    context_object_name = 'data'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        card_job_list = CompanyCardJob.objects.select_related(
            'job',
        ).filter(
            user=user,
            delete=False,
        ).values(
            'id',
            'job__title',
            'job__salary_low',
            'job__salary_high',
            'job__work_years',
            'job__address',
            'job__degree',
            'job__key_points',
            'job__desc',
            'job__skill_desc',
            'job__company__company_name',
            'job__company__key_points',
            'job__company__desc',
            'job__company__company_stage',
            'job__company__url',
            'job__company__product_url',
            'job__company__id',
            'send_time',
            'status',
        ).order_by(
            '-id',
        )
        return card_job_list

    def get_context_data(self, **kwargs):
        context = super(CardJobList, self).get_context_data(**kwargs)
        data = context.get('data', [])

        for job in data:
            company_id = job['job__company__id']
            company_query = Company.objects.prefetch_related(
                'category'
            ).filter(
                id=company_id
            )

            if not company_query:
                job['company_category'] = []
                continue
            company = company_query[0]
            job['company_category'] = [i.category for i in company.category.all()]
        return context


class CardJobAction(LoginRequiredMixin, View):
    action = ''
    msg = ''

    def get(self, request, card_id):
        user = request.user
        card_job = get_object_or_none(
            CompanyCardJob,
            user=user,
            id=card_id,
        )
        if card_job:
            card_job.status = self.action
            try:
                JobUtils.card_feedback(card_job, self.action)
            except CompanyCardInterestExeception:
                logger.error(
                    'company card interst error',
                    exc_info=True,
                    extra={
                        'request': request,
                    }
                )
                return JsonResponse({
                    'status': 'exception',
                    'msg': '网络错误, 请稍后再试'
                })

            card_job.save()
            NotifyUtils.card_job_notify(card_job, self.action)

        return JsonResponse({
            'status': 'ok',
            'msg': self.msg,
        })


class DeleteCardJob(LoginRequiredMixin, View):

    action = ''
    msg = ''

    def get(self, request, card_id):
        user = self.request.user
        CompanyCardJob.objects.filter(
            user=user,
            id=card_id,
        ).update(
            delete=self.action
        )
        return JsonResponse({
            'status': 'ok',
            'msg': self.msg,
        })


class JobCardDetailMixin(object):

    def get_card_context(self, job, job_type='job'):
        '''
        为了兼容Feed和企业名片
        job_type: job是企业名片
                  feed 是专属定制
        '''
        user = self.request.user

        return {
            'pinbot_recommend': job.company.pinbot_recommend if job.company else '',
            'key_points': job.company.key_points if job.company else '',
            'company_desc': job.company.desc if job.company else '',
            'company_name': job.company.company_name if job.company else '',
            'address': job.address if job_type == 'job' else job.expect_area,
            'title': job.title,
            'salary_low': job.salary_low if job_type == 'job' else job.salary_min,
            'salary_high': job.salary_high if job_type == 'job' else job.salary_max,
            'desc': job.desc if job_type == 'job' else job.job_desc,
            'skill_desc': job.skill_desc if job_type == 'job' else job.skill_required,
            'product_url': get_http_url(job.company.product_url) if job.company else '',
            'url': get_http_url(job.company.url) if job.company else '',
            'company_stage': job.company.url if job.company else '',
            'company_category': [i.category for i in job.company.category.all()] if job.company else [],
            'company_id': job.company.id if job.company else '',
            'company_favour_count': job.company.favour_count if job.company else '',
            'has_favour': True if job.company and get_object_or_none(UserFavourCompany, company__id=job.company.id, user=user) else False,
            'job_welfare': [] if job_type == 'job' else [i for i in job.job_welfare.split(',') if i],
        }


class JobDetail(LoginRequiredMixin, View, JobCardDetailMixin):

    model = RecommendJob
    template = 'job_detail.html'

    def get(self, request, job_id):
        user = request.user
        recommend_job_query = self.model.objects.filter(
            user=user,
            id=job_id,
        ).select_related(
            'job',
            'job__company',
        )
        if not recommend_job_query:
            raise Http404

        job_detail = recommend_job_query[0]
        context = self.get_card_context(job_detail.job, job_type='feed')
        return render(
            request,
            self.template,
            context,
        )


class JobCardDetail(LoginRequiredMixin, View, JobCardDetailMixin):

    model = CompanyCardJob
    template = 'job_detail.html'

    def get(self, request, job_card_id):
        user = request.user
        job_card_query = self.model.objects.filter(
            user=user,
            id=job_card_id,
        )
        if not job_card_query:
            raise Http404

        job_detail = job_card_query[0]
        context = self.get_card_context(job_detail.job)
        return render(
            request,
            self.template,
            context,
        )


class MarkRecommendJobRead(LoginRequiredMixin, View, LimitDailyRecoMixin):

    def post(self, request):
        job_id_list = request.POST.getlist('job_id_list[]', [])
        job_id_list = [i for i in [get_int(i) for i in job_id_list] if i]

        if job_id_list:
            user = request.user
            read_count = RecommendJob.objects.filter(
                id__in=job_id_list,
                user=user,
                read_status='unread',
            ).update(
                read_status='read'
            )
            self.add_reco_times(default_times=read_count)
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class FavourCompany(LoginRequiredMixin, View):
    '''
    function: 用户为公司点赞和取消点赞
    '''

    @transaction.atomic
    def get(self, request, company_id):
        company = get_object_or_none(
            Company,
            id=company_id,
        )

        if not company:
            return JsonResponse({
                'status': 'data_error',
                'msg': '数据有误',
            })

        user = request.user
        fav_record = UserFavourCompany.objects.filter(
            company=company,
            user=user,
        )

        if fav_record:
            fav_record.delete()
            company.favour_count -= 1
            action = 'cancel'
        else:
            fav_record = UserFavourCompany(
                company=company,
                user=user,
            )
            fav_record.save()
            company.favour_count += 1
            action = 'favour'
        company.save()

        return JsonResponse({
            'status': 'ok',
            'msg': '操作成功',
            'data': {
                'action': action,
            }
        })
