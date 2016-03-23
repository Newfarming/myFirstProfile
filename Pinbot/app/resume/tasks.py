# coding: utf-8

import datetime

from pin_celery.celery_app import app

from resumes.models import (
    ResumeData,
    ContactInfoData,
)
from transaction.models import InterviewAlarm
from notifications import notify

from pin_utils.django_utils import (
    error_phone,
    get_oid,
)
from pin_utils.sms.sms_utils import asyn_send_sms


def get_resume_mapper(resume_id_list):
    resume_oid_list = [get_oid(resume_id) for resume_id in resume_id_list if get_oid(resume_id)]
    resume_data_query = ResumeData.objects.filter(
        id__in=resume_oid_list,
    ).only(
        'works',
    )
    mapper = {}
    for resume_data in resume_data_query:
        works = resume_data.works
        resume_id = str(resume_data.id)
        work = works[0] if works else None
        mapper[resume_id] = work.position_title if work else ''
    return mapper


def get_contactinfo_mapper(resume_id_list):
    contactinfo_query = ContactInfoData.objects.filter(
        resume_id__in=resume_id_list,
    )

    mapper = {}
    for contactinfo in contactinfo_query:
        mapper[contactinfo.resume_id] = contactinfo.name

    return mapper


@app.task(name='send-interview-alarm')
def send_interview_alarm():
    sms_notify_meta = u'【聘宝招聘】面试提醒：您安排了%(time)s，%(name)s的%(position_title)s职位面试，建议您再次与候选人确认面试信息，详细链接：%(url)s。祝面试顺利！'
    html_notify_meta = u'面试提醒：您安排了%(time)s，%(name)s的%(position_title)s职位面试，建议您再次与候选人确认面试信息。！'

    now = datetime.datetime.now()
    notify_end_time = now + datetime.timedelta(hours=2)

    alarms = InterviewAlarm.objects.select_related(
        'buy_record',
        'buy_record__user',
        'buy_record__user__userprofile',
    ).filter(
        has_alarm=False,
        interview_time__gte=now,
        interview_time__lte=notify_end_time,
    )

    resume_id_list = [alarm.buy_record.resume_id for alarm in alarms if alarm.buy_record.resume_id]
    resume_data_mapper = get_resume_mapper(resume_id_list)
    contactinfo_mapper = get_contactinfo_mapper(resume_id_list)

    for alarm in alarms:
        user = alarm.buy_record.user
        if not hasattr(user, 'userprofile'):
            continue

        resume_id = alarm.buy_record.resume_id
        interview_time = alarm.interview_time.strftime('%Y-%m-%d %H:%M')
        name = contactinfo_mapper.get(resume_id, '')
        position_title = resume_data_mapper.get(resume_id, '')
        userprofile = user.userprofile
        phone = userprofile.phone

        if not error_phone(phone):
            resume_url = 'http://www.pinbot.me/resumes/display/%s' % resume_id
            sms_notify = sms_notify_meta % {
                'time': interview_time,
                'name': name,
                'position_title': position_title,
                'url': resume_url,
            }
            asyn_send_sms(phone, sms_notify)

        html_notify = html_notify_meta % {
            'time': interview_time,
            'name': name,
            'position_title': position_title,
        }

        html_url = '/resumes/display/%s' % resume_id
        notify.send(
            user,
            recipient=user,
            verb='%s（<a class="c0091fa" href="%s">查看详情</a>）' % (html_notify, html_url),
            user_role='hr',
            notify_type='interview_alarm_notify',
        )
        alarm.has_alarm = True
        alarm.save()

    return True
