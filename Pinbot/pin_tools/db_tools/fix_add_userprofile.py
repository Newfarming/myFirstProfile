# coding: utf-8

import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from django.contrib.auth.models import User
from users.models import UserProfile
from app.vip.runtime.self_service import SelfServiceUtils


def add_userprofile(username):

    users = User.objects.filter(username=username)
    if not users:
        print 'error username'
        return False
    user = users[0]
    if not hasattr(user, 'userprofile'):
        userprofile = UserProfile(
            user=user,
            user_email=user.username,
            company_name=user.first_name,
            phone='',
            ip='127.0.0.1',
        )
        userprofile.save()
        SelfServiceUtils.active_experience_service(user)
        print 'create userprofile success'
        return True
    else:
        print 'user had a userprofile'
        return True

if __name__ == '__main__':
    username=sys.argv[1]
    add_userprofile(username)
