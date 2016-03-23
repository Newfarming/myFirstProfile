# coding:utf-8
# Create your views here.


from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from transaction.models import ResumeBuyRecord, UserChargePackage
from models import *
from datetime import datetime
from django.shortcuts import render, render_to_response
from feed.models import UserFeed, Feed
from bson import ObjectId
from Pinbot.settings import LOGIN_URL


def get_unexpired_pkg(user=None, package_type=None):
    """
    获取未过期的套餐
    """
    user_pkg = []
    if package_type is not None:
        user_charge_pkgs = UserChargePackage.objects.filter(
            user=user, end_time__gte=datetime.now(), package_type=package_type)
        for user_charge_pkg in user_charge_pkgs:
            if not user_charge_pkg.has_expired():
                user_pkg.append(user_charge_pkg)
                return user_pkg
    return None


def has_pkgs(user):
    """
    用户是否购买套餐
    """
    user_charge_pkgs = UserChargePackage.objects.filter(user=user)
    if len(user_charge_pkgs) >= 1:
        return True
    else:
        return False


def has_resumepkg_frozen(user=None):
    """
    判断用户是否被冻结
    """
    user_charge_pkgs = UserChargePackage.objects.filter(
        user=user, package_type=1)
    if len(user_charge_pkgs) >= 1:
        # 查看是否有未过期的简历套餐
        unexpired_resume_pkgs = user_charge_pkgs.filter(
            resume_end_time__gte=datetime.now())
        if len(unexpired_resume_pkgs) >= 1:
            return False
        else:
            return True
    else:
        return False


def has_feed_frozen(user=None, feed=None):
    """
    判断订阅是否冻结并返回冻结时间
    """
    try:
        user_feed = UserFeed.objects.get(
            user=user, is_deleted=False, feed=feed)
        if datetime.now() > user_feed.expire_time:
            return True, user_feed.expire_time
        else:
            return False
    except:
        return False


def get_one_feed_pkg(user):
    """
    @summary: 获取一个最远的有效的含有订阅的套餐
    """
    user_pkgs = UserChargePackage.objects.filter(
        user=user,
        rest_feed__gt=0,
        feed_end_time__gte=datetime.now(),
        pkg_source=1,
    ).order_by("start_time")
    if len(user_pkgs) >= 1:
        return user_pkgs[0]
    return None
