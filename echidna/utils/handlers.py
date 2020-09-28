"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/28 5:09 下午
"""
import os

from sys import stderr as console
from logging import Handler, Formatter
from rest_framework.views import exception_handler

from .common_return import CommonReturn
from echidna.settings import HttpResponseMessage

response_message = HttpResponseMessage()


class AccessLogHandler(Handler):
    """
    追加记录日志
    """

    ACCESS_LOG_FORMATTER = '%(ip)s %(levelname)s %(asctime)s %(pathname)s %(module)s [%(funcName)s:%(lineno)d]: %(' \
                           'message)s'

    def __init__(self, filename, **kwargs):
        super().__init__()
        self.fmt = Formatter(self.ACCESS_LOG_FORMATTER)
        self.filename = filename

    def emit(self, record) -> None:
        request = record.request
        record.ip = self.get_request_ip_address(request)
        log_content = self.fmt.format(record) + os.linesep
        console.write(log_content)

        with open(self.filename, 'a') as file:
            file.write(log_content)

    @staticmethod
    def get_request_ip_address(request):
        get_peer_fuc = getattr(request, "getpeername", None)
        try:
            if callable(get_peer_fuc):
                return request.getpeername()[0]
            else:
                return None
        except OSError:
            return None


# django rest framework 自定义异常信息
def drf_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data.clear()
        message = response_message(response.status_code)
        response.data['msg'], response.data['mood'] = message['msg'], message['mood']
    return response


# SEO 不返回错误的HTTP状态码
def http_403_handle(request, exception):
    return request.response(response_code=403, hasError=True)


def http_404_handle(request, exception):
    return request.response(response_code=404, hasError=True)


def http_500_handle(exception):
    response = CommonReturn()
    return response(response_code=500, hasError=True)
