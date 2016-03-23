# coding:utf-8

from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth.decorators import login_required
from django.db import transaction

from transaction.models import *
from models import *
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response, redirect
from statistics.access_counter import page_access_counter_dec
from statistics.global_variables import *
from pinbot_permission.pinbot_decorator import group_required
from Pinbot.settings import LOGIN_URL

from transaction.mark_utils import (
    MarkUtils,
)

from pin_utils.django_utils import (
    JsonResponse,
)


django_log = logging.getLogger('django')


@login_required(login_url=LOGIN_URL)
def taocv_nopermission(request):
    from Pinbot.settings import STATIC_URL
    user = request.user
    auth_fail = True
    tao_class = 'curr'
    areas = TaocvConfig.objects.filter(display=True).values('area').distinct()
    area_str = ''
    for area in areas:
        if area_str == '':
            area_str = area['area']
        else:
            area_str += ','+area['area']
    return render_to_response('tao-resume.html', locals())

def get_points(user):
    """
    获取用户的积分数
    """
    total_points = 0
    user_feedbacks = UserResumeFeedback.objects.order_by('-create_time').filter(user=user, check_status='success')
    for user_feedback in user_feedbacks:
        total_points += user_feedback.feedback_info.type.re_points

    user_point = None
    user_points = UserFeedbackPoints.objects.filter(user=user)
    if len(user_points) >= 1:
        user_point = user_points[0]
        total_points -= user_points[0].used_points
        total_points += user_points[0].reward_points
    else:
        total_points += 20
        user_point = UserFeedbackPoints(user=user, total_points=20, used_points=0)
        group_name = None
        if user.groups.all():
            group_name = user.groups.all()[0].name
        if (group_name is not None) and (group_name == 'taocv' or group_name == 'tmp-taocv'):
            user_point.save()
    return total_points, user_point

def get_notify(user):
    """
    获取用户获取的反馈点数奖励通知，如果积分用完则发送积分为0的提醒通知
    """
    user_feedbacks = UserResumeFeedback.objects.order_by('create_time').filter(user=user, check_status='success', notify_status=False)[:1]
    has_notify = False
    re_points = 0
    resume_id = ''
    if len(user_feedbacks) >= 1:
        re_points = user_feedbacks[0].feedback_info.type.re_points
        resume_id = user_feedbacks[0].resume_id
        has_notify = True
    if has_notify is False:
        total_points, user_point = get_points(user)
        if total_points == 0:
            if user_point is not None and user_point.zero_points_notify_status == 'need_notify':
                resume_id = 'zero_points'  # 积分为0的通知
    return has_notify, re_points, resume_id

def get_feedback(resume_id):
    feed_back_dict = {}
    feedbacks = UserResumeFeedback.objects.order_by('-create_time').filter(resume_id=resume_id)

    for feedback in feedbacks:
        feedback_value = feedback.feedback_value
        feedback_desc = feedback.feedback_info.feedback_desc
        type_desc = feedback.feedback_info.type.desc
        feedback_str = feedback_desc.replace('_', feedback_value)
        if feedback_desc == '其他':
            feedback_str = feedback_value
        if type_desc in feed_back_dict:
            feed_back_dict[type_desc].append(feedback_str)
        else:
            feed_back_list = list()
            feed_back_list.append(feedback_str)
            feed_back_dict[type_desc] = feed_back_list

    return feed_back_dict

def get_feedback_str(user, resume_id):
    """
    通过获取用户对某个简历的反馈并组装成字符串返回，如果没有反馈则返回None
    """
    user_feedbacks = UserResumeFeedback.objects.order_by('-create_time').filter(user=user, resume_id=resume_id)
    if len(user_feedbacks) >= 1:
        user_feedback = user_feedbacks[0]
        feedback_value = user_feedback.feedback_value
        feedback_desc = user_feedback.feedback_info.feedback_desc
        type_desc = user_feedback.feedback_info.type.desc
        feedback_str = feedback_desc.replace('_', feedback_value)
        if feedback_desc == '其他':
            feedback_str = feedback_value
        check_status = user_feedback.check_status
        if check_status == 'checking':
            feedback_str = '反馈正在验证中...'
        elif check_status == 'failed':
            feedback_str = '反馈审核未通过...'
        return check_status, type_desc, feedback_str
    else:
        return None, None, None

@csrf_exempt
@login_required
def add_feedback_ajax(request):
    """
    @summary: 添加用户反馈
    """
    data = request.POST.copy()
    feedback_id = data.get('feedback_id', None)
    feedback_value = data.get('feedback_value', None)
    resume_id = data.get('resume_id', None)
    user = request.user

    has_accu = UserResumeFeedback.objects.filter(
        user=request.user,
        resume_id=resume_id,
    )
    if has_accu:
        return JsonResponse({
            'status': 'failed',
            'msg': u'已举报过，请不要重复举报',
        })

    if MarkUtils.has_mark_record(user, resume_id):
        return JsonResponse({
            'status': 'failed',
            'msg': u'该简历处于标记状态，不能举报',
        })

    if feedback_id is not None and resume_id is not None :
        feedback_id = int(feedback_id)
        feedback_info = FeedBackInfo.objects.get(feedback_id=feedback_id)
        user_feedback = UserResumeFeedback(user=request.user, resume_id=resume_id, feedback_info=feedback_info, feedback_value=feedback_value)

        if feedback_info.type.desc == '简历反馈':
            user_feedback.check_status = 'pass'

        accu_type = 'feed_back' if feedback_info.type.desc == '简历反馈' else 'accusation'
        with transaction.atomic():
            user_feedback.save()
            MarkUtils.add_accu_mark(user, resume_id, accu_type)
        return HttpResponse(json.dumps({"status": "success"}), 'application/json')
    else:
        return HttpResponse(json.dumps({"status": "failed", "msg":"empty"}), 'application/json')

@csrf_exempt
@login_required
def notify_read_ajax(request, resume_id):
    """
    用户已读通知
    """
    try:
        if resume_id is not None:
            if resume_id == 'zero_points':
                # 处理积分为0的通知消息
                total_points, user_point = get_points(request.user)
                user_point.zero_points_notify_status = 'read'
                user_point.save()
            else:
                user_feedbacks = UserResumeFeedback.objects.filter(user=request.user, resume_id=resume_id)
                if len(user_feedbacks) >= 1:
                    user_feedback = user_feedbacks[0]
                    user_feedback.notify_status = True
                    user_feedback.save()
            return HttpResponse(json.dumps({"status": "success"}), 'application/json')
    except:
        return HttpResponse(json.dumps({"status": "failed"}), 'application/json')

@login_required(login_url=LOGIN_URL)
@page_access_counter_dec(page_type_id=TAOCV_URL)
@group_required(['tao-cv', 'tao-cv|feed'], permissions=('feed.visit_taocv',), redirect_url='/taocv/nopermission')
def index(request,city='北京'):
    from Pinbot.settings import STATIC_URL
    p = request.GET.copy()
    tao_class = 'curr'
    user = request.user
    user_points, user_point = get_points(user)
    result, re_point, resume_id = get_notify(user)
    taocv_feeds = TaocvConfig.objects.filter(area=city,display=True).order_by('sequence')
    http_response = render_to_response("tao-resume.html", locals())
    return http_response
