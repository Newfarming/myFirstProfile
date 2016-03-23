# coding: utf-8

import datetime
import requests

from django.db import transaction

from .models import (
    RecommendJob,
    CompanyCardJob,
)
from .exception import CompanyCardInterestExeception
from Brick.App.my_resume.models import (
    Resume,
)
from Brick.App.chat.chat_utils import (
    ChatUtils,
)
from Brick.App.notify.notify_utils import (
    NotifyUtils,
)
from Brick.Utils.django_utils import (
    get_object_or_none,
    get_int,
)
from Brick.settings import COMPANY_CARD_API


class JobUtils(object):

    @classmethod
    def download_send_resume(cls, job_id, hr_user):
        job_id = get_int(job_id)
        if not job_id:
            return False

        recommend_job_query = RecommendJob.objects.filter(
            id=job_id,
            hr_user=hr_user,
            action='send',
        )
        if not recommend_job_query:
            return False

        now = datetime.datetime.now()
        recommend_job = recommend_job_query[0]
        with transaction.atomic():
            recommend_job.company_action = 'download'
            recommend_job.company_action_time = now
            job_card = recommend_job.job
            hr_user = recommend_job.hr_user
            user = recommend_job.user
            recommend_job.save()
            ChatUtils.add_chat(job_card, hr_user, user, chat_type='feed')
            NotifyUtils.company_notify(recommend_job, 'interview')

        return True

    @classmethod
    def get_recommend_job(cls, job_id, hr_user):
        recommend_job_query = RecommendJob.objects.select_related(
            'user',
        ).filter(
            id=job_id,
            hr_user=hr_user,
            action='send',
        )

        if not recommend_job_query:
            return False

        recommend_job = recommend_job_query[0]
        return recommend_job

    @classmethod
    def send_company_card(cls, hr_user, job, resume_id, token):
        if not resume_id:
            return False

        resume = get_object_or_none(
            Resume,
            resume_id=resume_id,
        )
        not_need_send = (not resume or resume.user == hr_user)

        if not_need_send:
            return False

        company_card_job = CompanyCardJob(
            job=job,
            hr_user=hr_user,
            user=resume.user,
            token=token,
        )
        company_card_job.save()
        return company_card_job

    @classmethod
    def card_feedback(cls, card_job, feed_type):
        token = card_job.token
        interest = 'true' if feed_type == 'accept' else 'false'

        url = COMPANY_CARD_API.format(token=token, interest=interest)
        try:
            result = requests.get(url, params={'brick': 'true'})
        except:
            raise CompanyCardInterestExeception

        if result.status_code != 200:
            raise CompanyCardInterestExeception
        return result

    @classmethod
    def company_card_interest(cls, job, job_id, interest_type):
        job_id = get_int(job_id)

        if not job_id:
            return False

        company_card_job = get_object_or_none(
            CompanyCardJob,
            job=job,
            id=job_id,
            status='waiting',
        )

        if not company_card_job:
            return False

        now = datetime.datetime.now()
        if interest_type == 1:
            company_card_job.status = 'accept'
        else:
            company_card_job.status = 'reject'

        company_card_job.action_time = now
        company_card_job.save()
        return company_card_job
