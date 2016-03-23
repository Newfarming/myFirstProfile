# coding: utf-8

import bleach
import datetime

from django import template

register = template.Library()


@register.filter
def show_skill(skill_list):
    s = '<br>'.join(i.skill_desc for i in skill_list)
    s = bleach.clean(s, tags=['br'], strip=True)
    return s


@register.filter
def get_mark_logs(resume_mark):
    if not resume_mark:
        return []
    return list(resume_mark.mark_logs.all())


@register.filter
def not_accu(accu_status):
    return False if accu_status in (1, 2) else True


@register.filter
def can_accu(resume_mark):
    return True if not resume_mark else False


@register.filter
def is_accu(feedback_info):
    return True if feedback_info and feedback_info.id in (220, 221) else False


@register.filter
def mark_logs(mark_logs):
    log_data = [
        {
            'mark_time': i.mark_time.strftime("%Y-%m-%d %H:%M"),
            'mark_name': i.mark.name,
            'is_admin': True if i.user and i.user.is_staff else False,
            'good_result': True if i.mark.good_result else False,
            'comment': i.desc if i.is_display else '',
        }
        for i in list(mark_logs)
    ]
    return log_data[::-1]


@register.filter
def reco_keywords(keywords):
    return [] if not keywords else keywords


@register.filter
def interview_alarm(interview_alarms):
    interview = list(interview_alarms)[-1] if interview_alarms else None
    return interview


@register.filter
def is_interview(mark):
    return True if mark.code_name in ('invite_interview', 'next_interview') else False


@register.filter
def need_reply(send_company_card):
    if not send_company_card:
        return False

    now = datetime.datetime.now()
    send_time = send_company_card.send_time
    feedback_status = send_company_card.feedback_status

    if feedback_status == 0 and (now - send_time).days > 7:
        return False
    return True


@register.filter
def card_reply_msg(feedback_status):
    feedback_meta = {
        0: u'待反馈',
        1: u'候选人反馈感兴趣',
        2: u'候选人不感兴趣',
        3: u'未反馈',
    }
    return feedback_meta.get(feedback_status, u'待反馈')


@register.filter
def no_reply(send_company_card):
    if not send_company_card:
        return False

    now = datetime.datetime.now()
    send_time = send_company_card.send_time
    feedback_status = send_company_card.feedback_status

    if feedback_status == 3 or (feedback_status == 0 and (now - send_time).days > 7):
        return True

    return False


@register.filter
def get_mark_display(current_mark, interview_alarm):
    if not interview_alarm:
        return current_mark.name

    code_name = current_mark.code_name
    if code_name not in ('invite_interview', 'next_interview'):
        return current_mark.name

    interview_count = interview_alarm.interview_count
    return u'安排第%s轮面试' % interview_count


@register.filter
def reco_is_del(is_recommend):
    return True if not is_recommend else False
