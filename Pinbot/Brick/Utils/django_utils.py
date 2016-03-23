# coding: utf-8

import re
import json
import bson
import datetime
import os
import uuid

from bson.json_util import default as bson_encoder

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.serializers.json import DjangoJSONEncoder


require_superuser = user_passes_test(lambda u: u.is_superuser)
require_staff = user_passes_test(lambda u: u.is_staff)

get_today = lambda: datetime.datetime.combine(
    datetime.date.today(),
    datetime.datetime.min.time(),
)
get_tomommow = lambda: get_today() + datetime.timedelta(days=1)
get_after_tomommow = lambda: get_today() + datetime.timedelta(days=2)
after7day = lambda: get_today() + datetime.timedelta(days=8)
get_tomorrow = get_tomommow
get_yesterday = lambda: get_today() + datetime.timedelta(days=-1)


class DateTimeJSONEncoder(json.JSONEncoder):
    '''
    change datetime to %Y-%m
    datetime.datetime(2014, 1, 11) -> 2014-01
    '''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m')
        else:
            return super(DateTimeJSONEncoder, self).default(obj)


def JsonResponse(ret, *args, **kwargs):
    if 'default' not in kwargs:
        kwargs.update({'default': bson_encoder})

    if 'cls' not in kwargs:
        kwargs.update({'cls': DjangoJSONEncoder})

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
    except ValueError:
        return 0


def str2datetime(time_str, format=None):
    default_formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m',
        '%Y',
    ]

    if format:
        default_formats.append(format)

    for format in default_formats[::-1]:
        try:
            time = datetime.datetime.strptime(time_str, format)
            return time
        except ValueError:
            continue
    return None


def get_float(str_num):
    try:
        num = float(str_num)
        return num
    except ValueError:
        return 0


def error_phone(phone):
    pattern = re.compile(r'^(?:\+86)?(\d{3})\d{8}$|^(?:\+86)?(0\d{2,3})\d{7,8}$')
    return False if pattern.match(phone) else True


def error_email(email):
    pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
    return False if pattern.match(email) else True


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


class UploadFilepath(object):
    def __init__(self, path_prefix='image'):
        self.path_prefix = path_prefix

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return os.path.join(self.path_prefix, today, filename)


upload_filepath = UploadFilepath


def django_model2json(ret, *args, **kwargs):
    if 'cls' not in kwargs:
        kwargs.update({'cls': DjangoJSONEncoder})

    return json.dumps(ret, *args, **kwargs)


def get_http_url(url):
    if not url:
        return ''

    if url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        return 'http://%s' % url
