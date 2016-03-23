# coding: utf-8

import datetime

from django.views.generic import View
from django.shortcuts import render

from pin_utils.django_utils import (
    JsonResponse,
    get_int,
)

from ..models import AdminSchedule
from ..forms.calendar_forms import AdminScheduleForm

from transaction.models import InterviewAlarm
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.django_utils import (
    get_today,
    get_tomorrow,
)


class Calendar(LoginRequiredMixin, View):

    def get(self, request):
        template_name = 'calendar/calendar.html'
        return render(
            request,
            template_name,
        )


class CalendarEvents(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user

        schedules = []
        schedule_query = AdminSchedule.objects.filter(
            user=user
        )
        alarm_query = InterviewAlarm.objects.select_related(
            'buy_record__user__userprofile__company_name',
            'buy_record__resume_id',
            'buy_record__feed_id',
        ).filter(
            buy_record__user__crm_client_info__admin=user
        )
        for alarm in alarm_query:
            backgroundColor = 'black' if alarm.interview_time < datetime.datetime.today() else 'green'
            schedules.append({
                'id': 'alarm_id_{0}'.format(alarm.id),
                'title': '客户面试提醒：{0}'.format(alarm.buy_record.user.userprofile.company_name),
                'start': alarm.interview_time.isoformat(),
                'backgroundColor': backgroundColor,
                'url': "/resumes/display/{0}/?feed_id={1}".format(
                    alarm.buy_record.resume_id,
                    alarm.buy_record.feed_id,
                ),
                'borderColor': backgroundColor,
                'editable': False,
            })
        for schedule in schedule_query:
            backgroundColor = 'black' if schedule.start_time < datetime.datetime.today() else schedule.backgroundcolor
            schedules.append({
                'id': schedule.id,
                'title': schedule.title,
                'start': schedule.start_time.isoformat(),
                'url': schedule.url,
                'backgroundColor': backgroundColor,
                'borderColor': backgroundColor,
                'editable': False,
            })

        return JsonResponse(schedules)

    def post(self, request):

        user = request.user
        schedule_id = get_int(request.POST.get('schedule_id'))
        schedule_instance = AdminSchedule.objects.filter(
            id=schedule_id,
            user=user,
        ).first()
        form = AdminScheduleForm(request.POST, instance=schedule_instance) if schedule_instance else AdminScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = user
            schedule.save()
            return JsonResponse({
                'status': 'ok',
                'msg': 'success'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'msg': 'form error'
            })


class DeleteCalendarEvents(LoginRequiredMixin, View):

    def post(self, request):

        event_id = request.POST.get('id')

        AdminSchedule.objects.filter(
            id=int(event_id)
        ).delete()
        return JsonResponse({
            'status': 'ok',
            'msg': 'success',
        })


class CalendarUndo(LoginRequiredMixin, View):

    def get(self, request):

        user = request.user

        custom_schedule_count = AdminSchedule.objects.filter(
            user=user,
            start_time__gt=get_today(),
            start_time__lt=get_tomorrow()
        ).count()

        alarm_count = InterviewAlarm.objects.filter(
            buy_record__user__crm_client_info__admin=user,
            interview_time__gt=get_today(),
            interview_time__lt=get_tomorrow(),
        ).count()

        return JsonResponse({
            'all_count': custom_schedule_count + alarm_count,
            'custom_schedule_count': custom_schedule_count,
            'alarm_count': alarm_count,
        })
