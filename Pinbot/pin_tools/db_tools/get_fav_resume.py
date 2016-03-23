# coding: utf-8

import datetime

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from resumes.models import (
    UserWatchResume
)
from pin_utils.django_utils import (
    get_date_range
)

start_report_date = datetime.date(2016, 02, 16)
end_report_date = datetime.date(2016, 03, 02)

def get_favs(add_time):

    add_time_2 = add_time + datetime.timedelta(days=1)
    favs = UserWatchResume.objects.filter(
        add_time__gte=add_time,
        add_time__lt=add_time_2,
        type=1
    )
    for f in favs:
        resume_link = 'http://www.pinbot.me/resumes/display/{0}/'.format(f.resume_id)
        print '{0},{1},{2}'.format(
            f.user.username,
            f.add_time,
            resume_link
        )



if __name__ == '__main__':

    report_date_list = get_date_range(start_report_date, end_report_date)
    for date in  report_date_list:
        get_favs(date)