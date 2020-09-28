"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/14 2:54 下午
"""
from datetime import datetime
from rest_framework import authentication
from echidna import exception


def handle_token(request):
    # 尝试获取header头部的token
    token = request.META.get("HTTP_TOKEN")
    if request.META.get("HTTP_TOKEN"):
        token = request.META.get("HTTP_TOKEN")
    # 尝试获取 drf 中的token
    elif request.data.get('token'):
        token = request.data.get('token')
    else:
        # 尝试获取django请求参数中的token
        for method in ['GET', 'POST']:
            if hasattr(request, method):
                token = getattr(request, method).get('token')
                if token:
                    break
        # 尝试获取cookie中的token
        if not all([token]):
            for cookie_name in ['token', 'butter-kol-token']:
                if request.COOKIES.get(cookie_name):
                    token = request.COOKIES.get(cookie_name)
                    break

    if not all([token]):
        raise exception.AuthenticationException(msg='未授权的请求')

    return token


class TokenAuthentication(authentication.BaseAuthentication):
    """
        基于Token的身份认证
    """

    def authenticate(self, request):
        from apps.user import models

        token = handle_token(request)

        # 根据token获取用户信息
        user_info = models.User.objects.filter(token=token).first()

        if not user_info:
            raise exception.AuthenticationException(msg='认证信息不存在，请重新登录')
        else:
            if datetime.now() < user_info.expired_date_time:

                if not user_info.is_active:
                    raise exception.AuthenticationException(msg='用户已被冻结')

                return user_info, token
            else:
                raise exception.AuthenticationException(msg='认证失效，请重新登录')
