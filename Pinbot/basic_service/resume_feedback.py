# coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response, redirect
from transaction.models import *

django_log = logging.getLogger('django')
#
# @login_required
# def notify_read_ajax(request):
#     """
#     用户已读通知
#     """
#     data = request.POST.copy()
#     notify_id = data.get('notify_id',None)
#     if notify_id is not None:
#         user_feedbacks = UserResumeFeedback.objects.filter(id = notify_id)
#         if len(user_feedbacks) == 1:
#             user_feedback = user_feedbacks[0]
#             user_feedback.notify_status = True
#             user_feedback.save()
#             return HttpResponse(json.dumps({"status": "success"}),'application/json')
#     return HttpResponse(json.dumps({"status": "failed"}),'application/json')


def get_points(user):
    """
    获取用户的积分数,套餐失效 积分就失效
    """

    user_point = 0
    user_points = UserChargePackage.objects.filter(user = user,resume_end_time__gte=datetime.now())
    if len(user_points) >= 1:
        user_point = user_points[0].rest_points
    return user_point

def get_feedback(resume_id):
    feed_back_dict = None
    feedbacks = UserResumeFeedback.objects.order_by('-create_time').filter(resume_id = resume_id)

    for feedback in feedbacks:
        if feedback.feedback_info is not None:
            feed_back_dict = {}
            if feedback.feedback_info.type.id != 3:
                feedback_value = feedback.feedback_value or ''
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
    user_feedbacks = UserResumeFeedback.objects.order_by('-create_time').filter(user = user, resume_id = resume_id)
    if len(user_feedbacks) >= 1:
        re_points = 0
        user_feedback = user_feedbacks[0]
        if user_feedback.feedback_info.type.id != 3:
            feedback_value = user_feedback.feedback_value or ''
            feedback_desc = user_feedback.feedback_info.feedback_desc
            re_points = user_feedback.feedback_info.type.re_points
            type_desc = user_feedback.feedback_info.type.desc
            feedback_str = feedback_desc.replace('_', feedback_value)
            if feedback_desc == '其他':
                feedback_str = feedback_value
            check_status = user_feedback.check_status
            if check_status == 'checking':
                feedback_str = '反馈正在验证中...'
            elif check_status == 'failed':
                feedback_str = '反馈审核未通过...'
            return check_status, type_desc, feedback_str,re_points
    return None, None, None,None

def get_offical_feedback(resume_id):
    feedback_str = None
    user_feedbacks = UserResumeFeedback.objects.order_by('-create_time').filter(resume_id = resume_id,feedback_info__type__id=3)
    if len(user_feedbacks) >= 1:
        user_feedback = user_feedbacks[0]
        feedback_value = user_feedback.feedback_value
        feedback_desc = user_feedback.feedback_info.feedback_desc
        if feedback_desc == '其他_' or feedback_desc == '其他':
            feedback_str = feedback_value
        else:
            feedback_str = feedback_desc
    return feedback_str

@csrf_exempt
@login_required
def add_feedback_ajax(request):
    """
    添加用户反馈
    """
    data = request.POST.copy()
    feedback_id = data.get('feedback_id',None)
    feedback_value = data.get('feedback_value',None)
    resume_id = data.get('resume_id',None)
    if feedback_id is not None and resume_id is not None :
        feedback_id = int(feedback_id)
        user_feedback = UserResumeFeedback(user=request.user,resume_id=resume_id,feedback_info=feedback_id,feedback_value=feedback_value)
        user_feedback.save()
        return HttpResponse(json.dumps({"status": "success"}),'application/json')
    else:
        return HttpResponse(json.dumps({"status": "failed","msg":"empty"}),'application/json')
