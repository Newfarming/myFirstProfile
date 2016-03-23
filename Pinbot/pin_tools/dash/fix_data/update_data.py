# coding: utf-8

import datetime
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from pin_tools.dash.drivers.task import DriversTask
from pin_utils.django_utils import (

    get_date_range
)


if __name__ == '__main__':

    start_report_date = datetime.date(2014, 2, 17)
    end_report_date = datetime.date(2014, 2, 19)
    report_date_list = get_date_range(start_report_date, end_report_date)
    task = DriversTask()

    for report_date in report_date_list:
        task.set_report_date(report_date=report_date)
        task.set_task_type(task_type='today')
        task.set_task_name(task_name='resume_data')
        task.make_data()
