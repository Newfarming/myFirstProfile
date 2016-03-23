# -*- coding: utf-8 -*-

import requests
import base64
import logging
from exceptions import Exception

from django.core.cache import cache

from pin_celery.celery_app import app
from pin_utils.retry import retry
from Pinbot.settings import (
    SPIDER_MSG_TOKEN_REQ_URL,
    SPIDER_DOWNLOAD_MSG_REQ_URL,
    SPIDER_MSG_USERNAME,
    SPIDER_MSG_PASSWORD,
)

CONNECT_EXCEPTION = requests.exceptions.ConnectionError
logger = logging.getLogger('django')


class UnAuthException(Exception):
    pass


class SpiderMsgDispatch(object):

    @classmethod
    @retry(CONNECT_EXCEPTION, tries=3, delay=5)
    def request_api(cls, url, kwargs, method='get'):

        try:
            if method.lower() == 'get':
                result = requests.get(
                    url,
                    **kwargs
                )
            else:
                result = requests.post(
                    url,
                    **kwargs
                )
            logger.info('send_download_msg_info {url} {kwargs}'.format(url=url, kwargs=kwargs))
        except CONNECT_EXCEPTION:
            logger.error(
                'api %s connect_error, kwargs is %s' % (url, str(kwargs))
            )
            raise CONNECT_EXCEPTION
        if result.status_code == 500:
            logger.error('spider server error')
        logger.info('download_msg_return: status:{status} content:{content}'.format(status=result.status_code, content=result.content))
        return result

    @classmethod
    def get_token(cls):
        data = {
            'username': SPIDER_MSG_USERNAME,
            'password': SPIDER_MSG_PASSWORD,
        }
        data = {
            'data': data
        }
        url = SPIDER_MSG_TOKEN_REQ_URL
        response = cls.request_api(url, data, method='post')
        token = response.json().get('token')
        return token

    @classmethod
    def get_cache_token(cls, timeout=False, token_key='spider_msg_token'):
        token = cache.get(token_key)
        if token is None or timeout:
            token = cls.get_token()
            cache.set('spider_msg_token', token, 7200)
        return token

    @classmethod
    def get_crypto_token(cls, token_key):
        token = cls.get_cache_token(token_key)
        return 'Basic ' + base64.b64encode(token)

    @classmethod
    def get_auth_header(cls, token_key):
        headers = {
            'Authorization': cls.get_crypto_token(token_key)
        }
        return headers

    @classmethod
    @retry(UnAuthException, tries=3, delay=1)
    def auth_request(cls, url, data=None, method='get', cache_key='spider_msg_token'):

        auth_header = cls.get_auth_header(cache_key)
        params = {
            'data': data,
            'headers': auth_header
        }

        response = cls.request_api(url, params, method=method)

        if response.status_code == 401:
            cache.delete(cache_key)
            raise UnAuthException
        return response

    @classmethod
    def send_download_msg(cls, resume_id):

        url = SPIDER_DOWNLOAD_MSG_REQ_URL + str(resume_id) + '/'
        return cls.auth_request(url)


asyn_send_download_msg = app.task(name='send_download_msg')(SpiderMsgDispatch.send_download_msg)
