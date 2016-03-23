# coding: utf-8

import datetime

from django.http.request import HttpRequest
from Pinbot.settings import ON_LINE_TIME
from feed.models import (
    FeedResult,
    Feed2,
)
from app.task_system.models import (
    TaskFinishedStatus,
    Task,
)


def check_special_task(task_code, current_task, current_count):

    def continue_read_resume_task_op(current_task, current_count):
        if (
                current_task.finished_time is not None and
                current_task.finished_time.date() == datetime.datetime.today().date() or
                current_count == 0
        ):
            return 0
        task_count = current_task.task.task_count
        current_count = current_count % task_count
        current_count = task_count if current_count == 0 else current_count
        return current_count

    task_code_dict = {
        'continue_look_up_resume': continue_read_resume_task_op,
    }

    return task_code_dict.get(task_code)(current_task, current_count) if task_code in task_code_dict else current_count


def deal_simple_repeat_task(current_task):
    current_task.current_process = current_task.current_process + 1
    current_task.repeat_times = current_task.repeat_times + 1
    current_task.save()
    return True


def deal_ordinary_signal_task(current_task, task):
    finished_time = datetime.datetime.now()
    reward_due_time = None
    if task.reward_due_time is not None:
        reward_due_time = finished_time + datetime.timedelta(days=task.reward_due_time)
    current_task.current_process = current_task.current_process + 1 if not task.task_count else task.task_count
    current_task.finished_time = finished_time
    current_task.reward_due_time = reward_due_time
    current_task.finished_status = 2
    current_task.repeat_times = current_task.repeat_times + 1
    current_task.save()
    return True


def deal_ordinary_count_task(current_task, current_count):
    if current_count is None:
        current_task.current_process = current_task.current_process + 1
    else:
        current_task.current_process = current_count
    current_task.save()
    return True


def create_or_update_task_status(current_task, task, current_count):

    is_ordinary_signal_task_finished = (
        (
            current_task.current_process + 1 >= task.task_count
            and current_count is None
        )
        or current_count >= task.task_count
    )

    task_has_finished = current_task.finished_status == 2
    is_simple_repeat_task = current_task.task.task_level == 4

    if task_has_finished:
        return None
    if is_simple_repeat_task:
        return deal_simple_repeat_task(current_task)
    elif is_ordinary_signal_task_finished:
        return deal_ordinary_signal_task(current_task, task)
    else:
        return deal_ordinary_count_task(current_task, current_count)


def get_or_create_record(user, task_code, current_count=None):
    task_query = Task.objects.filter(
        task_code=task_code,
        is_apply=True,
    )
    for task in task_query:
        current_task = TaskFinishedStatus.objects.get_or_create(
            user=user,
            task=task,
            task_times=task.task_count,
        )
        current_task = current_task[0]
        current_count = check_special_task(task_code, current_task, current_count)
        create_or_update_task_status(current_task, task, current_count)

    return True


def get_request(args):
    for arg in args:
        if isinstance(arg, HttpRequest):
            return arg
    return False


def resume_read_finished(func):
    def f_record_task_finished(*args, **kwargs):
        request = get_request(args)
        user = request.user
        result = func(*args, **kwargs)
        if not user.is_authenticated():
            return result
        if result:
            feeds = list(Feed2.objects.filter(
                username=user.username
            ).only('id'))

            read_num = FeedResult.objects.filter(
                feed__in=feeds,
                user_read_status='read',
                user_read_time__gt=ON_LINE_TIME,
            ).count()
            get_or_create_record(user, 'lookup_resume', current_count=read_num)
        return result
    return f_record_task_finished


def feedback_finished(func):
    def f_record_task_finished(*args, **kwargs):
        request = get_request(args)
        user = request.user
        result = func(*args, **kwargs)
        if not user.is_authenticated():
            return result
        feeds = list(Feed2.objects.filter(
            username=user.username
        ).only('id'))
        feedback_num = FeedResult.objects.filter(
            feed__in=feeds,
            is_recommended=False,
            published=True,
            user_feedback_time__gt=ON_LINE_TIME,
        ).count()
        get_or_create_record(user, 'feedback_resume', current_count=feedback_num)
        return result
    return f_record_task_finished


def look_up_extention(func):
    def f_look_up_extention(*args, **kwargs):
        request = get_request(args)
        user = request.user
        result = func(*args, **kwargs)
        is_extend_request = int(request.GET.get('extend_match', 0))
        if not is_extend_request:
            return result
        get_or_create_record(user, 'look_up_extention')
        return result
    return f_look_up_extention


def continue_read_resume(func):
    def f_record_task_finished(*args, **kwargs):
        request = get_request(args)
        user = request.user
        result = func(*args, **kwargs)
        if not user.is_authenticated():
            return result
        if result:
            feeds = list(Feed2.objects.filter(
                username=user.username
            ).only('id'))

            # time_terval = datetime.datetime.today() - datetime.timedelta(days=15)
            time_terval = datetime.datetime(year=2016, month=3, day=12)
            read_time_list = FeedResult.objects.filter(
                feed__in=feeds,
                user_read_status='read',
                user_read_time__gt=time_terval,
            ).values_list(
                'user_read_time'
            )
            current_count = get_continue_read_day(read_time_list)
            get_or_create_record(user, 'continue_look_up_resume', current_count)
        return result
    return f_record_task_finished


def get_continue_read_day(read_time_list):

    today=datetime.datetime.today()
    today_date = datetime.datetime(today.year, today.month, today.day)
    time_delta = datetime.timedelta(days=1)

    continue_read_day = 0

    read_count = 0
    the_date = today_date
    flag = True
    while flag:
        history_read_count = len(filter(lambda x: x > the_date, read_time_list))
        if history_read_count <= read_count or continue_read_day > 15:
            break
        read_count = history_read_count
        the_date = the_date - time_delta
        continue_read_day += 1

    return continue_read_day
