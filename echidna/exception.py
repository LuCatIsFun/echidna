"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/14 1:51 下午
"""

import json


class BaseException(Exception):
    """
        Error handling
    """

    response_code = 500

    def __init__(self, msg: str):
        super(BaseException, self).__init__()
        self._msg = msg

    @property
    def msg(self):
        return self._msg

    def __str__(self):
        return u"{msg}".format(msg=json.dumps(self.msg, ensure_ascii=False))


class AuthenticationException(BaseException):
    response_code = 401


class SystemException(BaseException):
    response_code = 500


class PermissionException(BaseException):
    response_code = 403
