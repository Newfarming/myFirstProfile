# coding: utf-8

from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from .models import (
    UserToken,
)

from Brick.Utils.email.send_mail import (
    asyn_send_mail,
)


class SendMailMixin(object):
    email_template = 'account_active_email.html'
    subject = '聘宝-验证邮件'
    url_name = 'account-valid-active-email'
    token_type = 'register'

    def send_active_email(self, user):
        token = default_token_generator.make_token(user)
        email = user.userprofile.notify_email
        valid_url = self.request.build_absolute_uri(
            reverse(self.url_name, args=(token, ))
        )

        html = render_to_string(
            self.email_template,
            {
                'username': email,
                'valid_url': valid_url,
                'request': self.request,
            }
        )

        user_tokens = user.user_token.filter(
            token_type=self.token_type
        )
        if user_tokens:
            user_token = user_tokens[0]
        else:
            user_token = UserToken(
                user=user,
                token=token,
                token_type=self.token_type
            )
        user_token.token = token
        user_token.active = True
        user_token.save()
        asyn_send_mail.delay(email, self.subject, html)
        return True
