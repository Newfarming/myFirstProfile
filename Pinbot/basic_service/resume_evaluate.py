# coding:utf-8
'''
Created on Sep 26, 2013

@author: likaiguo
'''
import logging

from django.conf import settings

from variables.score_variables import *
from jieba import cut, cut_for_search

from resumes.models import *

from Pinbot.settings import PROJECT_ROOT
import Config
import Input

import re
import math
import datetime

from basic import get_month, compare_time

config = Config.Config(PROJECT_ROOT + '/config/properties.prop')
famousCompany_file_path = PROJECT_ROOT + \
    config.get_prop_value('main', 'famousCompany_file_path')
school_file_path = PROJECT_ROOT + \
    config.get_prop_value('main', 'school_file_path')

famous_company_dict = config.read_company(famousCompany_file_path)
school_dict = config.read_school(school_file_path)

resume_score_log = logging.getLogger('resume_score_log')
input_process = Input.input_data()

from variables.score_variables import *


class ResumeEvaluate(object):

    '''
    classdocs
    @summary:  需要的模块：自我评价，工作经历，项目经历，教育经历，专业技能
    '''

    def __init__(self, keywords=''):
        '''
        Constructor
        '''
        self.keywords = keywords
        keywords_dict, jobs_dict = input_process.get_extend_words_dict(
            keywords)
        self.extend_keywords_dict = keywords_dict
        self.search_keywords_list = [
            keyword for keyword, weight in keywords_dict.items() if weight > 1]
        self.jobs_dict = jobs_dict

    def reset(self):

        self.job_related = 0  # 是输入关键词扩展出的相关职位,则job_related 应该 >1
        self.project_arr = []
        self.has_famous_company_bg = False
        self.is_job_hopper = False
        self.has_managerial_exp = False
        self.recent_work_not_stable = False
        self.school_reputation = ''
        self.match_search_word_count = 0

    def composite_score(self, resume):
        """
        @summary:  make a score of a resume

        """
        self.reset()

        score = 0.0
        resume_score_log.info(
            "\nresume_score_start:" + str(resume.id) + ":" + resume.url)
        self.keywords_score = self.score_self_evaluation(resume)
        self.work_experience_score = self.score_work_experience(resume)
        self.project_experience_socre = self.score_project_experience(resume)
        self.professional_skill_socre = self.score_professional_skill(resume)
        self.education_experience_score = self.score_education_experience(
            resume)

        score += self.keywords_score
        score += self.work_experience_score
        score += self.project_experience_socre
        score += self.professional_skill_socre
        score += self.education_experience_score

        self.score = score

        resume.score = score

        resume_score_log.info(
            'has_famous_company_bg:' + str(self.has_famous_company_bg))
        resume_score_log.info('is_job_hopper:' + str(self.is_job_hopper))
        resume_score_log.info(
            'has_managerial_exp:' + str(self.has_managerial_exp))
        resume_score_log.info(
            'recent_work_not_stable:' + str(self.recent_work_not_stable))
        resume_score_log.info(
            'match_search_word_count:' + str(self.match_search_word_count))
        resume_score_log.info(
            'school reputation:' + unicode(self.school_reputation))
        resume_score_log.info('score:' + str(score) + '\n')
        return score

    def display_score_related(self):
        pass
#         print 'keywords_score' , self.keywords_score
#         print 'work_experience_score', self.work_experience_score
#         print 'project_experience_socre', self.project_experience_socre
#         print 'professional_skill_socre', self.professional_skill_socre
#         print 'education_experience_score', self.education_experience_score
#         print 'composite score', self.score

    def score_resumes(self, resume_list):
        """
        @summary:  make scores of a series of resumes

        """

    def calc_keywords_score(self, text):
        """
        @summary:  增加复用,减少代码copy.  查看描述内容中,关键词出现数量,和是否担任重要职务

        """

        text = text.replace('\n', '').replace('\r\n', ' ')
        # 全文分词
        seg_list = cut_for_search(text)

        temp_dict = {}
        resume_score_log.info(text)
        # 统计得分词的次数
        for word in seg_list:
            word = word.lower().strip()
            if not word:
                continue
            word_weight = self.extend_keywords_dict.get(word, 0)
            if word_weight:
                word_count = temp_dict.get(word, 0)
                temp_dict[word] = word_count + 1

        keywords_score = float(0)

        # 对每个词进行打分,大于4时对 次数取 2底的指数
        for word, count in temp_dict.items():
            word_weight = self.extend_keywords_dict.get(word, 0)
            if count > 4:
                count = math.log(count, 2.0) + 2

            word_score = word_weight * count
            keywords_score += word_score
#             resume_score_log.info("keywords_score:%s  ext_keyword: %s weight:%s     word_count:%s = word_score %s"\
#                                 % (str(keywords_score), word, str(word_weight)), str(count) , str(word_score))
            msg = "%s <=(%s) %s =%s * %s" % (str(keywords_score),
                                             word, str(word_score), str(word_weight), str(count))
            resume_score_log.info(msg)
        # 限定关键词的最高得分为50 超过这个分数则统一规约为50+**
        keywords_score = 50 + (keywords_score - 50) / \
            10 if keywords_score > 50 else keywords_score
        # 将正则表达式编译成Pattern对象
        other_score = 0
        for pattern, weight in RESPONSIBILITY_REGEX_LIST:
            match = pattern.match(text)
            if match:
                other_score += weight
        resume_score_log.info('keywords_score:%s  importance_score:%s' % (
            str(keywords_score), str(other_score)))

        keywords_score += other_score
        resume_score_log.info('desc score:%s' % (str(keywords_score)))

        return keywords_score

    def score_self_evaluation(self, resume):
        # 对自我评价打分
        resume_score_log.info('......score_self_evaluation........')
        keywords_score = float(0)
        if resume.self_evaluation:
            keywords_score = self.calc_keywords_score(resume.self_evaluation)
        return keywords_score

    def score_work_experience(self, resume):
        # 对工作经验打分
        self.job_related = 0

        resume_score_log.info('......score_work_experience........')
        work_experience_score = 0
        for i, work in enumerate(resume.works):
            score = self.score_work(work, resume)
            work_experience_score += score
            resume_score_log.info(
                'the %d th  work totally %f' % (i, work_experience_score))

        if len(resume.works):
            self.job_related = self.job_related / len(resume.works)

        resume_score_log.info(
            'workhsitory_socre is  ' + str(work_experience_score) + '')

        return work_experience_score

    def score_work(self, work, resume):

        resume_score_log.info('......score_work........')
        score = 0
        # 职位得分
        position_title = work.position_title.strip().lower()
        job_title_score = 0
        for job, weight in self.jobs_dict.items():

            if position_title == job:
                job_title_score += weight

            elif position_title.find(job) != -1:
                job_title_score += weight - 2

            resume_score_log.info("position_title %s ,job: %s weight:%d=score:%s" % (
                position_title, job, weight, str(job_title_score)))

        # 职位词中存在用户搜索词
        for search_keyword in self.search_keywords_list:
            if search_keyword in position_title:
                job_title_score += 6

        self.job_related += job_title_score

        if job_title_score:
            # 相关职位
            score += job_title_score
            resume_score_log.info(
                "position_title job %s ,%s" % (position_title, str(score)))
        else:
            # 非相关职位
            job_title_score = 1

        company_name = work.company_name.strip()
        industry_category = work.industry_category.strip()
        work_content = work.job_desc + position_title
        # 0.查找是否有属于该工作区间段的项目经验

        project_content = ''
        for poject_num, project in enumerate(resume.projects):
            if compare_time(project.start_time, work.start_time) >= 0 and compare_time(project.end_time, work.end_time) <= 0:
                self.project_arr.append(poject_num)
                project_content += project.get_proj_all_text()

        work_content += project_content
        # 1.industry_category
        if industry_category in INDUSTRY_CATAGORY_LIST:
            resume_score_log.info(
                "work is related industry work,%s" % industry_category)
            # 名企经历加分
            company_name_list = cut(company_name)
            for name in company_name_list:
                name = name.lower()
                if name in famous_company_dict:
                    resume_score_log.info(
                        company_name + ',company type: famous_internet, game' + company_name + ', score: 12')
                    score += 12
                    self.has_famous_company_bg = True
                    break
            # 最为相关的行业加分
            if SPECIAL_INDUSTRY_DICT.get(industry_category):
                score += SPECIAL_INDUSTRY_DICT[industry_category]
                resume_score_log.info('%s , company type: internet, score: %d ' % (
                    company_name, SPECIAL_INDUSTRY_DICT[industry_category]))
            else:
                score = score + 1
                resume_score_log.info(
                    company_name + ' , company type: other, score: 1')

            # 2. postion_title 有管理经验的加分
            for title, weight in POSTION_TITLE_DICT.iteritems():
                if position_title.find(title) != -1:
                    self.has_managerial_exp = True
                    score = weight
                    title_str = '%s contains:%s ,%d ' % (
                        position_title, title, weight)
                    resume_score_log.info(title_str)
                    break

            # 3. keywords ,计算内容中关键词得分

            keywords_score = self.calc_keywords_score(work_content)
            tmp = job_title_score * 10

            if keywords_score > tmp:

                keywords_score = tmp + (keywords_score - tmp) / 10
                msg = 'keywords_score > job_title_score * 10=%s 规约:keyword_score:%s' % (
                    str(keywords_score), str(tmp))
                resume_score_log.info(msg)

#                 score += keywords_score * math.log(total_month, 6)
# 不是太相关的工作经验的分数随着工作年限的增速慢一些
#                 resume_score_log.info('this  work %d  months  score: %f' % (total_month, score))
            else:
                msg = 'keywords_score:%s' % (str(keywords_score))
                resume_score_log.info(msg)

            score += keywords_score
            total_month = get_month(work.start_time, work.end_time)
            if job_title_score > 4:
                # 相关的工作才根据年限进行增加分数

                if total_month < 6:
                    score = score * 0.4
                elif total_month < 12:
                    score = score * 0.8
                elif total_month < 24:
                    score = score * 1.3
                elif total_month < 36:
                    score = score * 1.8
                else:
                    score = score * 2.2
                resume_score_log.info('job_title_score > 4')
            elif job_title_score >= 2:
                # 不是特别相关的工作,加分降低
                if total_month < 6:
                    score = score * 0.3
                elif total_month < 12:
                    score = score * 0.6
                elif total_month < 24:
                    score = score * 1
                elif total_month < 36:
                    score = score * 1.5
                else:
                    score = score * 1.8
                resume_score_log.info('job_title_score > 2  && < 4')
            else:
                # 不是很相关的工作,基本上不加分
                if total_month < 6:
                    score = score * 0.2
                elif total_month < 12:
                    score = score * 0.4
                elif total_month < 24:
                    score = score * 0.6
                resume_score_log.info('job_title_score < 2')

            resume_score_log.info(
                'this  work %d  months  score: %f' % (total_month, score))

        return score

    # 对项目经历进行评分
    def score_project_experience(self, resume):

        resume_score_log.info('......score_project_experience......')
        project_score = float(0)
        projectList = resume.projects
        project_content = ''

        for i, project in enumerate(projectList):
            score = 0
            if i in self.project_arr:
                resume_score_log.info(
                    'the ' + str(i) + 'th project is has been socred in work')
                i = i + 1
                continue
            project_content = project.get_proj_content()

            # keywords
            score += self.calc_keywords_score(project_content)
#             total_month = 0
#             total_month = get_month(project.start_time, project.end_time)
#             if total_month != 0:
#                 log_value = math.log(total_month, 2.0)
#                 score = score * log_value

            project_score = project_score + score

            resume_score_log.info(
                'the %sth project score: %s = %s' % (str(i), str(score), str(project_score)))
            i = i + 1

        return project_score

    # 对专业技能进行评分
    def score_professional_skill(self, resume):

        resume_score_log.info('......score_professional_skill......')
        professinal_skill_score = float(0)
        for skill in resume.professional_skills:
            skill_desc = skill.skill_desc
            proficiency = skill.proficiency
            score = self.calc_keywords_score(skill_desc)
            proficiency_value = PROFICIENCY_DICT.get(proficiency, 0)

            professinal_skill_score += score * proficiency_value
            resume_score_log.info("%f = up + %s * %s = %s * %s" % (professinal_skill_score,
                                                                   score, proficiency_value, skill_desc, proficiency))
        # 如果填入技能词过于不靠谱则过滤掉
        if professinal_skill_score > self.project_experience_socre:
            professinal_skill_score = self.project_experience_socre
        if professinal_skill_score > self.work_experience_score:
            professinal_skill_score = self.work_experience_score

        resume_score_log.info(
            '......score_professional_skill......' + str(professinal_skill_score))
        return professinal_skill_score

    def score_education_experience(self, resume):
        # 对学习经历打分
        resume_score_log.info('......score_education_experience......')
        education_score = 0

        for education in resume.educations:
            endtime = education.end_time
            school = education.school.strip()
            education_degree = education.degree.strip()
            school_type = school_dict.get(school)
            for degree, weight in DEGREE_TUPLE_LIST:
                if education_degree.find(degree) != -1 and education_degree != u'大专':
                    if school_type == '985':
                        education_score = education_score + 5
                        if self.school_reputation != '211':
                            self.school_reputation = school_type + u'院校'
                        else:
                            self.school_reputation = '985,211院校'
                    elif school_type == '211':
                        education_score = education_score + 3
                        if self.school_reputation != '985':
                            self.school_reputation = school_type + u'院校'
                        else:
                            self.school_reputation = '985,211院校'
                    elif school_type:
                        education_score = education_score + 2
                        self.school_reputation = school_type

                    if endtime != u'至今':
                        if education_score < weight:
                            education_score += weight + 2
                    else:
                        if education_score < weight:
                            education_score += weight
                    resume_score_log.info(
                        'education_score, ' + unicode(school) + unicode(degree) + unicode(education_score))
                    break

        resume_score_log.info(
            'education_score_total, ' + unicode(education_score))

        return education_score

    def produce_brief_comment(self):
        """
            @summary:  produce a resume brief comment from a resume object.
            @author:  likaiguo.happy@gmail.com 2103-09-26 10:46
        """

        brief_comment_list = []

        if self.has_famous_company_bg:
            brief_comment_list.append(u'名企经历')
        if self.match_search_word_count >= 4:
            brief_comment_list.append(u'与搜索词较匹配')

        if self.has_managerial_exp:
            brief_comment_list.append(u'管理经验')

        if self.is_job_hopper:
            brief_comment_list.append(u'跳槽频繁')

        if self.recent_work_not_stable:
            brief_comment_list.append(u'近期不稳定')

        if self.school_reputation:
            brief_comment_list.append(self.school_reputation)

        brief_comment = ','.join(brief_comment_list)
        resume_score_log.info('brief_comment: ' + brief_comment)

        return brief_comment

    def get_job_related(self):

        return self.job_related

if __name__ == '__main__':
    from mongoengine import connect
    connect('recruiting', host='192.168.1.190', port=27017)
    from bson import ObjectId
    resumes = ResumeData.objects.filter(
        id=ObjectId("524002951d41c836677f36ae")).limit(30)

    resume = resumes[0]

    temp = resume.get_person_level()
    # 其他用户-还没有评过分
    res_evaluate = ResumeEvaluate(keywords='游戏 cocos2d')

    # 如果以前没有计算记录过 职位title得分情况.
    res_evaluate.reset()
    res_evaluate.score_work_experience(resume)
    res_evaluate.get_job_related()

    pass
