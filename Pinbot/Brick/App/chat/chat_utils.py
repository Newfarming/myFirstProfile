# coding: utf-8

from .models import Chat

from Brick.App.my_resume.resume_utils import (
    ResumeUtils,
)

from Brick.Utils.django_utils import (
    get_object_or_none,
)


class ChatUtils(object):

    @classmethod
    def add_chat(cls, job_card, hr_user, user, chat_type='job'):

        if chat_type == 'job':
            chat = get_object_or_none(
                Chat,
                job_hunter=user,
                hr=hr_user,
                job=job_card,
            )

            if not chat:
                resume = ResumeUtils.get_resume(user)
                chat = Chat(
                    job_hunter=user,
                    hr=hr_user,
                    job=job_card,
                    resume=resume,
                )
                chat.save()
        else:
            chat = get_object_or_none(
                Chat,
                job_hunter=user,
                hr=hr_user,
                feed=job_card,
                chat_type=chat_type,
            )

            if not chat:
                resume = ResumeUtils.get_resume(user)
                chat = Chat(
                    job_hunter=user,
                    hr=hr_user,
                    feed=job_card,
                    resume=resume,
                    chat_type=chat_type,
                )
                chat.save()
        return chat
