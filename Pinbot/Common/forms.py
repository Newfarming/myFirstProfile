# coding: utf-8

import bleach
import datetime

from django import forms


class NormalizeFormStringMixin(object):

    def clean(self):
        for key, value in self.cleaned_data.iteritems():
            if isinstance(value, basestring):
                value = bleach.clean(value.strip(), tags=['br'], strip=True)
            self.cleaned_data[key] = value
        return self.cleaned_data


class DatetimeCleanMixin(object):
    start_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )
    end_time = forms.DateTimeField(
        input_formats=(
            '%Y.%m',
            '%Y-%m',
        ),
    )
    min_time = datetime.datetime(1990, 01, 01)
    max_time = datetime.datetime(2100, 01, 01)

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if self.max_time < start_time or start_time < self.min_time:
            raise forms.ValidationError('所选时间必须在1990-01~2100-01之间')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        if self.max_time < end_time or end_time < self.min_time:
            raise forms.ValidationError('所选时间必须在1990-01~2100-01之间')
        return end_time
