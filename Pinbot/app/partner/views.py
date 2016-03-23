# coding: utf-8

import json
import datetime
import bson

from django.views.generic.base import View
from django.http import Http404
from django.shortcuts import render, redirect
from django.db import transaction
from django.views.generic import TemplateView
from django.core.cache import cache
from django.db.models import Q

from .models import (
    UploadResume,
    UserAcceptTask,
    UserTaskResume,
    UploadTaskSetting,
    ResumeProject,
    ResumeWork,
    ResumeSkill,
    ResumeEducation,
    TaskCoinRecord,
    RecoResumeTask,
    FollowTaskRecord,
    HotTaskSetting,
)
from .forms import (
    UploadTaskSettingForm,
    ResumePersonInfoForm,
    ResumeWorkInfoForm,
    ResumeProjectInfoForm,
    ResumeSkillInfoForm,
    ResumeEduInfoForm,
)
from .partner_utils import (
    UploadResumeUtils,
    PartnerCoinUtils,
    PartnerNotify,
    PartnerLevelUtils,
)

from feed.models import (
    Feed,
)
from jobs.models import (
    CompanyCategory,
)
from resumes.resume_utils import (
    PinbotResumeUtils,
)
from resumes.models import (
    ContactInfoData,
)
from users.forms import (
    UserContactInfoForm,
)

from app.special_feed.feed_utils import (
    FeedUtils,
)

from Brick.App.system.models import (
    City,
)

from Common.utils.AjaxView import (
    PaginatedJSONListView,
)

from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    StaffRequiredMixin,
    NotMaliceGroupUser,
)
from pin_utils.django_utils import (
    get_object_or_none,
    JsonResponse,
    get_int,
    django_model2json,
    get_tomorrow,
    error_phone,
    error_email,
)
from pin_utils.parse_utils import (
    ParseUtils,
)


class TaskSettingMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'task_setting'):
            feed_citys = Feed.objects.filter(
                user=user,
                deleted=False,
            ).values_list(
                'expect_area',
                flat=True,
            )

            citys = list(
                City.objects.filter(
                    name__in=list(
                        set(','.join([c.replace('，', ',').replace(' ', ',') for c in feed_citys]).split(','))
                    )
                )
            )
            task_setting = UploadTaskSetting(
                user=user,
            )
            task_setting.save()
            task_setting.citys.add(*citys)
        return super(TaskSettingMixin, self).dispatch(request, *args, **kwargs)


class FeedDictMixin(object):

    def get_company_dict(self, feed):
        if not feed.company:
            company_name = feed.user.first_name
            return {
                'company_name': company_name,
            }
        company = feed.company
        company_dict = {
            'company_name': company.company_name,
            'key_points': company.key_points,
            'desc': company.desc,
            'company_stage': company.company_stage,
            'url': company.url,
            'product_url': company.product_url,
            'categorys': [{'id': i.id, 'category': i.category} for i in list(company.category.all())],
        }
        return company_dict

    def get_feed_dict(self, feed):
        if not feed:
            return {}

        now = datetime.datetime.now()
        feed_dict = {
            'id': feed.id,
            'title': feed.title,
            'salary_min': feed.salary_min,
            'salary_max': feed.salary_max,
            'job_domain': [i.category.strip() for i in list(feed.job_domain.all()) if i.category.strip()],
            'company_prefer': [i.name.strip() for i in list(feed.company_prefer.all()) if i.name.strip()],
            'expect_area': [i for i in feed.expect_area.replace('，', ',').replace(' ', ',').split(',') if i],
            'job_welfare': [i for i in feed.job_welfare.split(',') if i],
            'company': self.get_company_dict(feed),
            'job_desc': feed.job_desc,
            'keywords': feed.keywords,
            'deleted': feed.deleted,
            'active': True if feed.feed_expire_time > now else False,
        }
        return feed_dict


class AcceptTaskMixin(object):

    def save_feed_result(self, feed, resume):
        feed_result = FeedUtils.add_feed_result(
            feed.feed_obj_id,
            resume.resume_id,
            source='talent_partner',
        )
        return feed_result

    def create_upload_task(self, feed, resume):
        user = self.request.user
        accept_task = get_object_or_none(
            UserAcceptTask,
            user=user,
            feed=feed,
        )
        if not accept_task:
            accept_task = UserAcceptTask(
                user=user,
                feed=feed,
                task_id=bson.ObjectId(),
            )
            accept_task.save()

        task_resume = get_object_or_none(
            UserTaskResume,
            task=accept_task,
            resume=resume,
        )
        if not task_resume:
            now = datetime.datetime.now()
            task_resume = UserTaskResume(
                task=accept_task,
                resume=resume,
            )
            task_resume.save()

            # 这里是为了兼容任务系统，认领互助招聘任务，所以不用save方法，改用update
            UserAcceptTask.objects.filter(
                user=user,
                feed=feed,
                task_id=accept_task.task_id,
            ).update(
                update_time=now
            )
            PartnerNotify.upload_resume_notify(feed.user, resume.resume_id, feed.feed_obj_id)

        return accept_task

    def has_same_user_task(self, feed, resume):
        same_user = feed.user
        has_task = UserTaskResume.objects.filter(
            task__feed__user=same_user,
            resume=resume,
        )
        return True if has_task else False

    def not_valid_feed(self, feed):
        if feed.deleted:
            return True

        now = datetime.datetime.now()
        if feed.feed_expire_time < now:
            return True
        return False

    def is_fit_task_city(self, feed, resume):
        '''
        判断城市是否匹配
        '''
        feed_citys = feed.expect_area
        resume_citys = resume.expect_work_place.replace(
            '、', ','
        ).replace(
            '，', ','
        ).split(',')
        for city in resume_citys:
            if city in feed_citys:
                return True
        return False

    def is_fit_task_salary(self, feed, resume):
        '''
        判断薪资是否匹配
        '''
        salary_low, salary_high = feed.salary_min, feed.salary_max
        if salary_low == 0 and salary_high == 0:
            return True
        if salary_low == 0 and salary_high == 1000000:
            return True

        target_salary = resume.target_salary
        return False if target_salary > salary_high else True

    def is_valid_task_resume(self, task, resume):
        '''
        接受任务
        valid_feed 定制已被删除或者7天未查看过期
        same_user 定制和简历是同一个人的
        has_task 已经接受同一个HR的任务了
        city_unfit 简历期望工作地和任务的工作地不匹配
        salary_unfit 简历的期望薪资和任务的薪资不匹配
        ok 接受任务成功
        '''
        if self.not_valid_feed(task):
            return False, 'valid_feed'

        if task.user == resume.user:
            return False, 'same_user'

        if self.has_same_user_task(task, resume):
            return False, 'has_task'

        if not self.is_fit_task_city(task, resume):
            return False, 'city_unfit'

        if not self.is_fit_task_salary(task, resume):
            return False, 'salary_unfit'

        return True, 'ok'

    def accept_task(self, task, resume):
        accept_task = self.create_upload_task(task, resume)
        self.save_feed_result(task, resume)
        return accept_task


class FollowTaskRecordMixin(object):

    follow_type = 1

    def save_follow_record(self, task_resume):
        now = datetime.datetime.now()
        follow_record_query = FollowTaskRecord.objects.filter(
            task_resume=task_resume,
            follow_type=self.follow_type,
            follow_time__month=now.month,
            follow_time__day=now.day,
        )

        if not follow_record_query:
            follow_record = FollowTaskRecord.objects.create(
                task_resume=task_resume,
                follow_type=self.follow_type,
            )
        else:
            follow_record = follow_record_query[0]
        return follow_record


class ValidTaskMixin(object):

    def get_has_accept_task(self):
        '''
        接受过的任务定制不应该展示，需要找出来
        排除掉
        '''
        user = self.request.user
        accept_task_id_list = UserAcceptTask.objects.select_related(
            'feed'
        ).filter(
            user=user,
        ).values_list('feed__feed_obj_id', flat=True)
        return accept_task_id_list


class PartnerTplView(
        LoginRequiredMixin,
        NotMaliceGroupUser,
        TaskSettingMixin,
        TemplateView):
    malice_group = 'malice_partner'
    redirect_url = '/partner/no_rights/'


class EditTaskSetting(LoginRequiredMixin, NotMaliceGroupUser, TaskSettingMixin, View):
    '''
    新增、编辑任务设置
    '''
    template = 'task_setting.html'
    malice_group = 'malice_partner'
    redirect_url = '/partner/no_rights/'

    def get(self, request):
        user = request.user
        upload_setting = user.task_setting
        setting = {
            'id': upload_setting.id,
            'title': [t for t in upload_setting.title.split(',') if t],
            'job_domain': list(upload_setting.job_domains.all().values(
                'id',
                'category',
            )),
            'citys': list(upload_setting.citys.all().values(
                'id',
                'name',
            )),
            'task_time': upload_setting.task_time,
        }

        all_citys = list(City.objects.all().values(
            'id',
            'name',
        ))
        all_company_domain = list(CompanyCategory.objects.values(
            'id',
            'category',
        ))
        reco_title = [
            'iOS开发',
            'Android开发',
            'JAVA后端',
            'APP开发',
            'Web前端',
            '产品经理',
            '游戏开发',
            'UI设计',
        ]

        return render(
            request,
            self.template,
            {
                'data': json.dumps({
                    'setting': setting,
                    'all_citys': all_citys,
                    'all_company_domain': all_company_domain,
                    'reco_title': reco_title,
                }, ensure_ascii=False)
            }
        )

    def normalize_form_data(self, post_data):
        post_data['citys'] = [i.get('id', 0) for i in post_data.get('citys', []) if get_int(i.get('id'))]
        post_data['job_domains'] = [i.get('id') for i in post_data.get('job_domain', []) if get_int(i.get('id'))]
        post_data['title'] = ','.join(post_data.get('title', []))
        return post_data

    def post(self, request):
        user = request.user
        post_data = json.loads(request.body)
        post_data = self.normalize_form_data(post_data)
        form = UploadTaskSettingForm(post_data, instance=user.task_setting) if hasattr(user, 'task_setting') else UploadTaskSettingForm(post_data)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            form.save_m2m()
            return JsonResponse({
                'status': 'ok',
                'msg': '保存成功',
                'redirect_url': '/partner/reco_task/',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class HomePage(LoginRequiredMixin, NotMaliceGroupUser, View):

    template_name = 'partner_home_page.html'
    malice_group = 'malice_partner'
    redirect_url = '/partner/no_rights/'

    def get(self, request):
        user = request.user
        user_accept_task = UserAcceptTask.objects.filter(
            user=user,
        )
        if user_accept_task:
            return redirect('partner-reco-task')

        user_upload_resume = UploadResume.objects.filter(
            user=user,
        )
        if user_upload_resume:
            return redirect('partner-reco-task')

        return render(
            request,
            self.template_name,
            {},
        )


class NoRightsPage(LoginRequiredMixin, View):

    template_name = 'no_access_rights.html'

    def get(self, request):
        user = request.user
        accu_resumes = UserTaskResume.objects.select_related(
            'resume'
        ).filter(
            resume__user=user,
            resume_status=5,
        )
        return render(
            request,
            self.template_name,
            {
                'accu_resumes': accu_resumes,
            }
        )


class RecoTaskList(
        LoginRequiredMixin,
        PaginatedJSONListView,
        FeedDictMixin,
        ValidTaskMixin):
    '''
    任务池列表
    author: runforever
    '''

    context_object_name = 'data'
    paginate_by = 6

    income_base = 0.3

    def invalid_feed_id_list(self):
        '''
        找出用户自己的定制和管理员的定制，
        这部分定制不应该出现在推荐的数据中，需要排除掉
        '''
        user = self.request.user
        feed_id_list = Feed.objects.filter(
            Q(user=user) | Q(user__is_staff=True),
            deleted=False
        ).values_list('feed_obj_id', flat=True)
        return feed_id_list

    def exclude_feed_id_list(self):
        '''
        找出已经接受过任务的定制和用户自己的定制和管理员的定制
        '''
        exclude_feed_id_list = list(self.get_has_accept_task())
        invalid_feed_id_list = list(self.invalid_feed_id_list())
        exclude_feed_id_list.extend(invalid_feed_id_list)
        return list(set(exclude_feed_id_list))

    def init_all_citys(self):
        self.all_citys = list(City.objects.all().values_list('name', flat=True))
        return self.all_citys

    def get_query_citys(self):
        citys = self.request.GET.getlist('city', [])
        query_citys = ','.join(c for c in citys if c in self.all_citys)
        return query_citys

    def get_query_keywords(self):
        keywords = self.request.GET.get('keywords', '').replace(' ', ',')
        return keywords

    def get_queryset(self):
        exclude_task_id_list = self.exclude_feed_id_list()

        self.init_all_citys()
        query_citys = self.get_query_citys()
        query_keywords = self.get_query_keywords()

        search_params = {
            'feed_type': 1,
            'start': 0,
            'citys': query_citys,
            'query_feed_result': True,
            'keywords': query_keywords,
            'need_company': True,
            'size': 100,
            'ids_list_nin': ','.join(exclude_task_id_list),
            'time_field_gte': 'feed_expire_time:-7',
            'default_operator': 'and',
        }

        search_result = ParseUtils.search_job(search_params)
        feed_data = search_result.get('data', {}).get('results', [])
        feed_obj_id_list = [i['id'] for i in feed_data if i.get('id')]
        now = datetime.datetime.now()

        task_query = Feed.objects.filter(
            deleted=False,
            feed_expire_time__gt=now,
            feed_obj_id__in=feed_obj_id_list,
        ).select_related(
            'company',
            'user',
        ).prefetch_related(
            'job_domain',
            'company_prefer',
            'company__category',
        )
        return task_query

    def get_expect_income(self, feed):
        salary_min = feed.salary_min
        salary_max = feed.salary_max

        if salary_min == 0 and salary_max == 1000000:
            return '以入职薪资为准'
        if salary_min == 0 and salary_max == 0:
            return '以入职薪资为准'
        if salary_max <= 5000:
            return 900 * self.income_base
        if salary_max <= 20000:
            return 2900 * self.income_base
        if salary_max <= 30000:
            return 3900 * self.income_base
        if salary_max > 30000:
            return 29900 * self.income_base

    def get_hot_tasks(self):
        hot_tasks = list(HotTaskSetting.objects.all().values_list('name', flat=True)[:5])
        return hot_tasks

    def get_context_data(self, *args, **kwargs):
        context = super(RecoTaskList, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        context['data'] = [
            {
                'id': d.id,
                'feed': self.get_feed_dict(d),
                'expect_income': self.get_expect_income(d),
                'reco_time': d.last_click_time.strftime('%Y-%m-%d %H:%M') if d.last_click_time else '2015-06-11 12:12',
                'reco_index': 0,
            }
            for d in data
        ]
        context['has_resume'] = True if self.request.user.uploadresume_set.all().exists() else False
        context['upload_task_url'] = '/partner/edit_resume/?task_id='
        context['select_resume_url'] = '/partner/resume_manage/#/manage_preview/'

        context['all_citys'] = self.all_citys
        context['hot_tasks'] = self.get_hot_tasks()
        context['examples'] = ['Web前端 移动端']
        return context


class AcceptTask(
        LoginRequiredMixin,
        NotMaliceGroupUser,
        View,
        AcceptTaskMixin):
    '''
    接受任务
    '''
    task_model = Feed
    malice_group = 'malice_partner'
    redirect_url = '/partner/no_rights/'

    def operation(self, task, resume):
        return self.accept_task(task, resume)

    @transaction.atomic
    def get(self, request, task_id, resume_id):
        task = get_object_or_none(
            self.task_model,
            id=task_id,
        )

        if not task:
            return JsonResponse({
                'status': 'task_error',
                'msg': '任务数据有误',
            })

        user = request.user
        resume = get_object_or_none(
            UploadResume,
            user=user,
            id=resume_id,
        )

        if not resume:
            return JsonResponse({
                'status': 'resume_error',
                'msg': '上传简历数据有误',
            })

        is_valid, status = self.is_valid_task_resume(task, resume)
        if is_valid:
            self.operation(task, resume)
            return JsonResponse({
                'status': status,
                'msg': status,
            })
        else:
            return JsonResponse({
                'status': status,
                'msg': status,
            })


class CheckAcceptTask(AcceptTask):
    '''
    检查任务和简历匹配情况接口，判断是否可以接受任务
    '''

    def operation(self, task, resume):
        '''
        只是检查数据，不需要做操作
        '''
        return False


class AcceptResumeTask(
        LoginRequiredMixin,
        NotMaliceGroupUser,
        View,
        AcceptTaskMixin):

    malice_group = 'malice_partner'
    redirect_url = '/partner/no_rights/'

    @transaction.atomic
    def get(self, request, task_id, resume_id):
        user = request.user
        task = get_object_or_none(
            RecoResumeTask,
            user=user,
            id=task_id,
        )

        if not task:
            return JsonResponse({
                'status': 'task_error',
                'msg': '任务数据有误',
            })

        user = request.user
        resume = get_object_or_none(
            UploadResume,
            user=user,
            id=resume_id,
        )

        if not resume:
            return JsonResponse({
                'status': 'resume_error',
                'msg': '上传简历数据有误',
            })

        feed = task.feed
        is_valid, status = self.is_valid_task_resume(feed, resume)

        if is_valid:
            self.accept_task(feed, resume)
            now = datetime.datetime.now()
            task.action = 1
            task.action_time = now
            task.save()

            return JsonResponse({
                'status': status,
                'msg': '接受任务成功',
            })
        else:
            return JsonResponse({
                'status': status,
                'msg': status,
            })


class EditResume(
        LoginRequiredMixin,
        NotMaliceGroupUser,
        View,
        AcceptTaskMixin):
    '''
    新增、编辑上传简历
    '''
    template = 'partner_edit_resume.html'
    TIME_FORMAT = '%Y.%m'
    malice_group = 'malice_partner'
    redirect_url = '/partner/no_rights/'

    def get_resume_dict(self, resume):
        if not resume:
            return {}

        resume_dict = {
            'id': resume.id,
            'name': resume.name,
            'gender': resume.gender,
            'phone': resume.phone,
            'email': resume.email,
            'work_years': resume.work_years,
            'age': resume.age,
            'qq': resume.qq,
            'address': resume.address,
            'self_evaluation': resume.self_evaluation,
            'degree': resume.degree,
            'job_hunting_state': resume.job_hunting_state,
            'expect_work_place': resume.expect_work_place,
            'expect_position': resume.expect_position,
            'last_contact': resume.last_contact,
            'hr_evaluate': resume.hr_evaluate,
            'target_salary': resume.target_salary / 1000,
            'works': [
                {
                    'id': w.id,
                    'start_time': w.start_time.strftime(self.TIME_FORMAT),
                    'end_time': w.end_time.strftime(self.TIME_FORMAT),
                    'position_title': w.position_title,
                    'company_name': w.company_name,
                    'job_desc': w.job_desc,
                }
                for w in list(resume.resume_works.all())
            ],
            'projects': [
                {
                    'id': p.id,
                    'start_time': p.start_time.strftime(self.TIME_FORMAT),
                    'end_time': p.end_time.strftime(self.TIME_FORMAT),
                    'project_name': p.project_name,
                    'project_desc': p.project_desc,
                }
                for p in list(resume.resume_projects.all())
            ],
            'educations': [
                {
                    'id': e.id,
                    'start_time': e.start_time.strftime(self.TIME_FORMAT),
                    'end_time': e.end_time.strftime(self.TIME_FORMAT),
                    'school': e.school,
                    'major': e.major,
                    'degree': e.degree,
                }
                for e in list(resume.resume_educations.all())
            ],
            'skills': [
                {
                    'id': s.id,
                    'skill_desc': s.skill_desc,
                    'proficiency': s.proficiency,
                }
                for s in list(resume.resume_skills.all())
            ],
        }
        return resume_dict

    def get_resume(self, resume_id):
        if not resume_id:
            return {}

        user = self.request.user
        resume_query = UploadResume.objects.prefetch_related(
            'resume_works',
            'resume_projects',
            'resume_educations',
            'resume_skills',
        ).filter(
            user=user,
            id=resume_id,
        )
        if not resume_query:
            raise Http404
        resume = resume_query[0]
        return resume

    def get_all_citys(self):
        all_citys = list(City.objects.all().values_list('name', flat=True))
        return all_citys

    def get(self, request, resume_id=None):
        '''
        展示简历信息
        '''
        resume = self.get_resume(resume_id)
        resume_dict = self.get_resume_dict(resume)
        task_id = request.GET.get('task_id', 0)
        all_citys = self.get_all_citys()

        return render(
            request,
            self.template,
            {
                'data': django_model2json(resume_dict, ensure_ascii=False),
                'task_id': task_id,
                'all_citys': json.dumps(all_citys, ensure_ascii=False),
            }
        )

    def save_person_info(self, post_data, resume):
        person_info_form = ResumePersonInfoForm(post_data, update_resume=resume, instance=resume) if resume else ResumePersonInfoForm(post_data, update_resume=resume)
        user = self.request.user
        save_resume = person_info_form.save(commit=False)
        save_resume.user = user

        if not resume:
            save_resume.resume_id = str(bson.ObjectId())

        save_resume.save()
        return save_resume

    def save_key_info(self, post_data, resume, key, form_cls, model_cls):
        info_list = post_data.get(key, [])
        model_cls.objects.filter(
            resume=resume
        ).delete()
        for info in info_list:
            form = form_cls(info)
            info_obj = form.save(commit=False)
            info_obj.resume = resume
            info_obj.save()

    def save_resume(self, post_data, update_resume):
        resume = self.save_person_info(post_data, update_resume)
        self.save_key_info(post_data, resume, 'projects', ResumeProjectInfoForm, ResumeProject)
        self.save_key_info(post_data, resume, 'works', ResumeWorkInfoForm, ResumeWork)
        self.save_key_info(post_data, resume, 'skills', ResumeSkillInfoForm, ResumeSkill)
        self.save_key_info(post_data, resume, 'educations', ResumeEduInfoForm, ResumeEducation)
        return resume

    def __valid_key_info(self, post_data, valid_result, key, form_cls):
        for i, w in enumerate(post_data.get(key, [])):
            form = form_cls(w)
            if not form.is_valid():
                valid_result['is_valid'] = False
                valid_result[key].append({
                    'index': i,
                    'errors': form.errors,
                })
        return valid_result

    def __valid_post_data(self, post_data, update_resume):
        '''
        校验post数据
        '''
        valid_result = {
            'is_valid': True,
            'person_info': [],
            'works': [],
            'projects': [],
            'educations': [],
            'skills': [],
        }
        person_info_form = ResumePersonInfoForm(post_data, update_resume=update_resume)
        if not person_info_form.is_valid():
            valid_result['is_valid'] = False
            valid_result['person_info'] = person_info_form.errors

        self.__valid_key_info(post_data, valid_result, 'works', ResumeWorkInfoForm)
        self.__valid_key_info(post_data, valid_result, 'projects', ResumeProjectInfoForm)
        self.__valid_key_info(post_data, valid_result, 'educations', ResumeEduInfoForm)
        self.__valid_key_info(post_data, valid_result, 'skills', ResumeSkillInfoForm)
        return valid_result

    def post(self, request, resume_id=None):
        '''
        简历保存
        '''
        post_data = json.loads(request.body)
        update_resume = self.get_resume(resume_id)
        valid_result = self.__valid_post_data(post_data, update_resume)

        if valid_result['is_valid']:
            with transaction.atomic():
                resume = self.save_resume(post_data, update_resume)
                resume_id = resume.id
                # save resume to pinbot
                resume = self.get_resume(resume.id)
                resume_dict = UploadResumeUtils.get_sync_resume_dict(resume)
                PinbotResumeUtils.save(resume_dict)

            resume_dict.pop('created_at', None)
            resume_dict.pop('updated_at', None)
            resume_dict.pop('resume_id', None)
            resume_dict.pop('contact_info', None)

            ParseUtils.insert_resume(resume_dict)

            task_id = post_data.get('task_id', 0)
            task = get_object_or_none(
                Feed,
                id=task_id,
            )

            if task:
                is_valid, status = self.is_valid_task_resume(task, resume)
                if is_valid:
                    self.accept_task(task, resume)

                msg = '接受任务成功'
                resume_source = 'add_task'
            else:
                status = 'ok'
                msg = '保存成功'
                resume_source = 'edit_resume' if update_resume else 'add_resume'

            result = {
                'status': status,
                'msg': msg,
                'resume_id': resume_id,
                'resume_source': resume_source,
            }

            return JsonResponse(result)
        else:
            result = {
                'status': 'form_error',
                'msg': '表单错误',
                'errors': valid_result,
            }

            return JsonResponse(result)


class UploadResumeList(
        LoginRequiredMixin,
        PaginatedJSONListView,
        FeedDictMixin,
        ValidTaskMixin):

    context_object_name = 'data'
    paginate_by = 6

    def get_query_keyword(self):
        keyword = self.request.GET.get('query', '')
        if not keyword:
            return {}

        page = get_int(self.request.GET.get('page', 0))
        page = 0 if page - 1 < 0 else page - 1
        owner = self.request.user.username

        search_params = {
            'owners': owner,
            'size': 100,
            'start': 0,
            'keywords': keyword,
        }
        search_result = ParseUtils.search_resume(search_params)
        resume_data = search_result.get('data', {}).get('results', [])
        return {
            'resume_id__in': [i['id'] for i in resume_data if i.get('id')]
        }

    def get_query_task(self):
        user = self.request.user
        task_id = get_int(self.request.GET.get('task_id', ''))
        if not task_id:
            return {}

        feed = get_object_or_none(
            Feed,
            id=task_id,
        )
        if not feed:
            raise Http404

        upload_resume_list = UserTaskResume.objects.filter(
            task__feed__user=feed.user,
            resume__user=user,
        ).values_list('resume__id', flat=True)

        if not upload_resume_list:
            return {}
        return {'id__in': upload_resume_list}

    def get_queryset(self):
        user = self.request.user
        query_cond = self.get_query_keyword()
        exclude_cond = self.get_query_task()
        upload_resume_query = UploadResume.objects.prefetch_related(
            'resume_coin_records',
            'reco_resume_tasks__feed',
            'reco_resume_tasks__feed__company',
            'reco_resume_tasks__feed__user',
            'reco_resume_tasks__feed__job_domain',
            'reco_resume_tasks__feed__company_prefer',
            'reco_resume_tasks__feed__company__category',
        ).filter(
            user=user,
            **query_cond
        ).exclude(**exclude_cond).order_by('-id')
        return upload_resume_query

    def is_valid_task(self, task, accept_task_id_list):
        now = datetime.datetime.now()
        valid_task = task.action == 0 and task.display and not task.feed.deleted and task.feed.feed_expire_time > now and task.feed.feed_obj_id not in accept_task_id_list
        return True if valid_task else False

    def get_reco_resume_task(self, resume):
        accept_task_id_list = self.get_has_accept_task()
        all_task = [
            {
                'feed': self.get_feed_dict(i.feed),
                'reco_time': i.reco_time.strftime('%Y-%m-%d %H:%M'),
                'id': i.id,
            }
            for i in list(resume.reco_resume_tasks.all()) if self.is_valid_task(i, accept_task_id_list)
        ]
        all_task.sort(key=lambda x: x['reco_time'], reverse=True)
        return all_task[:5]

    def get_context_data(self, *args, **kwargs):
        context = super(UploadResumeList, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])

        context['data'] = [
            {
                'id': d.id,
                'name': d.name,
                'target_salary': d.target_salary,
                'work_years': d.work_years,
                'expect_position': d.expect_position,
                'update_time': d.update_time.strftime('%Y-%m-%d %H:%M'),
                'expect_work_place': d.expect_work_place,
                'resume_id': d.resume_id,
                'coin': sum(r.coin for r in list(d.resume_coin_records.all())),
                'reco_resume_tasks': self.get_reco_resume_task(d),
            }
            for d in data
        ]
        return context


class AcceptTaskList(
        LoginRequiredMixin,
        PaginatedJSONListView,
        FeedDictMixin):

    context_object_name = 'data'
    paginate_by = 6

    def get_query_keyword(self):
        keyword = self.request.GET.get('query', '')
        if not keyword:
            return {}

        user = self.request.user
        page = get_int(self.request.GET.get('page', 0))
        page = 0 if page - 1 < 0 else page - 1

        feed_id_list = UserAcceptTask.objects.filter(
            user=user,
        ).values_list(
            'feed__feed_obj_id',
            flat=True,
        )
        search_params = {
            'start': 0,
            'size': 100,
            'feed_type': 1,
            'keywords': keyword,
            'ids_list': ','.join(list(feed_id_list))
        }
        search_result = ParseUtils.search_job(search_params)
        feed_data = search_result.get('data', {}).get('results', [])
        return {
            'feed__feed_obj_id__in': [i['id'] for i in feed_data if i.get('id')]
        }

    def get_queryset(self):
        user = self.request.user
        query_keyword = self.get_query_keyword()
        accept_task_query = UserAcceptTask.objects.select_related(
            'feed',
            'feed__company',
            'feed__user',
        ).prefetch_related(
            'task_resumes__resume',
            'task_resumes__resume__resume_coin_records',
            'task_coin_records',
            'feed__job_domain',
            'feed__company_prefer',
            'feed__company__category',
        ).filter(
            user=user,
            **query_keyword
        ).order_by('-update_time')
        return accept_task_query

    def get_resume_coin(self, task, resume):
        total_coins = sum([i.coin for i in list(resume.resume_coin_records.all()) if i.task_id == task.id])
        return total_coins

    def get_task_resumes(self, accept_task):
        task_resumes = [
            {
                'name': r.resume.name,
                'upload_time': r.upload_time,
                'target_salary': r.resume.target_salary,
                'resume_status': r.resume_status,
                'resume_id': r.resume.resume_id,
                'resume_coin': self.get_resume_coin(accept_task, r.resume),
                'id': r.resume.id,
            }
            for r in list(accept_task.task_resumes.all())
        ]
        task_resumes.sort(key=lambda x: x['upload_time'], reverse=True)
        return task_resumes

    def get_context_data(self, *args, **kwargs):
        context = super(AcceptTaskList, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        context['data'] = [
            {
                'feed': self.get_feed_dict(d.feed),
                'total_coin': sum(i.coin for i in list(d.task_coin_records.all())),
                'task_resumes': self.get_task_resumes(d),
                'update_time': d.update_time.strftime('%Y-%m-%d %H:%M'),
                'task_id': d.task_id,
                'id': d.id,
            }
            for d in data
        ]
        return context


class FollowTaskResume(
        LoginRequiredMixin,
        NotMaliceGroupUser,
        View,
        FollowTaskRecordMixin):

    template_name = 'follow_resume.html'
    malice_group = 'malice_partner'
    redirect_url = '/partner/no_rights/'

    notify_msg_meta = {
        1: '符合你JD的简历一枚已送达，收好不谢！（<a class="c0091fa" href="%s">查看详情</a>）',
        2: '优秀的候选人不能等，过时不候哟~（<a class="c0091fa" href="%s">查看详情</a>）',
        3: '互助伙伴给你送人才来啦（<a class="c0091fa" href="%s">查看详情</a>）',
    }

    def get_follow_status(self, task_id, resume_id):
        follow_key = 'PARTNER_%s_%s' % (task_id, resume_id)
        follow_status = cache.get(follow_key, False)
        return follow_status

    def get_hr_contact(self, task):
        hr_contact = {
            'has_hr_info': task.has_hr_info,
        }
        if task.has_hr_info:
            user = task.feed.user
            hr_userprofile = user.userprofile
            hr_contact['company_name'] = hr_userprofile.company_name
            hr_contact['phone'] = hr_userprofile.phone
            hr_contact['name'] = hr_userprofile.name
            hr_contact['email'] = user.username
            hr_contact['qq'] = hr_userprofile.qq
        return hr_contact

    def get_user_info(self, user):
        contact_info_query = user.contact_infos.all()
        if not contact_info_query:
            return {}

        contact_info = contact_info_query[0]
        user_info = {
            'name': contact_info.name,
            'phone': contact_info.phone
        }
        return user_info

    def get(self, request, task_id, resume_id):
        user = request.user
        now = datetime.datetime.now()
        task_query = UserAcceptTask.objects.select_related(
            'feed',
            'feed__user',
        ).filter(
            user=user,
            id=task_id,
            feed__deleted=False,
            feed__feed_expire_time__gt=now,
        )
        if not task_query:
            raise Http404

        task = task_query[0]
        task_resume = task.task_resumes.filter(
            resume__id=resume_id
        )

        if not task_resume:
            raise Http404

        context_data = {
            'has_send_notify': self.get_follow_status(task_id, resume_id),
            'hr_contact_info': self.get_hr_contact(task),
            'user_info': self.get_user_info(user),
            'task_id': task_id,
            'resume_id': resume_id,
        }

        return render(
            self.request,
            self.template_name,
            {
                'data': json.dumps(context_data)
            }
        )

    def set_send_cache(self, task_id, resume_id):
        now = datetime.datetime.now()
        tomorrow = get_tomorrow()
        follow_key = 'PARTNER_%s_%s' % (task_id, resume_id)
        expire_time = (tomorrow - now).total_seconds()
        cache.set(follow_key, True, expire_time)
        return True

    @transaction.atomic
    def post(self, request, task_id, resume_id):
        user = request.user
        now = datetime.datetime.now()
        task_query = UserAcceptTask.objects.select_related(
            'feed',
            'feed__user',
        ).filter(
            user=user,
            id=task_id,
            feed__deleted=False,
            feed__feed_expire_time__gt=now,
        )
        if not task_query:
            raise Http404

        task = task_query[0]
        task_resume_query = task.task_resumes.filter(
            resume__id=resume_id
        )

        if not task_resume_query:
            raise Http404

        task_resume = task_resume_query[0]
        msg_type = get_int(request.POST.get('msg_type', 0))

        if msg_type not in self.notify_msg_meta.keys():
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的站内信',
            })

        self.set_send_cache(task_id, resume_id)

        follow_record = self.save_follow_record(task_resume)
        desc = self.notify_msg_meta[msg_type] % PartnerNotify.resume_follow_url(follow_record.id)
        PartnerNotify.follow_resume_notify(
            task.feed.user,
            desc,
        )
        follow_record.desc = desc
        follow_record.save()

        return JsonResponse({
            'status': 'ok',
            'msg': '跟进成功',
        })


class GetHrContact(
        LoginRequiredMixin,
        View,
        FollowTaskRecordMixin):

    follow_type = 2

    def get_hr_info(self, task_resume):
        user = task_resume.task.feed.user
        hr_userprofile = user.userprofile
        hr_contact = {
            'company_name': hr_userprofile.company_name,
            'phone': hr_userprofile.phone,
            'name': hr_userprofile.name,
            'email': user.username,
            'qq': hr_userprofile.qq,
        }
        return hr_contact

    @transaction.atomic
    def post(self, request, task_id, resume_id):
        user = request.user
        now = datetime.datetime.now()
        task_query = UserAcceptTask.objects.select_related(
            'feed',
            'feed__user',
        ).filter(
            user=user,
            id=task_id,
            feed__deleted=False,
            feed__feed_expire_time__gt=now,
        )
        if not task_query:
            raise Http404

        task = task_query[0]
        task_resume_query = task.task_resumes.filter(
            resume__id=resume_id
        )

        if not task_resume_query:
            raise Http404

        contact_info_query = user.contact_infos.all()
        form = UserContactInfoForm(request.POST) if not contact_info_query else UserContactInfoForm(request.POST, instance=contact_info_query[0])
        if form.is_valid():
            user_contact = form.save(commit=False)
            user_contact.user = user
            user_contact.save()

            task_resume = task_resume_query[0]
            task.has_hr_info = True
            task.save()

            follow_record = self.save_follow_record(task_resume)
            notify_msg = '互助伙伴%s（%s）给你推荐了一封简历，<br>并且近期可能会联系你（<a class="c0091fa" href="%s">查看详情</a>）' % (
                user_contact.name,
                user_contact.phone,
                PartnerNotify.resume_follow_url(follow_record.id)
            )
            follow_record.desc = notify_msg
            follow_record.save()

            PartnerNotify.follow_resume_notify(
                task.feed.user,
                notify_msg,
            )

            return JsonResponse({
                'status': 'ok',
                'msg': 'ok',
                'contact_info': self.get_hr_info(task_resume)
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'errors': form.errors,
            })


class TaskCoinRecordList(LoginRequiredMixin, PaginatedJSONListView):

    models = TaskCoinRecord
    context_object_name = 'data'
    paginate_by = 6

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        user = self.request.user
        queryset = self.models.objects.select_related(
            'upload_resume',
        ).filter(
            task__id=task_id,
            task__user=user,
        ).order_by('-id')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCoinRecordList, self).get_context_data(*args, **kwargs)
        data = context.get('data', [])
        context['data'] = [
            {
                'record_time': d.record_time.strftime('%Y-%m-%d %H:%M'),
                'resume_name': d.upload_resume.name,
                'desc': d.desc,
                'coin': d.coin,
            }
            for d in data
        ]
        return context


class GrantTakingWork(StaffRequiredMixin, View):

    grant_method = PartnerCoinUtils.taking_work
    grant_type = 'normal'

    @transaction.atomic
    def post(self, request, resume_task_id):
        coin = get_int(request.POST.get('coin'))

        if not coin:
            return JsonResponse({
                'result': 'form_error',
                'new_data': {'offline_pay_success': u'金币错误'},
                'new_html': {'offline_pay_success': u'金币错误'},
            })

        user_task_resume = UserTaskResume.objects.select_related(
            'task__feed',
            'resume',
            'resume__user',
        ).get(
            id=resume_task_id,
        )

        self.grant_method(
            user_task_resume.task.feed.feed_obj_id,
            user_task_resume.resume.resume_id,
            coin,
        )

        if self.grant_type == 'normal':
            user = user_task_resume.resume.user
            level_utils = PartnerLevelUtils(user)
            level_status = level_utils.get_taking_work_level()
            if level_status['level'] > 1:
                update_fields = {
                    'verify': False,
                    'extra_grant': True,
                }
            else:
                update_fields = {
                    'verify': False
                }

            UserTaskResume.objects.filter(
                id=resume_task_id,
            ).update(
                **update_fields
            )

        if self.grant_type == 'extra':
            UserTaskResume.objects.filter(
                id=resume_task_id,
            ).update(
                extra_grant=False,
            )

        return JsonResponse({
            'result': 'success',
            'new_data': {'offline_pay_success': u'奖励成功'},
            'new_html': {'offline_pay_success': u'奖励成功'},
        })


class TaskInfo(LoginRequiredMixin, View, FeedDictMixin):

    def get(self, request, task_id):
        now = datetime.datetime.now()
        feed_query = Feed.objects.select_related(
            'company',
        ).prefetch_related(
            'job_domain',
            'company_prefer',
            'company__category',
        ).filter(
            id=task_id,
            deleted=False,
            feed_expire_time__gt=now,
        )

        if not feed_query:
            return JsonResponse({
                'status': 'data_error',
                'msg': '没有找到有效的任务数据',
            })

        task_dict_list = [self.get_feed_dict(f) for f in list(feed_query)]
        task_dict = task_dict_list[0]

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'feed': task_dict,
            },
        })


class CheckFollowMsg(LoginRequiredMixin, View):

    def get(self, request, follow_id):
        user = request.user
        follow_record_query = FollowTaskRecord.objects.select_related(
            'task_resume__resume',
            'task_resume__task__feed',
        ).filter(
            task_resume__task__feed__user=user,
            id=follow_id
        )

        if not follow_record_query:
            raise Http404

        follow_record = follow_record_query[0]
        if not follow_record.has_check:
            now = datetime.datetime.now()
            follow_record.has_check = True
            follow_record.check_time = now
            follow_record.save()

        return redirect(
            PartnerNotify.resume_display_url(
                follow_record.task_resume.resume.resume_id,
                follow_record.task_resume.task.feed.feed_obj_id,
            ),
        )


class PartnerRecoTaskCheck(LoginRequiredMixin, View):

    cache_key = 'PARTNER_TASK_CHECK_COUNT'

    def expire_time(self):
        now = datetime.datetime.now()
        tomorrow = get_tomorrow()
        expire_time = (tomorrow - now).total_seconds()
        return expire_time

    def get(self, request):
        count = cache.get(self.cache_key, 0)
        count += 1
        cache.set(self.cache_key, count, self.expire_time())

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })


class CheckResumeInfo(LoginRequiredMixin, View):

    info_meta = {
        'email': {
            'valid_method': error_email,
        },
        'phone': {
            'valid_method': error_phone,
        },
    }

    check_info = 'phone'

    def get(self, request):
        '''
        判断简历重复需要从上传简历和简历库判断
        新录入简历判断重复，直接从pinbot简历库ContactInfoData里判断是否存在，
        即没有录入简历UploadResume并且ContactInfoData不存在才能通过

        编辑简历判断重复，如果用户编辑的简历联系信息是自己上传的简历UploadResume即可以录入
        如果用户编辑的简历联系信息不存在，并且不在聘宝简历库中，与新简历信息录入判断逻辑一
        致
        '''
        info = request.GET.get('info', '').strip()
        resume_id = get_int(request.GET.get('id', ''))
        info_setting = self.info_meta[self.check_info]

        invalid_info = info_setting['valid_method'](info)
        if invalid_info:
            return JsonResponse({
                'status': 'invalid_format',
                'msg': '格式错误',
            })

        has_resume = UploadResume.objects.filter(
            **{self.check_info: info}
        ).values_list('id', flat=True)

        has_contact = ContactInfoData.objects.filter(
            **{self.check_info: info}
        ).exists()

        if not has_resume and not has_contact:
            status = 'ok'
        elif resume_id in has_resume:
            status = 'ok'
        else:
            status = 'exist'

        return JsonResponse({
            'status': status,
            'msg': status,
        })
