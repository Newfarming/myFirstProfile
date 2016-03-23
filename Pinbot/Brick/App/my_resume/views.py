# coding: utf-8

import bson

from django.shortcuts import render
from django.views.generic.base import View
from django.db import transaction
from django.db.models import Q
from django.forms.models import model_to_dict

from .models import (
    Resume,
    ResumeTargetCity,
    ResumePositionTag,
    SocialPage,
    ResumePreferField,
)
from .forms import (
    SocialPageForm,
    WorkExperienceForm,
    ProjectForm,
    EducationForm,
    ProfessionalSkillForm,
)
from .resume_utils import (
    asyn_sync_resume,
)

from Brick.App.job_hunting.templatetags.job_tags import (
    cn_display,
)
from Brick.App.system.models import (
    City,
    PositionCategory,
    PositionCategoryTag,
)
from jobs.models import (
    CompanyCategory,
)

from Brick.Utils.django_utils import (
    get_object_or_none,
    JsonResponse,
    get_int,
    django_model2json,
    DateTimeJSONEncoder,
)
from Brick.Utils.mixin_utils import (
    LoginRequiredMixin,
    CSRFExemptMixin,
)


class UserResumeMixin(object):

    def get_user_resume(self):
        user = self.request.user
        resume_set = Resume.objects.select_related(
            'educations',
            'projects',
            'position_tags',
            'expectation_area',
            'works',
            'projects',
            'trainings',
            'professional_skills',
            'prefer_fields',
        ).filter(
            user=user
        )
        if not resume_set:
            resume = Resume(
                user=user,
            )
            resume.resume_id = str(bson.ObjectId())
            resume.save()
        else:
            resume = resume_set[0]
        return resume


class SelectGender(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    def get(self, request):
        resume = self.get_user_resume()
        gender = resume.gender
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'gender': gender,
            }
        })

    def post(self, request):
        gender = request.POST.get('gender')
        if gender not in ('male', 'female'):
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的性别',
            })
        resume = self.get_user_resume()
        resume.gender = gender
        resume.save()
        return JsonResponse({
            'status': 'ok',
            'msg': '选择成功',
            'data': {
                'gender': gender,
            }
        })


class SelectCity(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    def get(self, request):
        resume = self.get_user_resume()
        expectation_area = resume.expectation_area.filter().values(
            'city__id',
        )
        city = City.objects.filter().values('id', 'name')
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'city': list(city),
                'expectation_area': list(expectation_area),
            }
        })

    def post(self, request):
        city_list = request.POST.getlist('city[]', [])
        resume = self.get_user_resume()

        city = [get_object_or_none(City, id=get_int(c)) for c in city_list]
        if not city or None in city:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的城市',
                'data': {
                    'city': city_list,
                }
            })

        with transaction.atomic():
            ResumeTargetCity.objects.filter(
                resume=resume
            ).delete()
            for c in city:
                target_city = ResumeTargetCity(
                    resume=resume,
                    city=c,
                )
                target_city.save()
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'city': city_list,
            }
        })


class SelectPositionCategory(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    def get(self, request):
        resume = self.get_user_resume()
        job_category = resume.job_category

        if job_category:
            category = job_category.id
        else:
            category = None
        position = PositionCategory.objects.filter().values('id', 'name')

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'category': category,
                'position': list(position),
            }
        })

    def post(self, request):
        category = request.POST.get('category')
        position_category = get_object_or_none(
            PositionCategory,
            id=category,
        )
        if not position_category:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的职位类别',
                'data': {
                    'category': category,
                }
            })
        resume = self.get_user_resume()
        with transaction.atomic():
            resume.job_category = position_category
            resume.save()
            resume.position_tags.filter(
                ~Q(position_tag__category=position_category)
            ).delete()
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'category': category,
            }
        })


class SelectCategoryTag(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    def get(self, request):
        resume = self.get_user_resume()
        job_category = resume.job_category
        if not job_category:
            return JsonResponse({
                'status': 'no_category',
                'msg': '没有选择职位类别',
                'data': {
                },
            })
        resume_tag = resume.position_tags.filter().values(
            'position_tag__id',
        )
        category_tag_query = PositionCategoryTag.objects.select_related(
            'child_tags'
        ).filter(
            category=job_category,
            parent=None,
        )

        category_tag = [
            {
                'id': c.id,
                'name': c.name,
                'child': list(c.child_tags.all().values(
                    'id',
                    'name',
                )),
            }
            for c in category_tag_query
        ]

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'resume_tag': list(resume_tag),
                'category_tag': list(category_tag),
                'previous_tag': {
                    'id': job_category.id,
                    'name': job_category.name,
                    'level': 1,
                },
            }
        })

    def post(self, request):
        resume = self.get_user_resume()
        job_category = resume.job_category
        if not job_category:
            return JsonResponse({
                'status': 'no_category',
                'msg': '没有选择职位类别',
                'data': {
                },
            })

        category_tag = request.POST.getlist('tag[]', '')

        tag = [
            get_object_or_none(PositionCategoryTag, id=t)
            for t in category_tag
        ]
        if not tag or None in tag:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的标签',
                'data': {
                    'category_tag': category_tag,
                },
            })

        with transaction.atomic():
            ResumePositionTag.objects.filter(
                resume=resume
            ).delete()

            code_name_list = []
            for t in tag:
                if t.name in code_name_list:
                    continue
                resume_tag = ResumePositionTag(
                    resume=resume,
                    position_tag=t,
                )
                resume_tag.save()
                code_name_list.append(t.name)

        if len(tag) == 1:
            child_tags = tag[0].child_tags.all().values(
                'id',
                'name',
            )
            previous_tag = {
                'id': tag[0].id,
                'name': tag[0].name,
            }
        else:
            child_tags = []
            previous_tag = {}

        resume_tag = resume.position_tags.filter().values(
            'position_tag__id',
        )

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'category_tag': list(child_tags),
                'resume_tag': list(resume_tag),
                'previous_tag': previous_tag,
            }
        })


class SelectDegree(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):
    degree_meta = [d for d in Resume.DEGREE_META if d[0]]
    degree_keys = [d[0] for d in Resume.DEGREE_META if d[0]]

    def get(self, request):
        resume = self.get_user_resume()
        degree = resume.degree

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'degree': degree,
                'degree_meta': self.degree_meta,
            }
        })

    def post(self, request):
        degree = request.POST.get('degree')
        if degree not in self.degree_keys:
            return JsonResponse({
                'status': 'form_error',
                'msg': '选择正确的学历',
                'data': {
                    'degree': degree,
                }
            })

        resume = self.get_user_resume()
        resume.degree = degree
        resume.save()
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'degree': degree,
            }
        })


class SelectWorkyears(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    work_year_meta = range(2, 7)

    def get(self, request):
        resume = self.get_user_resume()
        work_years = resume.work_years

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'work_years': work_years,
                'work_year_meta': self.work_year_meta,
            }
        })

    def post(self, request):
        work_years = get_int(request.POST.get('work_years'))
        if work_years not in self.work_year_meta:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的工作年限',
                'data': {
                    'work_years': work_years,
                }
            })
        resume = self.get_user_resume()
        resume.work_years = work_years
        resume.save()
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'work_years': work_years,
            }
        })


class ShowResume(LoginRequiredMixin, View, UserResumeMixin):

    template = 'show_resume.html'

    def get_resume_json(self, resume):
        resume_dict = model_to_dict(
            resume,
            fields=(
                'id',
                'job_category',
                'name',
                'phone',
                'email',
                'age',
                'work_years',
                'gender',
                'self_evaluation',
                'social_page',
            )
        )
        resume_dict['educations'] = list(resume.educations.values(
            'start_time',
            'end_time',
            'school',
            'degree',
            'major',
            'id',
        ))
        resume_dict['projects'] = list(resume.projects.values(
            'id',
            'project_desc',
            'start_time',
            'end_time',
            'responsible_for',
            'project_name',
            'company_name',
        ))
        resume_dict['position_tags'] = list(resume.position_tags.values(
            'id',
            'position_tag__name',
        ))
        resume_dict['expectation_area'] = list(resume.expectation_area.values(
            'id',
            'city__name',
        ))
        resume_dict['works'] = list(resume.works.values(
            'id',
            'start_time',
            'end_time',
            'position_title',
            'company_name',
            'job_desc',
        ))
        resume_dict['professional_skills'] = list(resume.professional_skills.values(
            'id',
            'skill_desc',
            'proficiency',
            'month',
        ))
        if hasattr(resume, 'social_page'):
            social_page = resume.social_page
            resume_dict['social_page'] = {
                'twitter': social_page.twitter,
                'weibo': social_page.weibo,
                'zhihu': social_page.zhihu,
                'github': social_page.github,
                'dribbble': social_page.dribbble,
                'douban': social_page.douban,
                'linkedin': social_page.linkedin,
            }
        else:
            resume_dict['social_page'] = {
                'twitter': '',
                'weibo': '',
                'zhihu': '',
                'github': '',
                'dribbble': '',
                'douban': '',
                'linkedin': '',
            }
        json_obj = django_model2json(resume_dict, cls=DateTimeJSONEncoder)
        return json_obj

    def get(self, request):
        resume = self.get_user_resume()
        resume_json = self.get_resume_json(resume)
        send_btn = request.GET.get('send')

        return render(
            request,
            self.template,
            {
                'resume': resume,
                'resume_json': resume_json,
                'send_btn': send_btn,
            }
        )


class PersonInfo(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):
    form = None

    def post(self, request):
        resume = self.get_user_resume()
        form = self.form(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            asyn_sync_resume.delay(self.request.user)
            return JsonResponse({
                'status': 'ok',
                'msg': 'ok',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'data': {
                    'errors': form.errors,
                }
            })


class SocialPageView(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    def get_social_page(self, resume):
        social_page = get_object_or_none(
            SocialPage,
            resume=resume,
        )
        if not social_page:
            social_page = SocialPage(
                resume=resume
            )
            social_page.save()
        return social_page

    def post(self, request, page_type):

        form = SocialPageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            url = data['url']
            resume = self.get_user_resume()
            social_page = self.get_social_page(resume)
            social_page.__dict__[page_type] = url
            social_page.save()

            return JsonResponse({
                'status': 'ok',
                'msg': '保存成功',
            })
        else:
            return JsonResponse({
                'status': 'form_error',
                'msg': '表单错误',
                'data': {
                    'errors': form.errors,
                }
            })


class AbstractAdditionInfo(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    form = WorkExperienceForm

    def get_update_obj(self, resume):
        update_id = self.request.POST.get('update_id', '0')
        update_obj = resume.works.filter(
            id=get_int(update_id)
        )
        return update_obj

    def post(self, request):
        resume = self.get_user_resume()
        update_obj = self.get_update_obj(resume)
        if update_obj:
            obj = update_obj[0]
            form = self.form(request.POST, instance=obj)
        else:
            form = self.form(request.POST)

        if form.is_valid():
            save_obj = form.save(commit=False)
            save_obj.resume = resume
            save_obj.save()
            asyn_sync_resume.delay(self.request.user)
            result = {
                'status': 'ok',
                'msg': 'ok',
                'data': {
                    'update_id': save_obj.id
                }
            }
        else:
            result = {
                'status': 'form_error',
                'msg': '表单错误',
                'data': {
                    'errors': form.errors,
                }
            }
        return JsonResponse(result)


class WorkExperienceView(AbstractAdditionInfo):
    pass


class EducationView(AbstractAdditionInfo):
    form = EducationForm

    def get_update_obj(self, resume):
        update_id = get_int(self.request.POST.get('update_id', '0'))
        obj = resume.educations.filter(
            id=update_id
        )
        return obj


class ProjectView(AbstractAdditionInfo):
    form = ProjectForm

    def get_update_obj(self, resume):
        update_id = get_int(self.request.POST.get('update_id', '0'))
        obj = resume.projects.filter(
            id=update_id
        )
        return obj


class ProfessionalSkillView(AbstractAdditionInfo):
    form = ProfessionalSkillForm

    def get_update_obj(self, resume):
        update_id = get_int(self.request.POST.get('update_id', '0'))
        obj = resume.professional_skills.filter(
            id=update_id
        )
        return obj


class DeleteAdditionInfo(LoginRequiredMixin, View, UserResumeMixin):

    model = None

    def get(self, request, obj_id):
        resume = self.get_user_resume()
        self.model.objects.filter(
            resume=resume,
            id=obj_id,
        ).delete()

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'obj_id': obj_id,
            },
        })


class EditResumeTag(LoginRequiredMixin, View, UserResumeMixin):

    template = 'edit_resume_tag.html'

    def get(self, request):
        resume = self.get_user_resume()
        selected = {
            'city': list(resume.expectation_area.all().select_related('city').values_list('city__name', flat=True)),
            'gender': cn_display(resume.gender),
            'job_category': resume.job_category.name if resume.job_category else '',
            'category_tag': [
                {
                    'name': t[0],
                    'id': t[1],
                }
                for t in list(resume.position_tags.select_related('position_tag').all().values_list('position_tag__name', 'id'))
            ],
            'degree': cn_display(resume.degree),
            'work_years': cn_display(resume.work_years),
            'recommend_tag': [
                {'id': 1, 'name': 'hello'},
                {'id': 2, 'name': 'word'},
            ],
            'salary_lowest': resume.salary_lowest,
        }

        return JsonResponse({
            'status': 'ok',
            'msg': '成功',
            'data': {
                'selected': selected,
            }
        })


class EditCategoryTag(
        CSRFExemptMixin,
        LoginRequiredMixin,
        View,
        UserResumeMixin):

    def get(self, request):
        category = request.GET.get('category', '0')
        position_category = get_object_or_none(
            PositionCategory,
            id=category,
        )
        if not position_category:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的职位类别',
                'data': {
                    'category': category,
                }
            })

        resume = self.get_user_resume()
        resume_tag = resume.position_tags.filter().values(
            'position_tag__id',
        )
        category_tag_query = PositionCategoryTag.objects.filter(
            category=position_category,
            parent=None,
        ).prefetch_related(
            'child_tags',
        )

        category_tag = [
            {
                'id': c.id,
                'name': c.name,
                'child': [
                    {
                        'id': ct.id,
                        'name': ct.name,
                    }
                    for ct in list(c.child_tags.all())],
            }
            for c in list(category_tag_query)
        ]

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'resume_tag': list(resume_tag),
                'category_tag': list(category_tag),
                'previous_tag': {
                    'id': position_category.id,
                    'name': position_category.name,
                    'level': 1,
                },
            }
        })

    def post(self, request):
        category = request.POST.get('category', '0')
        position_category = get_object_or_none(
            PositionCategory,
            id=category,
        )
        if not position_category:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的职位类别',
                'data': {
                    'category': category,
                }
            })

        category_tag = request.POST.getlist('tag[]', '')
        tag = [
            get_object_or_none(
                PositionCategoryTag,
                id=t,
                category=position_category
            )
            for t in category_tag
        ]
        tag = [t for t in tag if t]
        if not tag:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的标签',
                'data': {
                    'category_tag': category_tag,
                },
            })

        resume = self.get_user_resume()
        with transaction.atomic():
            resume.job_category = position_category
            resume.save()
            resume.position_tags.filter().delete()

            code_name_list = []
            for t in tag:
                if t.name in code_name_list:
                    continue
                resume_tag = ResumePositionTag(
                    resume=resume,
                    position_tag=t,
                )
                resume_tag.save()
                code_name_list.append(t.name)

        return JsonResponse({
            'status': 'ok',
            'msg': '修改成功',
        })


class DeleteResumeTag(LoginRequiredMixin, View, UserResumeMixin):

    def get(self, request, tag_id):
        resume = self.get_user_resume()
        resume.position_tags.filter(id=tag_id).delete()
        return JsonResponse({
            'status': 'ok',
            'msg': '删除成功',
        })


class AddResumeTag(CSRFExemptMixin, LoginRequiredMixin, View, UserResumeMixin):

    def get(self, request):
        resume = self.get_user_resume()
        job_category = resume.job_category
        if not job_category:
            return JsonResponse({
                'status': 'data_error',
                'msg': 'no job category',
            })
        category_tag_query = PositionCategoryTag.objects.filter(
            category=job_category,
        ).values(
            'name',
            'id',
        )
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': list(category_tag_query),
        })

    def post(self, request):
        tag_id = request.POST.get('tag_id', '0')
        tag = get_object_or_none(
            PositionCategoryTag,
            id=tag_id,
        )
        if not tag:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的标签',
            })

        resume = self.get_user_resume()
        job_category = resume.job_category
        if not job_category:
            return JsonResponse({
                'status': 'data_error',
                'msg': 'no job category',
            })

        has_tag = resume.position_tags.filter(
            position_tag__name=tag.name
        )
        if not has_tag:
            resume_tag = ResumePositionTag(
                resume=resume,
                position_tag=tag,
            )
            resume_tag.save()
        return JsonResponse({
            'status': 'ok',
            'msg': '添加成功',
            'data': [
                {
                    'name': t.position_tag.name,
                    'id': t.id,
                }
                for t in resume.position_tags.all()
            ],
        })


class EditSalaryLowest(
        CSRFExemptMixin,
        LoginRequiredMixin,
        View,
        UserResumeMixin):

    SALARY_MIN = 1000
    SALARY_MAX = 9999999

    def get(self, request):
        resume = self.get_user_resume()
        salary_lowest = resume.salary_lowest

        return JsonResponse({
            'status': 'ok',
            'msg': '成功',
            'data': {
                'salary_lowest': salary_lowest,
            },
        })

    def post(self, request):
        salary_lowest_str = request.POST.get('salary_lowest', '0')
        salary_lowest = get_int(salary_lowest_str)
        if salary_lowest > self.SALARY_MAX or salary_lowest < self.SALARY_MIN:
            return JsonResponse({
                'status': 'form_error',
                'msg': '最低薪资范围必须在%s-%s之间' % (self.SALARY_MIN, self.SALARY_MAX),
                'data': {
                    'salary_lowest': salary_lowest
                }
            })

        resume = self.get_user_resume()
        resume.salary_lowest = salary_lowest
        resume.save()
        return JsonResponse({
            'status': 'ok',
            'msg': '保存成功',
        })


class SelectPreferField(
        CSRFExemptMixin,
        LoginRequiredMixin,
        View,
        UserResumeMixin):

    def get(self, request):
        resume = self.get_user_resume()
        prefer_fields = resume.prefer_fields.all().values(
            'category__id',
        )
        all_fields = CompanyCategory.objects.filter(
            brick_display=True,
        ).order_by(
            '-sort'
        ).values(
            'category',
            'id',
        )
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'prefer_fields': list(prefer_fields),
                'all_fields': list(all_fields),
            },
        })

    def post(self, request):
        field_id_list = request.POST.getlist('field_id_list[]', '')
        fields = [
            get_object_or_none(CompanyCategory, id=t, brick_display=True)
            for t in field_id_list
        ]
        if not fields or None in fields:
            return JsonResponse({
                'status': 'form_error',
                'msg': '请选择正确的标签',
                'data': {
                    'field_id_list': field_id_list,
                },
            })

        resume = self.get_user_resume()
        with transaction.atomic():
            ResumePreferField.objects.filter(
                resume=resume
            ).delete()

            for f in fields:
                resume_fields = ResumePreferField(
                    resume=resume,
                    category=f,
                )
                resume_fields.save()

        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
            'data': {
                'prefer_fields': field_id_list,
            },
        })
