# coding: utf-8

import datetime
import json

from django.test import (
    TestCase,
    Client,
)

from .models import TaskFinishedStatus
from django.contrib.auth.models import User
#from django.http.request import HttpRequest
from django.core.urlresolvers import reverse
from feed.models import Feed
from resumes.models import UserWatchResume
from transaction.models import (
    ResumeBuyRecord,
    DownloadResumeMark,
)
from jobs.models import SendCompanyCard
from app.vip.models import UserOrder
from app.partner.models import UploadResume
from app.activity.models import QuestionnaireResult
from app.promotion_point.models import PromotionPointRecord
from .task_finished_judge import resume_read_finished


class TaskSystemTest(TestCase):

    fixtures = [
        'user.json',
        'resumedata.json',
        'userprofile.json',
        'weixin.json',
        'task.json',
        'resume_buy_record.json',
        'userorder.json',
    ]

    def setUp(self):
        self.c = Client()
        self.c.login(username='runforever@163.com', password='199o1113')
        self.user = User.objects.get(username='runforever@163.com')

    def test_get_task_status_list(self):
        result = self.c.get(reverse('task-list'))
        self.assertEqual(result.status_code, 200)

    @ resume_read_finished
    def do_resume_read_task(self, request):
        return True

    def do_feedback_task(self):
        return True

    def do_task(self, task_code):

        if task_code == 'commit_customization':
            feed = Feed(
                user=self.user,
                deleted=False,
            )
            feed = feed.save()
            return True

#        if task_code == 'lookup_resume':
#            request = HttpRequest()
#            request.user = self.user
#            self.do_resume_read_task(request)

        if task_code == 'collect_resume':
            watch_record = UserWatchResume(
                user=self.user,
                resume_id='567cd2bd563310078dda3db9',
                feed_id='522db684fb6dec1d505249f9',
                add_time=datetime.datetime.now(),
                type=1,
            )
            watch_record = watch_record.save()
            return True

        if task_code == 'download_resume':
            buy_record = ResumeBuyRecord(
                user=self.user,
                resume_id='',
                resume_url='',
                status='LookUp'
            )
            buy_record = buy_record.save()
            return True

        if task_code == 'mark_resume':
            buy_record = ResumeBuyRecord.objects.all()
            buy_record = buy_record[0]
            mark_record = DownloadResumeMark(
                buy_record=buy_record,
                mark_time=datetime.datetime.now()
            )
            mark_record = mark_record.save()
            return True

#        if task_code == 'feedback_resume':
#            result = self.c.post()
#            self.assertEqual(result.status_code, 200)

        if task_code == 'buy_package':
            order = UserOrder.objects.all()
            order = order[0]
            order.order_status = 'paid'
            order.order_type = 1
            order = order.save()
            return True

        if task_code == 'send_company_card':
            send_record = SendCompanyCard(send_user=self.user)
            send_record.save()
            return True

        if task_code == 'mutual_recruitment':
            upload_record = UploadResume(user=self.user)
            upload_record.save()
            return True

        if task_code == 'user_portrait':
            questionnaire_record = QuestionnaireResult(user=self.user)
            questionnaire_record.save()
            return True

    def test_do_task(self):
        task_code_list = [
            'commit_customization',
#            'lookup_resume',
            'collect_resume',
            'mark_resume',
            'download_resume',
#            'feedback_resume',
            'buy_package',
            'send_company_card',
            'mutual_recruitment',
            'user_portrait',
        ]
        for task_code in task_code_list:
            self.assertEqual(self.do_task(task_code), True)
        print TaskFinishedStatus.objects.all()

        task_datas = [
            '1_commit_customization',
#            '1_lookup_resume',
            '1_collect_resume',
            '1_mark_resume',
            '1_download_resume',
#            '1_feedback_resume',
            '1_buy_package',
            '1_send_company_card',
            '1_mutual_recruitment',
            '1_user_portrait',
        ]

        for task_data in task_datas:
            data = {
                'task_data': task_data
            }
            result = self.c.post(
                reverse('receive-reward'),
                data
            )
            self.assertEqual(result.status_code, 200)
            print data
            self.assertEqual(json.loads(result.content).get('msg'), 'success')
