# coding: utf-8
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from users.models import (
    UserProfile
)

def convert_emai_bind_status():

    ret = UserProfile.objects.filter(
        is_email_bind=False
    ).update(
        is_email_bind=True
    )
    print 'convert all emai bind status success!'

if __name__ == '__main__':

    convert_emai_bind_status()