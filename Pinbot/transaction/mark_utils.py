# coding: utf-8

import datetime
from django.db.models import Q

from .models import (
    ResumeBuyRecord,
    DownloadResumeMark,
    UserMarkLog,
)

from Brick.App.system.models import (
    ResumeMarkSetting,
)

from Pinbot.settings import (
    MARK_TIME
)

from pin_utils.django_utils import (
    get_today,
    get_object_or_none,
)


class MarkUtils(object):

    @classmethod
    def has_unmark_record(cls, user):
        '''
        查找未标记过的简历和举报失败的未标记简历
        '''
        today = get_today()
        time_limit = today + datetime.timedelta(days=-7)

        if time_limit < MARK_TIME:
            return False

        unmark_record = ResumeBuyRecord.objects.filter(
            Q(resume_mark=None) | Q(resume_mark__accu_status=3),
            user=user,
            finished_time__gt=MARK_TIME,
            finished_time__lte=time_limit,
            status='LookUp',
        )
        return True if unmark_record else False

    @classmethod
    def add_accu_mark(cls, user, resume_id, accu_type):
        if accu_type != 'accusation':
            return False

        buy_record = get_object_or_none(
            ResumeBuyRecord,
            user=user,
            resume_id=resume_id,
        )
        if hasattr(buy_record, 'resume_mark'):
            return False

        mark = get_object_or_none(
            ResumeMarkSetting,
            code_name='accusation',
        )

        resume_mark = DownloadResumeMark(
            buy_record=buy_record,
            current_mark=mark,
            accu_status=1,
        )
        resume_mark.save()

        mark_log = UserMarkLog(
            resume_mark=resume_mark,
            mark=mark,
        )
        mark_log.save()
        return resume_mark

    @classmethod
    def accu_mark_result(cls, user, resume_id, result):
        buy_record = get_object_or_none(
            ResumeBuyRecord,
            user=user,
            resume_id=resume_id,
        )

        if hasattr(buy_record, 'resume_mark'):
            resume_mark = buy_record.resume_mark
        else:
            resume_mark = DownloadResumeMark(
                buy_record=buy_record,
            )

        if result == 'pass':
            mark = get_object_or_none(
                ResumeMarkSetting,
                code_name='accu_success',
            )
            resume_mark.accu_status = 2
            resume_mark.last_mark = resume_mark.current_mark
            resume_mark.current_mark = mark
        else:
            mark = get_object_or_none(
                ResumeMarkSetting,
                code_name='accu_fail',
            )
            resume_mark.current_mark = mark
            resume_mark.accu_status = 3

        resume_mark.save()
        mark_log = UserMarkLog(
            resume_mark=resume_mark,
            mark=mark,
        )
        mark_log.save()
        return resume_mark

    @classmethod
    def has_mark_record(cls, user, resume_id):
        buy_record = get_object_or_none(
            ResumeBuyRecord,
            user=user,
            resume_id=resume_id,
        )
        return True if buy_record and hasattr(buy_record, 'resume_mark') else False
