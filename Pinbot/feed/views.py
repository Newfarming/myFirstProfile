# coding:utf-8
'''
Created on 2013-11-25

@author: dell
@summary:  订阅页面
'''

from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db import transaction as dj_trans

from transaction.models import *
import base64
from resumes.models import *

from Pinbot.settings import LOGIN_URL, PINBOT_ADMIN_AUTH_DICT
from resumes.models import ResumeTag
from models import *

from resumes.models import UserResumeRead

from basic_service.resume_util import produce_return_json, get_resume_from_url
import datetime
from variables.PageID_variables import *
import json

from resumes.views import django_log
from basic_service.feed_query import find_new_feed, get_datetime, get_latest_reco_resumes

from resumes.models import ResumeScore
from basic_service.resume_util import produce_resume_keywords
from resumes.models import Comment
from resumes.models import UserResume

from pinbot_permission.pinbot_decorator import feed_unexpired_required, group_required, page_access_counter_dec, email_access_record_desc

from base_data import compare_keywords_category, get_most_possible_second_category
from app.special_feed.feed_utils import FeedUtils

from resumes.helper import mongo_to_dict
from jobs.models import Company, Job

from pin_utils.django_utils import (
    model_to_dict,
    JsonResponse,
    get_today,
)
from pin_utils.django_deco import (
    pin_login_required,
)
from app.task_system.task_finished_judge import feedback_finished


@login_required(login_url=LOGIN_URL)
@feed_unexpired_required('')
@page_access_counter_dec(page_type_id=PINBOT_FEED_ADD_NEW)
def add_new(request):
    """
    @summary: 添加新订阅页面

    """
    from Pinbot.settings import STATIC_URL
    if request.method == "GET":
        company = Company.objects.filter(user=request.user)
        company_card_dict = {};
        company_card_dict['status'] = True
        jobs_arr = []
        has_jobs =False
        if len(company) >= 1:
            company = company[0]
            company_card_dict['status'] = True
            jobs = Job.objects.filter(company=company,deleted=False)
            for job in jobs:
                has_jobs = True
                job_json = model_to_dict(job)
                jobs_arr.append(job_json)
            company_card_dict['jobs'] = jobs_arr
            jobs_json = json.dumps(company_card_dict)

        page_type = 'feed_submit'
        feed_class = 'curr'
        return render_to_response('feed.html', locals())
    else:
        return redirect('/feed/')


@login_required(login_url=LOGIN_URL)
def feed_nopermission(request):
    from Pinbot.settings import STATIC_URL
    user = request.user
    auth_fail = True
    feed_class = 'curr'
    return render_to_response('feed.html', locals())

@login_required(login_url=LOGIN_URL)
@group_required(['feed', 'tao-cv|feed'], redirect_url='/feed/nopermission')
@page_access_counter_dec(page_type_id=PINBOT_FEED_INDEX)
def feed_list(request):
    """
    @summary: 推荐列表页
    #每日推荐数量,根据最近24小时推荐得到

    """
    from Pinbot.settings import STATIC_URL, USER_FEED_AMOUNT_LIMIT, USER_FEED_NEW_LIMIT, REGISTER_DEADLINE
    username = request.user.username
    user = request.user
    page_type = 'feed_list'
    # 当前页面样式
    feed_class = 'curr'
#     user_feeds = UserFeed.objects.filter(user=user, is_deleted=False)
    user_feeds = UserFeed2.objects.filter(username=username, is_deleted=False)
    user_feeds_count = user_feeds.count()
    if user_feeds_count == 0:
        return redirect('/feed/new')
    # 最近一天推荐未读已发布简历的总数
    unread_resumes_all_count = 0
    total_recommend_count = 0
    total_count = 0
    user_feed_list = []

    time_now = datetime.datetime.now()

    for user_feed in user_feeds:
        # ----推荐---未读---已发布 推荐
        read_id_list = []
        user_resume_reads = UserResumeRead.objects.filter(feed_id=str(user_feed.feed.id))
        if len(user_resume_reads) >= 1:
            user_resume_read = user_resume_reads[0]
            read_id_list = user_resume_read.read_id_list

        latest_unread_reco_count = get_latest_reco_resumes(user_feed.feed.id, user=request.user, count=True)

        user_feed_list.append((user_feed, latest_unread_reco_count))

    return render_to_response('feed.html', locals())


def feed_group_search_ajax(start, feed_id, read_id_list):
    """
    @summary: 订阅数据获取核心接口
    @change: likaiguo.happy@163.com 调整修复系统bug,已读数量,已读简历

    """
    start_time = time.time()
    plantforms = ['zhilian_spider', 'liepin_spider', 'wuyou_spider']
    feed_results_resumes = FeedResult.objects.filter(feed=feed_id, is_recommended=True).order_by("-calc_time").limit(200).values_list('resume')
    feed = Feed2.objects.get(id=feed_id)
    query_has_reco = time.time() - start_time

    search_results = []
    for plantform in plantforms:
        sch_results = SearchResult.objects.filter(feed_id=feed_id, plantform=plantform).order_by("-search_time")
        if sch_results.count():
            search_results.append(sch_results[start])
    search_result_list = []
    user_feed_keywords = feed.keywords + feed.job_type

    for search_result in search_results:

        keywords = [keyword.lower().strip() for keyword in jieba.cut(search_result.keywords_str) if len(keyword.strip())]
        resumes = ResumeData.objects.filter(id__in=search_result.resume_id_list)
        print get_most_possible_second_category(search_result.keywords_str), search_result.keywords_str
        for resume in resumes:
            if resume in feed_results_resumes:
#                 print resume.id,'has reco'
                continue

            education_dict = resume.get_educations_dict(education_count=1)
            if education_dict:
                education_dict = education_dict[0]
            else:
                education_dict = {}

            latest_work_dict = resume.get_latest_work_dict()

            display = False
            position_title = latest_work_dict.get('position_title', '')
            desc = position_title + latest_work_dict.get('job_desc', '')
            desc = desc.lower()

            # 判断是否在一个大类
            if not compare_keywords_category(search_result.keywords_str + user_feed_keywords, position_title):
                if get_most_possible_second_category(position_title):
                    print get_most_possible_second_category(position_title), position_title
                    continue

            for keyword in keywords:
                if keyword in desc:
                    display = True
                    break
            if not display:
#                 print resume.id,'ignored',latest_work_dict.get('position_title',''), '-'.join(keywords)
                continue

            resume_data = {
                "source": resume.get_source(),
                "opened": False,
                "feed_id": str(feed_id),
                "feed_keywords": "java",
                "resume_id": str(resume.id),
                "profile": {
                    "age": resume.get_age(),
                    "gender": resume.get_gender(),
                    "degree": education_dict.get('degree', ''),
                    "school": education_dict.get('school', ''),
                    "work_years": resume.get_work_years(),
                    "address": resume.address
                },
                "calc_time": str(search_result.search_time)[:-7],
                "is_manual": '爬虫搜索:'+search_result.keywords_str,
                "latest_work": latest_work_dict,
                "update_time": resume.update_time,
                "job_target": resume.get_job_target_dict(),
                "keywords": "",
                "recommended_words": {
                    "comment": "",
                    "scope": "",
                    "comment_id": ""
                },
                "resume": mongo_to_dict(resume, []),
                "feed": {
                    "id": str(feed_id),
                    "keywords": "java",
                },
            }

            if resume.id in read_id_list:
                resume_data['opened'] = True
                resume_data['latest'] = False

            search_result_list.append(resume_data)

    total_cost = time.time() - start_time
    data = {
        "status": "ok",
        "start": start,
        "count": len(search_result_list),
        'data': search_result_list,
        'query_has_reco': query_has_reco,
        'total_cost': total_cost,
    }

    next_start = start + 1
    if next_start > 20 or next_start > 100:
        data["next_start"] = -1
    else:
        data["next_start"] = next_start

    return HttpResponse(json.dumps(data))


from pinbot_permission.pinbot_decorator import feed_ajax_cache
@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_FEED_AJAX)
@feed_ajax_cache('')
def feed_group_ajax(request, feed_id):
    """
    @summary: 订阅数据获取核心接口
    @change: likaiguo.happy@163.com 调整修复系统bug,已读数量,已读简历

    """
    if not feed_id or feed_id == "":
        return HttpResponse("")
    all_tags = []
    tag_names = []
    limit = 36
    p = request.GET.copy()
    try:
        start = int(p.get('start', 0))
    except:
        start = 0
    try:
        limit = int(p.get('limit', 36))
    except:
        limit = 36

    try:
        feed_id = ObjectId(feed_id)
    except Exception, e:
        json_data = produce_return_json(status=False, error_dict={"error":str(e)})
        return  HttpResponse(json_data)

    # 获取用户已读的简历id
    from models import UserFeed2, UserFeed

#     user_resume_reads = UserFeed2.objects.filter(username=request.user.username, feed=ObjectId(feed_id))
#     for user_resume_read in user_resume_reads:
#         read_id_list.extend(user_resume_read.read_id_list)

    read_id_list = UserReadResume.objects.filter(user=request.user, feed_id=str(feed_id)).values_list('resume_id')
    read_id_list = set([ObjectId(res[0]) for res in read_id_list if res])

    view = p.get('view', 'user')

    if view == 'search_result':
        print start, feed_id, read_id_list
        return feed_group_search_ajax(start, feed_id, read_id_list)

    yestoday_deadline = get_datetime(hours=-10)
    today_deadline = get_datetime(hours=14)

    # 该项推荐的所有结果
    feed_results = FeedResult.objects.filter(feed=feed_id)

#     newest_feed_result = feed_results.order_by('-calc_time')[0]

    all_reco_feed_results = feed_results.filter(is_recommended=True)

    all_reco_published_feed_results = all_reco_feed_results.filter(published=True)

#     all_reco_not_published_feed_results = all_reco_feed_results.filter(published=False)

    # 总计算数
    total_count = feed_results.count()

    unread_resumes_all_count = 0

    feed_res_unread_id_list = []

    if view in ['user', 'tomorrow']:
        """
        @summary: 用户可以查看的已推荐的并且已发布简历
        """

        if view == 'user':
            time_line = yestoday_deadline
        else:
            time_line = today_deadline

        feed_res_unread_id_list = get_latest_reco_resumes(feed_id, user=request.user, time_line=time_line)

        feed_results = all_reco_published_feed_results(calc_time__lte=time_line)

    elif view == 'cached':
        """
        @summary: 系统推荐待审核的简历

        """
        resume_update_time_deadline = get_datetime(hours=-30 * 24)

        feed_results = feed_results.filter(calc_time__lte=today_deadline, \
                                           resume_update_time__gte=resume_update_time_deadline, \
                                            is_recommended=True, published=False)
        feed_results.limit(limit)

        feed_res_unread_id_list = get_latest_reco_resumes(feed_id, user=request.user, time_line=today_deadline)

    elif view == 'shield':
        all_not_reco_feed_results = feed_results.filter(is_recommended=False)
        feed_results = all_not_reco_feed_results
    else:
        resume_update_time_deadline = get_datetime(hours=-14 * 24)
        feed_results = feed_results.filter(is_recommended=False, \
                                           resume_update_time__gte=resume_update_time_deadline)

    total_recommend_count = feed_results.count()
    # 只看未读按钮
    if p.get('latest') == '1':
        # 未读的简历
        feed_results = feed_results.filter(resume__nin=read_id_list)

    # 关键的排序
    orderby = p.get('orderby', '')
    if orderby in [ '-resume_update_time']:
        feed_results = feed_results.order_by(orderby, '-reco_index', '-calc_time')
    elif orderby in [ '-calc_time']:
        feed_results = feed_results.order_by('-calc_time', '-reco_index', '-resume_update_time')
    elif orderby in [ '-reco_index']:
        feed_results = feed_results.order_by('-reco_index', '-resume_update_time', '-calc_time')
    else:
        feed_results = feed_results.order_by('-calc_time', '-reco_index', '-resume_update_time')


    # 所有未读或者已读的条目数量，用于分页请求计数
    feed_result_count = feed_results.count()

    resumeid_list = []

    # 取某个区段的记录,用于分页
    feed_results = feed_results.skip(start).limit(limit)
    feed_result_list = []
    i = 0

    for feed_result in feed_results:
        resume = feed_result.resume
        i += 1
        try:
            education_dict = resume.get_educations_dict(education_count=1)
            if education_dict:
                education_dict = education_dict[0]
            else:
                education_dict = {}

            brief_keywords = []
            search_keywords = ""
            resume_scores = ResumeScore.objects.filter(resume_id=str(resume.id))
            user_resumes = UserResume.objects.filter(username=request.user.username, resume_id=str(resume.id)).order_by('-add_time')

            if user_resumes:
                search_keywords = user_resumes[0].keywords.strip().lower()

            if resume_scores:
                resume_score = resume_scores[0]
                brief_keywords = produce_resume_keywords(str(resume.id), search_keywords, resume_score.extract_keywords, max_len=8)
            scope = "feed"
            comment_content = ""
            comment_id = ""
            comments = Comment.objects.filter(type=1, resume_id=str(resume.id))
            if comments:
                comment = comments[0]
                comment_content = comment.content
                comment_id = comment.id

                if not comment.feed_id or comment.feed_id == '':
                    scope = 'resume'

            resume_data = {
              "source": resume.get_source(),

              "opened": False,
              "feed_id": str(feed_result.feed.id),
              "feed_keywords":"java",
              "resume_id":str(resume.id),
              "profile": {
                "age": resume.get_age(),
                "gender": resume.get_gender(),
                "degree": education_dict.get('degree', ''),
                "school": education_dict.get('school', ''),
                "work_years": resume.get_work_years(),
                "address":resume.address
              },
              "calc_time":str(feed_result.calc_time)[:-7],
              "is_manual":'猎头推荐' if feed_result.is_manual else '',
             "latest_work": resume.get_latest_work_dict(),
             "update_time":resume.update_time,
             "job_target":resume.get_job_target_dict(),
             "keywords":brief_keywords,
             "recommended_words":{
                "comment":comment_content,
                "scope":scope,
                "comment_id":str(comment_id)
            }
            }
            if '12:00' in resume_data['calc_time']:
                resume_data['is_manual'] = '%s' % (feed_result.admin)
                resume_data['is_manual'] += ' 推荐' if feed_result.is_recommended else '屏蔽'
                resume_data['is_manual'] += '[人工]' if feed_result.is_manual else ''

            if feed_result.id in feed_res_unread_id_list:
                resume_data['latest'] = True

            # opened表示已读未读
            # latest表示左上角是否加新的标志

            if resume.id in read_id_list:
                resume_data['opened'] = True
                resume_data['latest'] = False


            resume_tags = ResumeTag.objects.filter(resume_id=str(resume.id), status='new')
            tag_list = []
            for resume_tag in resume_tags:
                tag_obj = {'tag_id':str(resume_tag.tag_id), 'tag':resume_tag.tag_content}
                tag_list.append(tag_obj)
                if not resume_tag.tag_content in tag_names:
                    all_tags.append(tag_obj)
                    tag_names.append(resume_tag.tag_content)
            resume_data['tags'] = tag_list
            """
            ends
            """

            feed_result_list.append(resume_data)

            resumeid_list.append(str(resume.id))
        except Exception, e:
            django_log.error(e)
            pass

    total_count *= 13

    data = {
        "status": "ok",
        "start": start,
        "count": len(feed_result_list),
        'data' : feed_result_list
      }

    if feed_id:
        if request.user:
            feed_query_log = LogFeedQuery(username=request.user.username, feed_id=str(feed_id), resume_list=resumeid_list, total_num=len(feed_result_list))
            feed_query_log.save()

    next_start = start + limit
    if next_start > feed_result_count or next_start > 100:
        data["next_start"] = -1
    else:
        data["next_start"] = next_start

    data['all_tags'] = all_tags
    data['total_count'] = total_count
    data['total_recommend_count'] = total_recommend_count
    data['newest_recommend_count'] = unread_resumes_all_count
    data['yestoday_deadline'] = str(yestoday_deadline)
    data['unread_resumes_all_count'] = unread_resumes_all_count
    data['feed_result_count'] = feed_result_count
    return HttpResponse(json.dumps(data))


@pin_login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=PINBOT_FEED_DELETE)
@dj_trans.atomic
def feed_delete(request, feed_id):
    """
    删除订阅后将用户的剩余订阅数加1
    """
    ajax_request = request.is_ajax()
    username = request.user.username
    now = datetime.datetime.now()

    user_feeds_mysql = UserFeed.objects.select_related(
        'user_charge_pkg',
        'feed',
    ).filter(
        feed__feed_obj_id=feed_id,
        feed__deleted=False,
        feed__expire_time__gt=now,
    )

    for user_feed in user_feeds_mysql:
        user_pkg = user_feed.user_charge_pkg
        feed = user_feed.feed

        if user_pkg and (user_pkg.rest_feed + 1) <= user_pkg.extra_feed_num:
            user_pkg.rest_feed += 1
            user_pkg.save()

        user_feed.is_deleted = True
        user_feed.delete_time = now

        feed.deleted = True
        feed.delete_time = now
        feed.save()
        user_feed.save()

    user_feeds_mongo = UserFeed2.objects.filter(
        username=username,
        feed=ObjectId(feed_id)
    ).select_related()

    for user_feed in user_feeds_mongo:
        user_feed.is_deleted = True
        user_feed.feed.deleted = True
        user_feed.feed.delete_time = now
        user_feed.delete_time = now

        user_feed.feed.save()
        user_feed.save()

    if ajax_request:
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })
    return redirect(reverse('special-feed-page'))


@pin_login_required(login_url=LOGIN_URL)
def feed_get(request, feed_id, resume_id):

    if request.is_ajax():
        FeedUtils.read_feed(request, feed_id, resume_id)
        return JsonResponse({
            'status': 'ok',
            'msg': 'ok',
        })

    return redirect('/resumes/display/%s/?feed_id=%s' % (resume_id,feed_id))


@csrf_exempt
def add_manual_feed_result(request):
    """
    @summary: 向订阅添加人工的结果
    """
    p = request.POST
    feed_id = p.get('feed_id')
    url = p.get('url')
    username = p.get('username') or request.user.username
    recommend = p.get('recommend', True)
    user = request.user

    if not recommend:
        recommend = False

    feed = ObjectId(feed_id)
    x_pinbot_admin_auth = request.META.get('HTTP_X_PINBOT_ADMIN_AUTH', '')

    if x_pinbot_admin_auth != PINBOT_ADMIN_AUTH_DICT['x-pinbot-admin-auth'] and not user.is_staff:
        data = produce_return_json(data=' x_pinbot_admin_auth is error', status=False)
    elif feed_id and url:
        try:
            resume = get_resume_from_url(url)
            try:
                if resume.update_time.find("-") > 0:
                    resume_update_time = datetime.datetime.strptime(resume.update_time, "%Y-%m-%d")
                elif resume.update_time.find("/") > 0:
                    resume_update_time = datetime.datetime.strptime(resume.update_time, "%Y/%m/%d")
                else:
                    resume_update_time = datetime.datetime.today()
            except :
                resume_update_time = datetime.datetime.today()
            if resume:
                ManualPushResume(username=username, feed=feed, resume=resume, url=url, reco_index=300).save()
                feed_results = FeedResult.objects.filter(feed=feed, resume=resume)
                if feed_results:
                    for feed_result in feed_results:

                        # 判断是否用户自己已经屏蔽过了
                        if feed_result.is_manual  and feed_result.is_recommended == False:
                            data = produce_return_json(data='用户已经被人工屏蔽过了,这条推荐没有保存', status=False)
                            break
                        elif feed_result.is_manual == False and feed_result.is_recommended == False:
                            feed_result.is_recommended = recommend
                            feed_result.resume_update_time = resume_update_time
                            feed_result.is_manual = True
                            feed_result.calc_time = get_datetime(hours=12)
                            feed_result.admin = username
                            feed_result.is_staff = 1 if 'hopperclouds.com' in username else 0
                            feed_result.published = False
                            feed_result.save()
                            data = produce_return_json(data='已经成功修改结果(机器屏蔽数据)', status=False)
                        else:
                            reco_er = ''
                            if '@' in feed_result.admin:
                                reco_er = feed_result.admin
                            else:
                                reco_er = '算法%s_%s' % (feed_result.algorithm, feed_result.admin)
                            hint = "[已推]%s 在 %s[added] 不会强推" % (reco_er, feed_result.calc_time)
                            data = produce_return_json(data = hint  , status = False)
                else:
                    # 管理员,首次添加新的推荐
                    feed_result = FeedResult(feed=feed, resume=resume, \
                                                is_recommended=recommend, reco_index=300, \
                                                job_related=30)
                    feed_result.resume_update_time = resume_update_time
                    feed_result.is_manual = True
                    feed_result.calc_time = datetime.datetime.today()
                    feed_result.published = False
                    feed_result.admin = username
                    feed_result.is_staff = 1 if 'hopperclouds.com' in username else 0
                    feed_result.save()

                    data = produce_return_json(data='首次添加成功')
            else:
                # 人工添加但是还不能在resumeData中找到
                ManualPushResume(username=username, feed=feed, url=url, reco_index=110, has_collected=False).save()
                data = produce_return_json(data='Pinbot 还没有收集到这个简历.has not collected in pinbot sys', status=False)

        except Exception, e:
            data = produce_return_json(data=str(e), status=False)
    else:
        data = produce_return_json(data='feed_id or url is null', status=False)

    return HttpResponse(data, 'application/json')


@login_required
@feedback_finished
def modify_feed_result(request):
    """
    @summary: 功能1.修改机器推荐的结果
              功能2.手工添加结果推荐结果
    """

    get_data = request.GET
    feed_id = get_data.get('feed_id')
    resume_id = get_data.get('resume_id')

    if not (feed_id and resume_id):
        data = produce_return_json(data='feed_id or resume_id is None', status=False)
        return JsonResponse(data)

    reco_index = get_data.get('reco_index', 100)
    feedback_list = get_data.getlist('feedback[]', [])
    user = request.user
    username = user.username
    now = datetime.datetime.now()

    feed = ObjectId(feed_id)
    resume = ObjectId(resume_id)
    reco_index = int(reco_index)

    manual_push_resume = ManualPushResume(
        username=username,
        feed=feed,
        resume=resume,
        reco_index=reco_index,
        op_time=now,
    )
    manual_push_resume.save()

    recommend = True if reco_index >= 0 else False
    resume_update_time = get_today()

    feed_results = FeedResult.objects.filter(feed=feed, resume=resume)
    if not feed_results:
        # 对于搜索结果的推荐点击很合适
        feed_result = FeedResult(
            feed=feed,
            resume=resume,
            algorithm='search_result'
        )
        feed_results = [feed_result]

    for feed_result in feed_results:
        if not feed_result.is_recommended:
            feed_result.is_manual = True

        feed_result.is_recommended = recommend
        feed_result.resume_update_time = resume_update_time

        if reco_index >= 0:
            feed_result.calc_time = now
            feed_result.manual_ensure_time = now
        else:
            # 任务系统中会用到user_feedback_time字段，记录下用户反馈不感兴趣的时间
            feed_result.user_feedback_time = now

        feed_result.reco_index += reco_index

        # 记录下管理员账号,如果是用户自己点击不合适,则留下用户的账号
        feed_result.admin = username
        feed_result.feedback_list = feedback_list
        feed_result._data['is_staff'] = 1 if request.user.is_staff else 0

        # 添加cls_score
        if reco_index >= 0 and request.user.is_staff:
            feed_result.score['cls_score'] = 100

        feed_result.save()

    data = produce_return_json()
    return HttpResponse(data, 'application/json')


def send_feed_email(request):
    sended_num = find_new_feed()
    return HttpResponse('邮件发送完毕！邮件发送完毕，共发送了 ' + str(sended_num) + ' 封邮件')


@login_required
@email_access_record_desc(email_type_id=2)
def record_feed_email(request, feed_str):
    """
    统计每天早上用户点击系统订阅邮件推送之后的点击情况
    """
    p = request.GET.copy()
    action = p.get('action', '')
    token = p.get('token', '')
    if action == "all":
        return redirect("/feed/")
    elif action == "change_profile":
        return redirect("/users/change_profile/#rss")
    else:
        token = base64.b64decode(token)
        token = token.split('&&&')

        if len(token) < 2:
            return redirect("/special_feed/page/")

        feed_id = token[1]
        return redirect("/special_feed/page/#/group/" + feed_id)


@login_required
@csrf_exempt
def modify_send_frequency(request):
    """
    修改邮件发送频率
    """
    data = {}
    try:
        days = int(request.POST['frequency'])
        username = request.user.username
        emailSendInfos = EmailSendInfo.objects.filter(username=username)
        if len(emailSendInfos) == 0:
            emailSendInfo = EmailSendInfo(username=username, sendFrequency=days,
                                lastSendDate=datetime.datetime.now())
        else:
            emailSendInfo = emailSendInfos[0]
            emailSendInfo.sendFrequency = days

        emailSendInfo.save()
        data = {'status':'success'}
    except Exception, e:
        data = {'status':'fail', 'msg':str(e)}
    return HttpResponse(json.dumps(data), 'application/json')


@login_required
def feed_frequency_set(request):
    from Pinbot.settings import STATIC_URL
    if request.method == 'GET':
        page_type = 'feed_list'
        function = 'email_setting'
        username = request.user.username
        userSendInfos = EmailSendInfo.objects.filter(username=username)
        days = -1
        if len(userSendInfos) >= 1:
            userSendInfo = userSendInfos[0]
            days = str(userSendInfo.sendFrequency)

        return render(request, "feed.html", locals())
