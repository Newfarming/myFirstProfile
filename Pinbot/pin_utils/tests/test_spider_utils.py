# coding: utf-8

import responses
import unittest

from ..spider_utils import (
    SpiderMsgDispatch,
    UnAuthException,
)
from Pinbot.settings import (
    SPIDER_MSG_TOKEN_REQ_URL,
    SPIDER_MSG_USERNAME,
    SPIDER_MSG_PASSWORD,
)


class TestSpiderMsgUtils(unittest.TestCase):

    @responses.activate
    def test_request_api(
            self,
            response_method=responses.GET,
            status=200,
            method='get'
        ):
        responses.add(
            response_method,
            SPIDER_MSG_TOKEN_REQ_URL,
            body={},
            status=status,
            content_type='application/json'
        )
        result = SpiderMsgDispatch.request_api(
            SPIDER_MSG_TOKEN_REQ_URL,
            {},
            method=method
        )
        assert result.status_code == status

    def test_request_api_status(self):
        status = [200, 301, 302, 401, 404, 500]
        for status_code in status:
            self.test_request_api(
                response_method=responses.GET,
                status=status_code,
                method='get'
            )
            self.test_request_api(
                response_method=responses.POST,
                status=status_code,
                method='post'
            )

    @responses.activate
    def test_auth_request(
            self,
            response_method=responses.GET,
            status=401,
            method='get'
        ):
        responses.add(
            response_method,
            SPIDER_MSG_TOKEN_REQ_URL,
            body={},
            status=status,
            content_type='application/json'
        )
        responses.add(
            responses.POST,
            SPIDER_MSG_TOKEN_REQ_URL,
            body='{"token": "test"}',
            status=status,
            content_type='application/json'
        )
        try:
            result = SpiderMsgDispatch.auth_request(
                SPIDER_MSG_TOKEN_REQ_URL,
                data={
                    "username": SPIDER_MSG_USERNAME,
                    "password": SPIDER_MSG_PASSWORD
                },
                method=method
            )
        except UnAuthException:
            result = '401'

        assert result == '401' or result.status_code == status

    def test_auth_request_status(self):
        status = [200, 301, 302, 401, 404, 500]
        for status_code in status:
            self.test_auth_request(
                response_method=responses.GET,
                status=status_code,
                method='get'
            )
            self.test_request_api(
                response_method=responses.POST,
                status=status_code,
                method='post'
            )
