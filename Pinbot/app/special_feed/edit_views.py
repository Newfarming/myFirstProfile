# coding: utf-8

import json
import datetime
from copy import deepcopy

from django.views.generic import View
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from Pinbot.settings import SUPPORT_EMAIL_LIST

from .feed_utils import (
    CheckRestFeed,
    FeedParserUtils,
)

from jobs.models import (
    Company,
    CompanyCategory,
)
from feed.models import (
    Feed,
    Feed2,
    UserFeed,
    UserFeed2,
)
from feed.forms import (
    NewFeedForm,
    ChangeFeedForm,
    FeedStep1Form,
)
from transaction.models import (
    UserChargePackage,
)
from Brick.App.system.models import (
    City,
    CompanyCategoryPrefer,
    CompanyWelfare,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    CSRFExemptMixin,
)
from pin_utils.django_utils import (
    get_oid,
    get_int,
    get_object_or_none,
    JsonResponse,
    after7day,
)
from pin_utils.parse_utils import (
    ParseUtils,
)
from pin_utils.email.send_mail import (
    asyn_send_mail,
)
from FeedCelery.celery_utils import CeleryUtils


class EditFeed(LoginRequiredMixin, View, CheckRestFeed):
    '''
    新增编辑定制的第一步
    与算法接口做交互
    '''

    template_name = 'edit_feed.html'

    def get_feed_dict(self, feed_query):
        if not feed_query:
            return {}

        split_strip = lambda string, split_key: [i.strip() for i in string.split(split_key) if i.strip()]

        feed = feed_query[0]
        feed_dict = {
            'feed_id': feed.feed_obj_id,
            'keywords': split_strip(feed.keywords, ','),
            'analyze_titles': split_strip(feed.analyze_titles, ','),
            'talent_level': split_strip(feed.talent_level, ','),
            'expect_area': split_strip(feed.expect_area, ','),
            'job_desc': feed.job_desc,
            'title': feed.title,
            'salary_min': feed.salary_min,
            'salary_max': feed.salary_max,
            'skill_required': feed.skill_required,
            'job_domain': [
                {
                    'id': i.id,
                    'category': i.category,
                }
                for i in list(feed.job_domain.all())
            ],
            'company_prefer': [
                {
                    'id': i.id,
                    'name': i.name,
                }
                for i in list(feed.company_prefer.all())
            ],
            'job_welfare': split_strip(feed.job_welfare, ','),
        }
        return feed_dict

    def get_company_dict(self):
        user = self.request.user
        company_query = Company.objects.prefetch_related(
            'category',
        ).filter(
            user=user,
        )
        if not company_query:
            return {}
        company = company_query[0]
        company_dict = {
            'company_name': company.company_name,
            'key_points': company.key_points,
            'desc': company.desc,
            'company_stage': company.company_stage,
            'url': company.url,
            'product_url': company.product_url,
            'categorys': [{'id': i.id, 'category': i.category}for i in list(company.category.all())],
        }
        return company_dict

    def get(self, request, feed_id=''):
        '''
        兼容接口请求和页面请求
        '''
        ajax_request = request.is_ajax()
        user = request.user
        feed_query = Feed.objects.prefetch_related(
            'job_domain',
            'company_prefer',
        ).filter(
            feed_obj_id=feed_id,
            user=user,
            deleted=False,
        )

        feed_error = feed_id and not feed_query
        if feed_error:
            if not ajax_request:
                return redirect('payment-my-account')

            return JsonResponse({
                'status': 'feed_error',
                'msg': '请选择正确的定制',
            })

        no_rest_feed = not feed_query and not feed_id and not self.has_rest_feed()

        if no_rest_feed:
            if not ajax_request:
                return redirect('payment-my-account')

            return JsonResponse({
                'status': 'no_rest_feed',
                'msg': '没有剩余定制数，无法添加定制',
            })

        feed_dict = self.get_feed_dict(feed_query)
        company_dict = self.get_company_dict()
        expect_area = list(City.objects.all().values_list('name', flat=True))
        company_prefer = list(CompanyCategoryPrefer.objects.all().order_by(
            '-sort',
        ).values(
            'id',
            'name',
        ))
        job_welfare = list(CompanyWelfare.objects.all().order_by(
            '-sort',
        ).values_list(
            'name',
            flat=True,
        ))

        data = {
            'company': company_dict,
            'feed': feed_dict,
            'expect_area': expect_area,
            'company_prefer': company_prefer,
            'job_welfare': job_welfare,
        }

        if not ajax_request:
            response = render(
                request,
                self.template_name,
                {
                    'data': json.dumps(data, ensure_ascii=False)
                },
            )
        else:
            response = JsonResponse({
                'status': 'ok',
                'msg': 'ok',
                'data': data
            }, ensure_ascii=False)
        return response


class AnalyzeJD(CSRFExemptMixin, LoginRequiredMixin, View):

    def post(self, request):
        post_data = json.loads(request.body)
        form = FeedStep1Form(post_data)
        if not form.is_valid():
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })

        form_data = form.cleaned_data
        result = ParseUtils.parse_jd(form_data)

        data = result.get('data', {})
        return JsonResponse({
            'status': 'ok',
            'data': {
                'analyze_keywords': [i.strip() for i in data.get('keywords', []) if i.strip()],
                'analyze_job_domain': list(CompanyCategory.objects.filter(
                    category__in=data.get('job_domain', []),
                ).values('id', 'category')),
                'analyze_titles': [i.strip() for i in data.get('extend_titles', []) if i.strip()],
                'feed_extra_info': {
                    'language': data.get('language', ''),
                    'degree': data.get('degree') or 0,
                    'gender': data.get('gender', ''),
                    'major': data.get('major', ''),
                    'job_type': data.get('job_type', ''),
                },
            },
        })


class SubmitFeed(CSRFExemptMixin, LoginRequiredMixin, View, CheckRestFeed):
    '''
    新增编辑定制第二步
    提交定制
    '''

    def get_form(self, feed):
        return NewFeedForm if not feed else ChangeFeedForm

    def consume_feed_pkg(self):
        user_pkg_query = UserChargePackage.objects.filter(
            user=self.user,
            rest_feed__gt=0,
            feed_end_time__gte=datetime.datetime.now(),
            pkg_source=1,
        ).order_by('start_time')

        if not user_pkg_query:
            return False

        user_pkg = user_pkg_query[0]
        return user_pkg

    def create_mysql_feed(self, feed_pkg):
        feed = self.form.save(commit=False)
        feed.feed_expire_time = after7day()
        feed.expire_time = feed_pkg.feed_end_time
        feed.user = self.user
        return feed

    def create_mongo_feed(self, feed_pkg):
        mongo_feed = Feed2()
        mongo_feed._data = deepcopy(self.data)
        mongo_feed.username = self.user.username
        mongo_feed.deleted = False
        mongo_feed.remarks = []
        mongo_feed.ignored = False
        mongo_feed.feed_type = 1
        mongo_feed.display = True
        mongo_feed.add_time = datetime.datetime.now()
        mongo_feed.feed_expire_time = after7day()
        mongo_feed.expire_time = feed_pkg.feed_end_time

        mongo_feed.job_domain = [i.category for i in self.data['job_domain']]
        mongo_feed.job_welfare = self.data['job_welfare'].split(',') if self.data['job_welfare'] else []
        mongo_feed.company_prefer = [i.name for i in self.data['company_prefer']]
        return mongo_feed

    def create_mysql_userfeed(self, mysql_feed, feed_pkg):
        user_feed = UserFeed(
            user=self.user,
            add_time=datetime.datetime.now(),
        )
        user_feed.user_charge_pkg = feed_pkg
        user_feed.expire_time = feed_pkg.feed_end_time
        return user_feed

    def create_mongo_userfeed(self, mongo_feed, feed_pkg):
        user_feed2 = UserFeed2()
        user_feed2.feed = mongo_feed
        user_feed2.username = self.user.username
        return user_feed2

    def create_feed(self):
        feed_pkg = self.consume_feed_pkg()
        mongo_feed = self.create_mongo_feed(feed_pkg)
        mysql_feed = self.create_mysql_feed(feed_pkg)
        mongo_userfeed = self.create_mongo_userfeed(mongo_feed, feed_pkg)
        mysql_userfeed = self.create_mysql_userfeed(mysql_feed, feed_pkg)

        mongo_feed.save()
        mongo_userfeed.save()

        feed_pkg.rest_feed -= 1
        feed_pkg.save()

        mysql_feed.feed_obj_id = str(mongo_feed.id)
        if self.company:
            mysql_feed.company = self.company
        mysql_feed.save()
        self.form.save_m2m()

        mysql_userfeed.feed = mysql_feed
        mysql_userfeed.save()

        return mysql_feed

    def update_mysql_feed(self):
        feed = self.form.save(commit=False)
        if not feed.title:
            feed.title = self.data.get('title', '')
        feed.user = self.user
        return feed

    def update_mongo_feed(self, mysql_feed):
        feed_oid = get_oid(mysql_feed.feed_obj_id)
        mongo_feed = Feed2.objects.filter(id=feed_oid).first()
        now = datetime.datetime.now()

        if not mongo_feed.title:
            mongo_feed.title = self.data.get('title', '')
        mongo_feed.keywords = self.data['keywords']
        mongo_feed.analyze_titles = self.data['analyze_titles']
        mongo_feed.talent_level = self.data['talent_level']
        mongo_feed.job_desc = self.data['job_desc']
        mongo_feed.salary_min = self.data['salary_min']
        mongo_feed.salary_max = self.data['salary_max']
        mongo_feed.job_domain = [i.category for i in self.data['job_domain']]
        mongo_feed.job_welfare = self.data['job_welfare'].split(',') if self.data['job_welfare'] else []
        mongo_feed.company_prefer = [i.name for i in self.data['company_prefer']]
        mongo_feed.update_time = now
        mongo_feed.calced = False
        return mongo_feed

    def update_feed(self):
        mysql_feed = self.update_mysql_feed()
        mongo_feed = self.update_mongo_feed(mysql_feed)

        if self.company:
            mysql_feed.company = self.company

        mysql_feed.save()
        self.form.save_m2m()
        mongo_feed.save()
        return mysql_feed

    def strip_post_data(self, post_data):
        for key, value in post_data.iteritems():
            if isinstance(value, basestring):
                post_data[key] = value.strip()

        if not post_data.get('degree'):
            post_data['degree'] = 0
        return post_data

    def send_feed_email(self, feed):
        '''
        发送定制成功提醒邮件，分别发送给用户和运营
        '''
        client_notify_html = render_to_string(
            'add_feed_email.html',
            {'feed': feed}
        )
        email_to = self.user.userprofile.notify_email

        asyn_send_mail.delay(
            email_to,
            '聘宝已收到你的需求，即刻开始寻找人才',
            client_notify_html
        )

        support_notify_html = render_to_string(
            'new_feed_notify.html',
            {'feed': feed, 'user': self.user},
        )
        support_email_to = ';'.join(SUPPORT_EMAIL_LIST)
        asyn_send_mail.delay(
            support_email_to,
            '［通知］新增定制%s' % self.user.first_name,
            support_notify_html
        )
        return True

    def post(self, request):
        post_data = json.loads(request.body)
        post_data = self.strip_post_data(post_data)
        feed_id = post_data.get('feed_id', '')
        self.user = request.user

        feed = get_object_or_none(
            Feed,
            feed_obj_id=feed_id,
            user=self.user,
        )
        if feed_id and not feed:
            return JsonResponse({
                'status': 'feed_error',
                'msg': '定制数据有误',
            })

        form = self.get_form(feed)
        self.form = form(post_data, post_data=post_data) if not feed else form(post_data, post_data=post_data, instance=feed)

        if not self.form.is_valid():
            return JsonResponse({
                'status': 'form_error',
                'msg': self.form.get_first_errors(),
                'errors': self.form.errors,
            })

        user = request.user
        self.data = self.form.cleaned_data
        self.company = get_object_or_none(
            Company,
            user=user
        )

        if not feed:
            if not self.has_rest_feed():
                return JsonResponse({
                    'status': 'no_feed',
                    'msg': '没有剩余订制可用',
                })

            feed = self.create_feed()

            self.send_feed_email(feed)
            result = {
                'status': 'ok',
                'msg': '添加成功',
                'show_mission': False,
                'mission_time': None,
                'username': user.username,
                'redirect_url': '/feed',
                'feed_id': feed.feed_obj_id,
            }
        else:
            feed = self.update_feed()
            result = {
                'status': 'ok',
                'msg': '保存成功',
                'redirect_url': '/feed',
                'feed_id': feed.feed_obj_id,
            }

        FeedParserUtils.save_feed_parser(
            feed.feed_obj_id,
            post_data.get('keywords', '').split(','),
            post_data.get('block_keywords', '').split(','),
            post_data.get('analyze_titles', '').split(','),
            post_data.get('block_titles', '').split(','),
        )
        CeleryUtils.user_feed_task(feed.feed_obj_id)
        return JsonResponse(result)


class PredictionSalary(LoginRequiredMixin, View):
    '''
    预测薪资，与算薪资接口交互
    '''

    def post(self, request):
        feed = json.loads(request.body)
        result = ParseUtils.parse_salary(feed)
        return JsonResponse(result)


class PredictionNum(LoginRequiredMixin, View):
    '''
    预测人数，与预测人数接口交互
    '''

    def post(self, request):
        feed = json.loads(request.body)
        result = ParseUtils.parse_num(feed)
        return JsonResponse(result)


class PredictionRelated(CSRFExemptMixin, LoginRequiredMixin, View):
    '''
    预测人数，与预测人数接口交互
    '''

    def api_post_data(self, post_data):
        post_data['company_prefer'] = list(CompanyCategoryPrefer.objects.filter(
            id__in=[get_int(i) for i in post_data.get('company_prefer', []) if get_int(i)]
        ).values_list(
            'code_name',
            flat=True,
        ))
        post_data['job_domain'] = list(CompanyCategory.objects.filter(
            id__in=[get_int(i) for i in post_data.get('job_domain') if get_int(i)]
        ).values_list(
            'category',
            flat=True,
        ))
        return post_data

    def post(self, request):
        feed = json.loads(request.body)
        feed = self.api_post_data(feed)
        result = ParseUtils.parse_related(feed)
        return JsonResponse(result)
