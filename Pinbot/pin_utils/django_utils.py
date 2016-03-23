# coding: utf-8

import re
import json
import bson
import datetime
import os
import uuid
from dateutil.relativedelta import relativedelta
from mongoengine import fields

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse

require_superuser = user_passes_test(lambda u: u.is_superuser)
require_staff = user_passes_test(lambda u: u.is_staff)

get_today = lambda: datetime.datetime.combine(
    datetime.date.today(),
    datetime.datetime.min.time(),
)
get_tomorrow = get_tomommow = lambda: get_today() + datetime.timedelta(days=1)
get_yesterday = lambda: get_today() + datetime.timedelta(days=-1)
get_after_tomommow = lambda: get_today() + datetime.timedelta(days=2)
after7day = lambda: get_today() + datetime.timedelta(days=8)


def JsonResponse(ret, *args, **kwargs):
    if 'default' not in kwargs:
        bson_encoder = bson.json_util.default
        kwargs.update({'default': bson_encoder})

    return HttpResponse(
        json.dumps(ret, *args, **kwargs),
        content_type='application/json'
    )


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def get_oid(str_id):
    try:
        oid = bson.ObjectId(str_id)
        return oid
    except bson.errors.InvalidId:
        return ''


def get_int(str_num):
    try:
        num = int(str_num)
        return num
    except (ValueError, TypeError):
        return 0


def model_to_dict(model):
    d = {}
    for field in model._meta.fields:
        data = getattr(model, field.name)
        data = str(data)
        d[field.name] = data
    return d


def str2datetime(
        time_str,
        format=None,
        default=datetime.datetime(1990, 01, 01)):

    default_formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m',
        '%Y',
        '%Y/%m/%d',
        '%Y/%m',
        '%Y.%m',
    ]

    if format:
        default_formats.append(format)

    for format in default_formats[::-1]:
        try:
            time = datetime.datetime.strptime(time_str, format)
            return time
        except ValueError:
            continue
    return default


def get_float(str_num):
    try:
        num = float(str_num)
        return num
    except ValueError:
        return 0


def error_phone(phone):
    pattern = re.compile(
        r'^(?:\+86)?(\d{3})\d{8}$|^(?:\+86)?(0\d{2,3})\d{7,8}$')
    return False if pattern.match(phone) else True


def error_email(email):
    pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
    return False if pattern.match(email) else True


def get_phone(str_phone):
    if not str_phone:
        return ''

    pattern = re.compile(
        r'(?:\+86)?(\d{3})\d{8}|(?:\+86)?(0\d{2,3})\d{7,8}')
    search_phone = pattern.search(str_phone)
    return search_phone.group(0) if search_phone else ''


def error_weixin_code(code):
    if not isinstance(code, basestring):
        return False
    pattern = re.compile('^[A-Za-z0-9]+$')
    return False if not pattern.match(code) else True


def error_weixin_next_url(next_url):
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return False if not pattern.match(next_url) else True


def user_add_group(user, group_name):
    group = get_object_or_none(Group, name=group_name)
    if not group:
        group = Group(name=group_name)
        group.save()
    group.user_set.add(user)
    return True


def user_add_permission(user, *permissions):
    user.user_permissions.add(*permissions)
    return True


def upload_filepath(path_prefix='image'):
    def unique_filename(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return os.path.join(path_prefix, today, filename)
    return unique_filename


def update_document(document, **data_dict):
    def field_value(field, value):
        if field.__class__ in (fields.ListField, fields.SortedListField):
            return [
                field_value(field.field, item)
                for item in value
            ]
        if field.__class__ in (
                fields.EmbeddedDocumentField,
                fields.GenericEmbeddedDocumentField,
                fields.ReferenceField,
                fields.GenericReferenceField
        ):
            return field.document_type(**value)
        else:
            return value

    [setattr(
        document, key,
        field_value(document._fields[key], value)
    ) for key, value in data_dict.items()]
    return document


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_week(date):
    """Return the full week (Sunday first) of the week containing the given date.

    'date' may be a datetime or date instance (the same type is returned).
    """
    one_day = datetime.timedelta(days=1)
    day_idx = (date.weekday()) % 7  # turn sunday into 0, monday into 1, etc.
    sunday = date - datetime.timedelta(days=day_idx)
    date = sunday
    for n in xrange(7):
        yield date
        date += one_day


def get_pre_week():
    week_last_day = list(get_week(datetime.datetime.now().date()))[0]
    today = week_last_day
    dates = [today - datetime.timedelta(days=i) for i in range(1, 8)]
    return [day for day in dates]


def get_pre2_week():
    today = get_pre_week()[6]
    dates = [today - datetime.timedelta(days=i) for i in range(1, 8)]
    return [day for day in dates]


def get_pre_month():
    first = datetime.date(day=1, month=get_today().month, year=get_today().year)
    lastMonth = first - datetime.timedelta(days=1)
    return get_month_first_day(lastMonth), get_month_last_day(lastMonth)


def get_pre2_month():
    first = datetime.date(day=1, month=get_today().month - 1, year=get_today().year)
    lastMonth = first - datetime.timedelta(days=1)
    return get_month_first_day(lastMonth), get_month_last_day(lastMonth)


def get_month_first_day(dt, d_years=0, d_months=0):
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m - 1, 12)
    return datetime.date(y + a, m + 1, 1)


def get_month_last_day(dt):
    return get_month_first_day(dt, 0, 1) + datetime.timedelta(-1)


def django_model2json(ret, *args, **kwargs):
    if 'cls' not in kwargs:
        kwargs.update({'cls': DjangoJSONEncoder})

    return json.dumps(ret, *args, **kwargs)


def today_rest_seconds():
    now = datetime.datetime.now()
    tomorrow = get_tomorrow()
    expire_time = (tomorrow - now).total_seconds()
    return expire_time


def get_proportion(v, total):

    if v is None:
        v = 0
    if total is None:
        total = 0
    try:
        value = (float(v) / total) * 100
    except ZeroDivisionError:
        value = 0
    return '{:.2f}%'.format(value)


def get_contrast(v, total):
    """获取环比比例"""
    if v is None:
        v = 0
    if total is None:
        total = 0

    try:
        gap_val = v - total
        value = (float(gap_val) / total) * 100
    except ZeroDivisionError:
        value = 0
    return '{:.2f}%'.format(value)


def error_qq(qq):
    pattern = re.compile(r'^[0-9]\d{4,12}$')
    return False if pattern.match(qq) else True


def get_http_url(url):
    if not url:
        return ''

    if url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        return 'http://%s' % url


def get_after_month(months):
    return datetime.datetime.today() + relativedelta(months=+months)


def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")


def get_monday():
    today = get_today()
    monday = today + datetime.timedelta(days=-today.weekday())
    return monday


def get_previous_monday():
    current_monday = get_monday()
    previous_monday = current_monday + datetime.timedelta(weeks=-1)
    return previous_monday


def get_next_monday():
    current_monday = get_monday()
    next_monday = current_monday + datetime.timedelta(weeks=1)
    return next_monday


def get_valid_next_url(ref):
    parttern = re.compile(r'^/[\?\w%#_/&=]+/?$')
    return ref if parttern.match(ref) else reverse('goto-pinbot')


def get_date_range(*args):
    if len(args) == 3:
        start, stop, step = args
        if isinstance(step, datetime.timedelta):
            int_step = step.days
        else:
            int_step = step
        parsed_args = (start.toordinal(), stop.toordinal(), int_step)
    else:
        parsed_args = tuple(x.toordinal() for x in args)

    return map(datetime.date.fromordinal, range(*parsed_args))
