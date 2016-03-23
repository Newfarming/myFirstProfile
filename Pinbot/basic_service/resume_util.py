# coding:utf-8
"""
@summary:  some common util tools function

@author:  likaiguo 2013-09-10 created

"""
import datetime
import json
import re
import urlparse

from bson import ObjectId
import jieba

from judge_unicode import is_chinese, is_other
from pin_utils.django_utils import (
    get_int,
)
from resume_evaluate import ResumeEvaluate
from resumes.models import *
from time_precess import time_delt_str
from variables.resume_global_variables import *
from variables.score_variables import STAR_LIST


def produce_return_json(data='', status=True, error_dict=None):
    """
    @summary:  produce return json data packet.
    """

    data_dict = {}

    data_dict['data'] = data
    data_dict['status'] = True if status else False
    if error_dict:
        data_dict['error'] = error_dict

    return json.dumps(data_dict)


def get_text_words(text):
    """
    @summary:  from text to get english words.

    """
    s = re.findall("\w+", text)

    l = sorted(list(set(s)))
    words = []

    for i in l:
        m = re.match("\d+", i)
        n = re.search("\W+", i)
        if not m and not n and len(i) > 1:
            words.append((s.count(i), i))
    words = sorted(words)

    words = [w for c, w in words]

    return words


def get_url_id(url):
    """
    @summary: from url get the unique id of resume.
        url_list = [
                'http://h.lietou.com/resume/showresumedetail/?res_id=17600485',
                'http://rd.zhaopin.com/resumepreview/resume/viewone/2/JR347093729R90250001000_1_1',
                'http://rd.zhaopin.com/resumepreview/resume/viewone/1/3180340954',
                'http://ehire.51job.com/Candidate/ResumeView.aspx?hidUserID=26087386&hidEvents=23&hidKey=f4f6f9f96416fbaa4138048ce9c4ef26',
                'http://ehire.51job.com/Candidate/ResumeViewFolder.aspx?hidSeqID=157796051&hidFolder=BAK',
                'http://www.headin.cn/Jobs/Talent/ShowResume/2690416',
                'http://pinbot.me/resumes/display/52acb977d8b9f725619a8272/?feed_keywords='
                ]

    """
    if '51job' in url:
        url = url.lower()
    url_id_dict = {'source': '', 'id': '', 'url_q': '', 'id_type': 'source_id'}
    result = urlparse.urlparse(url)
    params = urlparse.parse_qs(result.query, True)
    netloc = result.netloc
    try:
        if 'zhaopin.com' in netloc:
            zhaopin_id = result.path.split('/')[-1].split('_')[0]
            url_id_dict['source'] = 'zhilian'
            url_id_dict['id'] = zhaopin_id
            if '/viewone/2/' in url:
                url_id_dict['url_q'] = '/viewone/2/' + zhaopin_id
            elif '/viewone/1/' in url:
                url_id_dict['url_q'] = '/viewone/1/' + zhaopin_id
                url_id_dict['id_type'] = 'view_id'

        elif 'lietou' in netloc or 'liepin' in netloc:
            url_id_dict['source'] = 'liepin'
            url_id_dict['id'] = params.get('res_id_encode', [0])[0]
            url_id_dict['url_q'] = 'res_id_encode=' + url_id_dict['id']
            url_id_dict['id_type'] = 'url_id'
        elif '51job' in netloc:
            url_id_dict['source'] = '51job'
            url_id_dict['id'] = params.get('hiduserid', [0])[0]

            if not url_id_dict['id']:
                url_id_dict['id'] = params.get('hidseqid', [0])[0]
                url_id_dict['url_q'] = 'hidseqid=' + url_id_dict['id']
                url_id_dict['id_type'] = 'view_id'
            else:
                url_id_dict['url_q'] = 'hiduserid=' + url_id_dict['id']
        elif 'head' in netloc:
            url_id_dict['source'] = 'headin'
            url_id_dict['id'] = result.path.split('/')[-1]
            url_id_dict['url_q'] = 'Talent/ShowResume/' + url_id_dict['id']
        elif 'pinbot.me' in netloc:
            url_id_dict['id_type'] = 'id'
            url_id_dict['id'] = ObjectId(result.path.split('/')[3])
    except Exception, e:
        pass
    return url_id_dict


def get_resume_from_url(url):
    """
    @summary: 通过url查询对应的resume对象，查询不到则返回None
    @author:  2013-12-25 16:07:10 likaiguo.happy@163.com
    """
    url_id_dict = get_url_id(url)
    resume = None
    from resumes.models import ResumeData

    try:
        resumes = []
        if url.find('lietou') >= 0 or url.find('liepin') >= 0:
            resumes = ResumeData.objects.filter(
                url_id=url_id_dict['id'], source__contains=url_id_dict['source'])
        elif url_id_dict['id_type'] == 'source_id':
            resumes = ResumeData.objects.filter(
                source_id=url_id_dict['id'], source__contains=url_id_dict['source'])
        elif url_id_dict['id_type'] == 'view_id':
            resumes = ResumeData.objects.filter(
                view_id=url_id_dict['id'], source__contains=url_id_dict['source'])
        elif url_id_dict['id_type'] == 'url_id':
            resumes = ResumeData.objects.filter(
                url_id=url_id_dict['id'], source__contains=url_id_dict['source'])
        elif url_id_dict['id_type'] == 'id':
            resumes = ResumeData.objects.filter(id=url_id_dict['id'])
        if len(resumes):
            resume = resumes.order_by('-update_time')[0]
    except Exception, e:
        pass

    return resume


def get_resumes_watch(user, page=1, page_count=10, page_type='all'):
    """
    @summary:
    """
    from resumes.models import UserWatchResume, Comment
    from resumes.models import ResumeData, ResumeScore

    if page_type == 'all':
        user_resumes = UserWatchResume.objects.filter(user=user
                                                      ).order_by('-add_time')
    else:
        user_resumes = UserWatchResume.objects.filter(user=user,
                                             type=page_type).order_by('-add_time')

    start = (page - 1) * page_count
    records_count = user_resumes.count()
    if start < 0 or start > records_count:
        start = 0
    end = start + page_count
    if end > records_count:
        user_resumes = user_resumes[start:records_count]
    else:
        user_resumes = user_resumes[start:end]
    page_all_count = records_count / page_count + 2
    page_list = range(1, page_all_count)
    user_resume_id_list = []
    resume_list = []

    user_resume_contact_dict = {}
    for user_resume in user_resumes:
        resume_id, keywords = user_resume.resume_id, user_resume.keywords + \
            " " + user_resume.feed_keywords
        temp = resume_id, keywords
        if user_resume.has_contact:
            # 该用户是否有这份简历的联系信息
            data = {resume_id: user_resume.has_contact}
            user_resume_contact_dict.update(data)

        if temp not in user_resume_id_list:
            user_resume_id_list.append(temp)
            try:
                resume = ResumeData.objects.get(id=ObjectId(str(resume_id)))
                resume.job_target.set_expectation_area_list()
                resume.job_target.job_hunting_state = resume.job_target.job_hunting_brief()
                resume.get_work_years()
            except:
                continue

            has_contact = user_resume_contact_dict.get(resume_id, 0)
            resume.has_contact = has_contact
            resume.watch_time = user_resume.add_time

            extra_info = {}
            extra_info['keywords'] = keywords
            comments = Comment.objects.filter(
                user=user, resume_id=resume_id).order_by('-comment_time')
            if comments:
                extra_info['comment'] = comments[0].content
            # 待完成
            brief_comment = ''
            extra_info['brief_comment'] = brief_comment
            extra_info[
                'feed_id'] = user_resume.feed_id if user_resume.feed_id and user_resume.feed_id != '' else ''

            resume_list.append((resume, extra_info))

    return resume_list, page_list


def get_resumes(username, page=1, page_count=10, page_type='all'):

    from resumes.models import UserResume, ResumeData, ResumeScore
    start = (page - 1) * page_count
    if page_type == 'all':
        user_resumes = UserResume.objects.filter(username=username
                                                 )
    else:
        user_resumes = UserResume.objects.filter(username=username,
                                             type=page_type)

    records_count = user_resumes.count()
    user_resumes = user_resumes.skip(start).limit(
        page_count).order_by('-add_time')
    page_all_count = records_count / page_count + 2
    page_list = range(1, page_all_count)
    user_resume_id_list = []
    resume_list = []

    user_resume_contact_dict = {}
    for user_resume in user_resumes:
        resume_id, search_keywords = user_resume.resume_id, user_resume.keywords + \
            " " + user_resume.feed_keywords
        temp = resume_id, search_keywords
        if user_resume.has_contact:
            # 该用户是否有这份简历的联系信息
            data = {resume_id: user_resume.has_contact}
            user_resume_contact_dict.update(data)
        if temp not in user_resume_id_list:
            user_resume_id_list.append(temp)
            try:
                resume = ResumeData.objects.get(id=ObjectId(resume_id))
                resume.job_target.set_expectation_area_list()
                resume.job_target.job_hunting_state = resume.job_target.job_hunting_brief()
                resume.get_work_years()
            except:
                continue

            has_contact = user_resume_contact_dict.get(resume_id, 0)
            resume.has_contact = has_contact
            resume.watch_time = user_resume.add_time

            resume_score = ResumeScore()
            resume_list.append((resume, resume_score))

    return resume_list, page_list


def score2star(score, css_cls=False):
    """
    @summary:  将100以内分数转换为五星级,当分数大于100时按照100取值
    @author: likaiguo.happy@163.com ,2013-10-23 10:38:48
    """

    # 由计算分数映射到星级

    if score <= 10:
        star = 0.5
        tmp = 0
    else:
        tmp = int(round(score / 10))
        if tmp > 9:
            tmp = 9
        star = STAR_LIST[tmp]
    if css_cls:
        if tmp == 0:
            star = "star-half"
        else:
            tmp = tmp + 1
            if tmp % 2 == 0:

                star = "star-%d" % (int(tmp / 2))
            else:
                star = "star-%d star-half" % (int(tmp / 2))
    return star


def produce_resume_data(resume, resume_score, user_resume):
    """
    @summary: 生成一个简历的tab数据,格式为json
    @author:likaiguo.happy@163.com 2013-10-16 13:54:15


    """
    data = {
        "id": "",  # 简历id
        "watch_status": 0,  # 0 默认状态, 1,已关注 , 2,已删除
#         "status":  1 ,  # ,未分析 0 ,已经分析过 1,已分析 并删除 2
        "summary": {
            "star": "",
            "keywords": [],
        },
        "profile": {

            "name": "pinboter",
            "age": "famale",
            "gender": "male",  # 性别
            "degree": "",  # 最高学历
            "job_hunting_state": "",  # 求职状态
            "location": "",  # 现居地
            "expectation_area": "",  # 期望工作地
            "brief_comment": "",  # 一句话简评
            "work_years": "",  # 工作年限
            "homepage": [],
        },
        "educations": [
            {"start_time": "", "end_time": "",
                "school": "", "degree": "", "major": ""},
        ],
        "works": [
            {
                "start_time": "",
                "end_time": "",
                "duration": "",  # 持续时间
                "department": "",  # 部门
                "position_title": "",  # 职位名称
                "salary": "",  # 该份工作薪资
                "job_desc": "",  # 工作描述抽取主干


                "company_name": "",  # 公司名称
                "company_category": "",  # 公司性质
                "company_scale": "",  # 公司规模
                "industry_category": "",  # 行业性质
                "date": "",
            }

        ],

        "projects": [  # 最近的项目经历
            {
                "start_time": "",
                "end_time": "",

                "project_name": "",
                "project_desc": ""
            }
        ]
    }

    if user_resume:
        data['watch_status'] = user_resume.type

    if not resume:
        json_data = produce_return_json(data_dict=data)
        return json_data

    # 简历id
    data['id'] = str(resume.id)

    # 如果职位评分 大于 0 则不过滤掉改简历
    if resume_score.job_related > 0.5:
        data['filtered'] = False
    else:
        data['filtered'] = True

    # 人员简单评级
    data.update(resume.get_person_level())

    # 一句话简评

    # 提取简历描述关键词
    # 来源: 1.用户搜索词 大于3次时 放在最前边  2.由简历的内容提取 topK的关键词,并且过滤

    if resume_score.extract_keywords:
        keywords = resume_score.extract_keywords
    else:
        keywords = resume.extract_keywords()
        resume_score.extract_keywords = keywords
        resume_score.save()

    star = resume_score.get_star()

    data["summary"] = {
        "star": star,
        "keywords": keywords,
    }

    if resume.job_target:
        job_hunting_state = resume.job_target.job_hunting_brief()
        expectation_area = resume.job_target.expectation_area
    else:
        job_hunting_state = ''
        expectation_area = ''

    data["profile"] = {
        "name": resume['name'],
        "age": resume['age'],
        "gender": resume.get_gender(),  # 性别
        "degree": resume.highest_degree(),  # 最高学历
        "job_hunting_state": job_hunting_state,  # 求职状态
        "location": resume.address,  # 现居地
        "expectation_area": expectation_area,  # 期望工作地
        "brief_comment": resume_score.brief_comment,  # 一句话简评
        "work_years": resume.get_work_years(),  # 工作年限
        "homepage": resume.urls,
        'avatar_url': resume['avatar_url'],
    }

    data['works'] = resume.get_works_dict(work_count=1)
    data['projects'] = resume.get_projects_dict(project_count=1)
    data['educations'] = resume.get_educations_dict(education_count=1)
    update_time = resume.get_update_time()
    outdated = update_time < time_delt_str()
    data['update_status'] = {"date": update_time, 'outdated': outdated}

    return data


def resume_search_keywords(resume_id, user_search_keywords='',
                           word_freq=1, user_search_count=20):
    """
    # 统计最近大家检索的高频关键词
    @param word_freq: 关键词出现的最小次数
    @param user_search_count: 用户最近检索resume_id的简历的 份数.

    @return: 按出现频次从大到小排序返回 简历搜索关键词列表

    """
    from resumes.models import UserResume
    search_keywords_str = ""
    search_keywords_str += ""

    user_resumes = UserResume.objects.filter(resume_id=resume_id,
                keywords__ne='').limit(user_search_count).order_by('-calc_time')
    for user_resume in user_resumes:
        search_keywords_str += user_resume.keywords + " "
    search_words_dict = {}
    search_word = jieba.cut(search_keywords_str)
    search_word = list(search_word)
    for keyword in search_word:
        keyword = keyword.strip().lower()
        search_words_dict[keyword] = search_words_dict.get(keyword, 0) + 1

    search_words_list = sorted(search_words_dict.items(
    ), key=lambda search_words_dict: search_words_dict[1], reverse=True)
    # 限定,大于等于2次的搜索词才能被展示
    search_words_list = [
        word for word, freq in search_words_list if freq >= word_freq]

    first_keywords = jieba.cut(user_search_keywords)
    first_keywords = [keyword for keyword in first_keywords if keyword]

    keywords = []
    for keyword in first_keywords:
        if keyword in search_words_list:
            search_words_list.remove(keyword)

    keywords.extend(first_keywords)
    keywords.extend(search_words_list)

    final_keywords = []
    for keyword in keywords:
        if not is_other(keyword):
            final_keywords.append(keyword)
    return final_keywords


def produce_resume_keywords(resume_id, user_search_keywords,
                            resume_extract_keywords=[], max_len=11):
    """
    @summary:  拼接用户搜索关键词和简历提取关键词,得到简历最后的关键词.
    @resume_id:简历id
    @user_search_keywords : 用户搜索关键词: 按照该用户搜索词-其他用户搜索词排序.
    @resume_extract_keywords: 简历中提取的关键词.

    """
    from variables.resume_global_variables import KEYWORDS_SET

    resume_keywords = []

    # 用户搜索关键词,放在头部
    search_words = resume_search_keywords(resume_id, user_search_keywords)
    resume_keywords.extend(search_words)
    # 简历中提取的词出现在人工提取的词表中
    for keyword in resume_extract_keywords:
        keyword_lower = keyword.lower()
        # 这个词不在人工词表中则删除
        if keyword_lower in KEYWORDS_SET:
            resume_keywords.append(keyword)
    for keyword in search_words:
        if keyword in resume_extract_keywords:
            resume_extract_keywords.remove(keyword)
    resume_keywords.extend(resume_extract_keywords)
#    过滤重复词
    token = '-XXXXXX-'
    keywords_len = len(resume_keywords)
    for i, keyword in enumerate(resume_keywords):
        keyword_lower = keyword.lower()
        base_j = i + 1
        if base_j >= keywords_len:
            continue
        tail_resume_keywords = resume_keywords[base_j:]
        for j, tmp in enumerate(tail_resume_keywords):
            tmp_lower = tmp.lower()
            # 后续有重复的词
            if keyword_lower == tmp_lower:
                resume_keywords[base_j + j] = token

            # 如果是中文词符则合并
            elif is_chinese(keyword):
                if len(keyword) == 1:
                    resume_keywords[i] = token
                elif keyword_lower in tmp_lower:
                    resume_keywords[i] = tmp_lower
                    resume_keywords[base_j + j] = token
                elif tmp_lower in keyword_lower:
                    resume_keywords[i] = keyword_lower
                    resume_keywords[base_j + j] = token

    # TODO:2013-10-31 17:43:20 用filter来简化.
    tmp_keywords = []
    for keyword in resume_keywords:
        if token != keyword:
            tmp_keywords.append(keyword)
    if len(tmp_keywords) > max_len:
        resume_keywords = tmp_keywords[0:max_len]
    else:
        resume_keywords = tmp_keywords

    return resume_keywords


def temp_func(resume, username, search_keywords, res_evaluate=None, is_refresh=False):
    """
    @summary:
    @author: likaiguo.happy@163.com 2013-10-23 11:38:50
    """
    from resumes.models import ResumeScore, ResumeData, UserResume

    resume_id = str(resume.id)
#     resume = resume.to_mongo()
    # 最近 一次 改简历 使用该关键词的评分
    resume_scores = ResumeScore.objects.filter(
        resume_id=resume_id, keywords=search_keywords).order_by('-calc_time')
    resume_score = None
    if resume_scores:
        # 其他用户 -已经评过分 -- 直接生成 json数据
        resume_score = resume_scores[0]
        score = resume_score.score
        # 其他用户-还没有评过分
        if not res_evaluate:
            res_evaluate = ResumeEvaluate(keywords=search_keywords)
        # 如果以前没有计算记录过 职位title得分情况.
        if resume_score.job_related < 1:
            res_evaluate.reset()
            res_evaluate.score_work_experience(resume)
            resume_score.job_related = res_evaluate.get_job_related()
            resume_score.save()
    else:
        # 其他用户-还没有评过分
        if not res_evaluate:
            res_evaluate = ResumeEvaluate(keywords=search_keywords)
#         有多份改简历评分是删除
#         try:
#             resume_score = ResumeScore.objects.get(resume_id=resume_id), keywords=search_keywords)
#
#             score = resume.score = resume_score.score
#         except Exception, MultipleObjectsReturned:
#
#             resume_scores = ResumeScore.objects.filter(resume_id=resume_id), keywords=search_keywords)
#             if resume_scores:
#                 resume_score = resume_scores[0]
#                 score = resume_score.score
#                 brief_comment = resume_score.brief_comment
#
#                 for resume_score in  resume_scores[1:]:
#                     resume_score.delete()

        score = res_evaluate.composite_score(resume)
        brief_comment = res_evaluate.produce_brief_comment()
        job_related = res_evaluate.get_job_related()
        resume_score = ResumeScore(username=username,
                                 resume_id=resume_id,
                                 keywords=search_keywords,
                                 calc_time=datetime.datetime.now(),
                                 score=score,
                                 brief_comment=brief_comment,
                                 job_related=job_related)

        resume_score.save()

    data = {}
    user_resumes = UserResume.objects.filter(username=username, keywords=search_keywords,
                                             resume_id=resume_id).order_by('-add_time')

    add_time = datetime.datetime.now()
    if user_resumes:
        # 该用户已经评过分

        if not is_refresh:
            # 如果是刷新页面则,不再添加计数
            for i, user_resume in enumerate(user_resumes):
                if i == 0:
                    user_resume.add_time = add_time
                user_resume.visit_time_list.append(add_time)
                user_resume.save()

        user_resume = user_resumes[0]
        if user_resume.get_visit_count() >= 2:
            data['status'] = 1
        else:
            data['status'] = 0

    else:
        # 该用户还没有评过分 ,将这个简历添加到该用户
        # 关键地方,将用户和简历绑定.
        data['status'] = 0
        user_resume = UserResume(username=username, resume_id=resume_id,
                                 add_time=add_time,
                                 keywords=search_keywords)
        user_resume.visit_time_list.append(add_time)
        user_resume.save()

    data_dict = produce_resume_data(resume, resume_score, user_resume)
    data.update(data_dict)

    resume_extract_keywords = data['summary']['keywords']
    resume_keywords = produce_resume_keywords(
        resume_id, search_keywords, resume_extract_keywords)

    if len(resume_keywords) > 11:
        resume_keywords = resume_keywords[0:11]

    data['summary']['keywords'] = resume_keywords

    return data, resume_score


def page_counter(page_list, page_cur):
    """
    @summary:分页脚标样式
        　　＃1-3,最后三页，当前页上下三页为默认状态．
            #当前页为不可点击状态．
            #其余页面为　...状态
    """
    page_deco_list = []

    page_sum = len(page_list)

    previous = 0
    _next = 0

    if page_sum <= 10:
        page_deco_list = [(page_num, 'default') if page_num != page_cur else (
            page_num, 'curr') for page_num in page_list]
    else:
        p = page_list
        if page_cur <= 7:
            page_new_list = p[:9] + [-10] + [-10] + p[-3:]
        elif page_cur >= page_sum - 6:
            page_new_list = p[:3] + [-10] + [-10] + p[-8:]
        else:
            page_new_list = p[:3] + [-10] + \
                p[page_cur - 4:page_cur + 4] + [-10] + p[-3:]
        for page_num in page_new_list:
            if page_num == -10:
                page_deco_list.append((page_num, 'dot'))
            elif page_num == page_cur:
                page_deco_list.append((page_num, 'curr'))
            else:
                page_deco_list.append((page_num, 'default'))

    if page_num == page_cur:
        _next = 0
        previous = page_cur - 1
    elif page_num == 1:
        _next = 2
    else:
        _next = page_cur + 1
        previous = page_cur - 1
    return page_deco_list, previous, _next


def get_contact_info(resume_id):
    """
    @summary: 通过resume_id查询得到该简历的联系信息
    @author:  likaiguo.happy@gmail.com 2014-1-6 14:21:08
    """
    from resumes.models import ContactInfoData
    try:
        contact_info = ContactInfoData.objects.get(resume_id=str(resume_id))
    except Exception, e:
        contact_info = None
        contact_infos = ContactInfoData.objects.filter(
            resume_id=str(resume_id))
        if contact_infos:
            contact_info = contact_infos[0]

    return contact_info


def get_age(birthday):
    if birthday is not None:
        birthday = birthday.replace(
            '年', '-').replace('月', '-').replace('日', '')
        year = datetime.date.today().year
        if len(birthday.split('-')) >= 1:
            return year - get_int(birthday.split('-')[0])
        else:
            return 20
    else:
        return 0


def is_exists(resume, contact_info):
    from resumes.models import ContactInfoData
    from resumes.models import UploadResumeData
    if contact_info is not None:
        contacts = ContactInfoData.objects.filter(
            email=contact_info.email).order_by("-add_time")
        if len(contacts) >= 1:
            print contacts[0].resume_id
            resume = UploadResumeData.objects.filter(
                pk=ObjectId(contacts[0].resume_id))
            if len(resume) >= 1:
                return True, resume[0]
            else:
                return False, None
        else:
            return False, None
    else:
        return False, None


if __name__ == "__main__":
    resume_id = '5384667981af590988f753f7'
    resume = ResumeData.objects.get(id=ObjectId(resume_id))
    url_list = [
#         "http://pinbot.me/resumes/display/52acb977d8b9f725619a8272/?feed_keywords=",
        'http://www.pinbot.me/resumes/display/556cea8e452f7141f2e66e19/?feed_id=565be72f036d4a762047e6dd',
#                 "http://ehire.51job.com/Candidate/ResumeViewFolder.aspx?hidSeqID=163818670&hidFolder=BAK",
#                 'http://h.lietou.com/resume/showresumedetail/?res_id=17600485',
#                 'http://rd.zhaopin.com/resumepreview/resume/viewone/2/JR347093729R90250001000_1_1',
#                 'http://rd.zhaopin.com/resumepreview/resume/viewone/1/3180340954',
#                 'http://ehire.51job.com/Candidate/ResumeView.aspx?hidUserID=26087386&hidEvents=23&hidKey=f4f6f9f96416fbaa4138048ce9c4ef26',
#                 'http://ehire.51job.com/Candidate/ResumeViewFolder.aspx?hidSeqID=157796051&hidFolder=BAK',
#                 'http://www.headin.cn/Jobs/Talent/ShowResume/2690416',
#                 'http://h.liepin.com/resume/showresumedetail/?res_id=10808655&keys=632B2B7CE69C8DE58AA1E599A87CE6B8B8E6888F7C6C75617C',
#                   "http://ehire.51job.com/Candidate/ResumeViewFolder.aspx?hidSeqID=165432191&hidFolder=BAK",
        'http://ehire.51job.com/Candidate/ResumeViewFolder.aspx?hidSeqID=165169116&hidFolder=BAK'

    ]

    from urllib import unquote
    for url in url_list:
        url = unquote(url)
        d = get_url_id(url)
        resume = get_resume_from_url(url)
