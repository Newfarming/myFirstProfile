# coding:utf-8
from celery_app import app
from django.core.mail.message import EmailMessage
from python_email import send_mass_email
from models import MarketEmailSendDetail
from django.contrib.auth.models import User
from transaction.models import UserChargePackage
from datetime import datetime
from django.template.loader import render_to_string
from jobs.models import SendCompanyCard
from resumes.models import ContactInfoData
from Pinbot.settings import DEFAULT_FROM_EMAIL
from Brick.App.job_hunting.job_utils import (
    JobUtils,
)
import time

@app.task
def send_single_email(subject, message,to_email, from_email=DEFAULT_FROM_EMAIL,info_dict={},token=None, job=None, resume_id=None):
    to=list()
    to.append(to_email)

    details = MarketEmailSendDetail()
    details.send_time = datetime.now()
    details.from_email = from_email
    details.subject = subject
    details.to_email = to_email
    details.status = True
    details.info_dict = info_dict
    details.save()
    token = str(details.id)

    try:
        if token:
            message = message.replace("pinbot_token",token)

        msg = EmailMessage(subject=subject, body=message, from_email=from_email, to=to)
        msg.content_subtype = "html"  # Main content is now text/html
        ret = msg.send()

        # 添加C端企业感兴趣
        brick_company_card = JobUtils.send_company_card(job.user, job, resume_id, token)
        if brick_company_card:
            details.info_dict['card_job_id'] = brick_company_card.id
        details.save()
        return True,str(details.id)
    except Exception , IntegrityError:
        details.status = False
        details.error_info = str(IntegrityError)
        details.save()
        return False, str(IntegrityError)
    return True, ret

@app.task
def send_market_email(subject, message,group=None,to_email=None):
    """
    @summary: 发送大量的市场邮件
    """
    if group:
        to_list = get_user(group)
        send_mass_email(to_list=to_list,subject=subject,message=message)
    elif to_email:
        send_single_email(subject=subject,message=message,to_email=to_email)

def get_user(group):
    users = set()
    if group == '全体注册会员':
        users = User.objects.all()
    elif group == '全体通过审核会员':
        users = User.objects.filter(is_active=True)
    elif group == '全体员工':
        users = User.objects.filter(is_staff=True)
    elif group == '所有有套餐用户':
        charges = UserChargePackage.objects.filter(actual_cost__gt=0)
        for charge in charges:
            users.add(charge.user)
    return users

@app.task
def send_card_task():
    """
    @summary: 发送企业名片
    """
    need_sends = SendCompanyCard.objects.filter(send_status=2).order_by('-send_time')
    for need_send in need_sends:
        print need_send.to_email
        job = need_send.job
        company = job.company
        resume_id = need_send.resume_id
        contactinfos = ContactInfoData.objects.filter(resume_id=resume_id)
        if len(contactinfos) > 0:
            need_send.to_email = contactinfos[0].email
            need_send.send_time = datetime.now()
            if contactinfos[0].name == '保密':
                need_send.send_status = 0
                need_send.to_email = '保密'
                need_send.feedback_status = 2
                result = True
            else:
                result,info = send_company_card(company=company,conatct_info=contactinfos[0],job=job,resume_id=resume_id,to_email=need_send.to_email)
            if result is True:
                need_send.send_status = 1
            elif result is False and info != 'nocontact':
                need_send.send_status = 0
                need_send.send_msg = info
            need_send.save()
    return True

def send_company_card(company,job,resume_id,conatct_info=None,to_email=None):
    from Pinbot.settings import WEBSITE
    name = conatct_info.name
    job.salary_low = job.salary_low/1000
    job.salary_high = job.salary_high/1000
    job.desc = job.desc.strip()
    skill_desc = job.skill_desc
    job.skill_desc = skill_desc.strip()
    subject = render_to_string('email-card-subject.txt',locals())
    message = render_to_string('email-card.html',locals())
    subject = ''.join(subject.splitlines())
    result,info = send_single_email(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, to_email=to_email,info_dict={'job_id':job.id}, token=None, job=job, resume_id=resume_id)

    return result,info
