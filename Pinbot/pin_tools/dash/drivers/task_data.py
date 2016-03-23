# coding: utf-8

import datetime

from pin_tools.dash.builder import (
    DataBuilder
)
from pin_utils.django_utils import (
    get_today
)


class TaskDailyDataDriver(object):

    def __init__(self, **kwargs):

        start_query_time = kwargs.get('start_query_time', get_today() - datetime.timedelta(days=1))
        end_query_time = kwargs.get('end_query_time', get_today())

        ret_list = [
            'task_system',
        ]
        self.db_builder = DataBuilder(
            start_query_time,
            end_query_time,
            ret_list=ret_list
        )
        self.db_builder.build_data()
        self.origin_data = self.db_builder.origin_data

    def get_task_A1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A1'
            ).count()

    def get_task_A2_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A2'
            ).count()

    def get_task_A3_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A3'
            ).count()

    def get_task_A4_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A4'
            ).count()

    def get_task_A5_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A5'
            ).count()

    def get_task_A6_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A6'
            ).count()

    def get_task_A6_R1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A6_R1'
            ).count()

    def get_task_A6_R2_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A6_R2'
            ).count()

    def get_task_A6_L1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A6_L1'
            ).count()

    def get_task_A7_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A7'
            ).count()

    def get_task_A7_R1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A7_R1'
            ).count()

    def get_task_A7_R2_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A7_R2'
            ).count()

    def get_task_A7_R3_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A7_R3'
            ).count()

    def get_task_A8_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A8'
            ).count()

    def get_task_A8_R1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A8_R1'
            ).count()

    def get_task_A8_R2_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A8_R2'
            ).count()

    def get_task_A8_R3_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A8_R3'
            ).count()

    def get_task_A9_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A9'
            ).count()

    def get_task_A9_R1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A9_R1'
            ).count()

    def get_task_A9_R2_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A9_R2'
            ).count()

    def get_task_A9_R3_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A9_R3'
            ).count()

    def get_task_A10_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A10'
            ).count()

    def get_task_A10_R1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A10_R1'
            ).count()

    def get_task_A11_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A11'
            ).count()

    def get_task_A12_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A12'
            ).count()

    def get_task_A13_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A13'
            ).count()

    def get_task_A14_L1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A14_L1'
            ).count()

    def get_task_A15_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A15'
            ).count()

    def get_task_A15_R1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A15_R1'
            ).count()

    def get_task_A15_R2_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A15_R2'
            ).count()

    def get_task_A16_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A16'
            ).count()

    def get_task_A17_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A17'
            ).count()

    def get_task_A18_R1_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A18_R1'
            ).count()

    def get_task_A18_R2_count(self):
        return self.origin_data.get('task_system').filter(
                task__task_id='A18_R2'
            ).count()
