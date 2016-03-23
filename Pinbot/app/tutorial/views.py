# coding: utf-8

import json

from django.views.generic import View

from .models import(
    InterviewTermQuestions,
)
from .form import FeedBackTextForm
from pin_utils.django_utils import(
    JsonResponse,
)
from pin_utils.mixin_utils import MaliceMixin


class InterviewTerm(View):

    def type_question(self, query, type):
        questions = filter(lambda x: x.question_type == type, query)
        return [
            {'question': question.question, 'anwser': question.anwser, 'id': question.id}
            for question in questions
        ]

    def get(self, request):
        all_questions_query = InterviewTermQuestions.objects.all()
        data = {
            'question': self.type_question(all_questions_query, type=1),
            'meet': self.type_question(all_questions_query, type=2),
        }
        return JsonResponse(data)


class FeedBack(View, MaliceMixin):

    MAX_ERROR_TIMES = 5
    EXPIRE_SECOND = 60 * 10
    MALICE_IP_PREFIX = 'feedback'
    METHOD = 'POST'

    def post(self, request):

        form = FeedBackTextForm(json.loads(request.body))
        if not form.is_valid():
            return JsonResponse({
                'status': 'error',
                'msg': form.get_first_errors()
            })
        if self.malice_ip():
            return JsonResponse({
                'status': 'error',
                'msg': '发送过于频繁'
            })
        form.save()
        return JsonResponse({
            'status': 'ok',
            'msg': '反馈成功'
        })
