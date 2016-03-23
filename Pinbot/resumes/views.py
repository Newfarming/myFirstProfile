# coding: utf-8
"""
@summary:  添加分页功能 2013-10-10 13:55
@author:  likaiguo.happy@163.com


"""

import os
import time

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.db import transaction as dj_trans

from resumes.models import *
from forms import *

import logging
from django.contrib.auth.decorators import login_required
from urllib import unquote

from basic_service.resume_feedback import get_feedback_str, get_feedback, get_offical_feedback

from Pinbot.settings import LOGIN_URL, MEDIA_ROOT, OTHER_DATABASE
from feed.models import ManualPushResume

from variables.resume_global_variables import *

from variables.PageID_variables import *
from basic_service.resume_util import *

from feed.models import FeedResult
from models import *
from pinbot_permission.pinbot_decorator import page_access_counter_dec
from basic_service.resume_util import get_age
from jobs.models import SendCompanyCard

from transaction.models import (
    ResumeBuyRecord,
)

from pin_utils.django_utils import (
    get_oid,
    get_object_or_none,
)
from pin_utils.pdf_utils import PDFUtils
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from Pinbot.settings import (
    PROJECT_ROOT,
    STATIC_URL,
)
from app.vip.vip_utils import MissionUtils
from app.special_feed.feed_utils import FeedUtils
from app.partner.partner_utils import PartnerCoinUtils, UploadResumeUtils
from Brick.App.job_hunting.job_utils import (
    JobUtils,
)

from pin_utils.django_deco import (
    pin_login_required,
)


django_log = logging.getLogger('django')
# channel.queue_declare(queue="plugin_resume_queue", durable=True)
queue_name = OTHER_DATABASE.get('rabbitmq').get('html_resume_queue')


@login_required(login_url=LOGIN_URL)
@csrf_exempt
@page_access_counter_dec(page_type_id=PINBOT_ANALYSE)
def analyse_resumes(request):
    """
    @summary:简历分析
    """
    p = request.POST.copy()
    data = p.get('data', {})

    is_refresh = False

    if data:
        # 第一次提交分析存储在session里边
        request.session['data'] = data
        request.session['is_refresh'] = is_refresh
    else:
        # 后边刷新的时候从session里边取出来
        data = request.session.get('data', {})
        request.session['is_refresh'] = True
        is_refresh = True

    try:
        data = json.loads(data)
    except:
        data = {}
    search_keywords = data.get('keywords', '').strip()

    from Pinbot.settings import STATIC_URL
    http_response = render_to_response(
        "resumes/analyse_resumes.html", locals())
    return http_response


@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=GET_ANALYSE_DATA)
def get_analyse_data(request):
    """
    @summary:  异步加载方式获取最近一次简历分析数据.
    @author: likaiguo.happy@163.com 2013-11-1 14:14:38

    """
    # 后边刷新的时候从session里边取出来
    p = request.POST.copy()
    data = p.get('data', {})
    if not data:
        data = request.session.get('data', {})

    is_refresh = request.session['is_refresh']

    request.session['score_data'] = {}
    try:
        data = json.loads(data)
    except:
        data = {}

    search_keywords = data.get('keywords', '').strip()
    if u'用空格' in search_keywords:
        search_keywords = ''
    urls = data.get('urls', '')

    username = request.user.username

    resume_list = []

    # 等待简历上传完毕 设置超时为 4秒
    res_evaluate = ResumeEvaluate(keywords=search_keywords)

    resume_len = len(urls)
    threshhold = resume_len * 0.9
    time_start = time.time()
    has_calc_list = []
    request.session['score_data']['total'] = resume_len if resume_len else 1
    query_time_total = 0
    calc_time_total = 0
    for i, url in enumerate(urls):
        time_now = time.time()
        has_calc_len = len(resume_list)
#         request.session['score_data']['score_count'] = has_calc_len
#         request.session['score_data']['ratio'] = int(has_calc_len * 100 / resume_len)

        if i >= resume_len:
            # 当处理时间超过5秒,并且已经完成一次算分处理则强制停止算分
            x = time.time() - time_start
            if x >= 5 or has_calc_len > threshhold:
                request.session['score_count'] = resume_len
                request.session['score_data']['score_count'] = has_calc_len
                request.session['score_data']['ratio'] = 1
                break

        # 避免重复计算
        if url in has_calc_list:
            continue
        url_id_dict = get_url_id(url)

        try:
            tmp_time = time.time()
#             resume = ResumeData.objects.get(url__contains=url_id_dict['id'], source__contains=url_id_dict['source'])
#             resume = ResumeData.objects.get(url=url)
#             resume = ResumeData.objects.get(url__contains=url_id_dict['url_q'])
            resume = ResumeData.objects.get(
                source_id=url_id_dict['id'], source__contains=url_id_dict['source'])
            query_time = time.time() - tmp_time
            query_time_total += query_time
            # 每个计算的时间大概为 0.05.  60个简历约花费时间为3.5秒
            # TODO: 修改为多线程.
            tmp_time = time.time()
            data, resume_score = temp_func(
                resume, username, search_keywords, res_evaluate, is_refresh)
            calc_time = time.time() - tmp_time
            calc_time_total += calc_time
            resume_list.append((data, resume_score))
            has_calc_list.append(url)
        except Exception, e:
            tmp_time = time.time()
            collected_resumes = CollectedResume.objects.filter(
                url__contains=url_id_dict['url_q'])
            if collected_resumes:
                # has been added into collected_resume but not parsed.
                resume_id = str(collected_resumes[0]['id'])
                msg = "%s %s %s" % (resume_id, url, 'collected but not parsed')
                user_resumes = UserResume.objects.filter(
                    username=username, resume_id=resume_id)
                create_time = datetime.datetime.now()
                if user_resumes:
                    for user_resume in user_resumes:
                        user_resume.add_time = create_time
                        user_resume.save()
                else:
                    user_resume = UserResume(username=username, resume_id=resume_id,
                                             add_time=create_time)
                    user_resume.save()
                django_log.error(msg)
            else:
                s = "not uploaded by pinbot plugin"
                django_log.error(url + s)
            urls.append(url)
            query_time = time.time() - tmp_time

    return_data = []
    if resume_list:
        resume_list = sorted(
            resume_list, key=lambda x: x[1].score, reverse=True)
        return_data = [tab_data for tab_data, score in resume_list]

    json_data = produce_return_json(data=return_data)
    msg = '%d res total cost: %f,query_time_total %f,calc_time_total %f' % \
        (len(resume_list), time.time() - time_start,
         query_time_total, calc_time_total)
    # TODO:插件简历分析 数据调用错误 http://sentry.pinbot.me/brick/pinbot/group/138/
    django_log.error(msg)

    return HttpResponse(json_data, 'application/json')


@login_required(login_url=LOGIN_URL)
def get_processed_count(request):
    data = request.session.get('score_data', 0)

    json_data = produce_return_json(data=data)

    return HttpResponse(json_data, 'application/json')


@login_required(login_url=LOGIN_URL)
def index(request, page):
    username = request.user.username.lower()
    django_log.info(username)
    if not page:
        page = 1
    if page < 1:
        page = 1

    page = int(page)

    resumes, page_list = get_resumes(username, page=page)
    page_deco_list, previous, page_next = page_counter(page_list, page)

    return render(request, "resumes/list.html", locals())


@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_MY_WATCH)
def resume_watch(request, page=1):
    if not page:
        page = 1

    if page < 1:
        page = 1

    watch_class = 'curr'

    page = int(page)
    username = request.user.username.lower()
#     resumes, page_list = get_resumes(username, page_type=WATCH_RESUME, page=page)
    resumes, page_list = get_resumes_watch(
        request.user, page_type=WATCH_RESUME, page=page)
    if len(page_list):
        page_deco_list, previous, page_next = page_counter(page_list, page)
    return render(request, "resumes/list.html", locals())


def operate_resume(request, resume_id, type):
    """
    @summary: if a user like some resume ,he can click watch on a resume page.
    @author: likaiguo.happy@163.com 2013-09-17 17:55
    """
    if request.method == "GET":
        user = request.user
        p = request.GET.copy()
        feed_keywords = p.get('feed_keywords', '')
        feed_id = p.get('feed_id', '')
        if resume_id:
            resume_id = str(resume_id)
            watch_time = datetime.datetime.now()
            user_watch_resumes = UserWatchResume.objects.filter(user=user,
                                                                resume_id=resume_id)
            if user_watch_resumes:
                for user_watch_resume in user_watch_resumes:
                    user_watch_resume.resume_id = resume_id
                    user_watch_resume.feed_id = feed_id
                    user_watch_resume.type = type  # 修改搜有搜索词的改简历的关注状态.
                    user_watch_resume.add_time = watch_time
                    user_watch_resume.feed_keywords = feed_keywords
                    user_watch_resume.save()
            else:
                user_resume = UserWatchResume(user=user, resume_id=resume_id,
                                              type=type, add_time=watch_time, feed_id=feed_id,
                                              feed_keywords=feed_keywords)
                user_resume.save()

            # 反馈关注结果给算法
            FeedUtils.feed_result_watch(resume_id, feed_id, type)

            json_data = produce_return_json(data={})
            return HttpResponse(json_data, 'application/json')


@pin_login_required
@page_access_counter_dec(page_type_id=PINBOT_ADD_WATCH)
def add_watch(request, resume_id, type=WATCH_RESUME):
    return operate_resume(request, resume_id, type)


@pin_login_required
@page_access_counter_dec(page_type_id=PINBOT_REMOVE_WATCH)
def remove_watch(request, resume_id, type=DEFAULT):
    return operate_resume(request, resume_id, type)


@login_required
@page_access_counter_dec(page_type_id=PINBOT_DISCARD_RESUME)
def discard_resume(request, resume_id, type=DISCARD_RESUME):
    return operate_resume(request, resume_id, type)


@login_required(login_url=LOGIN_URL)
def resume_discard(request, page):
    if not page:
        page = 1

    if page < 1:
        page = 1

    page = int(page)
    username = request.user.username.lower()
    resumes, page_list = get_resumes(
        username, page_type=DISCARD_RESUME, page=page)
    page_deco_list, previous, page_next = page_counter(page_list, page)

    return render(request, "resumes/list.html", locals())


@page_access_counter_dec(page_type_id=PINBOT_DISPLAY)
@dj_trans.atomic
def display(request, resume_id, resume_score):
    """
    @summary: 详细信息展示页面
    @author:liyao
    """
    from Pinbot.settings import STATIC_URL
    p = request.GET
    feed_id = p.get('feed_id')
    feed_result = FeedUtils.get_feed_result(feed_id, resume_id)
    if feed_result:
        calc_time = feed_result.calc_time
        if request.user.is_staff and feed_result.feed.username != request.user.username:
            read_user = 'admin'
        else:
            read_user = 'user'
        FeedUtils.read_feed(request, feed_id, resume_id, read_user=read_user)
    try:
        if hasattr(feed_result, 'tags'):
            keywords_new = feed_result.tags.keywords
            feed_keywords = u' '.join(keywords_new)
        else:
            feed_keywords = feed_result.feed.keywords
    except:
        feed_keywords = u''
    try:
        resume = ResumeData.objects.get(id=resume_id)
        if resume.source == 'pinbot':
            resume['age'] = get_age(resume.birthday)

        resume.work_years = resume.get_work_years()

    except Exception, e:
        raise Http404()
    resume.gender = resume.get_gender()
    user = request.user

    # 最近 一次 该简历 使用该关键词的评分
    search_keywords = ''

    if not user.is_anonymous():
        # 用户对于简历的状态,关注,删除,默认状态等.

        watch_status = 0
        username = user.username.lower()
        user_resumes = UserWatchResume.objects.filter(
            user=user, resume_id=resume_id).order_by('-add_time')

        if user_resumes:
            search_keywords = user_resumes[0].keywords.strip().lower()
            watch_status = user_resumes[0].type

    if not search_keywords:
        search_keywords = feed_keywords
    # 简历评分
    resume_scores = ResumeScore.objects.filter(
        resume_id=resume_id, keywords=search_keywords).order_by('-calc_time').limit(1)
    if resume_scores:
        # 已经进行过评分则取最近一次的评分
        resume_score = resume_scores[0]
    else:
        # 还为进行过评分,立即进行评分
        res_evaluate = ResumeEvaluate(keywords=search_keywords)
        score = res_evaluate.composite_score(resume)
        brief_comment = res_evaluate.produce_brief_comment()
        resume_score = ResumeScore(resume_id=resume_id,
                                   keywords=search_keywords,
                                   calc_time=datetime.datetime.now(),
                                   score=score,
                                   brief_comment=brief_comment)
        resume_score.save()

    # 提取简历描述关键词
    if resume_score.extract_keywords:
        keywords = resume_score.extract_keywords
    else:
        keywords = resume.extract_keywords()
        resume_score.extract_keywords = keywords
        resume_score.save()

    resume_score.get_star()

    resume_score.extract_keywords = produce_resume_keywords(
        resume_id, search_keywords, resume_score.extract_keywords,)

    content = resume.get_related_content()
    content = content.lower()

    extract_keywords = []
    for keyword in resume_score.extract_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in content:
            extract_keywords.append(keyword)
    resume_score.extract_keywords = extract_keywords

    # 获取简历的购买状态
    from transaction.models import ResumeBuyRecord
    user_buy_status = ''
    resumeBuyRecords = ResumeBuyRecord.objects.select_related(
        'resume_mark',
        'resume_mark__current_mark',
    ).prefetch_related(
        'resume_mark__mark_logs',
    ).filter(
        user=user.id, resume_id=str(resume_id)
    )
    if resumeBuyRecords:
        user_buy_status = resumeBuyRecords[0].status
        resume_buy_record = resumeBuyRecords[0]

    if resume.job_target:
        resume.job_target.job_hunting_state = resume.job_target.job_hunting_brief(
            source=resume.source)
        resume.job_target.set_expectation_area_list()
    resume.url_to_link()
    resume.set_project_company()
    resume.get_url()

    if resume is None:
        raise Http404

    contact_info = None
    display_src = False if 'lietou.com' in resume.url or 'liepin.com' in resume.url else True
    # 如果推荐度非常高则不显示原简历来源

    comment_content = ""
    comments = Comment.objects.filter(type=1, resume_id=str(resume.id))
    if comments:
        comment = comments[0]
        comment_content = comment.content
        has_feed_id = True
        feed_id_match = True

    if feed_id:
        try:
            feed_id = ObjectId(feed_id)
            reco_large = ManualPushResume.objects.filter(
                feed=feed_id, resume=ObjectId(resume_id), reco_index__gte=50).count()
            if reco_large:
                display_src = False
        except:
            feed_id = ''

    # 获取简历标签以及简历反馈信息
    resume_tags = ResumeTag.objects.filter(
        resume_id=str(resume.id), status='new')
    tag_list = []
    for resume_tag in resume_tags:
        tag_list.append((str(resume_tag.tag_id), resume_tag.tag_content))
    if not user.is_anonymous():
        check_status, type_desc, feedback_str, re_points = get_feedback_str(
            request.user, str(resume.id))
        offical_feedback = get_offical_feedback(str(resume.id))
    if request.user.is_staff == 1:
        feedback_dict = get_feedback(str(resume.id))
        if feedback_dict and len(feedback_dict) >= 1:
            has_feedback = True

    display_aside = True

    if not user.is_anonymous():
        # 第二次领取红包任务
        is_user_feed = False
        if FeedUtils.is_user_feed(user, feed_id):
            username = user.username
            is_user_feed = True

        is_send_resume = True if FeedUtils.is_send_resume(
            user, resume_id) else False

        # 人才伙伴添加点数
        PartnerCoinUtils.check_resume(feed_id, resume_id)

        # 是否是人才伙伴自己在查看简历
        self_upload_resume = True if UploadResumeUtils.is_self_upload(
            user, resume_id) else False

        # 获取投递工作
        job_id = request.GET.get('job_id', '0')
        recommend_job = JobUtils.get_recommend_job(job_id, user)

        is_admin = None
        # 查看该用户是否购买该简历
        contact_info = get_contact_info(resume.id)
        if user.is_staff == 0:
            if ResumeBuyRecord.objects.filter(user=request.user, resume_id=resume_id, status='LookUp').count() == 0 and not self_upload_resume:
                if contact_info is not None:
                    status = contact_info.status
                    contact_info = ContactInfoData()
                    contact_info.status = status
        if user.is_staff == 1:
            is_admin = True

        # 获取企业名片发送情况
        send_company_card = SendCompanyCard.objects.filter(
            resume_id=resume_id, send_user=user)
        if len(send_company_card) >= 1:
            send_company_card = send_company_card[0]
        return render(request, "resumes/display.html", locals())
    else:
        return render(request, "resumes/display_brief.html", locals())


# @login_required(login_url=LOGIN_URL)
@csrf_exempt
def get_resumes_state(request):
    """
    @summary:  简历搜索结果页面,先与服务器会话,查询该简历是否已经在服务器端下载过,返回下载状态
    @author: likaiguo.happy@163.com 2013-10-24 17:01:04
    """

    p = request.POST.copy()

    data = p.get('data')

    try:
        data = json.loads(data)
    except:
        data = {}

    urls = data.get('urls', [])
    update_times = data.get('update_times', [])
#     search_keywords = data.get("keywords", '')

    i = 0  # 服务器不存在简历的个数
    resumes_state_list = []
    if len(urls) == 1:
        """
        如果插件在简历详情页则直接覆盖之前的简历，直接简历未解析过而直接覆盖之前的简历
        """
        resumes_state_list.append(0)
        json_data = produce_return_json(data=resumes_state_list, status=False)
        return HttpResponse(json_data, 'application/json')

    j = 0
    for url in urls:
        #         resumes = ResumeData.objects.filter(url__contains=url_id_dict['url_q'])
        try:
            update_time = update_times[j]
        except:
            update_time = ''
        j += 1
        resume = get_resume_from_url(url)
        if resume:
            if resume.update_time != update_time:
                resume = None

        if resume:
            # 服务器端已存在则返回状态1
            resumes_state_list.append(1)

        else:
            # 服务器端不存在则返回状态 0
            i = i + 1
            resumes_state_list.append(0)

    json_data = produce_return_json(data=resumes_state_list)

    return HttpResponse(json_data, 'application/json')


@csrf_exempt
def collect_resume(request):
    """l
    @summary: collect resumes from plugin.

    @todo: 1.check the current user whether has the privilege of a resume contact info.

    """
    count_time_dict = {}
    try:
        p = request.POST.copy()
    except Exception, e:
        data = produce_return_json(data=str(e), status=False)
        return HttpResponse(data, 'application/json')

    if request.method == "GET":
        json_data = produce_return_json(
            {}, False, error_dict={'type': 'method error', 'message': 'please post data'})
        return HttpResponse(json_data, 'application/json')
    else:
        need_parse = "no"  # 用于确定是否需要解析简历
        if request.user:
            username = request.user.username
        else:
            username = 'hr@pinbot.com'
        url = p.get("url", '')
        update_time = p.get("update_time", '')
        url = unquote(url)
        search_keywords = request.POST.get("keywords", '')
        # TODO: 需要细化做的,比如 输入: java 开发 ,与 开发 java应该算作同一个,
        # 或者说,输入java    开发中间很多空格的应该算作同一个关键词.
        if search_keywords in [u'请输入简历关键词，多关键词可用空格分隔', u'多关键字用空格隔开']:
            search_keywords = ''
        if url == "":
            json_data = produce_return_json(data={'username': username},
                                            status=False,
                                            error_dict={'type': 'url null', 'message': 'url is required'})
            return HttpResponse(json_data, 'application/json')

        html = p.get('html', '').strip()
        html_len = len(html)
        phone_pub = True
        if "liepin.com" in url or "lietou.com" in url:
            # 判断猎聘的简历是否为不公开电话号码的简历
            pass
#                 import re
#                 phone_pub = re.search("mobile-number([\s\S]*?)</dd>",html)
#                 if phone_pub and "不公开" in phone_pub.group(1):
#                     phone_pub = False

        s = u"因请求量过大导致系统无法处理您的请求"
        if s in html or not phone_pub:
            django_log.error(html)
            error_dict = {'error': 'resume has been deleted! or needed verify code'}
            count_time_dict['username'] = username
            json_data = produce_return_json(
                data={'username': username}, error_dict=error_dict, status=False)
            return HttpResponse(json_data, 'application/json')

        add_time = datetime.datetime.now()

        try:
            if html.find('此简历为未下载简历') < 0 \
                    and html.find("免费查看联系方式") < 0 \
                    and html.find("如需联系方式请下载该简历") < 0:
                has_contact = 1
            else:
                has_contact = 0
        except:
            has_contact = 0

        resume = get_resume_from_url(url)
        if resume:
            raw_resume_id = resume.id
            need_parse = 'yes'
        else:
            #TODO: 2015-10-25 18:42:17 历史版本处理策略待定
#             existed_collect_resume = CollectedResume.objects.filter(url=url)
#             print(existed_collect_resume.count())
            raw_resume_id = ObjectId()
            need_parse = 'yes'

        resume_id = str(raw_resume_id)
        collected_resume = CollectedResume(
            id=raw_resume_id,
            userid=username,
            url=url,
            html=html,
            add_time=add_time,
            status='processing',
            resume_update_time=update_time,
            search_keywords=search_keywords,
        )
        collected_resume.save()

        # save the map from user to the un_paresed resume
        user_resumes = UserResume.objects.filter(username=username,
                                                 resume_id=resume_id,
                                                 keywords=search_keywords).order_by('-add_time')

        if user_resumes:
            for i, user_resume in enumerate(user_resumes):
                if i == 0:
                    user_resume.add_time = add_time
                user_resume.has_contact = has_contact
                user_resume.save()
        else:
            user_resume = UserResume(username=username, resume_id=resume_id,
                                     add_time=add_time, has_contact=has_contact,
                                     keywords=search_keywords)
            user_resume.save()

        # insert into rbmq
        if need_parse == 'yes':
            message = {"resume_id": resume_id, "file_id": None, "path":
                       None, "content_type": 'html', "start_process": need_parse}
            send_to_rabbitmq(message)

        count_time_dict['url'] = url
        count_time_dict['html_len'] = html_len
        count_time_dict['resume_id'] = resume_id
        json_data = produce_return_json(data=count_time_dict)
        return HttpResponse(json_data, 'application/json')


@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_SAVE)
def save_to_pinbot(request):

    p = request.GET.copy()
#     url = p.get('url','')
    url = unquote(p.get('url', ''))
    url_id_dict = get_url_id(url)
    collected_resumes = CollectedResume.objects.filter(
        url__contains=url_id_dict['url_q'])
    if collected_resumes:
        collected_resume = collected_resumes[0]
        resume_id = str(collected_resume['id'])

        return redirect('/resumes/display/%s/' % (resume_id))
    else:

        return HttpResponse('%s not exits in database' % url, 'text/html')


def send_to_rabbitmq(message):
    import basic_service.queue2 as queue
    queue.mutex.acquire(1)
    queue.channel.basic_publish(
        exchange='', routing_key=queue_name, body=json.dumps(message))
    queue.mutex.release()


@csrf_exempt
@login_required
@page_access_counter_dec(page_type_id=PLUGIN_POPUP)
def get_parsed_resume(request):
    """
    @summary: chrome-extension get the parsed resume data of some url.


    """
    p = request.GET.copy()
    username = request.user.username.lower()

    url = p.get('url')
    url = unquote(url)

    resume = get_resume_from_url(url)
    if not resume:
        # 简历未收到 或者 简历未解析

        data = {"status": 0,
                "profile": {"degree": " ",
                            "brief_comment": "",
                            "name": u"未解析",
                            "gender": "male",
                            "age": 22,
                            "job_hunting_state": "",
                            "work_years": 1,
                            "avatar_url": "",
                            "location": "",
                            "homepage": [],
                            "expectation_area": ""},
                "works": [{"salary": "", "company_name": "",
                           "start_time": "",
                           "position_title": "",
                           "end_time": "",
                           "duration": ""}]}
        json_data = produce_return_json(data=data)
        return HttpResponse(json_data, 'application/json')

    resume_id = str(resume.id)
    # 某个用户最近一次的检索关键词
    user_resumes = UserResume.objects.filter(
        resume_id=resume_id, username=username).order_by('-calc_time')
    search_keywords = ''
    for user_resume in user_resumes:
        if user_resume.keywords:
            search_keywords = user_resume.keywords.strip()
            break
    # 评分 -星级

    data, _ = temp_func(resume, username, search_keywords)

    json_data = produce_return_json(data=data)
    return HttpResponse(json_data, 'application/json')


@csrf_exempt
@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_ADD_RESUME_TAG)
def add_resume_tag(request):
    """
    @summary: 添加简历标签
    @author:  liyao 2014-5-13 17:45:22
    """
    re_message = {}
    try:
        username = request.user.get_username()
        p = request.POST.copy()
        tag = p.get('tag', None)
        resume_id = p.get('resume_id', None)
        tag_id = p.get('tag_id', None)
        if tag_id and resume_id:
            # 如果tag已经存在直接写resumetag表记录
            resume_tags = ResumeTag.objects.filter(
                resume_id=resume_id, tag_id=tag_id, status='new')
            if len(resume_tags) == 0:
                resume_tag = ResumeTag(user=request.user, resume_id=resume_id, tag_id=int(
                    tag_id), tag_content=tag, add_time=datetime.datetime.now())
                resume_tag.save()
            re_message = {'status': 'success', 'tag_id': tag_id, 'tag': tag}
        elif (resume_id != None and resume_id.strip() != '') and (tag != None and tag.strip() != ''):
            # 如果tag不存在先查询tag表记录是否存在，存在则直接取出tag，否则写入tag表和resume_tag表
            tags = Tag.objects.filter(tag_content__iexact=tag, type=1)
            if len(tags) >= 1:
                tag = tags[0]
                resume_tags = ResumeTag.objects.filter(
                    resume_id=resume_id, tag=tag, status='new')
                if len(resume_tags) == 0:
                    resume_tag = ResumeTag(
                        user=request.user, resume_id=resume_id, tag=tag, tag_content=tag.tag_content, add_time=datetime.datetime.now())
                    resume_tag.save()
                re_message = {
                    'status': 'success', 'tag_id': str(tag.id), 'tag': tag.tag_content}
            else:
                tag = Tag(add_user=request.user, scope='resume', resume_id=resume_id,
                          tag_content=tag, add_time=datetime.datetime.now())
                tag.save()
                resume_tag = ResumeTag(user=request.user, resume_id=resume_id, tag=tag,
                                       tag_content=tag.tag_content, add_time=datetime.datetime.now())
                resume_tag.save()
                re_message = {
                    'status': 'success', 'tag_id': str(tag.id), 'tag': tag.tag_content}
        else:
            re_message = {'status': 'fail', 'msg': 'no resume or tag'}

    except Exception, e:
        re_message = {'status': 'fail', 'msg': str(e)}

    json_data = json.dumps(re_message)
    return HttpResponse(json_data, 'application/json')


@csrf_exempt
@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_DEL_RESUME_TAG)
def del_resume_tag(request):
    """
    @summary: 删除简历标签
    @author:  liyao 2014-5-14
    """
    try:
        p = request.POST.copy()
        tag_id = p.get('tag_id', None)
        resume_id = p.get('resume_id', None)
        if (resume_id != None and resume_id.strip() != '') and (tag_id != None and tag_id.strip() != ''):
            resume_tags = ResumeTag.objects.filter(
                resume_id=resume_id, tag_id=int(tag_id), status='new')
            if len(resume_tags) >= 1:
                resume_tag = resume_tags[0]
                resume_tag.status = 'deleted'
                resume_tag.save()
                json_data = json.dumps(
                    {'status': 'success', 'tag_id': str(resume_tag.id)})
            else:
                json_data = json.dumps(
                    {'status': 'fail', 'msg': 'tag not existed'})
        else:
            json_data = json.dumps(
                {'status': 'fail', 'msg': 'no resume_id or tag_id provided'})
    except Exception, e:
        json_data = json.dumps({'status': 'fail', 'msg': str(e)})

    return HttpResponse(json_data, 'application/json')


@csrf_exempt
@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_ADD_FEED_TAG)
def add_search_tag(request):
    """
    @summary: 添加订阅标签
    @author:  liyao 2014-5-13 17:45:22
    """
    try:
        p = request.POST.copy()
        tag = p.get('tag', None)
        feed_id = p.get('feed_id', None)
        if (feed_id != None and feed_id.strip() != '') and (tag != None and tag.strip() != ''):
            resume_tag = Tag(type=2, user=request.user, feed_id=feed_id,
                             tag_content=tag, add_time=datetime.datetime.now())
            resume_tag.save()
            json_data = json.dumps(
                {'status': 'success', 'tag_id': str(resume_tag.id)})
        else:
            json_data = json.dumps(
                {'status': 'fail', 'msg': 'no resume or tag'})
    except Exception, e:
        json_data = json.dumps({'status': 'fail', 'msg': str(e)})

    return HttpResponse(json_data, 'application/json')


@csrf_exempt
@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_ADD_FEED_TAG)
def get_all_tags(request):
    all_tags = []
    tags = Tag.objects.filter(type=1)
    for tag in tags:
        if tag.tag_content == 'C++' or tag.tag_content == 'Android' or tag.tag_content == 'Windows' or tag.tag_content == 'IOS':
            continue
        else:
            tag_obj = {'tag_id': str(tag.id), 'tag': tag.tag_content}
            all_tags.append(tag_obj)
    json_data = json.dumps({'data': all_tags})
    return HttpResponse(json_data, 'application/json')


@csrf_exempt
@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_ADD_COMMENT)
def add_comment(request, resume_id):
    """
    @summary: 添加评论
    @author:  liyao 2014-3-7 18:13:22
    """
    try:
        type = 2
        if request.user.is_staff:
            type = 1
        user = request.user
        p = request.POST.copy()
#         p = request.GET.copy()
        comment = p.get('comment')
        scope = p.get('scope', '')

        feed_id = p.get('feed_id', None)
        comment_id = p.get('comment_id', None)

        if scope == '':
            type = 2
        if comment_id:
            user_comments = Comment.objects.filter(
                type=type, user=user, resume_id=resume_id, id=int(comment_id))
            comment_time = datetime.datetime.now()
            if scope == 'feed' and feed_id:
                new_user_comment = Comment(type=type, content=comment, feed_id=feed_id, comment_time=comment_time,
                                           resume_id=resume_id, user=user)
            else:
                new_user_comment = Comment(type=type, content=comment, comment_time=comment_time,
                                           resume_id=resume_id, user=user)
            if user_comments:
                user_comment = user_comments[0]
                new_user_comment.id = user_comment.id

            user_comment.delete()
            new_user_comment.save()
            json_data = produce_return_json(
                data={'comment_id': str(new_user_comment.id)})
        else:
            if comment:
                resume_id = str(resume_id)
                comment_time = datetime.datetime.now()

                if scope == 'feed' and feed_id:
                    comment = Comment(type=type, content=comment, feed_id=feed_id, comment_time=comment_time,
                                      resume_id=resume_id, user=user)
                else:
                    comment = Comment(type=type, content=comment, comment_time=comment_time,
                                      resume_id=resume_id, user=user)
                comment.save()
                json_data = produce_return_json(
                    data={'comment_id': str(comment.id)})
            else:
                json_data = produce_return_json(
                    status=False, error_dict='comment content is empty')
    except Exception, e:
        json_data = produce_return_json(status=False, error_dict=str(e))

    return HttpResponse(json_data, 'application/json')


@login_required(login_url=LOGIN_URL)
def get_comments(request, resume_id):
    """
    @summary: 获取简历评论
    @author: likaiguo.happy@163.com 2013-10-22 18:14:50
    """
    resume_id = str(resume_id)
    user = request.user

    comments_list = Comment.objects.filter(
        type=2, user=user, resume_id=resume_id).order_by('-comment_time')
    if comments_list:
        comments_list = [comment.to_dict() for comment in comments_list]
    else:
        comments_list = ''
    json_data = produce_return_json(data=comments_list)

    return HttpResponse(json_data, 'application/json')


@csrf_exempt
@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_DEL_COMMENT)
def delete_comment(request, resume_id, comment_id):
    """
    @summary: 删除某条评论
    @author:  likaiguo.happy@163.com 2013-10-22 18:14:35

    """
    resume_id = str(resume_id)
    comment_id = str(comment_id)
    comments = Comment.objects.filter(
        user=request.user, resume_id=resume_id, id=int(comment_id))
    comments.delete()

    json_data = produce_return_json()

    return HttpResponse(json_data, 'application/json')


def delete_collect_resume(request):
    j = 0
    resumes = CollectedResume.objects.filter().limit(500000)
    for resume in resumes:
        url = resume.url
        dup_resumes = CollectedResume.objects.filter(
            url=url, status='processed').order_by('-createtime')
        print len(dup_resumes)
        if len(dup_resumes) >= 3:
            dup_resumes = dup_resumes[0:len(dup_resumes) - 2]
            for dup_resume in dup_resumes:
                j += 1
                dup_resume.delete()
    return HttpResponse(json.dumps({'total': str(j)}), 'application/json')


def delete_fail_resume(request):
    resumes = ResumeData.objects.filter(update_time='')
    i = 0
    for resume in resumes:
        i += 1
        print i
        feed_results = FeedResult.objects.filter(resume=resume)
        if len(feed_results) >= 1:
            print resume.id
            collects = CollectedResume.objects.filter(pk=resume.id)
            if len(collects) >= 1:
                collect = collects[0]
                collect.status = 'processing'
                collect.save()
        else:
            resume.delete()


def notexistedresume(request):
    from bson import DBRef
    i = 0
    j = 0
    feed_results = FeedResult.objects.filter(published=True)
    for feed_result in feed_results:
        print i
        i += 1
        if isinstance(feed_result.resume, DBRef):
            j += 1
            print str(feed_result.resume)
    print 'total: ' + j


class DownloadResume(LoginRequiredMixin, View):
    template = 'download_resume.html'
    pdf_assert_path = os.path.join(PROJECT_ROOT, 'public/')

    def get_filename(self, contact_info, resume):
        name = contact_info.name if contact_info else ''
        position_title = resume.works[0].position_title if resume.works else ''
        gender = resume.gender
        work_years = '%s年' % resume.work_years
        degree = resume.educations[0].degree if resume.educations else ''
        filename = '_'.join(
            str(i).strip() for i in (u'聘宝', name, position_title, gender, work_years, degree) if i
        ).encode('utf-8')
        return filename

    def get(self, request, download_type, resume_id):
        resume_oid = get_oid(resume_id)

        if not resume_oid:
            raise Http404

        user = request.user
        request_dict = {
            key: True if get_int(value) else False
            for key, value in request.GET.items() if key in ('name', 'contact_info', 'salary')
        }

        resume = ResumeData.objects.filter(
            id=resume_oid,
        ).first()
        has_buy_resume = ResumeBuyRecord.objects.filter(
            user=user,
            resume_id=resume_id,
            status='LookUp'
        )
        is_pinbot_staff = user.is_staff
        show_contact_info = has_buy_resume or is_pinbot_staff
        contact_info = get_object_or_none(
            ContactInfoData,
            resume_id=resume_id,
        )

        filename = self.get_filename(contact_info, resume)
        resume_href = self.request.build_absolute_uri(
            reverse('resume-display-resume', args=(resume.id, 0))
        )
        context_data = {
            'download_type': download_type,
            'resume': resume,
            'contact_info': contact_info,
            'show_contact_info': show_contact_info,
            'resume_href': resume_href,
            'is_pinbot_staff': is_pinbot_staff,
            'request_dict': request_dict,
        }

        if download_type == 'pdf':
            filename = '%s.pdf' % filename
            context_data['assert_url'] = self.pdf_assert_path
            context_data['pdf_type'] = True
            response = PDFUtils.download_pdf(
                self.template,
                filename=filename,
                context_data=context_data,
            )
            return response
        else:
            filename = '%s.html' % filename
            html_assert_url = self.request.build_absolute_uri(
                STATIC_URL
            )

            context_data['assert_url'] = html_assert_url
            html_file = render_to_string(
                self.template,
                context_data,
            )
            response = HttpResponse(
                html_file,
                content_type='application/octet-stream',
            )
            response[
                'Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
