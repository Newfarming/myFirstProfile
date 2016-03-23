# coding: utf-8

import requests
import logging
import json
from bson import json_util

from Pinbot.settings import (
    API_PARSE_URL,
    API_PARSE_JD_URL,
    API_PARSE_NUM,
    API_PARSE_SALARY,
    API_PARSE_RELATED,
    API_SEARCH_JOB,
    API_SEARCH_RESUME,
    API_WRITE_ES,
)

logger = logging.getLogger('django')


class ParseUtils(object):

    @classmethod
    def parse_resume(cls, filepath):
        resume_result = requests.get(
            API_PARSE_URL,
            params={
                'path': filepath,
            }
        )
        if resume_result.status_code != 200:
            return {
                'status': 'error_500',
                'filepath': filepath,
            }
        return resume_result.json()

    @classmethod
    def request_api(cls, api_url, params, method='get', json_param=True):
        logger.info(
            'request api: api_url: {api_url}, method {method}, request data {params}'.format(
                api_url=api_url,
                method=method,
                params=params,
            )
        )
        kwargs = {'json': params} if json_param else {'params': params}
        request_method = requests.get if method.lower() == 'get' else requests.post

        try:
            api_result = request_method(
                api_url,
                timeout=10,
                **kwargs
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            logger.error(
                'api timeout: api_url: {api_url}, request data {params}'.format(
                    api_url=api_url,
                    params=params,
                ),
                exc_info=True
            )
            return {
                'status': 'api_timeout',
                'data': {},
            }

        if api_result.status_code != 200:
            logger.error(
                'api error: api_url: {api_url}, status_code {status_code}, error text is {api_text}, request data {params}'.format(
                    api_url=api_result.url,
                    status_code=api_result.status_code,
                    api_text=api_result.text,
                    params=params,
                ),
                exc_info=True,
            )
            return {
                'status': 'api_error',
                'http_code': api_result.status_code,
                'error_msg': api_result.text,
            }
        return {
            'status': 'ok',
            'data': api_result.json(),
        }

    @classmethod
    def parse_jd(cls, params):
        return cls.request_api(API_PARSE_JD_URL, params, 'post')

    @classmethod
    def parse_salary(cls, params):
        return cls.request_api(API_PARSE_SALARY, params, 'post')

    @classmethod
    def parse_num(cls, params):
        return cls.request_api(API_PARSE_NUM, params, 'post')

    @classmethod
    def parse_related(cls, params):
        return cls.request_api(API_PARSE_RELATED, params, 'post')

    @classmethod
    def search_job(cls, params):
        return cls.request_api(API_SEARCH_JOB, params, json_param=False)

    @classmethod
    def search_resume(cls, params):
        return cls.request_api(API_SEARCH_RESUME, params, json_param=False)

    @classmethod
    def insert_resume(cls, params):
        params = {
            'doc': 'resumeData',
            'data': json.dumps(
                params, default=json_util.default,
                ensure_ascii=False
            ),
        }
        return cls.request_api(API_WRITE_ES, params, 'post', json_param=False)

    @classmethod
    def insert_feed(cls, params):
        params = {
            'doc': 'feed',
            'data': json.dumps(
                params,
                default=json_util.default,
                ensure_ascii=False
            ),
        }
        return cls.request_api(API_WRITE_ES, params, 'post', json_param=False)
