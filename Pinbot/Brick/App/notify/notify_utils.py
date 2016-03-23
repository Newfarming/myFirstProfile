# coding: utf-8

from notifications import notify

from Brick.settings import (
    RESUME_BOUGHT_URL,
    RECEIVE_URL
)


MY_JOB_URL = '/job/my_job/'


class NotifyUtils(object):

    COMPANY_NOTIFY_TMPL = '''
    <h5>{company_name}</h5>
    <p class="feedback">{company_msg}（请到<a class="c0091fa" href="%s">我的职位</a>查看详情）</p>
    ''' % MY_JOB_URL

    SEND_NOTIFY_TMPL = '''
    <h5>{name}</h5>
    <p class="feedback">投递了你的{title}职位（<a class="c0091fa" href="%s">查看详情</a>）</p>
    ''' % RECEIVE_URL

    COMPANY_NOTIFY_MSG = {
        'fail': '没有通过你的简历',
        # 企业名片
        'interest': '对你感兴趣，期待你的反馈',
        'interview': '对你投递的简历感兴趣， 请耐心等待面试邀请',
    }

    CARD_NOTIFY_MSG = {
        'accept': '对你发送的企业名片反馈了感兴趣（<a class="c0091fa" href="%s">查看详情</a>）' % RESUME_BOUGHT_URL,
        'reject': '对你发送的企业名片反馈了不感兴趣（<a class="c0091fa" href="%s">查看详情</a>）' % RESUME_BOUGHT_URL,
    }

    CHECK_RESUME_TMPL = '''
    <h5>{company_name}</h5>
    <p class="feedback">查阅了你的简历，对你表示感兴趣，近期或与你联系。</p>
    '''

    SYSTEM_NOTIFY = {
        'welcome': '''
        <h5>系统通知</h5>
        <p class="feedback">你好，欢迎加入聘宝。</p>
        ''',
    }

    @classmethod
    def company_notify(cls, recommend_job, notify_type):
        '''
        notify_type:
            fail 没有通过你的简历
            interest 感兴趣，期待反馈
            interview 感兴趣，等待面试通知
        '''
        user = recommend_job.resume.user
        feed = recommend_job.job
        company_name = feed.company.company_name if feed.company else ''
        company_msg = cls.COMPANY_NOTIFY_MSG[notify_type]
        url = '/job/' if notify_type == 'interview' else '/job/my_job/'
        verb = cls.COMPANY_NOTIFY_TMPL.format(
            company_name=company_name,
            company_msg=company_msg,
            url=url,
        )
        notify.send(user, recipient=user, verb=verb)
        return True

    @classmethod
    def send_resume_notify(cls, job_manage):
        name = job_manage.resume.name
        title = job_manage.job.title
        user = job_manage.hr_user
        verb = cls.SEND_NOTIFY_TMPL.format(
            name=name,
            title=title,
        )
        notify.send(user, recipient=user, verb=verb)
        return True

    @classmethod
    def check_resume(cls, resume, feed):
        '''
        查看了简历
        '''
        user = resume.user
        company_name = feed.bind_job.company.company_name
        verb = cls.CHECK_RESUME_TMPL.format(
            company_name=company_name
        )
        notify.send(user, recipient=user, verb=verb)
        return True

    @classmethod
    def card_job_notify(cls, card_job, action):
        user = card_job.hr_user
        verb = cls.CARD_NOTIFY_MSG[action]
        notify.send(user, recipient=user, verb=verb)
        return True

    @classmethod
    def system_notify(cls, user, notify_type):
        '''
        param: notify_type
            welcome: 欢迎加入聘宝
        '''
        verb = cls.SYSTEM_NOTIFY[notify_type]
        notify.send(user, recipient=user, verb=verb)
        return True
