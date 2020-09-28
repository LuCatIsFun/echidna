"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/3/30 11:41 下午
@desc:
"""

import json
import datetime
import functools
from django.http import HttpResponse
from echidna.settings import HttpResponseMessage


# Json 无法解析 datatime 类型的数据，构建 DateEncoder 类解决 datatime 解析问题
class DateEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        else:
            return json.JSONEncoder.default(self, obj)


# 利用偏函数重写 dumps 方法，使其支持解析 datatime 类型
json.dumps = functools.partial(json.dumps, cls=DateEncoder)


class CommonReturn(object):
    """
        公共返回函数，封装了一个django HttpResponse 对象，自动把传入的参数转为json
    """
    # 业务返回码
    success = 0
    failed = -1

    # 默认http状态返回码
    http_response_default_code = 200
    http_response_success_code = 200
    http_response_failed_code = 200

    http_response_message = HttpResponseMessage()

    def __call__(self, *args, **kwargs):
        """
        :param response_code:
        :param kwargs:
        :return:
        """
        return self.return_data(args, kwargs)

    @staticmethod
    def handle_data_type(args: (list, dict), kwargs: dict) -> None:
        assert 'code' not in kwargs.keys() or 'code' in kwargs.keys() and \
               isinstance(kwargs['code'], int), kwargs['code']
        assert not args or isinstance(args[0], (list, dict)), args

    def SUCCESS(self, *args: (dict, list), **kwargs) -> HttpResponse:
        """
            Success message return format

            if args exist，the parameters in kwargs will be overridden

            >>> response = CommonReturn()
            >>> response.SUCCESS(msg="hello world")
            '<HttpResponse status_code=200, "application/json">'
            >>> response.SUCCESS(msg="hello world").getvalue()
            'b\'{"code": 0, "msg": "hello world"}\''



        :param response_code: set http response code
        :return:
        """
        self.handle_data_type(args, kwargs)

        code = kwargs['code'] if 'code' in kwargs.keys() else self.success
        kwargs['response_code'] = kwargs['response_code'] if 'response_code' in kwargs.keys() else \
            self.http_response_success_code
        return self.return_data(args, kwargs, code=code)

    def FAILED(self, *args: (dict, list), **kwargs) -> HttpResponse:
        """
            Failure message return format

            if args exist，the parameters in kwargs will be overridden

            >>> response = CommonReturn()
            >>> response.FAILED(msg="have some error")
            '<HttpResponse status_code=500, "application/json">'
            >>> response.FAILED(msg="have some error").getvalue()
            'b\'{"code": -1, "msg": "have some error"}\''

        :param response_code: set http response code
        :return:
        """
        self.handle_data_type(args, kwargs)

        code = kwargs['code'] if 'code' in kwargs.keys() else self.failed
        kwargs['response_code'] = kwargs['response_code'] if 'response_code' in kwargs.keys() else \
            self.http_response_failed_code
        return self.return_data(args, kwargs, code=code)

    def return_data(self, args: tuple, kwargs: dict, code: int = None):
        response = {}
        response_code = self.http_response_default_code
        for k in kwargs.keys():
            if k == 'response_code':
                assert isinstance(kwargs[k], int), kwargs[k]
                response_code = kwargs[k]

                http_response_message = self.http_response_message(code=response_code)
                for key in ['msg', 'mood']:
                    if key not in kwargs.keys():
                        response[key] = http_response_message[key]

            else:
                response[k] = kwargs[k]
        if not code and response_code != 200:
            response['code'] = self.failed
        else:
            response['code'] = code if isinstance(code, int) else self.success

        if args:
            response = args[0]
        try:
            return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json, charset=utf-8",
                                status=response_code)
        except UnicodeEncodeError:
            return HttpResponse(json.dumps(response), content_type="application/json, charset=utf-8",
                                status=response_code)

