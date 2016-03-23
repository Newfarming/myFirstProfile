# coding:utf-8
"""
@summary: 统计数据一些逻辑和展示.


以每一个客户为单位，统计每日0:00-24:00时间区段的以下信息：
1、聘宝登陆次数；
2、使用聘宝分析次数；
3、聘宝简历查看次数；
4、原简历中使用聘宝插件次数；
5、当天首次登陆时间；
6、当天末次使用时间；
7、关键词搜索明细；
8、聘宝简历关注数量。
PINBOT_ANALYSE = 10
PINBOT_ANALYSE_REFRESH = 11
GET_ANALYSE_DATA = 20
GET_ANALYSE_DATA_REFRESH = 21
PLUGIN_POPUP = 30
PINBOT_DISPLAY = 40

PINBOT_ADD_WATCH = 50
PINBOT_REMOVE_WATCH = 51
PINBOT_DISCARD_RESUME = 52

PINBOT_ADD_COMMENT = 60
PINBOT_SAVE = 70

Created on 2013-11-9

@author: likaiguo.happy@gmail.com 2013-11-9 23:10:50
"""

from statistics.patch_tools import add_read_rate
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from  django.contrib.auth.decorators import  login_required
from django.views.decorators.csrf import csrf_exempt
from  django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http.response import HttpResponse

from models import StatisticsModel, UserFeedBack
from statistics.global_variables import PINBOT_STATIS_LIST, PINBOT_STATIS_HEAD_LIST
from resumes.models import ResumeScore
from transaction.models import ResumeBuyRecord, UserChargePackage
from access_counter import page_access_counter_dec
from global_variables import PAGE_STATIS

from Pinbot.settings import ALLOWED_USERS

from feed.models import UserFeed, FeedResult, ManualPushResume,UserFeed2
from resumes.models import Comment,UserWatchResume
from users.views import send_email
from django.template.loader import render_to_string
from taocv.models import *

import  jieba

from bson import ObjectId
from basic_service.resume_util import produce_return_json

from mongoengine.queryset import Q
from basic_service.feed_query import get_datetime
import logging
from pin_utils.django_utils import get_tomommow, get_today

from FeedCelery.celery_utils import CeleryUtils

django_log = logging.getLogger('django')

# from basic_service.pin_Email import load_template, send_email


def get_latest_access_username(days=1):
    look_date = datetime.now() - timedelta(days)
    look_date = look_date.replace(hour=0, minute=0, second=0)
    access_username_list = StatisticsModel.objects.filter(access_time__gte=look_date).distinct('username')

    return access_username_list

@login_required
@csrf_exempt
@page_access_counter_dec(page_type_id=PAGE_STATIS)
def statistic_data(request):
    """
    @summary: 统计数据展示

    @author: likaiguo.happy@163.com 2014-2-21 14:37:13
    @change: 现阶段更加关键推荐的准确率和人工推荐的有效性,现加入新的指标
    #分为:已发布[总推荐数,人工推荐数,机器推荐数],用户阅读层面[用户阅读推荐总数,人工推荐数,机器推荐数],未发布[总推荐数,机器推荐数,人工推荐数,计算数]

    """

    if not request.user.is_staff:
        return redirect("/")
#     username_list = StatisticsModel.objects.distinct("username")
#     users_list = User.objects.all().order_by("-date_joined")
    statistic_res_list = []
    statis_keys_list = PINBOT_STATIS_HEAD_LIST
    p = request.GET.copy()
    days = p.get('days', 0)
    look_days = p.get('look_days', 30)
    t_now = datetime.now()
    t_now = t_now.replace(hour=0, minute=0, second=0)
    user_access_date = t_now - timedelta(int(days))

    look_date = t_now - timedelta(int(look_days))

    username_list = StatisticsModel.objects.filter(access_time__gte=user_access_date).distinct('username')
    username_list = sorted(set(username_list) - (set(username_list) & set(ALLOWED_USERS)), key=username_list.index)
    username_list.extend(ALLOWED_USERS)
    i = 1

    for  username in username_list:
#     for username, access_time in username_list:
#     for i, user in enumerate(users_list):
        access_list = []
#         username = user.username
#         # TODO:2013-12-13 16:09:30 特别注意这种方法有问题，用户量大时候效率很低
#         if StatisticsModel.objects(username=username, access_time__gte=look_date).count() == 0:
#             continue
        try:
            user = User.objects.get(username=username)
        except:
            continue
        company_name = user.get_short_name()
        for statis_type, page_id in PINBOT_STATIS_LIST:
            statistic_count = StatisticsModel.objects(username=username, page_id=page_id, \
                                                       access_time__gte=look_date).count()
            access_list.append(statistic_count)
#         # 用户订阅未删除总数
#         user_feeds = UserFeed.objects(username=username, is_deleted=False)  # , add_time__gte=look_date)
#         access_list.append(user_feeds.count())
#         # 用户订阅结果
#         feed_result_total_sum = 0
        feed_reco_sum = 0
        user_read_sum = 0
#         for user_feed in user_feeds:
# #             feed_result = FeedResult.objects(feed = user_feed.feed , calc_time__gte = look_date)
# #             feed_result_total_sum += feed_result.count()
# #             feed_reco_sum += feed_result.filter(is_recommended = True).count()
# #             user_read_sum += feed_result.filter(resume__in = user_feed.read_id_list).count()
#               user_read_sum += len(user_feed.read_id_list)
#

        access_list.append(feed_reco_sum)
        access_list.append(user_read_sum)
#         access_list.append(feed_result_total_sum)
        latest_access = StatisticsModel.objects(username=username).order_by('-access_time').limit(1)
        if latest_access:
            latest_access = latest_access[0]
            latest_access_time = latest_access.access_time
        else:
            latest_access_time = 0
        access_list.append(latest_access_time)

        statistic_res_list.append((username, company_name, access_list))
        i += 1

#     access_list = []
#     for statis_type, page_id in PINBOT_STATIS_LIST:
#         statistic_count = StatisticsModel.objects(page_id=page_id,
#                                                   access_time__gte=look_date).count()
#         access_list.append(statistic_count)
#     users_feeds = UserFeed.objects(is_deleted=False, add_time__gte=look_date)
#     access_list.append(users_feeds.count())
#
#
#     # 用户订阅结果
#     feed_result_total_sum = 0
#     feed_reco_sum = 0
#     user_read_sum = 0
#     feed_result = FeedResult.objects(calc_time__gte=look_date)
#     feed_result_total_sum += feed_result.count()
#     feed_reco_sum += feed_result.filter(is_recommended=True).count()
#
#     access_list.append(feed_reco_sum)
#     access_list.append(feed_reco_sum)
#     access_list.append(feed_result_total_sum)
#
#     access_list.append(datetime.now())
#     statistic_res_list.append(('total', "汇总", access_list, datetime.now()))
    from Pinbot.settings import STATIC_URL
    return render_to_response("statistic/vanilla.html", locals())


@login_required
def view_user_op(request):
    if not request.user.is_staff:
        return redirect("/")


    p = request.GET.copy()
    username = p.get('username')
    page = p.get('page', 0)
    page = int(page)
    if username == 'total':
        statis_data_list = StatisticsModel.objects.values_list("page_id", "username", \
                          "cost_time", "ip", "access_time").order_by("-access_time").skip(page * 500).limit(500)
    else:
        from django.contrib.auth.models import User
        user = User.objects.filter(username=username)[0]
        company_name = user.get_full_name()
        statis_data_list = StatisticsModel.objects(username=username).values_list("page_id", \
                            "search_keywords", "cost_time", "ip", "access_time").order_by("-access_time").skip(page * 200).limit(200)

        user_feeds = UserFeed.objects.filter(user=request.user).order_by('-add_time')

    from statistics.global_variables import PINBOT_STATIS_DICT

    access_record_list = []
    for idx, line in enumerate(statis_data_list):
        temp_line_list = []
        temp_line_list.append(PINBOT_STATIS_DICT.get(int(line[0]), line[0]))
        temp_line_list.extend(line[1:])
        access_record_list.append(temp_line_list)
    from Pinbot.settings import STATIC_URL
    return render_to_response("statistic/disp_user_access_list.html", locals())


@login_required
def view_user_feeds(request):
    if not request.user.is_staff:
        return redirect("/")

    p = request.GET.copy()

    days = p.get('days', 7)
    t_now = datetime.now()
    t_now = t_now.replace(hour=14, minute=0, second=0)
    look_date = t_now - timedelta(int(days))

    username = p.get('username')
    try:
        user = User.objects.get(username=username)
    except :
        user = User(username=username)

    user_feeds = UserFeed.objects.filter(user=request.user).order_by('-add_time')

    from Pinbot.settings import STATIC_URL

    current_url = "/statis/user_feeds?username=%s&" % (username)

    # 用户订阅结果
    user_feeds_list = []
    resume_update_time_deadline = get_datetime(-14 * 24)
    for user_feed in user_feeds:
        # 待审核的已推荐数量
        feed_id = ObjectId(user_feed.feed.feed_obj_id)
#         user_feed.feed = feed_id
        unpublished_count = FeedResult.objects(feed=feed_id, is_recommended=True, \
                                               resume_update_time__gte=resume_update_time_deadline, published=False).count()

        feed_result = FeedResult.objects(feed=feed_id, calc_time__gte=look_date)
        feed_result_total_sum = feed_result.count()
        manual_sheild_count = feed_result.filter(is_recommended=False, is_manual=True).count()

        feed_result = feed_result.filter(is_recommended=True, published=True)
        feed_reco_sum = feed_result.count()

        user_read_sum = 0  # feed_result.filter(resume__in=user_feed.read_id_list).count()
        manual_reco_count = feed_result.filter(is_manual=True).count()
        user_read_manual_count = 0  # feed_result.filter(is_manual=True, resume__in=user_feed.read_id_list).count()



        user_feeds_list.append((user_feed, user_read_manual_count, manual_reco_count, user_read_sum, \
                                 feed_reco_sum, manual_sheild_count, feed_result_total_sum, unpublished_count))

    return render_to_response("statistic/user_feeds.html", locals())


@login_required
def user_feed_result(request):
    """
    @summary: 推荐列表页
    #每日推荐数量,根据最近24小时推荐得到

    """
    from Pinbot.settings import STATIC_URL, USER_FEED_AMOUNT_LIMIT
#     username = request.user.username
    p = request.GET.copy()
    username = p.get('username')
    page_type = 'feed_list'
    # 当前页面样式
    feed_class = 'curr'
    user = get_object_or_404(User, username=username)

#     user_feeds = UserFeed.objects.filter(user__username=username, is_deleted=False).order_by('-add_time')
    from feed.models import UserFeed2
    user_feeds = UserFeed2.objects.filter(username = username,
                                            is_deleted = False
                                           ).order_by('-add_time')
    user_feeds_count = user_feeds.count()
    if user_feeds_count == 0:
        return redirect('/feed/new')

    unread_resumes_all_count = 0
    total_recommend_count = 0
    total_count = 0
    user_feed_list = []

    time_now = datetime.now()
    yestoday_deadline = get_datetime(hours=-8)
    tomommow = get_tomommow()
    today = get_today()

    for user_feed in user_feeds:
        feed_id = ObjectId(user_feed.feed.id)
        feed = user_feed.feed
        if not feed.display and feed.feed_type == 2:
            continue

        user_feed.feed.expire_status = True if user_feed.feed.feed_expire_time < tomommow else False
        user_feed.feed.has_expire = True if user_feed.feed.expire_time < today else False

        feed_results = FeedResult.objects.filter(feed=feed_id, is_recommended=True, \
#                                                  resume__nin=user_feed.read_id_list, \
                                                 calc_time__lte=yestoday_deadline,
                                                 published=True)

        # 距离现在最近的一天不为0的推荐
        i = 1
        latest_unread_reco_count = 0
        while latest_unread_reco_count == 0 and i < 10:
            latest_day = time_now - timedelta(days=i)
            latest_unread_recommend = feed_results.filter(manual_ensure_time__gte=latest_day)
#             latest_unread_recommend = latest_unread_recommend.limit(36)
            latest_unread_reco_count = latest_unread_recommend.count()
            i += 1

        user_feed_list.append((user_feed, latest_unread_reco_count))

    if not request.user.is_staff:
        if user_feeds_count > USER_FEED_AMOUNT_LIMIT:
            display_add_new = False
        else:
            display_add_new = True
    else:
        display_add_new = True

    oneday_feeds = add_read_rate(1, user_feeds)
    fiveday_feeds = add_read_rate(5, user_feeds)

    CeleryUtils.admin_feed_task(username)
    return render(
        request,
        'statistic/user_feed_result.html',
        locals()
    )


@login_required
def get_all_keywords(request):
    if not request.user.is_staff:
        return redirect("/")

    keywords_list = []
    resume_score_list = ResumeScore.objects.order_by("-calc_time")

    for resume_score in resume_score_list:
        keywords = resume_score.keywords
        keywords = jieba.cut(keywords)
        for keyword in keywords:
            if keyword not in keywords_list:
                keywords_list.append(keyword)
    keywords = ",".join(keywords_list)
    return render_to_response('statistic/disp_search_keywords.html', locals())

@csrf_exempt
@login_required
def feedback(request):

    username = request.user.username
    content = request.POST.get('content', '')
    user_feedback = UserFeedBack(username=username, feedback_conent=content)
    user_feedback.save()

    data = produce_return_json()
    return HttpResponse(data, 'application/json')


@login_required
def manual_reco_statis(request):
    p = request.GET.copy()
    start = p.get('start')
    end = p.get('end')

    days = p.get('days', 0)
    days = int(days)

    if start:
        start_time = datetime.strptime(start, '%Y-%m-%d')
    else:
        start_time = datetime.today()

    if end:
        end_time = datetime.strptime(end, '%Y-%m-%d')
    else:
        end_time = datetime.now()

    if days:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

    username_list = ManualPushResume.objects.distinct('username')


    statistic_res_list = []
    access_list = [0, 0, 0, 0]
    for username in username_list:
        total_count = ManualPushResume.objects.filter(Q(op_time__gte=start_time) & Q(op_time__lte=end_time), username=username).count()
        if 'hopperclouds.com' in username:
            username = u"浩泊云动-" + username
        if total_count:
            statistic_res_list.append((username, total_count, access_list))

    total_count = ManualPushResume.objects.filter(Q(op_time__gte=start_time) & Q(op_time__lte=end_time)).count()
    statistic_res_list.append(('total', total_count, access_list))

    from Pinbot.settings import STATIC_URL
    return render_to_response('statistic/manual_reco_statis.html', locals())


def taocv_daily_report(date_from,date_to,need_email=False):
    from feed.models import UserReadResume,Feed2
    statics_list = list()
    statics_list_total = list()

    staff_user_list = list()  # 获取员工账号列表 用于过滤
    customer_list = list()
    users = User.objects.filter()
    for user in users:
        if user.is_staff == 0 and user.is_active == 1:
            customer_list.append(user.username)
        elif user.is_staff == 1:
            staff_user_list.append(user.username)

    #获取所有淘简历的职位列表
    taocv_id_list = list()
    taocv_feeds = TaocvConfig.objects.filter(display=True).order_by('sequence')
    feed_clicks_total=0
    feed_resume_nums_total=0
    resume_clicks1_total=0
    resume_clicks2_total=0
    feed_user_nums_total=0
    down_user_nums_total=0
    resumes_down_nums_total=0
    improper_clicks_customer_total = 0
    improper_clicks_staff_total = 0
    resume_watch_total = 0
    buy_nums_total=0

    i = 0
    for feed in taocv_feeds:
        print i
        i += 1
        feed_id = feed.feed_id
        feed = Feed2.objects.get(id=ObjectId(feed_id))
        taocv_id_list.append(ObjectId(feed_id))
        access_url = "/feed/group/"+feed_id
        #职位点击数
        feed_clicks = len(StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to,
                                                         username__in=customer_list,access_url=access_url))
        feed_clicks_total += feed_clicks

        #该职位下推荐的简历数
        feed_resume_nums = FeedResult.objects.filter(feed=ObjectId(feed_id),published=True,pub_time__gte=date_from,pub_time__lte=date_to).count()
        feed_resume_nums_total +=  feed_resume_nums

        #该职位下简历被点击的次数
        resume_clicks1 = ManualPushResume.objects.filter(reco_index=40,op_time__gte=date_from,op_time__lte=date_to,feed=feed,username__in=customer_list).count()
        resume_clicks1_total += resume_clicks1
        resume_clicks2 = len(ManualPushResume.objects.filter(reco_index=40,op_time__gte=date_from,op_time__lte=date_to,feed=feed,username__in=customer_list).distinct('resume'))
        resume_clicks2_total += resume_clicks2  #简历点击数(去重)

        #该职位下有点击行为的用户数量
        feed_user_nums = len(ManualPushResume.objects.filter(reco_index=40,op_time__gte=date_from,op_time__lte=date_to,feed=feed,username__in=customer_list).distinct('username'))
        feed_user_nums_total += feed_user_nums

        #获取该订阅下的简历下载数量
        buy_nums = 0
        resumes_down_nums = ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from,op_time__lte=date_to,feed_id=str(feed.id)).count()
        buy_nums_total += resumes_down_nums
        down_user_nums = len(ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from,op_time__lte=date_to,feed_id=str(feed.id)).values('user').distinct())
        down_user_nums_total += down_user_nums
        resumes_down_nums_total += resumes_down_nums

        #不合适简历点击数
        improper_clicks_customer = ManualPushResume.objects.filter(feed=ObjectId(feed_id),op_time__gte=date_from, op_time__lte=date_to, reco_index__lte=-100, username__nin=staff_user_list).count()
        improper_clicks_staff = ManualPushResume.objects.filter(feed=ObjectId(feed_id),op_time__gte=date_from, op_time__lte=date_to, reco_index__lte=-100, username__in=staff_user_list).count()
        improper_clicks_customer_total += improper_clicks_customer
        improper_clicks_staff_total += improper_clicks_staff

        #简历关注数
        resume_watch = UserWatchResume.objects.filter(add_time__gte=date_from,add_time__lte=date_to,feed_id=str(feed.id)).count()
        resume_watch_total += resume_watch

        statics_list.append((feed.title,(feed_clicks,feed_resume_nums,resume_clicks1,resume_clicks2,feed_user_nums,buy_nums,resumes_down_nums,down_user_nums,improper_clicks_customer,improper_clicks_staff,resume_watch)))
    statics_list_total.append(("合计",(feed_clicks_total,feed_resume_nums_total,resume_clicks1_total,resume_clicks2_total,feed_user_nums_total,buy_nums_total,resumes_down_nums_total,down_user_nums_total,improper_clicks_customer_total,improper_clicks_staff_total,resume_watch_total)))
    return statics_list,statics_list_total,taocv_id_list

def daily_report(date_from, date_to, need_email=False):
    statics_list,statics_list_total,taocv_id_list = taocv_daily_report(date_from,date_to,need_email)

    staff_user_list = list()  # 获取员工账号列表 用于过滤
    customer_list = list()
    no_staff_user = list()
    users = User.objects.filter()
    for user in users:
        if user.is_staff == 0 and user.is_active == 1:
            customer_list.append(user.username)
        elif user.is_staff == 1:
            staff_user_list.append(user.username)

    # 获取前一天的注册用户数量
    signup_num = User.objects.filter(date_joined__gte=date_from, date_joined__lte=date_to, is_active=1, is_staff=0).count()
    # 获取访问的用户数量
    """
    当日0～24点访问过聘宝的用户数量
    """
    access_num = len(StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, username__in=customer_list).distinct('username'))
#     access_users = StatisticsModel.objects.filter(access_time__gte=date_from,access_time__lte=date_to)
#     access_num = len(access_users.distinct('username')) - staff_access_num

    # 统计日付费用户数
    packages_buy_num = UserChargePackage.objects.filter(start_time__gte=date_from, resume_end_time__lte=date_to, actual_cost__gte=1).count()

    # 统计活跃用户数
    """
    指标：当日创建订阅，或产生3封以上简历点击，或产生关注或购买行为的用户数量
    """
    active_users = get_active_users(date_from, date_to, staff_user_list)
    active_user_num = len(active_users)
    report_date = str(date_from.year) + "-" + str(date_from.month) + "-" + str(date_from.day)


    # 简历发布数
    advance_day_from, advance_day_to = day_get(date_to, 1)
    day_recommand = FeedResult.objects.filter(pub_time__gte=date_from, pub_time__lte=date_to,
                                                        published=True).count()
    day_recommand_feed = day_recommand - statics_list_total[0][1][1]
    # 统计简历点击数
#     day_clicks = StatisticsModel.objects.filter(access_time__gte=date_from,access_time__lte=date_to,page_id=40,username__in=customer_list).count()
    day_clicks = ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, username__in=customer_list, reco_index=40).count()
    if day_recommand == 0:
        day_clicks_rate = 0
    else:
        day_clicks_rate = float(day_clicks)/day_recommand * 100
    day_clicks_rate = str("%.2f" % day_clicks_rate) + "%"

    day_clicks_feed = day_clicks-statics_list_total[0][1][2]
    if day_recommand_feed == 0:
        day_clicks_rate_feed = 0
    else:
        day_clicks_rate_feed = float(day_clicks_feed)/day_recommand_feed * 100
    day_clicks_rate_feed = str("%.2f" % day_clicks_rate_feed) + "%"
    day_clicks_norepeat = len(ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, username__in=customer_list, reco_index=40).distinct('resume'))
    if day_recommand == 0:
        day_clicks_norepeat_rate = 0
    else:
        day_clicks_norepeat_rate = float(day_clicks_norepeat)/day_recommand * 100
    day_clicks_norepeat_rate = str("%.2f" % day_clicks_norepeat_rate) + "%"
    day_clicks_norepeat_feed = day_clicks_norepeat-statics_list_total[0][1][3]
    if day_recommand == 0:
        day_clicks_norepeat_rate_feed = 0
    else:
        day_clicks_norepeat_rate_feed = float(day_clicks_norepeat_feed)/day_recommand * 100
    day_clicks_norepeat_rate_feed = str("%.2f" % day_clicks_norepeat_rate_feed) + "%"
    improper_clicks = ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, reco_index__lte=-100, username__nin=staff_user_list).count()
    improper_clicks_feed = improper_clicks-statics_list_total[0][1][8]
    staff_improper_clicks = ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, reco_index__lte=-100, username__in=staff_user_list).count()
    staff_improper_clicks_feed = staff_improper_clicks-statics_list_total[0][1][9]
#     day_clicks = StatisticsModel.objects.filter(access_time__gte=date_from,access_time__lte=date_to,page_id=40).count()
#     day_clicks -= day_staf_clicks

    # 统计简历关注数
#     day_watch = StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, page_id=50, username__in=customer_list).count()
    day_watch = UserWatchResume.objects.filter(add_time__gte=date_from,add_time__lte=date_to).count()
    day_watch_feed = day_watch-statics_list_total[0][1][10]
    day_watch_norepeat = len(UserWatchResume.objects.filter(add_time__gte=date_from,add_time__lte=date_to).values("resume_id").distinct())
    day_watch_norepeat_feed = day_watch_norepeat-statics_list_total[0][1][10]
#     day_watch = StatisticsModel.objects.filter(access_time__gte=date_from,access_time__lte=date_to,page_id=50).count()
#     day_watch -= day_staf_watch

    day_pre_buy = ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to).count()
    day_pre_buy_feed = day_pre_buy-statics_list_total[0][1][5]
    day_pre_buy_norepeat = len(ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to).values("resume_id").distinct())
    day_pre_buy_norepeat_feed = day_pre_buy_norepeat-statics_list_total[0][1][6]
    day_buy = ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to, status='LookUp').count()
    day_buy_feed = day_buy-statics_list_total[0][1][5]
    day_buy_norepeat = len(ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to, status='LookUp').values("resume_id").distinct())
    day_buy_norepeat_feed = day_buy_norepeat-statics_list_total[0][1][6]
    if day_clicks > 0:
        resume_watch_rate = float(day_watch) / day_clicks * 100
        if day_clicks_feed > 0:
            resume_watch_rate_feed = float(day_watch_feed)/day_clicks_feed * 100
            resume_buy_rate_feed = float(day_buy_feed)/day_clicks_feed * 100
            resume_prebuy_rate_feed = float(day_pre_buy_feed) / day_clicks_feed * 100
        else:
            resume_watch_rate_feed = 0
            resume_buy_rate_feed = 0
            resume_prebuy_rate_feed = 0
        resume_buy_rate = float(day_buy) / day_clicks * 100

        resume_prebuy_rate = float(day_pre_buy) / day_clicks * 100

    else:
        resume_watch_rate_feed = 0
        resume_watch_rate = 0
        resume_wathc_rate_feed = 0
        resume_buy_rate = 0
        resume_buy_rate_feed = 0
        resume_prebuy_rate = 0
        resume_prebuy_rate_feed = 0

    resume_watch_rate = str("%.2f" % resume_watch_rate) + "%"
    resume_watch_rate_feed = str("%.2f" % resume_watch_rate_feed) + "%"
    resume_buy_rate = str("%.2f" % resume_buy_rate) + "%"
    resume_buy_rate_feed = str("%.2f" % resume_buy_rate_feed) + "%"
    resume_prebuy_rate = str("%.2f" % resume_prebuy_rate) + "%"
    resume_prebuy_rate_feed = str("%.2f" % resume_prebuy_rate_feed) + "%"

    from Pinbot.settings import STATIC_URL, DEFAULT_FROM_EMAIL, ALLOWED_USERS

    if need_email:
        subject, message = load_template('email-template/daily-report-subject.txt', 'email-template/daily-report.html', locals(), locals())
        result, info = send_email(subject, message, DEFAULT_FROM_EMAIL, tuple(ALLOWED_USERS))
        django_log.error('day_report '+str(info))
        return True
    else:
        return render_to_response('statistic/daily-report.html', locals())

def weekly_report(date_from, date_to, need_email=False):
    # 订阅推荐数据
    """
    指标：
    1.用户统计指标：
        注册数据－累计注册，周新增注册；
        访问数据－累计访问，周新增访问；
        活跃数据－周日活跃（全部客户中，如果某一天活跃，则在同时记为周日活跃），周新增日活跃（新增客户中的日活跃客户数）；周三日活跃，周新增三日活跃；
        交易数据－累计成交量&付费用户数&累计客均价值&累计客均付费时长，周新增成交量&付费用户数&周新增客均价值&周新增客均付费时长；
        流失数据－周准流失；周流失用户数。流失数据可以只看周新增。
        同时，对于注册/访问/活跃/流失，形成这一周内每一天数据的柱状图或曲线图
    2.订阅推荐数据指标
        简历推荐数：简历实际被推荐给用户的数量，被过滤掉的不算，推荐数可重复计算（例如一份简历当日被推荐给3名不同的用户，两位用户各推荐1次，一位用户推荐2次，则推荐数为4）
        简历展示数：简历推荐给一位用户时，如果被加载出来显示在页面上，则记为一次展示，未被加载出来则不算作展示
        简历点击数：如果简历被点击，进入到简历详情页，则记为一次点击
        简历关注数：如果用户点击“关注”按钮关注了简历，则记为一次关注
        简历购买总数：如果用户点击“购买”按钮，则记为一次购买
        简历实际购买数：如果用户点击“购买”按钮，且完成一次购买（用户获得了购买简历的完整信息），则记为一次实际购买

        比率数据如下：
        简历展示率＝简历点击数/简历展示数
        简历点击率＝简历点击数/简历展示数
        简历关注率＝简历关注数/简历点击数
        简历购买率＝简历购买总数/简历点击数
        简历实际购买数 ＝ 简历实际购买数/简历点击数

        根据上述指标，形成：
        订阅推荐数据周报（累计）：基于近一周及以前所有简历的推荐、展示、点击、关注、购买数据
        订阅推荐数据周报（一周）：基于近一周的简历推荐、展示、点击、关注、购买数据
        周报显示以下指标－简历推荐数，简历展示数，简历展示率，简历点击数，简历点击率，简历关注数，简历关注率，简历购买数，简历购买率
    """
    statics_list,statics_list_total,taocv_id_list = taocv_daily_report(date_from,date_to,need_email)

    staff_user_list = list()  # 获取员工账号列表 用于过滤
    customer_list = list()
    no_staff_user = list()
    users = User.objects.filter()
    for user in users:
        if user.is_staff == 0 and user.is_active == 1:
            customer_list.append(user.username)
        elif user.is_staff == 1:
            staff_user_list.append(user.username)

    # 用户统计指标
    active_day_list = list()  # 活跃日列表
    active_user_num = 0
    new_user_active_num = 0  # 周新增日活跃（新增客户中的日活跃客户数）
    user_3day_active_num = 0  # 周三日活跃
    new_user_3day_active_num = 0  # 周新增三日活跃


    date_from_2week, date_to_2week = week_get(date_to, 2)
#     date_to = datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)

    start_date = str(date_from.year) + "-" + str(date_from.month) + "-" + str(date_from.day)
    end_date = str(date_to.year) + "-" + str(date_to.month) + "-" + str(date_to.day)
#
    user_week_list = list()
    username_week_list = list()
    user_total_num = User.objects.filter(is_active=1, is_staff=0).count()  # 总共注册并激活用户数
    users_week = User.objects.filter(date_joined__gte=date_from, date_joined__lte=date_to, is_active=1, is_staff=0)
    user_week_num = len(users_week)  # 上周注册并激活用户数
    for user in users_week:
        user_week_list.append(user)
        username_week_list.append(user.username)

    access_total_num = len(StatisticsModel.objects.filter(access_time__lte=date_to, username__in=customer_list).distinct('username'))  # 累计访问(按照用户统计)
    access_week = StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, username__in=customer_list).distinct('username')  # 周新增访问(按照用户统计)
    access_week_num = len(access_week)
    day_info = list()
    user_active_num_week = 0  # 新增客户中的日活跃客户数
    user_active_dict = {}  # 活跃用户字典,用于统计用户活跃天数
    day_acitve_list = list()  # 便于统计每天有多少活跃用户
    active_user_num = len(get_active_users(date_from, date_to, staff_user_list))
    signup_list = list()
    access_list = list()
    active_list = list()
    for i in range(0, 7):
        iday = timedelta(days=6 - i)
        day = date_to - iday
        date_from_temp = datetime(day.year, day.month, day.day, 0, 0, 0)
        date_to_temp = datetime(day.year, day.month, day.day, 23, 59, 59)

        active_users = list()
        active_users = get_active_users(date_from_temp, date_to_temp, staff_user_list)
        day_info = list()

        signup_list.append(len(User.objects.filter(date_joined__gte=date_from_temp, date_joined__lte=date_to_temp, is_active=1, is_staff=0)))
        access_list.append(len(StatisticsModel.objects.filter(access_time__gte=date_from_temp, access_time__lte=date_to_temp, username__in=customer_list).distinct('username')))
        active_list.append(len(active_users))


        if len(active_users) > 0:
            active_day_list.append(7 - i)
        for user in active_users:
            if user in user_active_dict:
                user_active_dict[user] += 1
            else:
                user_active_dict[user] = 1

    day_list = ''
    for day in  active_day_list:
        day_list += ',' + str(day)

    for username, num in user_active_dict.items():
        if username in username_week_list:
            new_user_active_num += 1
            if num >= 3:
                new_user_3day_active_num += 1
        else:
            if num >= 3:
                user_3day_active_num += 1


    """
    累计成交量&付费用户数&累计客均价值&累计客均付费时长，周新增成交量&付费用户数&周新增客均价值&周新增客均付费时长；
    """
    total_pay = 0  # 累计成交量
    total_user_num = 0  # 付费用户数
    total_ave_value = 0  # 累计客均价值
    total_ave_paytime = 0  # 累计客均付费时长

    week_pay = 0  # 周新增成交量
    week_user_num = 0  # 付费用户数
    week_ave_value = 0  # 周新增客均价值
    week_ave_paytime = 0  # 周新增客均付费时长

    pre_loss_num = 0  # 周准流失
    loss_num = 0  # 周流失用户数

    ucps = UserChargePackage.objects.filter(actual_cost__gte=1)
    now = datetime.now()
    total_pay_last = now - now
    for ucp in ucps:
        try:
            total_pay_last += ucp.start_time - ucp.user.date_joined
            total_pay += ucp.actual_cost
            total_user_num += 1
        except:
            pass
    total_ave_value = total_pay / user_total_num
    total_ave_value = "%.2f" % total_ave_value
    total_ave_paytime = total_pay_last / total_user_num
    total_ave_paytime = str(total_ave_paytime.days) + "天" + str(total_ave_paytime.seconds / 3600) + "小时"

    ucps = UserChargePackage.objects.filter(start_time__gte=date_from, start_time__lte=date_to, actual_cost__gte=1)
    week_pay_last = now - now
    for ucp in ucps:
        week_pay_last += ucp.start_time - ucp.user.date_joined
        week_pay += ucp.actual_cost
        week_user_num += 1
    week_ave_value = week_pay / user_week_num
    week_ave_value = "%.2f" % week_ave_value
    week_ave_paytime = total_pay_last / user_week_num
    week_ave_paytime = str(week_ave_paytime.days) + "天" + str(week_ave_paytime.seconds / 3600) + "小时"

    pre_loss_num = user_total_num - len(StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, username__in=customer_list).distinct('username'))
    loss_num = user_total_num - len(StatisticsModel.objects.filter(access_time__gte=date_from_2week, access_time__lte=date_to, username__in=customer_list).distinct('username'))

    week_recommand = FeedResult.objects.filter(calc_time__gte=date_from, calc_time__lte=date_to,
                                                        is_recommended=True, published=True).count()
    week_recommand_feed = week_recommand - statics_list_total[0][1][1]
    # 统计简历点击数
#     day_clicks = StatisticsModel.objects.filter(access_time__gte=date_from,access_time__lte=date_to,page_id=40,username__in=customer_list).count()
    week_clicks = ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, username__in=customer_list, reco_index=40).count()
    if week_recommand == 0:
        week_clicks_rate = 0
    else:
        week_clicks_rate = float(week_clicks)/week_recommand * 100
    week_clicks_rate = str("%.2f" % week_clicks_rate) + "%"
    week_clicks_feed = week_clicks-statics_list_total[0][1][2]
    if week_recommand_feed == 0:
        week_clicks_rate_feed = 0
    else:
        week_clicks_rate_feed = float(week_clicks_feed)/week_recommand_feed * 100
    week_clicks_rate_feed = str("%.2f" % week_clicks_rate_feed) + "%"
    week_clicks_norepeat = len(ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, username__in=customer_list, reco_index=40).distinct('resume'))
    if week_recommand == 0:
        week_clicks_norepeat_rate = 0
    else:
        week_clicks_norepeat_rate = float(week_clicks_norepeat)/week_recommand * 100
    week_clicks_norepeat_rate = str("%.2f" % week_clicks_norepeat_rate) + "%"
    week_clicks_norepeat_feed = week_clicks_norepeat-statics_list_total[0][1][3]
    if week_recommand == 0:
        week_clicks_norepeat_rate_feed = 0
    else:
        week_clicks_norepeat_rate_feed = float(week_clicks_norepeat_feed)/week_recommand * 100
    week_clicks_norepeat_rate_feed = str("%.2f" % week_clicks_norepeat_rate_feed) + "%"
    improper_clicks = ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, reco_index__lte=-100, username__nin=staff_user_list).count()
    improper_clicks_feed = improper_clicks-statics_list_total[0][1][8]
    staff_improper_clicks = ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, reco_index__lte=-100, username__in=staff_user_list).count()
    staff_improper_clicks_feed = staff_improper_clicks-statics_list_total[0][1][9]
#     day_clicks = StatisticsModel.objects.filter(access_time__gte=date_from,access_time__lte=date_to,page_id=40).count()
#     day_clicks -= day_staf_clicks

    # 统计简历关注数
#     day_watch = StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, page_id=50, username__in=customer_list).count()
    week_watch = UserWatchResume.objects.filter(add_time__gte=date_from,add_time__lte=date_to).count()
    week_watch_feed = week_watch-statics_list_total[0][1][10]
    week_watch_norepeat = UserWatchResume.objects.filter(add_time__gte=date_from,add_time__lte=date_to).values("resume_id").distinct().count()
    week_watch_norepeat_feed = week_watch_norepeat-statics_list_total[0][1][10]
#     week_watch = StatisticsModel.objects.filter(access_time__gte=date_from,access_time__lte=date_to,page_id=50).count()
#     week_watch -= week_staf_watch

    week_pre_buy = ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to).count()
    week_pre_buy_feed = week_pre_buy-statics_list_total[0][1][5]
    week_pre_buy_norepeat = ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to).values("resume_id").distinct().count()
    week_pre_buy_norepeat_feed = week_pre_buy_norepeat-statics_list_total[0][1][6]
    week_buy = ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to, status='LookUp').count()
    week_buy_feed = week_buy-statics_list_total[0][1][5]
    week_buy_norepeat = ResumeBuyRecord.objects.filter(user__is_staff=0,op_time__gte=date_from, op_time__lte=date_to, status='LookUp').values("resume_id").distinct().count()
    week_buy_norepeat_feed = week_buy_norepeat-statics_list_total[0][1][6]
    if week_clicks > 0:
        resume_watch_rate = float(week_watch) / week_clicks * 100
        if week_clicks_feed > 0:
            resume_watch_rate_feed = float(week_watch_feed)/week_clicks_feed * 100
            resume_buy_rate_feed = float(week_buy_feed)/week_clicks_feed * 100
            resume_prebuy_rate_feed = float(week_pre_buy_feed) / week_clicks_feed * 100
        else:
            resume_watch_rate_feed = 0
            resume_buy_rate_feed = 0
            resume_prebuy_rate_feed = 0
        resume_buy_rate = float(week_buy) / week_clicks * 100

        resume_prebuy_rate = float(week_pre_buy) / week_clicks * 100

    else:
        resume_watch_rate = 0
        resume_watch_rate_feed = 0
        resume_buy_rate = 0
        resume_buy_rate_feed = 0
        resume_prebuy_rate = 0
        resume_prebuy_rate_feed = 0

    resume_watch_rate = str("%.2f" % resume_watch_rate) + "%"
    resume_watch_rate_feed = str("%.2f" % resume_watch_rate_feed) + "%"
    resume_buy_rate = str("%.2f" % resume_buy_rate) + "%"
    resume_buy_rate_feed = str("%.2f" % resume_buy_rate_feed) + "%"
    resume_prebuy_rate = str("%.2f" % resume_prebuy_rate) + "%"
    resume_prebuy_rate_feed = str("%.2f" % resume_prebuy_rate_feed) + "%"


    from Pinbot.settings import STATIC_URL, DEFAULT_FROM_EMAIL, ALLOWED_USERS

    if need_email:
        subject, message = load_template('email-template/weekly-report-subject.txt', 'email-template/weekly-report.html', locals(), locals())
        send_email(subject, message, DEFAULT_FROM_EMAIL, ALLOWED_USERS)
        return True
    else:
        return render_to_response('statistic/weekly-report.html', locals())

def get_active_users(date_from, date_to, staff_user_list):
    active_users = set()
    user_access_dict = {}
    user_feeds = UserFeed2.objects.filter(add_time__gte=date_from, add_time__lte=date_to).distinct('username')
    access_users = StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to)
    for username in user_feeds:
        if username in staff_user_list or username == '':
            continue;
        active_users.add(username)

    for access in access_users:
        if access.username in staff_user_list or access.username == '':
            continue;
        if access.username in user_access_dict:
            if access.page_id == 40:
                user_access_dict[access.username] += 1
            if access.page_id == 50:
                user_access_dict[access.username] += 3
        else:
            if access.page_id == 40:
                user_access_dict[access.username] = 1
            if access.page_id == 50:
                user_access_dict[access.username] = 3

    for username, num in user_access_dict.items():
        if num >= 3:
            active_users.add(username)

    resumes_buy = ResumeBuyRecord.objects.filter(op_time__gte=date_from, op_time__lte=date_to)
    for resume_buy in resumes_buy:
        if resume_buy.user.username in staff_user_list:
            continue;
        active_users.add(resume_buy.user.username)

    return active_users


def get_click_detail1(request):
    pass

def get_recommand_detail(request):
    user_list = list()
    feed_recommand_dict = {}

    date_from = datetime(2014, 2, 27, 0, 0, 0)
    date_to = datetime(2014, 3, 5, 23, 59, 59)

    publish_date_from = datetime(2014, 2, 26, 16, 0, 0)
    publish_date_to = datetime(2014, 3, 4, 14, 0, 0)

    days = (date_to - date_from).days
    users = User.objects.filter(is_active=1, is_staff=0)

    for user in users:
        user_list.append(user.username)
    num = 0

    user_feeds = UserFeed.objects.filter(username__in=user_list)

    for user_feed in user_feeds:
        num += 1
        date_list = list()
        total_recommands = FeedResult.objects.filter(feed=user_feed.feed, calc_time__gte=publish_date_from, calc_time__lte=publish_date_to, published=True).count()
        total_clicks = len(ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, feed=user_feed.feed, reco_index=40).distinct('resume'))
        feed_recommand_dict[str(user_feed.feed.id)] = (total_recommands, total_clicks)

    return render_to_response('statistic/week-recommand-clicks.html', locals())

def recomman_detail(request):
    """
    统计指标
    1.客户针对当前订阅的简历不合适点击数量:customer_improper_clicks
    2.员工针对当前订阅的简历不合适点击数量:staff_improper_clicks
    3.针对当前订阅的简历发布数量:publish_num
    4.针对当前订阅的简历未发布数量:unpublish_num
    5.针对当前订阅的机器推荐简历数量:machine_recommand_num
    6.针对当前订阅的人工补充简历数量:manual_recommand_num
    7.针对当前订阅的机器推荐并发布的简历数量:manchine_publish_num
    8.针对当前订阅的机器推荐但并未发布的简历数量:manchine_unpublish_num
    9.针对当前订阅的人工补充并发布的简历数量:manual_publish_num
    """

    user_list = list()
    date_list = list()
    feed_recommand_dict = {}

    date_from = datetime(2014, 2, 26, 0, 0, 0)
    date_to = datetime(2014, 3, 5, 23, 59, 59)
    days = (date_to - date_from).days
    users = User.objects.filter(is_active=1, is_staff=0)

    for user in users:
        user_list.append(user.username)
    num = 0

    user_feeds = UserFeed.objects.filter(username__in=user_list)
    for user_feed in user_feeds:
        recommand_dict = {}
        recommand_list = list()
        if(user_feed.feed.id != ObjectId('530ea26fb1c33751f5222c03')):
            continue
        for i in range(0, days):
            date_from_temp, date_to_temp = feed_day_get(date_to, days - 1 - i)
            daytime = str(date_to_temp.month) + "-" + str(date_to_temp.day)
            date_list.append(daytime)

            calc_feed_results = FeedResult.objects.filter(feed=user_feed.feed, calc_time__gte=date_from_temp, calc_time__lte=date_to_temp)
            improper_clicks = calc_feed_results.filter(reco_index__lte=-100).count()

            feed_recommands = calc_feed_results.filter(is_recommended=True)

            publish_num = feed_recommands.filter(published=True).count()
            unpublish_num = feed_recommands.filter(published=False).count()
            machine_recommand_num = feed_recommands.filter(is_manual=False).count()
            manual_recommand_num = feed_recommands.filter(is_manual=True).count()
            manchine_publish_num = feed_recommands.filter(is_manual=False, published=True).count()
            manchine_unpublish_num = machine_recommand_num - manchine_publish_num
            manual_publish_num = feed_recommands.filter(published=False, is_manual=True).count()


            recommand_dict['improper_clicks'] = improper_clicks
            recommand_dict['publish_num'] = publish_num
            recommand_dict['unpublish_num'] = unpublish_num
            recommand_dict['machine_recommand_num'] = machine_recommand_num
            recommand_dict['manual_recommand_num'] = manual_recommand_num
            recommand_dict['manchine_publish_num'] = manchine_publish_num
            recommand_dict['manchine_unpublish_num'] = manchine_unpublish_num
            recommand_dict['manual_publish_num'] = manual_publish_num
            recommand_list.append(recommand_dict)

        feed_recommand_dict[user_feed.feed.id] = recommand_list
    from Pinbot.settings import STATIC_URL
    return render_to_response('statistic/week-resume-clicks.html', locals())

# @login_required
def statistic_report(request):
    # 获取当前星期并确定是发日报还是周报
    import json

    p = request.GET.copy()
    flag = p.get('days', 1)
    token = p.get('token', '')
    last_day = p.get('lastday', "")
    need_email = p.get('sendEmail', "")
    auto_report = p.get('autoReport', "")  # 是否自动判断发日报还是周报

    auto_report = True if auto_report == 'True' else False
    need_email = True if need_email == 'True' else False

    from Pinbot.settings import PINBOT_ADMIN
    if token not in PINBOT_ADMIN:
        data = {"status":'failed', 'message':'token in valid'}
        return HttpResponse(json.dumps(data), 'application/json')

    if auto_report:
        now_day = datetime.now()
        week_day = now_day.isoweekday()
        if week_day == 1:
            date_from, date_to = week_get(datetime.now(), 1)
            weekly_report(date_from, date_to, need_email=need_email)
        else:
            date_from, date_to = day_get(datetime.now(), 1)
            daily_report(date_from, date_to, need_email=need_email)
    else:
        arr = last_day.split('-')
        if len(arr) != 3:
            data = {"status":'failed', 'msg':'invalidDate, you should input such as :2014-2-23!'}
            return HttpResponse(json.dumps(data), 'application/json')
        else:
            year = arr[0]
            month = arr[1]
            day = arr[2]

            last_date = datetime(int(year), int(month), int(day), 23, 59, 59)
            week_day = last_date.isoweekday()
            if flag == '1':
                if last_day == "":
                    report_day = datetime.now()
                else:
                    report_day = last_date
                date_from, date_to = day_get(report_day, 0)
                return daily_report(date_from, date_to, need_email=False)
            elif flag == '7' and week_day == 1:
                date_from, date_to = week_get(last_date, 1)
                return weekly_report(date_from, date_to, need_email=False)
            else:
                data = {"status":'failed', 'msg':'valid input!'}
                return HttpResponse(json.dumps(data), 'application/json')

def key_customer_daily_report(date_from, date_to, need_email):
    import json
    from email_send.models import LogEmailAccess
    from feed.models import LogFeedQuery
    report_date = str(date_from.year) + "-" + str(date_from.month) + "-" + str(date_from.day)
    key_customer_dict = {}
    key_customer_dict['liuli703@homoj.com'] = "北京浩摩创娱科技有限公司"
    key_customer_dict['efun-zp@efun.com'] = "广州易幻网络科技有限公司"
    key_customer_dict['zhaowenting@youxigongchang.com'] = "成都游戏工场科技有限公司"
    key_customer_dict['xiangshasha@youxigongchang.com'] = "成都游戏工场科技有限公司"
    key_customer_dict['zongchen@joyucn.com'] = "上海聚游网络信息技术有限公司"
    key_customer_dict['luog@gsoftcn.com'] = "上海朗时信息技术有限公司"
    key_customer_dict['yuejf@cnsuning.com'] = "苏宁云商集团股份有限公司"
    key_customer_dict['327475626@qq.com'] = "EA"
    key_customer_dict['lenkenghr@126.com'] = "深圳市朗强科技有限公司"
    key_customer_dict['443425698@qq.com'] = "易玩科技"
    key_customer_dict['dongmingmei@gamewave.net'] = "趣游时代"
    # 第二批十名客户
    key_customer_dict['job@apowo.com'] = "上海爱扑网络科技有限公司"
    key_customer_dict['hrzp@duoyi.com'] = "广州多益网络科技有限公司"
    key_customer_dict['hhj@83.app.com'] = "广州恒霆信息科技有限公司"
    key_customer_dict['jing.xie@huoji.com'] = "火极网络科技有限公司"
    key_customer_dict['hr@online-game.com.cn'] = "游龙在线（北京）科技有限公司"
    key_customer_dict['yewang@hifun.cc'] = "杭州嗨翻科技有限公司"
    key_customer_dict['bjzhangxinyu@4399.net'] = "4399北京"
    key_customer_dict['2824734279@qq.com'] = "Mokitech"
    key_customer_dict['hr@armorblade.com'] = "zly"
    key_customer_dict['mlfgame@163.com'] = "梦立方-mlf"

    report_list = []
    unuser_customer = []

    for email, company in key_customer_dict.items():
        info_list = []

        access = False  # 是否访问系统
        start_time = ''  # 开始访问时间
        end_time = ''  # 结束访问时间
        source = '网站'  # 用户进站入口
        total_feeds = 0  # 订阅数
        feeds_clicks = 0  # 订阅点击数
        resume_recommands = 0  # 简历推荐数
        resume_displays = 0  # 被推荐的简历中有多少被用户看到
        resume_displays_recommand = 0  # 前一天推荐的简历中显示了多少个

        resume_clicks_total = 0  # 用户总共的简历点击数
        resume_clicks_recommand = 0  # 被推荐的简历点击数
        resume_clicks_feed = 0  # 用户经过订阅点击的简历数量
        resume_watches = 0  # 关注数
        resume_buys = 0  # 简历购买数
        resume_imp_nums = 0  # 用户不合适点击数
        comments_nums = 0  # 备注数

        feed_date_from, feed_date_to = feed_day_get(date_to, 1)

        use_accesses_end = StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, username=email).order_by("-access_time").limit(1)
        use_accesses_start = StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, username=email).order_by("access_time").limit(1)
        feed_email_access = LogEmailAccess.objects.filter(access_time__gte=date_from, access_time__lte=date_to, username=email).count()
        if use_accesses_end:
            access = True
            end_time = use_accesses_end[0].access_time
            start_time = use_accesses_start[0].access_time
            end_time = end_time.strftime("%Y-%m-%d %H:%M")
            start_time = start_time.strftime("%Y-%m-%d %H:%M")
        if access:
            if feed_email_access > 0:
                source = '邮件'
            user_feeds = UserFeed.objects.filter(username=email, is_deleted=False)
            total_feeds = user_feeds.count()
            user_feedid_list = []
            for user_feed in user_feeds:
                user_feedid_list.append(user_feed.feed)

            resume_recommands_list = list()
            resumeid_recommands_list = list()
            resume_recommands = FeedResult.objects.filter(feed__in=user_feedid_list, calc_time__gte=feed_date_from, calc_time__lte=feed_date_to, published=True)
            for resume_recommand in resume_recommands:
                resume_recommands_list.append(str(resume_recommand.resume.id))
                resumeid_recommands_list.append(resume_recommand.resume.id)
            resume_recommands = len(resume_recommands_list)
            resume_recommands_set = set(resume_recommands_list)

            query_results_set = set()
            query_results_list = []
            feed_querys = LogFeedQuery.objects.filter(username=email, access_time__gte=date_from, access_time__lte=date_to)
            for feed_query in feed_querys:
                resume_list = feed_query.resume_list
                query_results_list.extend(resume_list)
            query_results_set = set(query_results_list)
            resume_displays = len(query_results_set)
            resume_displays_recommand = len(resume_recommands_set & query_results_set)

            feeds_clicks = len(LogFeedQuery.objects.filter(username=email, access_time__gte=date_from, access_time__lte=date_to).distinct("feed_id"))

            resume_clicks_total = len(ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, feed__in=user_feedid_list, reco_index=40).distinct('resume'))
            resume_clicks_recommand = len(ManualPushResume.objects.filter(resume__in=resumeid_recommands_list, op_time__gte=date_from, op_time__lte=date_to, feed__in=user_feedid_list, reco_index=40).distinct('resume'))

            resume_watches = StatisticsModel.objects.filter(access_time__gte=date_from, access_time__lte=date_to, page_id=50, username=email).count()

            resume_buys = ResumeBuyRecord.objects.filter(op_time__gte=date_from, op_time__lte=date_to, user__username=email).count()

            resume_imp_nums = ManualPushResume.objects.filter(op_time__gte=date_from, op_time__lte=date_to, reco_index__lte=-100, username=email).count()

            comments_nums = Comment.objects.filter(username=email, comment_time__gte=date_from, comment_time__lte=date_to).count()

            info_list.append(start_time)
            info_list.append(end_time)
            info_list.append(source)
            info_list.append(total_feeds)
            info_list.append(feeds_clicks)
            info_list.append(resume_recommands)
            info_list.append(resume_displays_recommand)


            info_list.append(resume_displays)
            info_list.append(resume_clicks_recommand)
            info_list.append(resume_clicks_total)
            info_list.append(resume_watches)
            info_list.append(resume_buys)
            info_list.append(resume_imp_nums)
            info_list.append(comments_nums)

            report_list.append((email, company, info_list))
        else:
            unuser_customer.append(company)


    from Pinbot.settings import STATIC_URL, DEFAULT_FROM_EMAIL, ALLOWED_USERS

    if need_email:
        subject, message = load_template('email-template/key-customer-daily-report-subject.txt', 'statistic/key-customer-report.html', locals(), locals())
        send_email(subject, message, DEFAULT_FROM_EMAIL, ALLOWED_USERS)
        data = {"status":'success'}
        return HttpResponse(json.dumps(data), 'application/json')
    else:
        return render_to_response('statistic/key-customer-report.html', locals())


def load_template(subject_file,message_file,subject_dict=None,message_dict=None):
    subject = render_to_string(subject_file,subject_dict)
    message = render_to_string(message_file,message_dict)
    subject = ''.join(subject.splitlines())
    return subject,message

def day_get(input_day, days=0):
    """
    获取指定某一天的开始和结束时间
    """
    days = timedelta(days=days)
    day = input_day - days
    date_from = datetime(day.year, day.month, day.day, 0, 0, 0)
    date_to = datetime(day.year, day.month, day.day, 23, 59, 59)
    return date_from, date_to

def feed_day_get(input_day, days=0):
    """
    获取指定某一天的开始和结束时间
    """
    days = timedelta(days=days)
    day = input_day - days
    advance_date_from, advance_date_to = day_get(day, 1)
    date_from = datetime(advance_date_from.year, advance_date_from.month, advance_date_from.day, 14, 0, 0)
    date_to = datetime(day.year, day.month, day.day, 16, 0, 0)
    return date_from, date_to

def week_get(last_week_day, weeks=1):
    """
    获取指定某一或者几周的开始和结束时间
    """
    dayscount = timedelta(days=last_week_day.isoweekday())
    dayto = last_week_day - dayscount
    weekdays = timedelta(days=6 + 7 * (weeks - 1))
    dayfrom = dayto - weekdays
    date_from = datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    date_to = datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    return date_from, date_to

def month_get(last_day, months=1):
    """
    获取指定某一个或者几个月开始和结束时间
    """
    dayscount = timedelta(days=last_day.day)
    dayto = last_day - dayscount
    date_from = datetime(dayto.year, dayto.month, 1, 0, 0, 0)
    date_to = datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    return date_from, date_to

if __name__ == '__main__':
    latest_access_username = get_latest_access_username(days=0)
    i = 1
    for  username in  latest_access_username:
        try:
            user = User.objects.get(username=username)
            i += 1
        except Exception, e:
            pass
#     oneday = timedelta(days=1)
#     day = datetime.now() - oneday
#     date_from = datetime(day.year, day.month, day.day, 0, 0, 0)
#     date_to = datetime(day.year, day.month, day.day, 23, 59, 59)

#     feed_id = "52ae6a2bb1c3373e8bd85252"
#     feed_results = FeedResult.objects.filter(feed=ObjectId(feed_id)).order_by("-calc_time")
    pass
