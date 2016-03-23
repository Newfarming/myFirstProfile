# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from points.models import (
    PointsDetail,
    UserPoints,
)
from transaction.models import (
    ResumeBuyRecord,
)
from jobs.models import (
    SendCompanyCard,
)

from app.pinbot_point.models import (
    PinbotPoint,
    PointRecord,
)

RECORD_META = {
    'upload': {
        'p_type': 'partner',
        'detail': u'上传简历获得积分',
        'point_rule': 'partner_upload',
    },
    'promotion': {
        'p_type': 'promotion',
        'detail': u'推广用户获得积分',
        'point_rule': 'promotion',
    },
    'download': {
        'p_type': 'download_resume',
        'detail': u'下载简历',
        'point_rule': 'download_resume',
    },
    'send_company_card': {
        'p_type': 'send_company_card',
        'detail': u'发送企业名片',
        'point_rule': 'send_company_card',
    },
}


def point2pinbot_point():
    old_records = PointsDetail.objects.all()

    for record in old_records:
        user = record.user
        time = record.time
        p_type = record.type
        points = record.points

        new_record_meta = RECORD_META[p_type.title]
        new_record = PointRecord(
            user=user,
            record_type=new_record_meta['p_type'],
            point=points,
            point_rule=new_record_meta['point_rule'],
            detail=new_record_meta['detail'],
        )
        new_record.save()
        new_record.record_time = time
        new_record.save()
        print record.id, 'old point detail save success'

    old_points = UserPoints.objects.all()
    for p in old_points:
        total_point = p.login_points + p.upload_points + p.promotion_points
        user = p.user
        pinbot_point = PinbotPoint(
            user=user,
            point=total_point,
        )
        pinbot_point.save()
        print p.id, 'old point save success'


def get_download_point(record):
    if not record.send_card:
        return -10
    if record.send_card.points_used == 12:
        return -9
    if record.send_card.points_used == 13:
        return -10
    return -10


def download2point_record():
    new_record_meta = RECORD_META['download']
    buy_record = ResumeBuyRecord.objects.all()

    for record in buy_record:
        try:
            user = record.user
        except:
            continue
        buy_record_time = record
        point = get_download_point(record)
        buy_record_time = record.op_time

        new_record = PointRecord(
            user=user,
            record_type=new_record_meta['p_type'],
            point=point,
            point_rule=new_record_meta['point_rule'],
            detail=new_record_meta['detail'],
        )
        new_record.save()
        new_record.record_time = buy_record_time
        new_record.save()
        print record.id, 'download record save success'


def sendcard2point_record():
    new_record_meta = RECORD_META['send_company_card']
    records = SendCompanyCard.objects.filter(points_used__gt=0)

    for record in records:
        user = record.send_user
        buy_record_time = record.send_time
        point = -3

        new_record = PointRecord(
            user=user,
            record_type=new_record_meta['p_type'],
            point=point,
            point_rule=new_record_meta['point_rule'],
            detail=new_record_meta['detail'],
        )
        new_record.save()
        new_record.record_time = buy_record_time
        new_record.save()
        print record.id, 'send card record save success'


if __name__ == '__main__':
    point2pinbot_point()
    download2point_record()
    sendcard2point_record()
