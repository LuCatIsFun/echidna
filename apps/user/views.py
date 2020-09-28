import datetime
from django.shortcuts import resolve_url, reverse
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, authenticate
)

from rest_framework.views import APIView

from apps.user.models import User


class Login(APIView):
    # 登录接口不走认证token
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not all([username, password]):
            return request.response.FAILED(msg="用户名或密码错误,请尝试重新登录")

        response = dict(msg="登录成功，即将跳转")
        user_info = authenticate(request, username=username, password=password)
        if user_info:
            user_obj = User.objects.filter(id=user_info.id).first()
            auth_login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')

        else:
            user_info = User.objects.filter(username=username).first()

            if user_info:
                if not user_info.is_active:
                    return request.response.FAILED(msg='糟糕，登录失败，用户已被冻结')
            return request.response.FAILED(msg='用户名或密码错误,请尝试重新登录')

        if 'next' in request.data.keys():
            response['next'] = request.data['next']

        response['token'], response['token_expired_date_time'] = user_obj.create_token()
        return request.response.SUCCESS(**response)


def logout(request, next_page=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    # 清除token信息
    now = datetime.datetime.now()
    user_obj = request.user
    if user_obj:
        user_obj.expired_date_time = user_obj.dead_date_time = now
        user_obj.token = None
        user_obj.save()

    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
            redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    return HttpResponseRedirect(reverse('index'))
