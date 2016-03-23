# coding:utf-8
from points.models import *
import datetime
from transaction.models import UserChargePackage

def add_points(type=None,user=None):
    """
    增加用户积分
    """
    added_points = 0
    if type is not None:
        rewardConfigs = RewardConfig.objects.filter(title=type)
        if len(rewardConfigs) >= 1:
            rewardConfig = rewardConfigs[0]
            pointsDetail = PointsDetail(user=user,time=datetime.datetime.now(),
                                        type=rewardConfig,points=rewardConfig.points)
            pointsDetail.save()
            userPoints = UserPoints.objects.filter(user=user)
            if len(userPoints) >= 1:
                userPoint = userPoints[0]
                result,added_points = updatePoints(type,userPoint,rewardConfig)
            else:
                userPoint = UserPoints(user=user)
                result,added_points = updatePoints(type,userPoint,rewardConfig)
            return True,added_points
        else:
            return False,"type id is not existed"
    else:
        return False,'type can not be None'


def updatePoints(type,userPoint,rewardConfig):
    """
    根据type来更新不同值
    """
    add_points = rewardConfig.points
    try:
        if type == 'upload':
            userPoint.upload_points += rewardConfig.points
        elif type == 'login':
            userPoint.login_points += rewardConfig.points
        elif type == 'promotion':
            """
            推广积分具有最高上限，如果超过上限则不再增加积分
            """
            if userPoint.promotion_points >= rewardConfig.max_points_total:
                add_points = 0
            else:
                userPoint.promotion_points += rewardConfig.points
        
        userPoint.total += rewardConfig.points
        userPoint.save()
        return True,add_points
    except:
        return False,0


def get_total_points(user):
    """
    获取用户的总积分
    """
    total_points = 0
    userPoints = UserPoints.objects.filter(user=user)
    if len(userPoints) >= 1:
        user_point = userPoints[0]
        total_points += user_point.login_points
        total_points += user_point.upload_points
        total_points += user_point.promotion_points
        
        total_points -= user_point.consumed_points
    return total_points

def get_user_points(user):
    pkg_points = 0
    user_points = 0
    user_pkgs = UserChargePackage.objects.filter(user=user, package_type=1)
    user_charges_pkgs = user_pkgs.filter(resume_end_time__gte=datetime.datetime.now(), pay_status='finished')
    for user_charges_pkg in user_charges_pkgs:
        pkg_points += user_charges_pkg.rest_points + user_charges_pkg.re_points
    user_points = get_total_points(user)
    return pkg_points,user_points

def consume_points(user,points=0,pkg_points=0,user_points=0):
    """
    积分消费
    消费规则:优先消费套餐中的简历，如果套餐中简历不够则消费用户赚取的积分
    """
    if pkg_points + user_points >= points:
        still_need_points = points
        user_pkgs = UserChargePackage.objects.filter(user=user, package_type=1)
        user_charges_pkgs = user_pkgs.filter(resume_end_time__gte=datetime.datetime.now(), pay_status='finished')
        for user_charges_pkg in user_charges_pkgs:
            if user_charges_pkg.rest_points+user_charges_pkg.re_points < still_need_points:
                still_need_points -= user_charges_pkg.rest_points
                user_charges_pkg.rest_points = 0
            else:
                user_charges_pkg.rest_points -=  still_need_points
                still_need_points = 0
            
            user_charges_pkg.save()
        
        if still_need_points > 0:
            userPoints = UserPoints.objects.filter(user=user)
            for user_point in userPoints:
                user_point.consumed_points += still_need_points
                user_point.total -= still_need_points
                user_point.save()
                break
        return True
    else:
        return False
            
