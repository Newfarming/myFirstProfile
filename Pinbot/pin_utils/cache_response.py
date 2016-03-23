# coding: utf-8

from django.core.cache import cache


def cache_response(cache_time=300, prefix='CACHE_RESPONSE'):

    """为重复访问的频率较高的页面的response做缓存，
        缓存的键名为‘prefix_uid_method_path’的形式，

        参数:
            cache_time: 缓存过期时间，默认为5分钟；
            prefix:     键名前缀；
        使用:
            from django.utils.decorators import method_decorator

            class Foo(View):
                @method_decorator(cache_response())
                def get(self, request):
                    pass
    """
    def deco_cache(f):
        def func(*args, **kwargs):

            request = args[0]
            id = request.user.id
            method = request.method
            path = request.path
            key = '{prefix}_{uid}_{method}_{path}'.format(
                prefix=prefix,
                uid=str(id),
                method=method,
                path=path
            )
            response = cache.get(key)

            if response is None:
                response = f(*args, **kwargs)
                cache.set(key, response, cache_time)
                return response
            return response
        return func
    return deco_cache
