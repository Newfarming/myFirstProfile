# coding: utf-8

from django.core.cache import cache

from Brick.BCelery.celery_app import app


@app.task(name='clear-reco-limit')
def clear_reco_limit():
    '''
    清除每天推荐限制的条数
    每天00: 01 跑一次
    '''
    cache.delete_pattern('*DAILY_RECOMMEND_*')
