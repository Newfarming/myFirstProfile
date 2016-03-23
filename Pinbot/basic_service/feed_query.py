# coding:utf-8
'''
Created on 2014-6-18

@author: likaiguo.happy@163.com
@summary: 一些通用的功能函数

'''
from feed.models import UserFeed
from feed.models import EmailSendInfo
from feed.models import UserFeed2, UserReadResume
from users.models import User
from users.models import UserProfile
import datetime
from feed.models import  FeedResult, UserFeed2
from django.template.loader import render_to_string
from Pinbot import settings
import logging
import time
import base64
from bson.objectid import ObjectId
from pinbot_package.views import get_one_feed_pkg
from transaction.models import ResumeBuyRecord, UserChargePackage
from resumes.models import ResumeData

email_log = logging.getLogger('email_send')




def get_datetime(hours=-8):

    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0)
    delta = datetime.timedelta(hours=hours)
    yestoday_deadline = today + delta
    return yestoday_deadline


def get_latest_reco_resumes(feed_id, user, time_line=get_datetime(hours=-10), limit=36, count=False):
    """
    @summary: 传入订阅id,feed_id
    @param feed_id:订阅id
    @param time_line: 已发布数据截至时间点,datetime对象 
    
    @return: 如果count为True则返回数量,否则返回对应的feed_result的id列表
    
    """
    # 该项推荐的所有结果
    feed_results = FeedResult.objects.filter(feed=feed_id)
    all_reco_feed_results = feed_results.filter(is_recommended=True)
    all_reco_published_feed_results = all_reco_feed_results.filter(published=True)
    
    latest_unread_recommend = []
    # 某天之后没有数据则退出循环,避免10次无效循环
    # 距离现在最近的一天----简历数量不为0 的推荐结果
    if feed_results.count():
        
        latest_unread_reco_count = 0
        i = 0
        yestoday_all_reco_feed_results = all_reco_published_feed_results(calc_time__lte=time_line)
        while latest_unread_reco_count == 0  and i < 10:
            calc_time_from = get_datetime(hours=-10 - ((i + 1) * 24))
            latest_unread_recommend = yestoday_all_reco_feed_results.filter(calc_time__gte=calc_time_from)
            latest_unread_recommend = latest_unread_recommend.limit(limit)
            latest_unread_reco_count = latest_unread_recommend.count()
            i += 1

    # 获取用户已读的简历id
    read_id_list = []
    
    # user_resume_reads = UserResumeRead.objects.filter(username=request.user.username, feed_id=str(feed_id))
#     user_resume_reads = UserFeed2.objects.filter(feed=feed_id)
#     for user_resume_read in user_resume_reads:
#         read_id_list.extend(user_resume_read.read_id_list)
    read_id_list = UserReadResume.objects.filter(user=user, feed_id=str(feed_id)).values_list('resume_id')
    read_id_list = [ObjectId(res[0]) for res in read_id_list if res]
            
    # 所有未读的 需要标记为 [新] 推荐 
    feed_res_unread_id_list = []
    feed_res_unread_id_list.extend([feed_res.resume.id for feed_res in latest_unread_recommend if feed_res.resume.id not in read_id_list])
    
    if count:
        return len(feed_res_unread_id_list)
    
    return feed_res_unread_id_list


def find_new_feed():
    email_log.info("开始发送订阅结果邮件...")
    sended_num = 0
    failed_num = 0
    success_num = 0
    no_pkg_nums = 0
    freq_nums = 0
    no_feed_nums = 0
    try:
        send_deny_list = []
        send_deny_set = set()
        toal_username_set = set()
        user_feed_map = {}
        
        usernames1 = set()
        usernames2 = set(UserFeed2.objects.filter(is_deleted=False).distinct('username'))
        charge_pkgs = UserChargePackage.objects.filter(feed_end_time__gte=datetime.datetime.now())
        for charge_pkg in charge_pkgs:
            try:
                usernames1.add(charge_pkg.user.username)
            except:
                pass
       
        usernames3 = usernames1 & usernames2
        usernames4 = list(usernames3)
        userFeeds = UserFeed2.objects.filter(is_deleted=False,username__in=usernames4)
        for userFeed in userFeeds:
            username = userFeed.username
            if isinstance(username, unicode):  
                username = username.encode('utf-8')
            if username == '':
                continue
            if username in send_deny_list:
                continue
            
            if username in user_feed_map:
                user_feed_map[username].append(userFeed)
                continue
            toal_username_set.add(username)
            
            userSendInfos = EmailSendInfo.objects.filter(username=username)
            if len(userSendInfos) == 0:
                feed_list = []
                feed_list.append(userFeed)
                user_feed_map[username] = feed_list
            else:
                userSendInfo = userSendInfos[0]
                if userSendInfo.sendFrequency == 0:
                    no_feed_nums += 1
                    send_deny_set.add(username)
                    send_deny_list.append(username)
                else:
                    lastSendTime = userSendInfo.lastSendDate
                    now = datetime.datetime.now()
                    hours = ((now - lastSendTime).days * 24 * 3600 + (now - lastSendTime).seconds) / 3600
                    frequencyHours = (userSendInfo.sendFrequency) * 24 - 24
                    if hours >= frequencyHours :
                        feed_list = []
                        feed_list.append(userFeed)
                        user_feed_map[username] = feed_list
                    else:
                        freq_nums += 1
                        send_deny_set.add(username)
                        send_deny_list.append(username)
        for username, feed_list in user_feed_map.iteritems():
            if username == '':
                continue
            email_log.info("开始发送： " + username)
            sended_num = sended_num + 1
            total_resume = 0
            feed_info_list = []
            for userFeed in feed_list:
                token = username + "&&&" + str(userFeed.feed.id)
                token = base64.b64encode(token)
                result_dict = get_feed_result(userFeed)
                total_resume += result_dict['feed_result_num']
                result_dict['keywords'] = userFeed.feed.keywords
                result_dict['talent_level'] = userFeed.feed.talent_level
                result_dict['id'] = userFeed.feed.id
                result_dict['token'] = token
                if result_dict['feed_result_num'] > 0:
                    feed_info_list.append(result_dict)
            try:
                if total_resume > 0:
                    result, info = feed_find_email(username, feed_info_list, total_resume)
                    time.sleep(15)  # 限制发送频率防止发送过快被服务商屏蔽
                    success_num = success_num + 1
                    email_log.info("发送成功! ")
                    emailSendInfos = EmailSendInfo.objects.filter(username=username)
                    if len(emailSendInfos) == 0:
                        emailSendInfo = EmailSendInfo(username=username,
                                            lastSendDate=datetime.datetime.now(), send_status=str(info))
                    else:
                        emailSendInfo = emailSendInfos[0]
                        emailSendInfo.send_status = str(info)
                        emailSendInfo.lastSendDate = datetime.datetime.now()
                    emailSendInfo.save()
            except Exception , IntegrityError:
                failed_num = failed_num + 1
                email_log.info("发送失败! ")
                email_log.info(str(IntegrityError))
                    
    except Exception , IntegrityError:
        email_log.info(str(IntegrityError))
    
    email_log.info(" ")
    email_log.info(" ")
    email_log.info("发送完成! ")
    email_log.info("共发送 " + str(sended_num) + " 封邮件! ")
    email_log.info("成功发送 " + str(success_num) + " 封邮件! ")
    email_log.info("发送失败 " + str(failed_num) + " 封邮件! ")
    return sended_num
            
def get_feed_result(user_feed):
    result_dict = {}
    resume_list = list()
    user = User.objects.filter(username=user_feed.username)
    if len(user) >= 1:
        user = user[0]
        unread_id_list = get_latest_reco_resumes(user_feed.feed.id, user=user)
        result_dict['feed_result_num'] = len(unread_id_list)
        if len(unread_id_list) > 2:
            unread_id_list = unread_id_list[0:2]
        for resume_id in unread_id_list:
            resumes = ResumeData.objects.filter(pk=resume_id)
            if len(resumes) >= 1:
                resume_list.append(resumes[0])
        result_dict['feed_resumes'] = resume_list
    return result_dict

def feed_find_email(username, feed_info, total_num):
    username_token = base64.b64encode(username)
    titles = ''
    for feed in feed_info:
        if titles == '':
            titles = feed['keywords']
        else:
            titles += ","+feed['keywords']
    if titles > 20:
        titles = titles[0:19]+"..."
    if isinstance(username, unicode):  
        username = username.encode('utf-8')
    ctx_dict = {'feed_info_list':feed_info,
                'total_num':total_num,
                'username_token':username_token}
    subject = render_to_string('email-template/rss_feed_subject.txt',locals())  
    
    message = render_to_string('email-template/rss-feed.html', ctx_dict)
    subject = ''.join(subject.splitlines())
    from users.views import send_email
    result, info = send_email(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, email=username)
    return result, info


if __name__ == '__main__':
    
    read_id_list = UserReadResume.objects.filter(feed_id=str('5301d99dfb6dec344c92b636')).values_list('resume_id')
    
    x = [ObjectId(res[0]) for res in read_id_list if res]
    pass
