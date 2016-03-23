# coding: utf-8

import datetime
from .models import (
    Task,
    TaskFinishedStatus,
)
from jobs.models import (
    Company
)


class TaskCheckMixin(object):

    def add_task_finished_record(self, user, task):
        _, task_code = task.split('_', 1)
        task_query = Task.objects.filter(task_code=task_code)
        if not task_query:
            return False
        task = task_query[0]
        reward_due_time = task.reward_due_time
        finished_time = datetime.datetime.now()
        if reward_due_time is not None:
            reward_due_time = finished_time + datetime.timedelta(days=reward_due_time)
        TaskFinishedStatus.objects.create(
            user=user,
            task=task,
            reward_status=1,
            finished_time=finished_time,
            finished_status=2,
            reward_due_time=reward_due_time,
            task_times=task.task_count,
            current_process=1,
        )
        return True

    def check_user_isactive(self, user, task):
        if user.is_active is True:
            self.add_task_finished_record(user, task)
            return True
        return False

    def check_user_weixin_isbind(self, user, task):
        if hasattr(user, 'weixin_user'):
            weixin_user = user.weixin_user
            if weixin_user.is_bind:
                self.add_task_finished_record(user, task)
                return True
            return False
        return False

    def check_user_email_isbind(self, user, task):
        if not hasattr(user, 'userprofile'):
            return False
        if user.userprofile.is_email_bind is True:
            self.add_task_finished_record(user, task)
            return True
        return False

    def check_user_company_isdetail(self, user, task):
        user_company_info = Company.objects.filter(
            user=user
        )
        is_detail = (
            user_company_info
            and user_company_info[0].company_name
            and user_company_info[0].key_points
            and user_company_info[0].desc
            and user_company_info[0].category
        )
        if is_detail:
            self.add_task_finished_record(user, task)
            return True
        return False

    def check_task_is_finished(self, user, task_code):
        task_check_mapper = {
            '1_is_user_active': self.check_user_isactive,
            '1_is_user_email_bind': self.check_user_email_isbind,
            '1_is_user_weixin_bind': self.check_user_weixin_isbind,
            '1_is_user_company_detail': self.check_user_company_isdetail,
        }
        return task_check_mapper.get(task_code)(user, task_code)
