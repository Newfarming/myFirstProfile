# coding:utf-8
'''
Created on 2013-11-8

@author: likaiguo.happy@gmail.com 2013-11-8 13:08:26
每个页面访问量的统计装饰器
'''
import json
from datetime import datetime, date
import time

from django.shortcuts import redirect

from transaction.models import *
from pinbot_package.views import *
from basic_service.resume_util import produce_return_json
from feed.models import UserFeed2, Feed2
from app.pinbot_point.point_utils import point_utils

from statistics.models import StatisticsModel
from variables.PageID_variables import PINBOT_ANALYSE, \
    PINBOT_ANALYSE_REFRESH, GET_ANALYSE_DATA, GET_ANALYSE_DATA_REFRESH


FEED_INFO_URL = '/payment/my_account/'


def group_required(group_name_list=None, permissions=None, redirect_url='/feed/nopermission'):
    """
    @summary: 用户在组或者用户套餐在组里都可以通过
    如果用户没有过购买套餐的记录则直接导入套餐购买页面，如果用户有过购买记录则直接转入订阅购买页面
    @author: liyao
    """
    def _group_required(function):
        def __inner_deco(request, group_name=group_name_list, *arg, **kw):
            # 如果权限在这个组,可以访问
            # TODO:这样设置有个问题,权限的时间呢
            for group in request.user.groups.all():
                if group.name in group_name_list:
                    res = function(request, *arg, **kw)
                    return res

            # 如果用户带有这个权限
            if permissions:
                if request.user.has_perms(permissions):
                    return function(request, *arg, **kw)

            # 如果套餐含有这个权限
            user_charges_pkgs = UserChargePackage.objects.filter(user=request.user, pay_status='finished')
            for user_charges_pkg in user_charges_pkgs:
                if (user_charges_pkg.package_type == 1 and user_charges_pkg.resume_package.group.name in group_name_list) or (user_charges_pkg.package_type == 2 and user_charges_pkg.feed_package.name != u'人才伙伴订阅'):
                    res = function(request, *arg, **kw)
                    return res
            return redirect(redirect_url)
        return __inner_deco
    return _group_required


def calc_remain_feed_num(user):
    """
    @summary: 计算剩余实际有效订阅数量
    @author: likaiguo.happy@163.com 2014-6-15 19:34:29
    """

    now = datetime.now()
    # 所有有效订阅量
    user_charges_pkgs = UserChargePackage.objects.filter(
        user=user,
        feed_end_time__gte=now,
        pay_status='finished',
        pkg_source=1,
    )

    # 计算总共有的有效订阅数量
    total_valid_feed_num = 0
    for user_charges_pkg in user_charges_pkgs:
        total_valid_feed_num += user_charges_pkg.extra_feed_num

    # 计算用户实际已经使用的数量
    user_feed_count = Feed2.objects.filter(
        username=user.username,
        deleted=False,
        expire_time__gte=now,
        feed_type=1,
    ).count()
    return total_valid_feed_num - user_feed_count


def feed_unexpired_required(feed_id=None, redirect_url=FEED_INFO_URL):
    """
    @summary: 有未过期的订阅装饰器
    @author: liyao
    @change: likaiguo 2014-6-15 18:33:56 修改逻辑,获取正确的订阅数量

    """
    def _feed_unexpired_required(function):
        def __inner_deco(request, *arg, **kw):
            if calc_remain_feed_num(request.user) > 0:
                res = function(request, *arg, **kw)
                return res
            return redirect(redirect_url)
        return __inner_deco
    return  _feed_unexpired_required



def resume_points_required(group_name=None):
    """
    @summary: 有积分装饰器
    @author: liyao
    @change: liyao 2014年10月9日18:15:12 修改剩余积点判断逻辑,可以使用推广积分和简历上传积分购买简历
    """
    def _resume_points_required(function):
        def __inner_deco(request, group_name=group_name, *arg, **kw):
            pkg_point, pinbot_point = point_utils.get_user_point(request.user)
            total_points = pkg_point + pinbot_point
            if total_points >= 10:
                res = function(request, *arg, **kw)
                return res
            else:
                json_data = produce_return_json(data=3, status=False, error_dict=u'3.有效点数不够')
                return HttpResponse(json_data, "application/json")

        return __inner_deco
    return  _resume_points_required


def page_access_counter_dec(page_type_id=0):
    """
    @summary: 页面访问计数器
    @author: likaiguo.happy@gmail.com 2013-11-8 15:51:50
    """
    def _page_access_counter_dec(function):

        def __inner_deco(request, page_type_id=page_type_id, *arg, **kw):
            keywords = ''
            url = ''
            if request.method == 'GET':
                p = request.GET.copy()
                if  page_type_id in [PINBOT_ANALYSE, PINBOT_ANALYSE_REFRESH, GET_ANALYSE_DATA, GET_ANALYSE_DATA_REFRESH]:
                    data = request.session.get('data')
                    if request.session.get('is_refresh'):
                        if page_type_id == PINBOT_ANALYSE:
                            page_type_id = PINBOT_ANALYSE_REFRESH
                        elif page_type_id == GET_ANALYSE_DATA:
                            page_type_id = GET_ANALYSE_DATA_REFRESH
                    if data:
                        data = json.loads(data)
                        keywords = data.get('keywords', '')
                        urls = data.get('urls', [])
                        url = ','.join(urls)
                else:
                    keywords = p.get('keywords', '')
                    url = p.get('url', '')
            elif request.method == 'POST':
                p = request.POST.copy()
                if page_type_id == PINBOT_ANALYSE:
                    data = p.get('data')
                    if data:
                        data = json.loads(data)
                        keywords = data.get('keywords', '')
                        urls = data.get('urls', [])
                        url = ','.join(urls)
                else:
                    keywords = p.get('keywords', '')
                    url = p.get('url', '')
            username = request.user.username
            time_now = time.time()
            statistic_data = StatisticsModel(username=username, page_id=page_type_id, access_time=datetime.now())
            statistic_data.search_keywords = keywords
            statistic_data.url = url

            statistic_data.access_url = request.path
            statistic_data.refer_url = request.META.get('HTTP_REFERER', '')


#             statistic_data.user_agent = request.META.get('HTTP_USER_AGENT ', '')

            res = function(request, *arg, **kw)


            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            statistic_data.ip = ip
            statistic_data.cost_time = time.time() - time_now
            try:
                statistic_data.save()
            except Exception,e:
                pass
            
            return res
        return __inner_deco

    return  _page_access_counter_dec


def email_access_record_desc(email_type_id=1):
    """
    @summary: 邮件点击统计
    @author: liyao 2014-3-11 13:08:26
    """
    def _email_access_record_desc(function):

        def __inner_deco(request, email_type_id=email_type_id, *arg, **kw):
            try:
                p = request.GET.copy()
                user = request.user
                user_type = 'AnonymousUser'
                username = ''

                if user.pk:
                    user_type = 'user'
                    username = user.username

                if email_type_id == MARKET_EMAIL:
                    email = p.get('email', '')
                    send_date = p.get('sendtime', '')
                    send_date = datetime.strptime(send_date, "%Y-%m-%d-%H:%M")
                    time_now = time.time()
                    access_log = LogEmailAccess(email=email, send_date=send_date,
                                                type=email_type_id, username=username, user_type=user_type)

                    res = function(request, *arg, **kw)
                    access_log.cost_time = time.time() - time_now
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[-1].strip()
                    else:
                        ip = request.META.get('REMOTE_ADDR')
                    access_log.ip = ip
                    access_log.save()

                    return res
                elif email_type_id == FEED_EMAIL:
                    action = p.get('action', '')
                    token = p.get('token', '')
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[-1].strip()
                    else:
                        ip = request.META.get('REMOTE_ADDR')

                    email = ''
                    op_type = 0
                    op_detail = ''
                    time_now = time.time()
                    feed_access_record = LogEmailAccess(username=username, type=email_type_id, user_type=user_type)

                    if action == 'all':
                        op_type = 2
                        op_detail = 'all'
                        try:
                            feed_str = base64.b64decode(token)
                            email = feed_str
                            if isinstance(email, unicode):
                                email = email.encode('utf-8')
                        except:
                            pass
                    elif action == 'change_profile':
                        op_type = 3
                        op_detail = 'change_profile'
                        try:
                            feed_str = base64.b64decode(token)
                            feed_str = feed_str.split('&&&')
                            email = feed_str[0]
                            if isinstance(username, unicode):
                                email = email.encode('utf-8')
                        except:
                            pass
                    else:
                        try:
                            op_type = 1
                            feed_str = base64.b64decode(token)
                            feed_str = feed_str.split('&&&')
                            email = feed_str[0]
                            if isinstance(email, unicode):
                                email = email.encode('utf-8')
                            op_detail = feed_str[1]
                        except:
                            pass

                    res = function(request, *arg, **kw)
                    feed_access_record.cost_time = time.time() - time_now
                    feed_access_record.ip = ip
                    feed_access_record.op_type = op_type
                    feed_access_record.op_detail = op_detail
                    feed_access_record.email = email

                    feed_access_record.save()
                    return res
            except:
                res = function(request, *arg, **kw)
                return res

        return __inner_deco
    return  _email_access_record_desc





from django.core.cache import cache

def feed_ajax_cache(page_type=''):
    """
    @summary: 数据缓存策略

    """


    def data_cache(function):


        def __inner_deco(request, feed_id, *arg, **kw):

            p = request.GET.copy()
            if p.get('view') == 'user':
                p.pop('t')
                key = json.dumps(p)

                today = date.today()
                key = "%s-%s-%s-%s" % (today, request.user.username, feed_id, key)

                cache_data = cache.get(key)
                if cache_data:
                    return cache_data

                res = function(request, feed_id, *arg, **kw)


                cache.set(key, res, 150)

                return res

            else:

                res = function(request, feed_id, *arg, **kw)
                return res

        return __inner_deco

    return data_cache

if __name__ == '__main__':
    pass
