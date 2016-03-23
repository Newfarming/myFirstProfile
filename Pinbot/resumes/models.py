# coding: utf-8

import re

import datetime
import time
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import json
from mongoengine import *

from basic_service import cn2digit
from basic_service.basic import get_month, compare_time
from basic_service.resume_util import *
from Pinbot.settings import jieba_user_dict_file
import jieba.analyse
jieba.load_userdict(jieba_user_dict_file)
from variables.resume_global_variables import KEYWORDS_SET, DEGREE_LIST, SOURCE_DICT
from variables.score_variables import POSTION_TITLE_DICT


class UserResumeRead(Document):

    """
    记录用户的订阅简历点击记录
    """
    username = StringField(default='')
    feed_id = StringField(default='')
    read_id_list = ListField(default=[])  # 已读简历id列表


class Education(EmbeddedDocument):
    start = StringField(required=False, default='')
    end = StringField(required=False, default='')
    school = StringField(required=False, default='')
    degree = StringField(required=False, default='')
    major = StringField(required=False, default='')

    def to_dict(self):
        return {'start': self.start, 'end': self.end,
                'school': self.school, 'degree': self.degree,
                }


class OtherInfo(EmbeddedDocument):
    title = StringField(required=False, default='')
    content = StringField(required=False, default='')


class WorkHistory(EmbeddedDocument):
    start = StringField(required=False, default='')
    end = StringField(required=False, default='')
    company = StringField(required=False, default='')
    position = StringField(required=False, default='')


class WorkExperience(EmbeddedDocument):
    start_time = StringField(required=False, db_field="startTime", default='')
    end_time = StringField(required=False, db_field="endTime", default='')
    duration = StringField(required=False, db_field="druation", default='')

    position_title = StringField(
        required=False, db_field="positionTitle", default='')
    company_name = StringField(
        required=False, db_field="companyName", default='')
    job_desc = StringField(required=False, db_field="jobDesc", default='')

    industry_category = StringField(
        required=False, db_field="industryCatagory", default='')
    salary = StringField(required=False, db_field="salary")
    position_category = StringField(
        required=False, db_field="positionCatagory", default='')
    company_category = StringField(
        required=False, db_field="companyCatagory", default='')
    company_scale = StringField(
        required=False, db_field="companyScale", default='')

    def to_dict(self):

        return {'start_time': self.start_time,
                'end_time': self.end_time,
                'duration': self.duration,
                'position_title': self.position_title,
                'company_name': self.company_name,
                'job_desc': self.job_desc,
                "salary": self.salary,
                }

    def get_work_content(self):

        return self.position_title + self.job_desc + self.company_name


class EducationExperience(EmbeddedDocument):
    start_time = StringField(required=False, db_field="startTime")
    end_time = StringField(required=False, db_field="endTime")
    school = StringField(required=False, db_field='school')
    degree = StringField(required=False, db_field='degree')
    major = StringField(required=False, db_field='major')

    def to_dict(self):

        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "school": self.school,
            'degree': self.degree,
            'major': self.major
        }

    def get_text(self):

        text = "%s-%s %s %s %s" % (self.start_time, self.end_time, self.school,
                                   self.major, self.degree)
        return text


class ProjectExperience(EmbeddedDocument):
    start_time = StringField(required=False, db_field="startTime")
    end_time = StringField(required=False, db_field="endTime")
    hard_envir = StringField(required=False, db_field="hardEnvir", default='')
    software_envir = StringField(
        required=False, db_field="softwareEnvir", default='')
    develop_tool = StringField(
        required=False, db_field="developTool", default='')
    project_name = StringField(
        required=False, db_field="projectTitle", default='')

    responsible_for = StringField(
        required=False, db_field="responsibleFor", default='')
    job_title = StringField(required=False, default='')
    project_desc = StringField(
        required=False, db_field="projectDesc", default='')

    company_name = StringField(default='')

    def to_dict(self):

        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'project_name': self.project_name,
            'project_desc': self.project_desc,
        }

    def get_proj_content(self):

        return self.responsible_for + self.develop_tool + self.project_desc

    def get_proj_all_text(self):

        return self.software_envir + ',' + self.hard_envir + ',' + \
            self.responsible_for + self.develop_tool + self.project_desc


class TrainExperience(EmbeddedDocument):
    certificate = StringField(required=False)
    course = StringField(required=False)
    start_time = StringField(required=False, db_field="startTime")
    end_time = StringField(required=False, db_field="endTime")
    instituation = StringField(required=False)
    location = StringField(required=False)
    train_desc = StringField(required=False, db_field="trainDesc")

    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "instituation": self.instituation,
            'certificate': self.certificate,
            'course': self.course,
            'location': self.location,
            'train_desc': self.train_desc,
        }


class ProfessionalSkill(EmbeddedDocument):
    skill_desc = StringField(required=False, db_field='skillDesc')
    proficiency = StringField(required=False, db_field='proficiency')
    months = StringField(required=False, db_field='months')

    def get_text(self):

        return self.skill_desc


class JobTarget(EmbeddedDocument):
    job_career = StringField(required=False, db_field='jobCareer', default='')
    job_category = StringField(
        required=False, db_field='jobCatagory', default='')
    job_industry = StringField(
        required=False, db_field='jobIndustry', default='')
    expectation_area = StringField(
        required=False, db_field='jobLocation', default='')
    salary = StringField(required=False, db_field='salary', default='')
    job_hunting_state = StringField(
        required=False, db_field='status', default='')
    enroll_time = StringField(
        required=False, db_field='enrollTime', default='')

    def job_hunting_brief(self, source=''):
        desc = self.job_hunting_state.strip() + self.enroll_time.strip()

        hunting_pattern = re.compile(ur'正考虑|观望|看看新机会|急寻新工作|更好的工作机会')
        quit_hunting_pattern = re.compile(ur'离职状态|正在找工作')
        stable_pattern = re.compile(ur'暂无跳槽打算|无换工作的计划|不想找工作|暂无跳槽打算')
        graduate_pattern = re.compile(ur'应届毕业生')

        if hunting_pattern.search(desc):
            brief_desc = '观望(仍在职)'
        elif quit_hunting_pattern.search(desc):
            brief_desc = '求职(已离职)'
        elif stable_pattern.search(desc):
            brief_desc = '稳定(仍在职)'
        elif graduate_pattern.search(desc):
            brief_desc = '应届毕业生'
        else:
            brief_desc = desc

        return brief_desc

    def get_expectation_area_list(self, top=5):
        return self.expectation_area.replace(
            '，', ','
        ).replace(
            '、', ','
        ).replace(
            '；', ','
        ).replace(
            ';', ','
        ).split(',')[:top]

    def set_expectation_area_list(self):
        self.expectation_area = self.get_expectation_area_list()

    def get_text(self):

        return self.job_career + self.job_category + self.expectation_area + self.job_industry


class Certificate(Document):
    acquire_time = StringField(required=False)
    certificateTitle = StringField(required=False)
    comment = StringField(required=False)


class LanguageSkill(Document):
    category = StringField(required=False)
    listen_speark_ablility = StringField(required=False)
    read_write_ability = StringField(required=False)


class CollectedResume(Document):
    userid = StringField(required=True)
    url = StringField(required=True)
    html = StringField(required=False)
    search_keywords = StringField(required=False)
    add_time = DateTimeField(
        db_field='createtime', default=datetime.datetime.now())
    resume_update_time = StringField(required=False)  # 简历更新时间,特别是将搜索结果写入
    status = StringField(default='processing')
    source = StringField()
    res_id = StringField()
    text = StringField()

    meta = {
        'index_background': True,
        'db_alias': 'spiders',
        "indexes": [
            '-add_time',
            'userid',
            'url',
            "status",
            'res_id',
            '-resume_update_time',
            'source',
        ]
    }


class CommonResumeData(Document):
    status = StringField(default='processing')
    resume_type = StringField(default='', required=False)

    name = StringField(required=False, default='')
    email = StringField(required=False, default='')
    phone = StringField(required=False, default='')
    age = IntField(required=False, default=0)
    gender = StringField(required=False, default=u'男')
    birthday = StringField(required=False, default='')
    marital_status = StringField(
        required=False, default='', db_field='maritalStatus')
    political_landscape = StringField(
        required=False, default='', db_field='politicalLandscape')

    avatar_url = StringField(required=False, db_field='image_url', default='')

    address = StringField(
        required=False, db_field='address', default='')  # 现居地
    residence = StringField(
        required=False, db_field='residence', default='')  # 常住地

    work_years = StringField(
        required=False, db_field='workExperienceLength', default='')
    urls = ListField(default=[])
    job_target = EmbeddedDocumentField(
        JobTarget, required=False, db_field='jobTarget')

    educations = ListField(EmbeddedDocumentField(
        EducationExperience), required=False, db_field='educationExperience')
    works = ListField(EmbeddedDocumentField(
        WorkExperience), required=False, db_field='workExperience')
    projects = ListField(EmbeddedDocumentField(
        ProjectExperience), required=False, db_field='projectExperience')
    trains = ListField(EmbeddedDocumentField(
        TrainExperience), required=False, db_field='trainingExperience')
    professional_skills = ListField(EmbeddedDocumentField(
        ProfessionalSkill), required=False, db_field='professionalSkill')
    self_evaluation = StringField(
        required=False, db_field='selfEvaluation', default='')

    created_at = DateTimeField(required=False, default=datetime.datetime.now())
    created_time = DateTimeField(
        required=False, default=datetime.datetime.now(), db_field='createTime')
    updated_at = DateTimeField(required=False, default=datetime.datetime.now())

    update_time = StringField(
        required=False, default='', db_field='updateTime')

    source_id = StringField(required=False, db_field='sourceID')
    duplicate_id = StringField(required=False)

    view_id = StringField(required=False, db_field='viewID')
    url_id = StringField(required=False, db_field='urlID')
    upload_user = StringField(required=False)
    source = StringField(required=False, db_field='source', default='')

    has_contact_info = StringField(
        default='NO', db_field='isCotactInformation')
    current_salary = StringField(default='', db_field='currentSalary')
    latest_salary = StringField(default='', db_field='latestSalary')
    url = StringField(db_field='url', default='')
    raw_resume_text = StringField(
        required=False, db_field='resumeContent', default='')

    resume_text = StringField(default='', db_field='resumeText')
    no_repeat_words = StringField(default="")  # 关键词组合成字符串
    keywords_list = ListField(default=[])  # 通过结巴提取的关键词列表

    watch_time = None
    other_info = EmbeddedDocumentField(
        OtherInfo, required=False, db_field='otherInfoMap')

    # C 端简历的用户
    brick_username = StringField(default='')

    def to_dict(self):
        import helper
        return helper.mongo_to_dict(self, [])

    def get_projects_dict(self, project_count=-1):
        projects_list = []
        if len(self.projects):
            for project in self.projects[:project_count]:
                projects_list.append(project.to_dict())
        return projects_list

    def get_works_dict(self, work_count=-1):
        works_list = []

        if len(self.works):
            for work in self.works[:work_count]:
                works_list.append(work.to_dict())
        return works_list

    def get_source(self):
        data = {'tag': 'other', 'text': u'其他平台'}
        for key, value in SOURCE_DICT.items():
            if key in self.source:
                data = {'tag': key, 'text': value}

        return data

    def get_update_time(self):

        if 'zhaopin' in self.url:
            update_time = time.strptime(self.update_time, '%Y-%m-%d')
            update_time = time.strftime('%Y年%m月%d日')
        elif 'liepin' in self.url:
            update_time = time.strptime(self.update_time, '%Y-%m-%d')
            update_time = time.strftime('%Y/%m/%d')
        else:
            update_time = self.update_time

        return update_time

    def get_latest_work_dict(self):
        work_dict = {
            "company_name": "",
            "position_title": "",
            "salary": "",
            "job_desc": ""
        }
        if self.works:
            work = self.works[0]
            work_dict['company_name'] = work.company_name
            work_dict['position_title'] = work.position_title
            work_dict['job_desc'] = work.job_desc
            salary_list = self.get_recent_salary()
            try:
                if sum(salary_list) == 0:
                    work_dict['salary'] = u''
                else:
                    salary_list = [str(i) for i in salary_list]
                    work_dict['salary'] = '-'.join(salary_list) + u'元/月'
            except:
                work_dict['salary'] = u''

        return work_dict

    def get_job_target_dict(self):
        job_target_dict = {
            "salary": "",
            "job_hunting_state": "",
            "expectation_area": "",
            "hunting_status": "未知",
        }

        if self.job_target:
            job_target_dict = {
                "salary": self.job_target.salary,
                "job_hunting_state": self.job_target.job_hunting_state,
                "expectation_area": self.job_target.expectation_area,
                "hunting_status": self.job_target.job_hunting_brief(self.source),
            }
        return job_target_dict

    def get_works(self, count=1):

        works_list = []
        for work in self.works[:count]:
            works_list.append(work)
        return works_list

    def get_educations_dict(self, education_count=-1):
        educations_list = []
        if len(self.educations):
            for education in self.educations[:education_count]:
                educations_list.append(education.to_dict())

        return educations_list

    def get_educations_text(self):
        if len(self.educations):
            education = self.educations[0]
            return '%s.%s' % (
                education.degree,
                education.school
            )

    def get_gender(self):
        g = self.gender.strip()
        if g == 'male':
            return '男'
        if g == 'female':
            return '女'
        return g

    def get_age(self):

        try:
            s = "%d岁" % self.age
        except:
            s = self.age
        return s

    def highest_degree(self):

        degrees = []
        for education in self.educations:
            degrees.append(education.degree.strip())

        best_degree = ''
        for degree in DEGREE_LIST:
            if degree in degrees:
                best_degree = degree
                break

        return best_degree

    def get_work_years(self, display_origin=False):

        if self.work_years:
            if isinstance(self.work_years, int):
                return self.work_years

            if u'年' in self.work_years:
                year = self.work_years.split(u'年')
                year = year[0]

                self.work_years = cn2digit.cn2dig(year)
            if isinstance(self.work_years, int):
                self.work_years = int(self.work_years)
        else:
            # 工作年限里边没有填写该信息
            months = 0.0
            if display_origin:
                self.work_years = months / 12
            else:
                for work in self.works:
                    try:
                        month = get_month(work.start_time, work.end_time)
                    except:
                        month = get_month(work.start_time, work.end_time)
                        pass
                    months += month
                if months >= 12:
                    self.work_years = int((months / 12))
                elif months > 0:
                    self.work_years = "<1"
                else:
                    self.work_years = 0

        return self.work_years

    def get_url(self):

        if 'ehire64.51job.com' in self.url:
            self.url = self.url.replace('ehire64', 'ehire')

        return self.url

    def get_resume_text(self):
        """
        @summary: 组合简历中的工作经历,自我评价,项目经历,
        """
        text = ''

        for work in self.works:
            text += work.get_work_content()
        for project in self.projects:
            text += project.get_proj_content()

        for skill in self.professional_skills:
            text += skill.get_text()

        if self.self_evaluation:
            text += self.self_evaluation

        if self.raw_resume_text:
            text += self.raw_resume_text

        if self.job_target:
            text += self.job_target.get_text()

        return text

    def extract_keywords(self, TOP_K=30):
        """
        @summary: 抽取简历中关键词,去除url链接.

        """

        text = self.get_resume_text()

        # 从简历内容提取关键词

        # 删掉文本中的url
        for url in self.urls:
            text = text.replace(url, " ")

        # 用jieba分词算法,计算出简历内容中最重要的 40个词

        tags = jieba.analyse.extract_tags(text, topK=TOP_K)
        tags = list(tags)

        english_words = get_text_words(text)
        tags.extend(english_words)

        keywords = []
        # 过一遍人工词表
        for keyword in tags:
            tmp_keyword = keyword.strip().lower()
            if tmp_keyword in KEYWORDS_SET and (tmp_keyword not in keywords):
                keywords.append(keyword)

        return keywords

    def url_to_link(self):

        no_repeat_urls = set()
        for url in self.urls:
            #             if ":" in url:
            #                 url = url.split(':')[-1]
            #             if "//" not in url:
            #                 url = "//" + url
            if "http://" not in url:
                url = "http://" + url
            no_repeat_urls.add(url)

        for url in no_repeat_urls:
            link = u"<a href='%s' target='_blank'>链接</a>" % url
            if url in self.self_evaluation:
                self.self_evaluation.replace(url, link)
            for i, work in enumerate(self.works):
                self.works[i].job_desc = work.job_desc.replace(url, link)
            for i, proj in enumerate(self.projects):
                self.projects[
                    i].project_desc = proj.project_desc.replace(url, link)
        return True

    def get_related_content(self):
        """
        @summary: 获取项目经历工作经历中文本内容
        """
        desc = ""

        for work in self.works:
            desc += work.get_work_content()

        for proj in self.projects:
            desc += proj.get_proj_content()

        return desc

    def get_text_seg_word(self):
        """
        @summary: 获取当前简历的工作经历,项目经历分词后的数据
        """
        desc = self.get_related_content()

        desc += self.self_evaluation
        desc += self.raw_resume_text

        for edu in self.educations:
            desc += edu.get_text()
        for skill in self.professional_skills:
            desc += skill.skill_desc

        desc.replace('\n', ' ')
        desc.replace(',', ' ')
        return jieba.cut(desc)

    def set_project_company(self):
        """
        @summary: 设置某个项目在某个公司工作期间
        """

        for i, project in enumerate(self.projects):

            for work in self.works:
                if compare_time(project.start_time, work.start_time) >= 0 and compare_time(project.end_time, work.end_time) <= 0:
                    self.projects[i].company_name = work.company_name

    def get_recent_salary(self, count=1):
        """
        @summary: 获取简历中最近一份工作的薪资
        """

        regex = re.compile("\d{1,10}")

        salary = [0, 0]
        if self.current_salary:
            # 51数据
            salary = regex.findall(self.current_salary)
            if u'以下' in self.current_salary:
                salary = int(salary[0]) * 10000 / 12
                salary = [0, salary]
            elif u'以上' in self.current_salary:
                salary = int(salary[0]) * 10000 / 12
                salary = [salary, 10000000]
            elif len(salary) == 2:
                salary = [int(i) * 10000 / 12 for i in salary]
            else:
                salary = [0, 0]
        else:
            # 智联数据
            for work in self.get_works(count=1):
                if not work.salary:
                    continue
                salary = regex.findall(work.salary)
                if len(salary) == 2:
                    salary = [int(i) for i in salary]
                    break
                elif len(salary) == 1:
                    salary = int(salary[0])
                    if u'下' in work.salary:
                        salary = [0, salary]
                    elif u'上' in work.salary:
                        salary = [salary, 1000000]

                else:
                    salary = [0, 0]
        return salary

    def get_person_level(self, re_Chinese=False):
        """
        @summary: 根据求职者过往的薪资,工作年限判断该人为初级人才,中级,高级人才.
            #人家level定义:
            # 卡片页增加按人才级别筛选功能－薪资取最近一份工作。
            # 初级（经验小于等于2年，最高薪资低于5k的人才 或未填薪资）；
            # 高级（经验大于等于5年，最低薪资高于7k的薪资 或者未填薪资）；
            # 排除初级和高级的，均为中级人才。
            # 增加另一个状态－管理级（需要有管理经验，可以不写薪资，但需要排除最高薪资小于5k的薪资）
        @author:likaiguo.happy@163.com 2013-11-1 15:30:50
        >>
        @change: @summary: 根据求职者过往的薪资,工作年限判断该人为初级人才,中级,高级人才.
            #人家level定义:
            # 卡片页增加按人才级别筛选功能－薪资取最近一份工作。
            # 初级：经验小于等于2年 且 （最高薪资小于等于6k 或 未填薪资）；
            # 高级：经验大于等于5年 且 （最低薪资大于等于7k 或 未填薪资）；
            # 排除初级和高级的，均为中级人才。
            # 增加另一个状态－管理级（需要有管理经验，可以不写薪资，但需要排除最高薪资小于5k的薪资）
            #这样应该更清楚了
        @author:  likaiguo.happy@163.com 2014-1-2 16:13:01
        """
        work_years = self.get_work_years(display_origin=True)

        try:
            salary = self.get_recent_salary()
            low, high = tuple(salary)
        except:
            low, high = 0, 0

        level = 'junior'
        has_managerial_exp = False
        if work_years <= 2 and (high <= 6000 or high == 0):
            # 初级（经验小于等于2年，最高薪资低于5k的人才 或未填薪资）；
            level = 'junior'
        elif work_years >= 5 and (low >= 7000 or high == 0):
            # 高级（经验大于等于5年，最低薪资高于7k的薪资 或者未填薪资）；
            level = 'senior'
        else:
            level = 'intermediate'

        if level != "junior":

            for work in self.get_works():
                position_title = work.position_title
                # 2. postion_title 有管理经验的加分
                for title in POSTION_TITLE_DICT.keys():
                    if position_title.find(title) != -1:
                        has_managerial_exp = True
                        break

                if has_managerial_exp:
                    break
        if re_Chinese:
            level_dict = {
                'junior': u'初级', 'senior': u'高级', 'intermediate': u'中级'}
            level = level_dict[level]

        return {"level": level, "has_managerial_exp": has_managerial_exp}

    meta = {
        'abstract': True,
    }


class ResumeData(CommonResumeData):

    is_secret = BooleanField(
        required=False,
        default=False,
    )
    owner = StringField(
        required=False,
        default='pinbot_spider'
    )
    last_contact = StringField(
        required=False,
        default='',
    )
    hr_evaluate = StringField(
        required=False,
        default='',
    )
    tags = ListField(default=[])
    # 操作管理员
    admin = StringField(
        required=False,
        default='',
    )
    # 管理员操作时间
    admin_time = DateTimeField(
        required=False,
        default=datetime.datetime.now(),
    )

    def get_tags(self):
        return [tag.get('title', '') for tag in self.tags]

    meta = {
        "collection": "resumeData",
        "index_background": True,
        "indexes": [
            "-update_time",
            "-updated_at",
            "-created_at",
            "url",
            "source",
            "source_id",
            "residence",
            "address",
            "no_repeat_words",
            "view_id",
            "url_id",
        ],
    }


class UploadResumeData(CommonResumeData):

    meta = {
        "collection": "upload_resumedata",
        "indexes": [
            "-update_time",
            "-updated_at",
            "-created_at",
            "url",
            "source_id",
            "residence",
            "address",
            "job_target.job_career",
            "job_target.job_industry",
            "job_target.expectation_area",
            "no_repeat_words",
            "keywords_list"
        ],

    }

    def to_dict(self):
        import helper
        return helper.mongo_to_dict(self, [])


class ContactInfoData2(Document):

    """
    @summary: 简历的联系人数据
    """

    resume_id = ObjectIdField(db_field='resumeID')
    name = StringField()
    source = StringField()
    source_id = StringField(db_field='sourceID')
    phone = StringField()
    email = StringField()
    qq = StringField()
    weibo = StringField()
    identity_id = StringField(db_field='identityID')

    meta = {
        "collection": "contactInfoData"
    }


def StringToTime(strtime):
    t_tuple = time.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f")
    return time.mktime(t_tuple) * 1000


SOURCE_CHOICES = (
    ('zhilian', u'智联'),
    ('51job', u'前程无忧'),
    ('liepin', u'猎聘'),
    ('admin', u'工作人员添加'),
    ('upload', u'上传'),
    ('other', u'其它')
)


CONTACT_INFO_STATUS = (
    ('public', '公开'),
    ('secret', '保密'),
    (None, '公开'),
)


class CommonContactInfo(models.Model):
    resume_id = models.CharField(
        max_length=100,
        db_column='resumeID',
        verbose_name=u'简历id',
        unique=True,
    )
    name = models.CharField(max_length=100, verbose_name=u'姓名')
    source = models.CharField(max_length=100, verbose_name=u'来源', choices=SOURCE_CHOICES, default='other')
    source_id = models.CharField(max_length=100, db_column='sourceID', verbose_name=u'其他平台id', null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'电话')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'邮箱')
    qq = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'qq号码')
    weibo = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'微博地址')
    add_time = models.DateTimeField(
        default=datetime.datetime.now(),
        null=True,
        blank=True,
        verbose_name=u'添加时间',
    )
    identity_id = models.CharField(max_length=100, db_column='identityID', verbose_name=u'身份证号码', null=True, blank=True)

    reported_num = models.IntegerField(verbose_name=u'被举报次数',
                                       null=True, blank=True, default=0)
    status = models.CharField(max_length=100, choices=CONTACT_INFO_STATUS, default='public', verbose_name='公开状态')

    def __unicode__(self):
        return u'id:%d 简历编号:%s 姓名:%s 电话:%s 邮箱:%s' % (self.id, self.resume_id, self.name, self.phone, self.email)

    def __str__(self):
        return self.__unicode__()

    def to_dict(self):
        return dict(self)

    class Meta:
        abstract = True


class ContactInfoData(CommonContactInfo):

    ORIGIN_META = (
        (1, '直接购买'),
        (2, '简历导入'),
        (3, '人工更新'),
    )

    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
    )
    origin = models.IntegerField(
        default=1,
        choices=ORIGIN_META,
        verbose_name='添加来源',
    )

    class Meta:
        db_table = 'resumes_contactinfo'
        verbose_name = u'简历联系信息'
        verbose_name_plural = u'简历联系信息'

    def show_resume_url(self):
        origin_url = "<a href=/resumes/display/%s/ target=blank>%s</a>" % (
            str(self.resume_id), str(self.resume_id))

        return mark_safe(origin_url)

    show_resume_url.short_description = '简历'


class HistoryContactInfo(models.Model):

    ORIGIN_META = (
        (1, '直接购买'),
        (2, '简历导入'),
        (3, '人工更新'),
    )
    resume_id = models.CharField(
        max_length=100,
        db_column='resumeID',
        verbose_name=u'简历id',
    )
    name = models.CharField(max_length=100, verbose_name=u'姓名')
    source = models.CharField(max_length=100, verbose_name=u'来源', choices=SOURCE_CHOICES, null=True, blank=True,)
    source_id = models.CharField(max_length=100, db_column='sourceID', verbose_name=u'其他平台id', null=True, blank=True,)
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'电话')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'邮箱')
    qq = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'qq号码')
    weibo = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'微博地址')
    add_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=u'添加时间',
    )
    identity_id = models.CharField(max_length=100, db_column='identityID', verbose_name=u'身份证号码', null=True, blank=True)

    reported_num = models.IntegerField(verbose_name=u'被举报次数',
                                       null=True, blank=True, default=0)
    status = models.CharField(max_length=100, choices=CONTACT_INFO_STATUS, default='public', verbose_name='公开状态')

    contact_info = models.ForeignKey(
        ContactInfoData,
        related_name='history_infos',
    )
    origin = models.IntegerField(
        default=1,
        blank=True,
        choices=ORIGIN_META,
        verbose_name='添加来源',
    )

    def __unicode__(self):
        return 'id:%d 简历编号:%s 姓名:%s 电话:%s 邮箱:%s' % (self.id, self.resume_id, self.name, self.phone, self.email)

    class Meta:
        verbose_name = u'联系信息历史'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    # 1表示管理人员添加（一句话简评） 2表示客户添加
    type = models.IntegerField(
        default=2,
        verbose_name=u'价格',
    )
    user = models.ForeignKey(
        User,
        verbose_name=u'用户',
    )
    comment_obj_id = models.CharField(
        max_length=100,
        verbose_name=u'评论ID',
    )
    resume_id = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=u'简历ID'
    )
    content = models.CharField(
        max_length=100,
        verbose_name=u'评论内容'
    )
    comment_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'评论时间',
    )

    def show_resume(self):
        url = "<a href='/resumes/display/%s' target=%s>%s</a>" % (self.resume_id, self.resume_id, '查看简历')
        return mark_safe(url)

    show_resume.short_description = '查看简历'

    def to_dict(self):
        return {
            'id': str(self.id),
            'text': self.content,
            'date': str(self.comment_time)
        }

    def __str__(self):
        return self.content

    def __unicode__(self):
        return self.__str__()

    class Meta:
        db_table = 'resumes_comment'
        verbose_name = u'评论'
        verbose_name_plural = verbose_name


class Tag(models.Model):

    """
    标签实体，包括了标签的详细信息，如内容，创建者，创建时间，以及是否可以被修改
    """
    resume_id = models.CharField(max_length=100, null=True, blank=True)
    tag_obj_id = models.CharField(max_length=100, null=True, blank=True)
    feed_id = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    # tag 类型 1表示给简历添加的tag，2表示用户提交的搜索tag
    type = models.IntegerField(
        default=1, verbose_name=u'价格', null=True, blank=True)
    scope = models.CharField(max_length=100, default='resume',
                             verbose_name=u'用户', null=True, blank=True)  # 标签所属类别，用于标签分类
    add_time = models.DateTimeField()
    tag_content = models.CharField(
        max_length=100, verbose_name=u'标签内容', null=True, blank=True)  # 标签内容
    # 标签的状态：deleted,new,modified
    status = models.CharField(
        max_length=100, default='new', verbose_name=u'标签状态', null=True, blank=True)


class ResumeTag(models.Model):
    resume_id = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag)
    tag_content = models.CharField(max_length=100, verbose_name=u'标签内容')
    add_time = models.DateTimeField()
    # 标签的状态：deleted,new,modified
    status = models.CharField(
        max_length=100, default='new', verbose_name=u'标签内容')
    user = models.ForeignKey(User, null=True, blank=True)


class UserResume(Document):

    """
    @summary: 记录用户的简历访问信息
    """
    username = StringField(default='')
    resume_id = StringField(default='')
    resume = ReferenceField(ResumeData, reverse_delete_rule=DO_NOTHING)

    add_time = DateTimeField()

    visit_time_list = ListField(default=[], db_field='visit_time_list')

    # 0 default, 1 watch ,2 discard ,用户对改简历的操作状态.默认,关注,舍弃.
    type = IntField(default=0)

    # 0 don't have privilege of reading contact,1 have, 3 upload_file
    has_contact = IntField(default=0)
    keywords = StringField(default='')
    feed_keywords = StringField(default='')
    score = FloatField(default=0.0)

    analysis_id = StringField(default='')
    meta = {"collection": "user_resume",
            'indexes': [
                '-add_time',
                'username',
                'resume_id',
                'keywords'

            ]}

    def get_resume_search_keywords(self, freq_base=1):

        return freq_base

    def get_visit_count(self):

        return len(self.visit_time_list)


class UserWatchResume(models.Model):
    user = models.ForeignKey(User)
    resume_id = models.CharField(max_length=100, verbose_name=u'简历id')
    feed_id = models.CharField(
        max_length=100, verbose_name=u'订阅id', null=True, blank=True)
    add_time = models.DateTimeField()

    # 0 default, 1 watch ,2 discard ,用户对改简历的操作状态.默认,关注,舍弃.
    type = models.IntegerField(default=0)
    # 0 don't have privilege of reading contact,1 have, 3 upload_file
    has_contact = models.IntegerField(default=0)
    keywords = models.CharField(max_length=100, default='')
    feed_keywords = models.CharField(max_length=100, default='')
    analysis_id = models.CharField(max_length=100, default='')


class ResumeScore(Document):

    """
    @summary: 简历评分结果记录

    """
    username = StringField(default='pinbot')
    keywords = StringField()
    score = FloatField()

    resume_id = StringField(default='', required=True)
    resume = ReferenceField(ResumeData, reverse_delete_rule=DO_NOTHING)
    url = StringField()

    calc_time = DateTimeField()

    brief_comment = StringField(default='')
    star = StringField(default='2.5')

    job_related = IntField(default=-1)  # 是否跟输入关键词职位相关.

    # TODO:关键词进行一次计算后不再计算

    extract_keywords = ListField(default=[])

    meta = {"collection": "resume_score",
            "indexes": [
                'resume_id',
                'url',
                'keywords',
                '-calc_time'
            ]

            }

    def get_star(self, css_cls=False):

        self.star = score2star(self.score, css_cls)
        return self.star


class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        from datetime import date, datetime
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
