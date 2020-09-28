"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/30 4:42 下午
"""

import uuid
import time
import logging

from django.http.response import Http404
from django.utils.deprecation import MiddlewareMixin

from .utils import CommonReturn
from echidna.exception import BaseException
from ratelimit.exceptions import Ratelimited


logger = logging.getLogger(__name__)


class RegisterMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        request.process_time_start = time.process_time()
        request.response_time_start = time.perf_counter()
        request.response = CommonReturn()

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        pass

    @staticmethod
    def process_response(request, response):
        response.setdefault('process_time', "%.2fms" % ((time.process_time() - request.process_time_start) * 100))
        response.setdefault('response_time', "%.2fms" % ((time.perf_counter() - request.response_time_start) * 100))

        return response

    @staticmethod
    def process_exception(request, exception):
        import traceback
        error_id = uuid.uuid5(uuid.NAMESPACE_DNS, traceback.format_exc())
        error_detail = traceback.format_exc()
        logger.error('\nerror Id:{error_id}\ndetail:{detail}'.format(error_id=error_id, detail=error_detail))

        if isinstance(exception, Http404):
            raise exception
        elif isinstance(exception, Ratelimited):
            return request.response.FAILED(msg='请求频率过快，请稍后再试')
        elif isinstance(exception, AssertionError):
            return request.response.FAILED(msg=exception.__str__())
        elif isinstance(exception, BaseException):
            return request.response(msg=exception.msg, response_code=exception.response_code)
        else:
            return request.response.FAILED(msg='糟糕，服务器处理异常，您可凭借此ID：%s 咨询管理员' % error_id)
