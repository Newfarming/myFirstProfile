# coding: utf-8

import json


class JSONMiddleware(object):

    def process_request(self, request):
        content_type = request.META.get('CONTENT_TYPE', '') or ''
        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
            except ValueError:
                data = {}
            request.JSON = data
        else:
            request.JSON = {}
