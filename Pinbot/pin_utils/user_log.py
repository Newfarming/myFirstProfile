# coding: utf-8

from app.dash.document import (
    UserAccessLog
)


class UserLogService(object):

    @classmethod
    def write_user_access_log(self, **kwargs):
        user_log = UserAccessLog(
            **kwargs
        )
        user_log.save()
        return True
