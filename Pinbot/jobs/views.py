# coding:utf-8

from django.db import transaction
from django.core.urlresolvers import reverse

from users.models import User

from jobs.models import (
    Company,
    Job,
    SendCompanyCard,
    CompanyCategory,
)
from .forms import (
    CompanyForm,
)

from app.special_feed.feed_utils import (
    FeedUtils,
)

from django.shortcuts import render, render_to_response, HttpResponse
from datetime import datetime
from resumes.models import ContactInfoData
from transaction.models import ResumeBuyRecord
import json
import base64
from django.views.generic import View
from django.http import Http404
from basic_service.resume_util import produce_return_json
from bson import ObjectId
from pin_celery.models import MarketEmailSendDetail
from transaction.views import buy_resume

from resumes.models import ResumeData
from transaction.views import get_bought_resume, send_buy_email
from basic_service.resume_util import get_contact_info

from Pinbot.settings import COMPANY_CARD_EXPIRE_DAY
from pin_utils.django_utils import get_object_or_none, get_oid
from transaction.models import UserChargePackage

from pin_utils.django_utils import (
    JsonResponse,
    model_to_dict
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    CSRFExemptMixin,
    ResumePointsRequired
)
from Brick.App.job_hunting.job_utils import (
    JobUtils
)

from app.pinbot_point.point_utils import point_utils
from app.vip.vip_utils import VipRoleUtils


def get_waitting(request):
    pic_url = 'http://pinbot.me/static/beta/email'
    http_response = render_to_response("jobs/waitting.html", locals())
    return http_response


class CompanyCardGet(LoginRequiredMixin, View):
    template_name = 'company-card.html'

    def get(self, request):
        user = request.user

        company = Company.objects.select_related(
            'category',
        ).filter(
            user=user
        )
        company_card_dict = {}
        jobs_arr = []
        companycard_css = 'curr'
        company_category = []
        if len(company) >= 1:
            company = company[0]
            company.desc = company.desc.strip()
            company_json = model_to_dict(company)
            company_card_dict['company'] = company_json
            jobs = Job.objects.filter(company=company, deleted=False)
            for job in jobs:
                job_json = model_to_dict(job)
                jobs_arr.append(job_json)
            company_card_dict['jobs'] = jobs_arr
            company_category = company.category.all()
            company_card_dict['select_category'] = [
                {
                    'category': c.category,
                    'id': c.id,
                }
                for c in company_category
            ]

        all_company_category = CompanyCategory.objects.filter(
            display=True,
        ).order_by(
            '-sort',
        )

        select_id_list = [c.id for c in company_category]
        company_card_dict['all_company_category'] = [
            {
                'category': c.category,
                'id': c.id,
                'select': True if c.id in select_id_list else False
            }
            for c in all_company_category
        ]
        company_card_dict['show_mission'] = True if (
            not FeedUtils.has_use_feed(user)
            and VipRoleUtils.get_current_vip(user)
        ) else False
        company_card_json = json.dumps(company_card_dict)
        return render(
            request,
            self.template_name,
            {
                'company_json': company_card_json,
                'companycard_css': companycard_css,
            },
        )


class CompanyCardGetJson(LoginRequiredMixin, ResumePointsRequired, View):
    need_point = 3

    def get(self, request):
        user = request.user
        company = Company.objects.filter(user=user)
        company_card_dict = {}
        company_card_dict['company'] = {}
        company_card_dict['status'] = True
        company_card_dict['data'] = 10
        company_card_dict['error'] = ''
        jobs_arr = []
        if len(company) >= 1:
            company = company[0]
            company.desc = company.desc.strip()
            company_json = model_to_dict(company)
            company_card_dict['company'] = company_json
            company_card_dict['status'] = True
            company_card_dict['data'] = 10
            company_card_dict['error'] = ''
            jobs = Job.objects.filter(company=company, deleted=False)
            for job in jobs:
                job_json = model_to_dict(job)
                jobs_arr.append(job_json)
            company_card_dict['jobs'] = jobs_arr

        return JsonResponse(company_card_dict)


class CompanySave(CSRFExemptMixin, LoginRequiredMixin, View):

    def post(self, request):
        json_data = json.loads(request.body)
        user = request.user
        company_obj = get_object_or_none(
            Company,
            user=user,
        )
        form = CompanyForm(json_data) if not company_obj else CompanyForm(
            json_data, instance=company_obj)

        if form.is_valid():
            company = form.save(commit=False)
            company.user = user
            company.save()
            form.save_m2m()
            redirect_url = '' if FeedUtils.has_use_feed(
                user) else reverse('feed-add-new')
            return JsonResponse({
                "status": "ok",
                "id": company.id,
                'msg': 'ok',
                'redirect_url': redirect_url,
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': form.get_first_errors(),
                'data': {
                    'errors': form.errors,
                }
            })


class JobSave(CSRFExemptMixin, LoginRequiredMixin, View):

    def post(self, request):
        json_data = json.loads(request.body)
        company = Company.objects.get(user=request.user)
        job = Job(**json_data)
        job.company = company
        job.user = request.user
        job.save()
        return JsonResponse({"status": "ok", "id": job.id, 'msg': ''})


class JobDelete(CSRFExemptMixin, LoginRequiredMixin, View):

    def get(self, request, job_id):
        re = Job.objects.get(user=request.user, id=int(job_id))
        re.deleted = True
        re.save()
        return JsonResponse({"status": "ok", 'msg': ''})


class Card(CSRFExemptMixin, View):
    template_name = 'email-card.html'

    def get(self, request, job_id):
        p = request.GET.copy()
        jobs = Job.objects.filter(pk=int(job_id))
        preview = True
        if len(jobs) >= 1:
            job = jobs[0]
            job.salary_low = job.salary_low / 1000
            job.salary_high = job.salary_high / 1000
            job.desc = job.desc.strip()
            skill_desc = job.skill_desc
            job.skill_desc = skill_desc.strip()
            company = job.company
            company_url_encode = base64.b64encode(company.product_url)
            url_encode = base64.b64encode(company.url)
            job_degree = ''
            if job.degree == 0:
                job_degree = '不限'
            elif job.degree == 3:
                job_degree = '大专及以上'
            elif job.degree == 4:
                job_degree = '本科及以上'
            elif job.degree == 7:
                job_degree = '硕士及以上'
            elif job.degree == 10:
                job_degree = '博士及以上'
        return render(
            request,
            self.template_name,
            locals()
        )


class CompanyCardPreview(View):

    def get(self, request, job_id):
        pass


class InterestClick(View):

    """
    @summary: 用户邮件点击反馈
    """
    template_name = ''

    def startProcess(self, p, request):
        http_refer = request.META.get('HTTP_REFERER', None)
        token = p.get('token', '')
        interest = p.get('interest', 'true')
        brick = p.get('brick', '')
        if interest == 'true':
            interest = 1
            self.template_name = 'agree.html'
        else:
            interest = 2
            self.template_name = 'disagree.html'

        detail_id = get_oid(token)
        if detail_id is None:
            raise Http404()

        to_email = ''
        detail = get_object_or_none(MarketEmailSendDetail, id=detail_id)
        if detail is None:
            raise Http404()
        else:
            to_email = detail.to_email
            detail.user_request = str(request)
            detail.click_time = datetime.now()
            card_job_id = detail.info_dict.get('card_job_id', '0')
            detail.save()

        if not http_refer and brick != 'true':
            self.template_name = 'confirm.html'
            return render(
                request,
                self.template_name,
                locals()
            )

        send_infos = SendCompanyCard.objects.filter(
            feedback_status=0, to_email=detail.to_email, job_id=int(detail.info_dict['job_id']))
        if len(send_infos) >= 1:
            send_info = send_infos[0]

            time_elapse_days = (datetime.now() - send_info.send_time).days
            if time_elapse_days >= COMPANY_CARD_EXPIRE_DAY:
                return render(
                    request,
                    self.template_name
                )

            send_info.feedback_status = interest
            send_info.feedback_time = datetime.now()
            if interest == 1:
                result = buy_resume(
                    user=send_info.send_user, resume_id=send_info.resume_id, send_record=send_info, feed_id=send_info.feed_id)
                if result:
                    send_info.points_used = 12
                    send_info.download_status = True
                else:
                    send_info.download_status = False

            send_info.save()
            JobUtils.company_card_interest(
                send_info.job, card_job_id, interest)

        return render(
            request,
            self.template_name,
            locals()
        )

    def post(self, request):
        p = request.POST.copy()
        return self.startProcess(p, request)

    def get(self, request):
        p = request.GET.copy()
        return self.startProcess(p, request)


class CompanyCardSend(CSRFExemptMixin, LoginRequiredMixin, ResumePointsRequired, View):

    """
    @summary: 发送企业名片
    """
    need_point = 3

    def use_points(self, request, points=3):
        user = request.user
        pkg_points, user_points = point_utils.get_user_point(user)
        result, point = point_utils.send_card_point(user, 3)

    def post(self, request):
        info_dict = {}
        p = request.POST.copy()
        user = request.user
        job_id = p.get('job_id', None)
        resume_id = p.get('resume_id', None)
        feed_id = p.get('feed_id', '')

        if not job_id or not resume_id:
            info_dict['status'] = 'fail'
            info_dict['msg'] = 'no job_id or resume_id'
            return JsonResponse(info_dict)
        job = Job.objects.get(id=int(job_id))
        sends = SendCompanyCard.objects.filter(
            send_user=user, resume_id=resume_id, job=job)
        if len(sends) >= 1:
            return JsonResponse({'status': 'error', 'msg': '已经给该求职者发送过该职位'})
        else:
            resume = ResumeData.objects.get(id=ObjectId(resume_id))
            contact_info = get_contact_info(resume_id)
            send_card = SendCompanyCard(
                send_user=user, resume_id=resume_id, job=job)
            send_card.points_used = 3
            send_card.feed_id = feed_id
            with transaction.atomic():
                if contact_info:
                    send_card.to_email = contact_info.email
                    send_card.save()
                    self.use_points(request, points=3)
                else:
                    # 简历未购买，添加一条购买记录
                    send_card.save()
                    self.use_points(request, points=3)

                    pinbot_user = User.objects.get(
                        username='pinbot@hopperclouds.com')
                    record = ResumeBuyRecord(user=pinbot_user, resume_id=resume_id,
                                             op_time=datetime.now(), status='Start', resume_url=resume.url)
                    record.send_card = send_card
                    record.feed_id = feed_id
                    record.save()
                    resume = ResumeData.objects.get(id=ObjectId(resume_id))
                    send_buy_email(
                        user, str(resume_id), resume.source, type='companycard')

            return JsonResponse({'status': 'ok', 'msg': ''})


class ResumeBuy(LoginRequiredMixin, ResumePointsRequired, View):
    need_point = 10

    def get(self, request):
        p = request.GET.copy()
        resume_id = p.get('resume_id', None)
        send_id = p.get('send_id', None)

        send_record = SendCompanyCard.objects.get(id=int(send_id))

        if ResumeBuyRecord.objects.filter(user=request.user, resume_id=resume_id).count():
            json_data = produce_return_json(
                data=2, status=False, error_dict=u'2.已购买过此简历_has bought this resume')
        else:
            result = buy_resume(
                user=request.user, resume_id=resume_id, send_record=send_record)
            if result:
                send_record.points_used = 13
                send_record.has_download = True
                send_record.save()
            else:
                send_record.download_status = False
                send_record.save()
            json_data = produce_return_json(data=8)
        return HttpResponse(json_data, "application/json")


class ResumeFilter(LoginRequiredMixin, View):

    def get(self, request):
        watch_class = 'curr'
        username = request.user.username

        resume_empty = False
        userChargePackages = True if UserChargePackage.objects.order_by(
            '-start_time').filter(user=request.user.id).count() else False

        resume_list = []
        user = request.user
        p = request.GET.copy()
        has_download = p.get('download', None)
        source = p.get('source', None)
        feedback = p.get('feedback', None)

        resume_list2 = get_bought_resume(user)
        for resume, extra_info in resume_list2:
            if is_match(extra_info, download=has_download, source=source, feedback=feedback):
                resume_list.append((resume, extra_info))

        page = "bought_resume"
        from_source = 'filter'
        return render(request, "resumes/bought-list.html", locals())


class CompanyCardTask(View):

    def get(self, request):
        from pin_celery.tasks import send_company_card

        need_sends = SendCompanyCard.objects.filter(send_status=2)[:7]

        for need_send in need_sends:
            job = need_send.job
            company = job.company
            resume_id = need_send.resume_id
            contactinfos = ContactInfoData.objects.filter(
                resume_id=resume_id)
            if len(contactinfos) >= 1:
                need_send.to_email = contactinfos[0].email
                need_send.send_time = datetime.now()

                if contactinfos[0].name == '保密':
                    need_send.send_status = 0
                    need_send.to_email = '保密'
                    need_send.feedback_status = 2
                    result = True
                else:
                    result, info = send_company_card(company=company, conatct_info=contactinfos[
                        0], job=job, resume_id=resume_id, to_email=need_send.to_email)

                if result:
                    need_send.send_status = 1
                elif not result and info != 'nocontact':
                    need_send.send_status = 0
                    need_send.send_msg = info
            else:
                need_send.send_status = 0
                need_send.send_msg = 'no resume'
            need_send.save()
        return JsonResponse({'status': 'ok', 'msg': ''})


def is_match(extra_info, download, source, feedback):
    download_list = []
    source_list = []
    feedback_list = []
    if download == '不限':
        download_list = ['已下载', '未下载']
    else:
        download_list = [download]

    if source == '不限':
        source_list = ['直接下载', '企业名片意向确认']
    else:
        source_list = [source]

    if feedback == '不限' or feedback == '':
        feedback_list = ['不感兴趣', '感兴趣', '无回复', '待确认', '']
    else:
        feedback_list = [feedback]

    if extra_info['download_status'] in download_list and extra_info['buy_source'] in source_list and extra_info['feed_back'] in feedback_list:
        return True
    else:
        return False


class DeleteCompanyCategory(LoginRequiredMixin, View):

    def get(self, request, category_id):
        user = request.user
        company = get_object_or_none(
            Company,
            user=user
        )
        if company:
            company.category.filter(id=category_id).delete()

        return JsonResponse({
            'status': 'ok',
            'msg': '删除成功',
        })
