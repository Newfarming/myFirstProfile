# coding: utf-8

from pin_utils.django_utils import (
    get_int,
)


class AdvanceQueryMixin(object):

    def get_advance_work_years(self):
        work_years_min = get_int(self.request.GET.get('work_years_min', ''))
        work_years_max = get_int(self.request.GET.get('work_years_max', ''))

        if work_years_min and not work_years_max:
            work_years_max = 30
        if not work_years_min and work_years_max:
            work_years_min = 0

        if work_years_min > 20 or work_years_max > 30 or work_years_min > work_years_max:
            return ''
        if work_years_min < 0 or work_years_max < 0 or (not work_years_min and not work_years_max):
            return ''
        return '%s,%s' % (work_years_min, work_years_max)

    def get_advance_degree(self):
        degree = self.request.GET.get('degree', '')
        if degree not in ('本科', '专科', '硕士', '博士'):
            return ''
        return degree

    def get_advance_gender(self):
        gender = self.request.GET.get('gender', '')
        if gender not in ('男', '女'):
            return ''
        return gender

    def get_advance_age(self):
        age_min = get_int(self.request.GET.get('age_min', ''))
        age_max = get_int(self.request.GET.get('age_max', ''))

        if age_min and not age_max:
            age_max = 60
        if not age_min and age_max:
            age_min = 0

        if age_min > 40 or age_max > 60 or age_min > age_max:
            return ''
        if age_min < 0 or age_max < 0 or (not age_min and not age_max):
            return ''

        return '%s,%s' % (age_min, age_max)

    def get_current_area(self):
        current_area = self.request.GET.get('current_area', '').strip()
        return current_area

    def get_advance_salary(self):
        MAX_SALARY = 1000000
        MIN_SALARY = 1000
        salary_min = get_int(self.request.GET.get('salary_min', ''))
        salary_max = get_int(self.request.GET.get('salary_max', ''))

        if salary_min and not salary_max:
            salary_max = MAX_SALARY
        if not salary_min and salary_max:
            salary_min = MIN_SALARY

        if salary_min > MAX_SALARY or salary_max > MAX_SALARY or salary_min > salary_max:
            return ''
        if salary_min < 0 or salary_max < 0 or (not salary_min and not salary_max):
            return ''
        return '%s,%s' % (salary_min, salary_max)
