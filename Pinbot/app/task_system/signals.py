# coding: utf-8

import datetime

from Pinbot.settings import ON_LINE_TIME
from .models import (
    TaskFinishedStatus,
    TaskFinishedNotify,
)
from .task_finished_judge import get_or_create_record
from feed.models import (
    Feed,
)
from resumes.models import (
    UserWatchResume
)
from transaction.models import (
    DownloadResumeMark,
    ResumeBuyRecord
)
from jobs.models import SendCompanyCard
from app.promotion_point.models import PromotionPointRecord
from app.vip.models import UserOrder
from app.activity.models import QuestionnaireResult
from app.partner.models import (
    UploadResume,
    UserAcceptTask,
)

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=ResumeBuyRecord)
def download_resume_finished(sender, **kwargs):
    user = kwargs['instance'].user
    buy_record_count = ResumeBuyRecord.objects.filter(
        user=user,
        op_time__gt=ON_LINE_TIME
    ).count()
    get_or_create_record(user, 'download_resume', current_count=buy_record_count)


@receiver(pre_save, sender=Feed)
def commit_feed_finished(sender, **kwargs):
    user = kwargs['instance'].user
    if kwargs['instance'].deleted is not True:
        get_or_create_record(user, 'commit_customization')


@receiver(pre_save, sender=UserWatchResume)
def collect_resume_finished(sender, **kwargs):
    user = kwargs['instance'].user
    watchcount = UserWatchResume.objects.filter(
        user=user,
        add_time__gt=ON_LINE_TIME,
        type=1,
    ).count()
    if kwargs['instance'].type == 1:
        watchcount = watchcount + 1
    if kwargs['instance'].type == 0:
        watchcount = watchcount - 1
    get_or_create_record(user, 'collect_resume', current_count=watchcount)


@receiver(pre_save, sender=DownloadResumeMark)
def resume_mark_finished(sender, **kwargs):
    user = kwargs['instance'].buy_record.user
    mark_count = DownloadResumeMark.objects.filter(
        buy_record__user=user,
        mark_time__gt=ON_LINE_TIME
    ).count()
    mark_count += 1
    get_or_create_record(user, 'mark_resume', current_count=mark_count)


@receiver(pre_save, sender=TaskFinishedStatus)
def user_task_status_change(sender, **kwargs):
    if kwargs['instance'].finished_status == 2:
        user_status = TaskFinishedNotify.objects.get_or_create(
            user=kwargs['instance'].user,
        )
        user_status[0].notify_status = 'reward_to_receive'
        user_status[0].save()


@receiver(pre_save, sender=UserOrder)
def buy_backage(sender, **kwargs):
    user = kwargs['instance'].user
    if kwargs['instance'].order_status == 'paid' and kwargs['instance'].order_type in [1, 2]:
        get_or_create_record(user, 'buy_package')


@receiver(pre_save, sender=SendCompanyCard)
def send_company_card(sender, **kwargs):
    user = kwargs['instance'].send_user
    get_or_create_record(user, 'send_company_card')


@receiver(pre_save, sender=PromotionPointRecord)
def invite_user(sender, **kwargs):
    user = kwargs['instance'].promotion_user
    get_or_create_record(user, 'invite_user')


@receiver(pre_save, sender=UploadResume)
def mutual_recruitment(sender, **kwargs):
    user = kwargs['instance'].user
    create_time = kwargs['instance'].create_time
    upload_count = UploadResume.objects.filter(
        user=user,
        create_time__gt=ON_LINE_TIME,
    ).count()
    upload_count = upload_count + 1 if create_time is None else upload_count
    get_or_create_record(user, 'mutual_recruitment', current_count=upload_count)


@receiver(pre_save, sender=UserAcceptTask)
def claim_task(sender, **kwargs):
    user = kwargs['instance'].user
    if datetime.datetime.today().weekday() in [5, 6]:
        get_or_create_record(user, 'claim_task_weekend')
    else:
        get_or_create_record(user, 'claim_task_weekday')


@receiver(pre_save, sender=QuestionnaireResult)
def questionnaire(sender, **kwargs):
    user = kwargs['instance'].user
    get_or_create_record(user, 'user_portrait')
