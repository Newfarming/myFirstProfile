# coding:utf-8
# Create your views here.

import json
from django.http.response import HttpResponse
from django.db import transaction as dj_trans
from django.shortcuts import render

from transaction.models import ResumeBuyRecord, UserChargePackage, UserResumeFeedback
from .mark_utils import MarkUtils
from pinbot_package.models import *
from django.contrib.auth.decorators import login_required
from resumes.models import ResumeData, ContactInfoData
from datetime import datetime
from bson import ObjectId

from basic_service.resume_util import produce_return_json
from django.template.loader import render_to_string
from users.views import send_email
from Pinbot import settings
from pinbot_permission.pinbot_decorator import resume_points_required
from jobs.models import SendCompanyCard
from Pinbot.settings import COMPANY_CARD_EXPIRE_DAY

from app.pinbot_point.point_utils import point_utils
from app.vip.vip_utils import VipRoleUtils

from app.partner.partner_utils import (
    PartnerCoinUtils,
)
from app.special_feed.feed_utils import (
    FeedUtils,
)
from Brick.App.job_hunting.job_utils import (
    JobUtils,
)
from pin_utils.django_utils import (
    require_staff,
    get_oid,
)
from pin_utils.email.send_mail import (
    asyn_send_mail,
)
from pin_utils.spider_utils import (
    asyn_send_download_msg,
)


@login_required
def bought_resume(request,page_curr):
    if not page_curr:
        page_curr = 1

    if page_curr < 1:
        page_curr = 1

    page_curr = int(page_curr)

    userChargePackages = True if UserChargePackage.objects.order_by('-start_time').filter(user=request.user.id).count() else False

    watch_class = 'curr'
    user = request.user
    username = request.user.username
    resume_list = get_bought_resume(user)
    has_download = '不限'
    source = '不限'
    feedback = '不限'
#     userChargePackages = UserChargePackage.objects.order_by('-start_time').filter(user=user)
    page = "bought_resume"
    from_source = "bought_resume"
#     if len(resume_list):
#         page_deco_list, previous, page_next = page_counter(page_list, page_curr)
#
    return render(request, "resumes/bought-list.html", locals())

def get_bought_resume(user):
    resume_list = []
    resume_id_list = []
    card_sends = SendCompanyCard.objects.filter(send_user=user).order_by('-send_time')
    for send in card_sends:
        resume_id = send.resume_id
        resumes = ResumeData.objects.filter(id=ObjectId(resume_id))
        contactinfos = ContactInfoData.objects.filter(resume_id=resume_id)
        feedback_status = send.feedback_status
        for resume in resumes:
            has_download = False
            buy_record_query = ResumeBuyRecord.objects.filter(
                user=user,
                resume_id=resume_id,
            ).select_related(
                'resume_mark',
                'resume_mark__mark',
            )
            buy_record = None
            if buy_record_query:
                has_download = True
                buy_record = buy_record_query[0]
            if send.has_download is False and has_download is True:
                send.has_download = True
                send.save()
            if contactinfos and has_download is True:
                resume.name = contactinfos[0].name
                resume.phone = contactinfos[0].phone
                resume.email = contactinfos[0].email
            extra_info = {}

            extra_info['op_time'] = send.send_time
            extra_info['buy_source'] = '企业名片意向确认'
            extra_info['used_points'] = send.points_used
            extra_info['feed_back'] = get_feed_back(send.send_time,feedback_status)
            extra_info['download_status'] = '已下载' if has_download else '未下载'
            extra_info['download_success'] = send.download_status
            extra_info['send_id'] = send.id
            extra_info['feed_id'] = send.feed_id
            extra_info['buy_record'] = buy_record

            resume_id_list.append(str(resume.id))
            resume_list.append((resume, extra_info,extra_info['op_time']))

    resume_bought_recds = ResumeBuyRecord.objects.order_by(
        '-op_time'
    ).select_related(
        'resume_mark',
        'resume_mark__mark',
    ).filter(
        user=user
    ).exclude(
        resume_id__in=resume_id_list
    )
    for resume_bought_recd in resume_bought_recds:
        resume_id = resume_bought_recd.resume_id
        resumes = ResumeData.objects.filter(id=ObjectId(resume_id))
        contactinfos = ContactInfoData.objects.filter(resume_id=resume_id)

        for resume in resumes:
            point_used = 10
            if contactinfos:
                resume.name = contactinfos[0].name
                resume.phone = contactinfos[0].phone
                resume.email = contactinfos[0].email
            extra_info = {}
            status = resume_bought_recd.status

            if resume.name == '保密':
                point_used = 0

            extra_info['keywords'] = resume_bought_recd.keywords
            extra_info['op_time'] = resume_bought_recd.op_time
            extra_info['buy_source'] = '直接下载'
            extra_info['used_points'] = point_used
            extra_info['feed_back'] = ''
            extra_info['download_status'] = '已下载' if status == 'LookUp' else '准备中'
            extra_info['feed_id'] = resume_bought_recd.feed_id
            extra_info['buy_record'] = resume_bought_recd
            resume_list.append((resume, extra_info,extra_info['op_time']))
    sorted_resume_list = sorted(resume_list,key=lambda tup:tup[2],reverse=True)
    resume_list = [(tup[0],tup[1]) for tup in sorted_resume_list]

    return resume_list

def get_feed_back(send_time,feed_back_status):
    time_elapse_days = (datetime.now() - send_time).days
    feedback = ''
    if feed_back_status == 1:
        feedback = '感兴趣'
    elif feed_back_status == 2:
        feedback = '不感兴趣'

    if feed_back_status == 0 and time_elapse_days >= COMPANY_CARD_EXPIRE_DAY:
        feedback = '无回复'
    if feed_back_status == 0 and time_elapse_days < COMPANY_CARD_EXPIRE_DAY:
        feedback = '待确认'
    return feedback

def send_buy_email(user, resume_id,source,type='buy'):
    buy_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if source == '51job':
        source = "前程无忧"
    if source == 'zhilian':
        source = "智联招聘"
    if source == 'liepin':
        source = "猎聘"

    if type == 'companycard':
        type = '企业名片发送'
    else:
        type = '简历购买申请'
    subject = render_to_string('email-template/resume-buy-subject.txt',locals())
    try:
        first_name = user.first_name
        message = render_to_string('email-template/resume-buy-info.html', locals())
    except Exception , IntegrityError:
        pass
    subject = ''.join(subject.splitlines())
    result, info = send_email(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, email='support@hopperclouds.com')
    return result


def notify_buy_resume(user, resume_id, source):
    '''
    通知管理员用户购买了简历
    '''
    source_meta = {
        '51job': '51job',
        'zhilian': '智联',
        'liepin': '猎聘',
    }
    subject = '[通知]用户购买简历%s' % source_meta.get(source, source)
    html = render_to_string(
        'transaction/notify_buy_resume.html',
        {'user': user, 'resume_id': resume_id}
    )
    support_email_to = ';'.join(settings.SUPPORT_EMAIL_LIST)
    asyn_send_mail.delay(
        support_email_to,
        subject,
        html,
    )
    return True


@login_required
@resume_points_required('')
@dj_trans.atomic
def buy(request):
    """
    @summary: 购买简历
    """
    try:
        p = request.GET.copy()
        resume_id = p.get('resume_id', '')
        feed_id = p.get('feed_id', '')
        keywords = p.get('feed_keywords', '')
        job_id = p.get('job_id', '')
        user = request.user

        if ResumeBuyRecord.objects.filter(user=request.user, resume_id=resume_id).count():
            json_data = produce_return_json(data=2, status=False, error_dict=u'2.已购买过此简历_has bought this resume')
        else:
            pkg_points, user_points = point_utils.get_user_point(user)
            result, point = point_utils.consume_download_point(user)
            if result == 'success':
                status = 'LookUp' if ContactInfoData.objects.filter(resume_id=ObjectId(resume_id)).count() > 0 else 'Start'
                if status == 'LookUp':
                    # pinbot系统已经购买过,可以马上查阅了
                    json_data = produce_return_json(data=8)
                else:
                    # pinbot系统还没有,要等一段时间,后边邮件提醒一下
                    json_data = produce_return_json(data=9)

                resume = ResumeData.objects.get(pk=ObjectId(resume_id))
                record = ResumeBuyRecord(user=user, resume_id=resume_id, \
                                         feed_id=feed_id,
                                         keywords=keywords,
                                          op_time=datetime.now(), status=status, resume_url=resume.url)
                if status == 'LookUp':
                    record.finished_time = datetime.now()

                PartnerCoinUtils.download_resume(feed_id, resume_id)
                JobUtils.download_send_resume(job_id, user)

                # 反馈结果给算法，修改feed_result
                FeedUtils.feed_result_download(resume_id, feed_id)
                send_id = p.get('sendid',None)
                if send_id:
                    send_record = SendCompanyCard.objects.get(id=int(send_id))
                    record.send_card = send_record
                    send_record.points_used = 13
                    send_record.has_download = True
                    send_record.save()

                record.save()

                # 如果状态是start，就表示是当前库中没有该简历的联系信息，先发送一个通知给管理员
                # 然后需要通知爬虫去下载
                if record.status == 'Start':
                    notify_buy_resume(user, str(resume_id), resume.source)
                    asyn_send_download_msg.delay(record.id)
            else:
                json_data = produce_return_json(
                    data=5,
                    status=False,
                    error_dict=u'点数不足10点',
                    msg=u'聘点不足10点'
                )
    except Exception, e:
        if resume_id:
            json_data = produce_return_json(data=4, status=False, error_dict=str(e))
        else:
            json_data = produce_return_json(data=4, status=False, error_dict='4.resume_id is null')

    return HttpResponse(json_data, "application/json")

def buy_resume(user,resume_id,send_record,feed_id=''):
    """
    @summary: 用户点击邮件中的感兴趣后添加简历购买记录
    """
    if ResumeBuyRecord.objects.filter(user=user, resume_id=resume_id).count() == 0:
        # pkg_points,user_points = get_user_points(user)
        # result = consume_points(user=user,points=9,pkg_points=pkg_points,user_points=user_points)
        pkg_points, user_points = point_utils.get_user_point(user)
        result, point = point_utils.consume_download_point(user, 9)
        if result:
            resume = ResumeData.objects.get(pk=ObjectId(resume_id))
            record = ResumeBuyRecord(user=user, resume_id=resume_id, \
                                      op_time=datetime.now(), status='LookUp', resume_url=resume.url)
            record.finished_time = datetime.now()
            record.send_card = send_record
            record.feed_id = feed_id
            record.save()
            return True

    return False

@login_required
def add_contactInfo(request):
    if not request.user.is_staff == 1:
        data = {"status":'failed', 'msg':'you are not authorized!'}
        return HttpResponse(json.dumps(data), 'application/json')
    try:
        p = request.GET.copy()
        source_id = p.get('sourceID', "")
        resume_id = p.get('resumeID', "")
        phone = p.get('phone', "")
        name = p.get('name', "")
        email = p.get('email', "")
        source = p.get('source', "")

        from resumes.models import ContactInfoData
        contactInfo = ContactInfoData(resume_id=ObjectId(resume_id), source=source, source_id=source_id, phone=phone, email=email, name=name)
        contactInfo.save()

        data = {"status:":'success'}
        return HttpResponse(json.dumps(data), "application/json")
    except Exception , IntegrityError:
        data = {"status:":'failed', "message:":str(IntegrityError)}
        return HttpResponse(json.dumps(data), "application/json")


@login_required
@dj_trans.atomic
def return_points(request, op_type, user_fd_back_id):
    """
    @summary: 返还用户返还的极点. 管理员审核通过后返还用户的积点.
    @author: likaiguo 2014-6-17 10:38:29
    """
    json_data = ''
    user_fd_backs = UserResumeFeedback.objects.filter(pk=int(user_fd_back_id))
    if user_fd_backs:
        user_fd_back = user_fd_backs[0]
        if op_type == 'deny':
            user_fd_back.check_status = 'deny'
            json_data = json.dumps({'status':'ok', 'data':'已拒绝返点'})
            user_fd_back.save()
            MarkUtils.accu_mark_result(
                user_fd_back.user,
                user_fd_back.resume_id,
                'deny',
            )
        elif user_fd_back.check_status != 'checking':
            json_data = json.dumps({'status':'error', 'data':'重复操作,当前返点状态-%s' % user_fd_back.check_status})
        elif request.user.is_staff:
            now = datetime.now()

            user_base_pkgs = UserChargePackage.objects.filter(
                user=user_fd_back.user,
                package_type=1,
                pay_status='finished',
                resume_end_time__gt=now,
            ).order_by('-start_time')

            if user_base_pkgs:
                base_pkg = user_base_pkgs[0]
                base_pkg.re_points += user_fd_back.feedback_info.type.re_points
                base_pkg.save()

                user_fd_back.check_status = 'pass'
                PartnerCoinUtils.resume_accusation(user_fd_back)
                PartnerCoinUtils.add_malice_user(user_fd_back)
                user_fd_back.save()

                json_data = json.dumps({'status':'ok', 'data':'已返还%d点' % user_fd_back.feedback_info.type.re_points})
                MarkUtils.accu_mark_result(
                    user_fd_back.user,
                    user_fd_back.resume_id,
                    'pass',
                )
            else:
                # 新服务模式返点到聘点中
                user = user_fd_back.user
                current_vip = VipRoleUtils.get_current_vip(user)
                if current_vip:
                    user_fd_back.check_status = 'pass'
                    user_fd_back.save()
                    point_utils.accu_return(user)
                    json_data = json.dumps({'status':'ok', 'data':'返点成功'})

                    MarkUtils.accu_mark_result(
                        user_fd_back.user,
                        user_fd_back.resume_id,
                        'pass',
                    )
                    PartnerCoinUtils.resume_accusation(user_fd_back)
                    PartnerCoinUtils.add_malice_user(user_fd_back)
                else:
                    json_data = json.dumps({'status':'error', 'data':'用户没有基础套餐'})
        else:
            json_data = json.dumps({'status':'error', 'data':'请使用员工号'})
    return HttpResponse(json_data, 'application/json')


@require_staff
@dj_trans.atomic
def return_secret_points(request, bought_id):
    """
    @summary:
        简历信息设置为保密,管理员下载时,发现这个情况后就
    # 1.将该条购买记录更改为保密状态,xadmin操作链接.
    # 2. 套餐积点加回去,加到返还点数里,并且已购买此简历的用户会在管理员确认后看见返还点数
    # 3. 把这个信息存储到联系人信息表,后续查看此简历的客户不能看到下载和反馈按钮
    """
    resumes_buy_recds = ResumeBuyRecord.objects.filter(
        id=int(bought_id),
        status='Start',
    )

    if resumes_buy_recds and request.user.is_staff:
        now = datetime.now()
        # 1.将该条购买记录更改为保密状态
        buy_recd = resumes_buy_recds[0]
        resume_id = buy_recd.resume_id
        buy_recd.status = 'Secret'
        buy_recd.finished_time = now
        buy_recd.save()

        data = ''

        resume_oid = get_oid(buy_recd.resume_id)
        ResumeData.objects.filter(
            id=resume_oid,
        ).update(
            set__is_secret=True,
        )

        user = buy_recd.user
        # 2. 套餐积点加回去,加到返还点数里
        # 套餐为基础套餐,服务未到期,并且已付款
        user_base_pkgs = UserChargePackage.objects.filter(user=user, package_type=1,
                                                          resume_end_time__gte=datetime.now(),
                                                          pay_status='finished'
                                                          ).order_by('-start_time')

        current_vip = VipRoleUtils.get_current_vip(user)
        if user_base_pkgs:
            base_pkg = user_base_pkgs[0]
            base_pkg.re_points += 10
            base_pkg.save()
            data += '已返还10点 到套餐'
        elif current_vip:
            point_utils.secret_return(user)
        else:
            data += '套餐不满足(有基础套餐,服务未到期,已付款)之一'


        # 3. 把这个信息存储到联系人信息表
        contact_infos = ContactInfoData.objects.filter(resume_id=resume_id)
        if contact_infos:
            data += ' 联系信息已存在'
        else:
            ContactInfoData(resume_id=resume_id, status='secret', \
                            name='保密', source='', \
                            email=' ', \
                            source_id=''
                            ).save()
            data += ' 新建了该简历联系信息保密'

        json_data = json.dumps({'status':'ok', 'data':data})
    else:
        json_data = json.dumps({'status':'ok', 'data':'没有该购买,或者你不是管理员'})

    return HttpResponse(json_data, 'application/json')

def filt_resumes(request):
    """
    @我的购买 中 简历查询
    """
    info_dict={}
    if request.method == 'POST':
        json_data = json.loads(request.body)
        has_download = json_data.get('has_download',None)
        source = json_data.get('source',None)
        feedback = json_data.get('feedback',None)
        sends = SendCompanyCard.objects.filter(send_user=request.user)
        if has_download and has_download == 'true':
            sends = sends.filter(hasdownload=True)
        elif has_download and has_download == 'false':
            sends = sends.filter(hasdownload=False)

        if source and source == 'buy':
            sends = sends.filter()
        elif source and source == 'companycard':
            sends = sends.filter(hasdownload=False)
