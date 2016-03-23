# coding: utf-8

import datetime

from django.db.models import Q

from pin_celery.celery_app import app

from .models import (
    RecoResumeTask,
    UploadResume,
    UserTaskResume,
)
from feed.models import (
    Feed,
    FeedResult,
)


class SyncRecoResumeTask(object):

    def create_reco_resume_task(self, fr):
        '''
        同步feed_result里的任务到简历匹配任务里

        1. 同一个人上传的简历和自己的定制不能同步
        2. 已经接受过该定制用户其他定制的简历不能同步
        3. 同步过的任务不能重复同步
        4. 如果is_recommended是False则不展示曾经同步过的任务
        5. 同步给管理员的任务不能同步
        '''
        feed_str_id = str(fr.feed.id)
        resume_id = str(fr.resume.id)

        feed_query = Feed.objects.select_related(
            'user',
        ).filter(
            feed_obj_id=feed_str_id,
        )
        if not feed_query:
            return False

        resume_query = UploadResume.objects.select_related(
            'user',
        ).filter(
            resume_id=resume_id,
        )
        if not resume_query:
            return False

        feed = feed_query[0]
        resume = resume_query[0]

        # 不能把任务同步给自己
        if feed.user == resume.user:
            return False

        # 管理员的定制不能同步
        if feed.user.is_staff:
            return False

        upload_resume_list = list(UserTaskResume.objects.filter(
            task__feed__user=feed.user,
            resume__user=resume.user,
        ).values_list('resume__id', flat=True))

        # 同一份简历不能同步给同一个人的不同定制中
        if resume_id in upload_resume_list:
            return False

        if fr.is_recommended:
            # 不能同步同一个HR的不同定制给同一个简历
            has_sync = RecoResumeTask.objects.filter(
                upload_resume=resume,
                feed__user=feed.user,
            )

            if has_sync:
                return False

            reco_task = RecoResumeTask(
                upload_resume=resume,
                feed=feed,
                user=resume.user,
                reco_index=fr.reco_index,
            )
            reco_task.save()
            return reco_task
        else:
            sync_resume_task_query = RecoResumeTask.objects.filter(
                upload_resume=resume,
                feed=feed,
                action=0,
            )

            if sync_resume_task_query:
                sync_resume_task = sync_resume_task_query[0]
                sync_resume_task.display = False
                sync_resume_task.save()
                return sync_resume_task
            return False

    def sync_task(self):
        feed_results = FeedResult.objects(
            resume_source='talent_partner',
            sync_partner=False,
        )
        for fr in feed_results:
            self.create_reco_resume_task(fr)
            fr.sync_partner = True
            fr.save()
        return True


class CleanRecoTask(object):

    def clean_reco_task(self):
        '''
        清理过期的任务
        清理无法认领的任务
        '''

        now = datetime.datetime.now()
        RecoResumeTask.objects.select_related(
            'feed',
            'feed__user',
        ).filter(
            Q(feed__deleted=True) | Q(feed__feed_expire_time__lt=now),
            action=0,
        ).delete()

        reco_resume_task = RecoResumeTask.objects.select_related(
            'feed',
            'feed__user',
            'upload_resume',
        ).filter(
            action=0
        )

        delete_list = []
        for resume_task in reco_resume_task:
            feed_user = resume_task.feed.user
            resume = resume_task.upload_resume

            has_task = UserTaskResume.objects.filter(
                task__feed__user=feed_user,
                resume=resume,
            ).exists()

            if has_task:
                delete_list.append(resume_task.id)

        RecoResumeTask.objects.filter(
            id__in=delete_list,
        ).delete()


reco_resume_task = SyncRecoResumeTask()
asyn_reco_resume_task = app.task(
    name='pinbot-reco-resume-task'
)(reco_resume_task.sync_task)

clean_task = CleanRecoTask()
clean_reco_resume_task = app.task(
    name='pinbot-clean-reco-task'
)(clean_task.clean_reco_task)
