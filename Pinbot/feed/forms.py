# coding:utf-8
'''
Created on 2013-11-28

@author: likaiguo.happy@163.com 2013-11-28 11:01:49
'''

import bleach
from django import forms
from .models import (
    Feed,
)

from Common.forms import NormalizeFormStringMixin
from pin_utils.django_utils import (
    get_int
)
from pin_utils.form_mixin import (
    FormErrors,
)


class BaseFeedForm(NormalizeFormStringMixin, forms.ModelForm, FormErrors):

    def clean_salary_min(self):
        salary_min = self.data['salary_min']
        salary_min = get_int(salary_min)
        salary_max = self.data['salary_max']
        salary_max = get_int(salary_max)

        if salary_min == 0 and salary_max == 1000000:
            return salary_min
        if salary_min < 1000 or salary_min > 1000001:
            raise forms.ValidationError(u'最小薪资有误，薪资数在1000~1000000之间')
        return salary_min

    def clean_salary_max(self):
        salary_min = self.data['salary_min']
        salary_min = get_int(salary_min)
        salary_max = self.data['salary_max']
        salary_max = get_int(salary_max)

        if salary_min == 0 and salary_max == 1000000:
            return salary_max
        if salary_max < 1000 or salary_max > 10000001:
            raise forms.ValidationError(u'最大薪资有误，薪资数在1000~1000000之间')
        if salary_min > salary_max:
            raise forms.ValidationError(u'最大薪资小于最小薪资，请重新填写')
        if salary_min * 2 < salary_max:
            raise forms.ValidationError(u'最高薪资不能高于最低薪资的两倍，请重新填写')
        return salary_max

    def clean_job_desc(self):
        job_desc = self.data['job_desc'].strip()
        if not job_desc:
            raise forms.ValidationError(u'职位描述必填')
        if len(job_desc) > 1000:
            raise forms.ValidationError(u'必须在1000字符以内')
        return bleach.clean(job_desc, tags=['br'], strip=True)


class FeedNewForm(BaseFeedForm):
    """
    @summary: 添加新的订阅表单

    """

    class Meta:
        model = Feed
        fields = (
            'job_desc',
            'salary_min',
            'salary_max',
            'skill_required',
            'expect_area',
            'talent_level',
            'job_type',
            'keywords',
            'title',
        )


class NewFeedForm(BaseFeedForm):

    analyze_fields = (
        'language',
        'degree',
        'gender',
        'major',
        'job_type',
    )
    unrequired_fields = (
        'company_prefer',
        'job_domain',
        'job_welfare',
        'job_desc',
    )

    def __init__(self, *args, **kwargs):
        self.post_data = kwargs.pop('post_data')
        super(NewFeedForm, self).__init__(*args, **kwargs)

        if self.instance and not self.instance.title:
            self.fields['title'] = forms.CharField(label='职位名称', max_length=100)

        for i in self.analyze_fields + self.unrequired_fields:
            self.fields[i].required = False

    def clean_job_desc(self):
        job_desc = self.cleaned_data['job_desc']
        return job_desc or u''

    class Meta:
        model = Feed
        fields = (
            'keywords',
            'talent_level',
            'expect_area',
            'title',
            'salary_min',
            'salary_max',
            'job_domain',
            'job_welfare',
            'company_prefer',
            'language',
            'degree',
            'gender',
            'major',
            'job_type',
            'job_desc',
            'analyze_titles',
        )
        error_messages = {
            'keywords': {
                'max_length': u"最多添加15个技能关键词",
            },
            'analyze_titles': {
                'max_length': u"最多添加15个职位拓展名",
            },
            'job_desc': {
                'max_length': u"必须少于1000字",
            },
            'skill_required': {
                'max_length': u"必须少于1000字",
            },
        }


class ChangeFeedForm(NewFeedForm):

    class Meta:
        model = Feed
        fields = (
            'keywords',
            'talent_level',
            'job_desc',
            'salary_min',
            'salary_max',
            'job_domain',
            'job_welfare',
            'company_prefer',
            'language',
            'language',
            'degree',
            'gender',
            'major',
            'job_type',
            'analyze_titles',
        )
        error_messages = {
            'keywords': {
                'max_length': u"最多添加15个技能关键词",
            },
            'analyze_titles': {
                'max_length': u"最多添加15个职位拓展名",
            },
            'job_desc': {
                'max_length': u"必须少于1000字",
            },
            'skill_required': {
                'max_length': u"必须少于1000字",
            },
        }


class FeedStep1Form(BaseFeedForm):

    class Meta:
        model = Feed
        fields = (
            'title',
            'talent_level',
            'job_desc',
            'expect_area',
        )
