# coding: utf-8

from django.core.cache import cache

from .models import EasterEgg

from pin_celery.celery_app import app

from pin_utils.django_utils import (
    today_rest_seconds,
)


class LoadEggData(object):
    gift_pool_key = 'EGG_GIFT_POOL'
    grant_gift_key = 'EGG_GRANT_GIFT'

    def load_data(self):
        egg_data_pool = dict(list(
            EasterEgg.objects.filter(is_active=True).values_list('code_name', 'amount'))
        )

        if not egg_data_pool:
            return False

        expire_time = today_rest_seconds()
        cache.set(self.gift_pool_key, egg_data_pool, expire_time)
        return True


load_egg_task = LoadEggData()
asyn_load_egg_task = app.task(
    name='pinbot-load-egg-task'
)(load_egg_task.load_data)
