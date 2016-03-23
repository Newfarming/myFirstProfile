# coding: utf-8

import datetime
from functools import partial

from django.contrib.auth.models import Group

from notifications import notify

from .models import (
    UserTaskResume,
    TaskCoinRecord,
    UploadResume,
    PartnerLevelManage,
)

from transaction.models import (
    ResumeBuyRecord,
)

from app.pinbot_point.point_utils import (
    coin_utils
)

from pin_utils.django_utils import (
    get_object_or_none,
    get_int,
)


class UploadResumeUtils(object):

    TIME_FORMAT = '%Y-%m'
    TO_NOW = datetime.datetime(2100, 01, 01)
    TO_NOW_STR = '至今'

    LAST_CONTACT_META = {
        1: '一周内',
        2: '一个月内',
        3: '3个月内',
    }
    GENDER_META = {
        'male': '男',
        'female': '女',
    }
    DEGREE_META = dict([
        ('', '未知'),
        ('bachelor', '本科'),
        ('master', '硕士'),
        ('phd', '博士'),
        ('hnd', '大专'),
    ])

    @classmethod
    def get_sync_resume_dict(cls, resume):
        if not resume:
            return {}

        resume_dict = {
            'id': resume.resume_id,
            'contact_info': {
                'name': resume.name,
                'gender': cls.GENDER_META.get(resume.gender, resume.gender),
                'phone': resume.phone,
                'email': resume.email,
                'work_years': resume.work_years,
                'age': resume.age,
                'qq': resume.qq,
                'self_evaluation': resume.self_evaluation,
                'degree': cls.DEGREE_META.get(resume.degree, resume.degree),
                'job_hunting_state': resume.job_hunting_state,
                'expect_work_place': resume.expect_work_place,
                'expect_position': resume.expect_position,
                'resume_id': resume.resume_id,
                'source': 'talent_partner',
            },

            'name': resume.name,
            'gender': cls.GENDER_META.get(resume.gender, resume.gender),
            'phone': resume.phone,
            'email': resume.email,
            'work_years': resume.work_years,
            'age': resume.age,
            'degree': cls.DEGREE_META.get(resume.degree, resume.degree),
            'job_hunting_state': resume.job_hunting_state,
            'expect_work_place': resume.expect_work_place,
            'expect_position': resume.expect_position,
            'last_contact': cls.LAST_CONTACT_META.get(resume.last_contact, 1),
            'hr_evaluate': resume.hr_evaluate,
            'address': resume.address,

            'self_evaluation': resume.self_evaluation,
            'work_years': str(resume.work_years),
            'created_at': resume.create_time,
            'updated_at': resume.update_time,
            'update_time': resume.update_time.strftime('%Y-%m-%d'),
            'resume_id': resume.resume_id,
            'source': 'talent_partner',
            'owner': resume.user.username,

            'job_target': {
                'expectation_area': resume.expect_work_place,
                'salary': str(int(resume.target_salary)),
                'job_career': resume.expect_position,
                'job_hunting_state': resume.job_hunting_state,
            },
            'current_job': {
            },
            'works': [
                {
                    'start_time': w.start_time.strftime(cls.TIME_FORMAT),
                    'end_time': w.end_time.strftime(cls.TIME_FORMAT) if w.end_time != cls.TO_NOW else cls.TO_NOW_STR,
                    'position_title': w.position_title,
                    'company_name': w.company_name,
                    'job_desc': w.job_desc,
                }
                for w in list(resume.resume_works.all())
            ],
            'projects': [
                {
                    'start_time': p.start_time.strftime(cls.TIME_FORMAT),
                    'end_time': p.end_time.strftime(cls.TIME_FORMAT) if w.end_time != cls.TO_NOW else cls.TO_NOW_STR,
                    'project_name': p.project_name,
                    'project_desc': p.project_desc,
                }
                for p in list(resume.resume_projects.all())
            ],
            'educations': [
                {
                    'start_time': e.start_time.strftime(cls.TIME_FORMAT),
                    'end_time': e.end_time.strftime(cls.TIME_FORMAT) if w.end_time != cls.TO_NOW else cls.TO_NOW_STR,
                    'school': e.school,
                    'major': e.major,
                    'degree': e.degree,
                }
                for e in list(resume.resume_educations.all())
            ],
            'professional_skills': [
                {
                    'skill_desc': s.skill_desc,
                    'proficiency': s.proficiency,
                }
                for s in list(resume.resume_skills.all())
            ],
        }
        return resume_dict

    @classmethod
    def is_self_upload(cls, user, resume_id):
        upload_resume_query = UploadResume.objects.filter(
            user=user,
            resume_id=str(resume_id),
        )
        return upload_resume_query[0] if upload_resume_query else False


class PartnerCoinUtils(object):

    RECORD_DESC_META = {
        'check': {
            'desc': '简历被查看',
            'index': 1,
        },
        'download': {
            'desc': '简历被下载',
            'index': 2,
        },
        'interview': {
            'desc': '进入面试',
            'index': 3,
        },
        'taking_work': {
            'desc': '已入职',
            'index': 4,
        },
        'accusation': {
            'desc': '简历被举报',
            'index': 5,
        },
        'extra_taking_work': {
            'desc': '已入职额外奖励',
            'index': 4,
        },
        'extra_download': {
            'desc': '简历被下载额外奖励',
            'index': 2,
        },
        'extra_interview': {
            'desc': '进入面试额外奖励',
            'index': 3,
        },
    }

    @classmethod
    def add_malice_user(cls, feedback_record):
        resume_id = feedback_record.resume_id
        user_resume_query = UserTaskResume.objects.filter(
            resume__resume_id=resume_id
        )
        if not user_resume_query:
            return False

        user_resume = user_resume_query[0]
        accusation_user = user_resume.resume.user
        malice_group = get_object_or_none(
            Group,
            name='malice_partner',
        )

        if malice_group in accusation_user.groups.all():
            return True

        has_accu_count = UserTaskResume.objects.filter(
            resume__user=accusation_user,
            resume_status=5
        ).count()

        if has_accu_count >= 2:
            accusation_user.groups.add(malice_group)
            return True
        return False

    @classmethod
    def get_task_resume(cls, feed_id, resume_id):
        accept_task_query = UserTaskResume.objects.select_related(
            'task',
            'task__user',
            'resume',
        ).filter(
            task__feed__feed_obj_id=feed_id,
            resume__resume_id=resume_id,
        )
        return accept_task_query[0] if accept_task_query else False

    @classmethod
    def add_coin_record(cls, accept_task, resume, coin, record_type):
        if not coin:
            return False

        desc = cls.RECORD_DESC_META[record_type]['desc']
        record = TaskCoinRecord(
            task=accept_task,
            upload_resume=resume,
            coin=coin,
            desc=desc,
            record_type=record_type,
        )
        record.save()
        return record

    @classmethod
    def is_malice_user(cls, user):
        return True if user.groups.filter(name='malice_partner').exists() else False

    @classmethod
    def grant_task_user(cls, feed_id, resume_id, coin_method, grant_type):
        feed_id = str(feed_id)
        resume_id = str(resume_id)
        task_resume = cls.get_task_resume(feed_id, resume_id)

        if not task_resume:
            return 0

        accept_task = task_resume.task
        resume = task_resume.resume
        grant_user = accept_task.user

        if cls.is_malice_user(grant_user):
            return 0

        _, coin = coin_method(
            grant_user,
            accept_task=accept_task,
            resume=resume,
            record_type=grant_type,
        )

        if coin:
            cls.add_coin_record(accept_task, resume, coin, grant_type)
            task_resume.resume_status = cls.RECORD_DESC_META[grant_type]['index']
            task_resume.save()

        return coin

    @classmethod
    def extra_grant_task_user(cls, feed_id, resume_id, grant_type):
        '''
        额外奖励方法
        用户升级就会增加额外金币
        '''
        feed_id = str(feed_id)
        resume_id = str(resume_id)
        task_resume = cls.get_task_resume(feed_id, resume_id)

        if not task_resume:
            return 0

        extra_meta = {
            'extra_download': {
                'desc': '简历被下载额外奖励',
                'coin_method': coin_utils.extra_download,
                'level_method': 'get_download_level',
            },
            'extra_interview': {
                'desc': '进入面试额外奖励',
                'coin_method': coin_utils.extra_interview,
                'level_method': 'get_interview_level',
            },
        }

        extra_setting = extra_meta[grant_type]
        accept_task = task_resume.task
        grant_user = accept_task.user

        if cls.is_malice_user(grant_user):
            return 0

        level_utils = PartnerLevelUtils(grant_user)
        grant_level_state = getattr(level_utils, extra_setting['level_method'])()
        extra_coin = grant_level_state.get('bonus_coin', 0)

        if not extra_coin:
            return 0

        resume = task_resume.resume
        coin_method = partial(extra_setting['coin_method'], coin=extra_coin)

        _, coin = coin_method(
            grant_user,
            accept_task=accept_task,
            resume=resume,
            record_type=grant_type,
        )
        if coin:
            cls.add_coin_record(accept_task, resume, coin, grant_type)
        return coin

    @classmethod
    def check_resume(cls, feed_id, resume_id):
        return cls.grant_task_user(
            feed_id,
            resume_id,
            coin_utils.check_resume,
            'check'
        )

    @classmethod
    def download_resume(cls, feed_id, resume_id):
        coin = cls.grant_task_user(
            feed_id,
            resume_id,
            coin_utils.download_resume,
            'download'
        )

        extra_coin = cls.extra_grant_task_user(
            feed_id,
            resume_id,
            'extra_download'
        )
        total_coin = coin + extra_coin
        return total_coin

    @classmethod
    def interview(cls, feed_id, resume_id):
        coin = cls.grant_task_user(
            feed_id,
            resume_id,
            coin_utils.interview,
            'interview'
        )

        extra_coin = cls.extra_grant_task_user(
            feed_id,
            resume_id,
            'extra_interview'
        )
        total_coin = coin + extra_coin
        return total_coin

    @classmethod
    def taking_work(cls, feed_id, resume_id, coin):
        grant_coin_method = partial(coin_utils.taking_work, coin=coin)
        coin = cls.grant_task_user(
            feed_id,
            resume_id,
            grant_coin_method,
            'taking_work'
        )

        return coin

    @classmethod
    def extra_taking_work(cls, feed_id, resume_id, coin):
        grant_coin_method = partial(coin_utils.extra_taking_work, coin=coin)
        coin = cls.grant_task_user(
            feed_id,
            resume_id,
            grant_coin_method,
            'extra_taking_work'
        )
        return coin

    @classmethod
    def accusation(cls, feed_id, resume_id):
        return cls.grant_task_user(
            feed_id,
            resume_id,
            coin_utils.accusation,
            'accusation'
        )

    @classmethod
    def verify_taking_work(cls, feed_id, resume_id):
        feed_id = str(feed_id)
        resume_id = str(resume_id)
        task_resume = cls.get_task_resume(feed_id, resume_id)

        if not task_resume:
            return False

        task_resume.verify = True
        task_resume.save()
        return task_resume

    @classmethod
    def resume_accusation(cls, feedback_record):
        resume_buy_record = get_object_or_none(
            ResumeBuyRecord,
            resume_id=feedback_record.resume_id,
            user=feedback_record.user,
        )
        if not resume_buy_record:
            return False

        feed_id, resume_id = resume_buy_record.feed_id, resume_buy_record.resume_id
        task_resume = cls.get_task_resume(feed_id, resume_id)
        if task_resume:
            reason = feedback_record.feedback_value or feedback_record.feedback_info.feedback_desc or ''
            task_resume.accusation_reason = reason
            task_resume.save()

        return cls.accusation(
            feed_id,
            resume_id,
        )


class PartnerNotify(object):

    @classmethod
    def resume_display_url(cls, resume_id, feed_id):
        return '/resumes/display/%s/?feed_id=%s' % (resume_id, feed_id)

    @classmethod
    def resume_follow_url(cls, follow_id):
        return '/partner/check_follow_msg/%s/' % follow_id

    @classmethod
    def upload_resume_notify(cls, user, resume_id, feed_id):
        notify.send(
            user,
            recipient=user,
            verb='互助伙伴向你推荐了一位候选人（<a class="c0091fa" href="%s">查看详情</a>）' % cls.resume_display_url(resume_id, feed_id),
            user_role='hr',
            notify_type='partner_upload_resume',
        )
        return True

    @classmethod
    def follow_resume_notify(cls, notify_user, msg):

        notify.send(
            notify_user,
            recipient=notify_user,
            verb=msg,
            user_role='hr',
            notify_type='partner_follow_resume',
        )
        return True

    @classmethod
    def reco_resume_task_notify(cls, upload_resume):
        notify_user = upload_resume.user
        verb = '你录入的简历%s，有了新的职位匹配（查看详情）' % upload_resume.name
        notify.send(
            notify_user,
            recipient=notify_user,
            verb=verb,
            user_role='hr',
            notify_type='partner_reco_resume_task',
        )
        return True


class PartnerUtils(object):

    @classmethod
    def is_partner(cls, user):
        partner_resume = user.uploadresume_set.all()
        return True if partner_resume else False


class PartnerLevelUtils(object):

    def __init__(self, user):
        self.user = user
        self.exp_state = self.user_exp_state()
        self.level_manage = self.get_level_manage()

    def user_exp_state(self):
        '''
        根据用户的奖励记录返回用户的经验状态
        返回:
        # 查看数量
        check_count
        # 下载数量
        download_count
        # 面试数量
        interview_count
        # 入职数量
        taking_work_count
        # 下载率 下载/查看
        download_ratio
        # 面试率 面试/下载
        interview_ratio
        入职率  面试/入职
        taking_work_ratio
        '''
        exp_state = TaskCoinRecord.objects.raw(
            '''
            SELECT `partner_taskcoinrecord`.`id`,
            SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'check' THEN 1 ELSE 0 END) AS `check_count`,
            SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'download' THEN 1 ELSE 0 END) AS `download_count`,
            SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'interview' THEN 1 ELSE 0 END) AS `interview_count`,
            SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'taking_work' THEN 1 ELSE 0 END) AS `taking_work_count`
            FROM `partner_taskcoinrecord`, `partner_uploadresume`
            WHERE `partner_taskcoinrecord`.`upload_resume_id` = `partner_uploadresume`.`id` and `partner_uploadresume`.`user_id` = %s
            ''' % self.user.id
        )[0]

        exp_state.download_count = get_int(exp_state.download_count)
        exp_state.interview_count = get_int(exp_state.interview_count)
        exp_state.taking_work_count = get_int(exp_state.taking_work_count)

        exp_state.download_ratio = float(exp_state.download_count) / float(exp_state.check_count) if exp_state.check_count > 0 else 0
        exp_state.interview_ratio = float(exp_state.interview_count) / float(exp_state.download_count) if exp_state.download_count > 0 else 0
        exp_state.taking_work_ratio = float(exp_state.taking_work_count) / float(exp_state.interview_count) if exp_state.interview_count > 0 else 0
        return exp_state

    def get_level_manage(self):
        level_manage = list(PartnerLevelManage.objects.all().values(
            'level_type',
            'exp',
            'bonus_coin',
            'level',
            'next_level',
            'next_exp',
            'next_bonus_coin',
            'is_max_level',
        ))
        return level_manage

    def get_level_by_type(self, level_type):
        level_meta = {
            0: {
                'exp_key': 'download_count',
                'ratio_key': 'download_ratio',
            },
            1: {
                'exp_key': 'interview_count',
                'ratio_key': 'interview_ratio',
            },
            2: {
                'exp_key': 'taking_work_count',
                'ratio_key': 'taking_work_ratio',
            },
        }
        setting = level_meta[level_type]
        exp = get_int(self.exp_state.__dict__[setting['exp_key']])

        for i in self.level_manage:
            if i['level_type'] != level_type:
                continue

            if i['exp'] <= exp < i['next_exp']:
                i['user_exp'] = exp
                return i

        return {
            'user_exp': exp,
        }

    def get_download_level(self):
        return self.get_level_by_type(0)

    def get_interview_level(self):
        return self.get_level_by_type(1)

    def get_taking_work_level(self):
        return self.get_level_by_type(2)

    def get_level_state(self):
        level_state = {
            'download_level': self.get_download_level(),
            'interview_level': self.get_interview_level(),
            'taking_work_level': self.get_taking_work_level(),
        }
        return level_state
