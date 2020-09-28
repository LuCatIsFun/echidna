"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/14 12:02 下午
"""
from echidna.settings.mood import MOOD
from random import choice

__all__ = ['HttpResponseMessage']


class HttpResponseMessage:
    """
        根据不同的http状态码，设置统一的默认返回信息
        https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status

        >>> from echidna.settings import HttpResponseMessage
        >>> HttpResponseMessage().random_mood
        (*・_・)ノ⌒*
        >>> hrm = HttpResponseMessage()
        >>> hrm(200)
        {'msg': 'ok', 'mood': ' ʅ(‾◡◝)'}
        >>> hrm.get_message(200)
        {'msg': 'ok', 'mood': '(ノ￣ω￣)ノ'}
    """

    http_default = '服务可能发生了一点点小问题，程序员哥哥正在加班处理..'

    http_200 = 'success'
    http_201 = '资源创建成功'

    http_400 = '糟糕，缺少必要的参数'
    http_401 = '糟糕，您的登陆信息失效或异常，可重新登陆后在尝试'
    http_403 = '糟糕，您没有权限访问此资源'
    http_404 = '您请求的资源不存在'
    http_405 = '不支持此方式请求，请以正确的姿势进入'
    http_429 = '请求频率过快，请降低访问频率'

    http_500 = '处理异常，服务器可能抽风了'

    def __call__(self, code: int, *args, **kwargs) -> dict:
        """
            根据http状态码返回默认信息和表情
        :param code: http_status_code
        :return: eg. {'msg': 'ok', 'mood': '(ノ￣ω￣)ノ'}
        """
        return self.get_message(code)

    @classmethod
    def get_message(cls, code: int) -> dict:
        """
            根据http状态码返回默认信息和表情
        :param code: http_status_code
        :return: eg. {'msg': 'ok', 'mood': '(ノ￣ω￣)ノ'}
        """
        assert isinstance(code, int) and 200 <= code < 600, 'code Must be a standard HTTP status code'
        message = getattr(cls, 'http_%s' % code) if hasattr(cls, 'http_%s' % code) else cls.http_default
        return {
            'msg': message,
            'mood': cls.get_http_code_mood(code)
        }

    @classmethod
    def get_http_code_mood(cls, code: int) -> str:
        """
            根据http状态码获取表情
        :param code:
        :return:
        """
        return {
            200: cls.get_mood(tag='happy'),
            201: cls.get_mood(tag='laugh'),
            400: cls.get_mood(tag='sorry'),
            401: cls.get_mood(tag='confuse'),
            403: cls.get_mood(tag='cry'),
            404: cls.get_mood(tag='surprise'),
            405: cls.get_mood(tag='sleep'),
            429: cls.get_mood(tag='wtf'),
            500: cls.get_mood(tag='cry'),
        }.get(code, cls.random_mood)

    @property
    def random_mood(self) -> str:
        """
            获取随机表情
        :return:
        """
        return choice(choice(MOOD)['yan'])

    @staticmethod
    def get_mood(tag: str) -> str:
        """
            根据tag获取表情
        :param tag:
        :return:
        """
        for mood in MOOD:
            if tag in mood['tag']:
                return choice(mood['yan'])
        return choice(choice(MOOD)['yan'])
