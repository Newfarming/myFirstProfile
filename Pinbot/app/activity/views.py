# coding: utf-8

import datetime
import bleach

from django.views.generic import (
    TemplateView,
    View,
)

from models import (
    Questionnaire,
    QuestionnaireResult,
    QuestionnaireAnwserResult,
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
)
from pin_utils.django_utils import JsonResponse


class NewPromotionView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        context = super(NewPromotionView, self).get_context_data(**kwargs)
        now = datetime.datetime.now()
        context['now_time'] = now.strftime('%s')
        return context


class Questions(LoginRequiredMixin, View):

    def get(self, request):

        question_query = Questionnaire.objects.filter(
            is_active=True
        ).order_by(
            'order'
        )

        questions = [
            {
                'question_id': question.id,
                'order': question.order,
                'question_type': question.question_type,
                'anwser_type': question.anwser_type,
                'question': question.question,
                'is_other_option': True if question.anwser_type in ['single_choies_or_text', 'multi_choies_or_text'] else False,
                'anwsers_count': len(question.anwser_options.split(';')),
                'anwser_options': {
                    option.split(':')[0]: option.split(':')[1]
                    for option in question.anwser_options.split(';')
                } if question.anwser_options else "",
            } for question in question_query
        ]
        question_types = [x[0] for x in Questionnaire.QUESTION_TYPE_META]
        question_types_zh_CN = [x[1] for x in Questionnaire.QUESTION_TYPE_META]

        return JsonResponse({
            'questions': questions,
            'question_types': question_types,
            'question_types_count': len(question_types),
            'question_types_zh_CN': question_types_zh_CN,
        })


class QuestionnaireFeedback(LoginRequiredMixin, View):

    def post(self, request):

        user = request.user
        data = request.JSON
        anwsers = data.get('anwsers')
        if not anwsers:
            return JsonResponse({
                'status': 'error',
                'msg': '格式错误'
            })

        is_commited = QuestionnaireResult.objects.filter(user=user)
        if is_commited:
            return JsonResponse({
                'status': 'error',
                'msg': '您已经提交过了,请勿重复提交'
            })
        for anwser in anwsers:
            if not anwser.get('answer'):
                return JsonResponse({
                    'status': 'error',
                    'msg': '填写不完整'
                })

        questionnaire_page = QuestionnaireResult(user=user)
        questionnaire_page.save()

        anwsers_query = [
            QuestionnaireAnwserResult(
                question_id=int(anwser.get('question_id')),
                anwser=bleach.clean(
                    anwser.get('answer'),
                    tags=[],
                    strip=True
                ).strip(','),
                questionnaire_page=questionnaire_page,
            ) for anwser in anwsers
        ]
        QuestionnaireAnwserResult.objects.bulk_create(
            anwsers_query
        )

        return JsonResponse({
            'status': 'ok',
            'msg': '提交成功'
        })