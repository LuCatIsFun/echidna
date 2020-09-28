"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/29 10:49 上午
"""

import os
import re
import urllib
import string
import hashlib
import requests
import shortuuid

from random import choice
from datetime import datetime

from django.conf import settings


class BaseUtil:
    STATIC_PATH = os.path.join(settings.BASE_DIR, "static")
    TEMPLATE_PATH = os.path.join(settings.BASE_DIR, "templates")
    EMAIL_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'email')
    IMAGE_PATH = os.path.join(STATIC_PATH, 'images')
    DEFAULT_BANNER_PATH = os.path.join(IMAGE_PATH, 'banner')
    BANNER_PATH = os.path.join(DEFAULT_BANNER_PATH, 'user')

    DEFAULT_AVATAR = 'https://s1-fs.pstatp.com/static-resource/v1/b36c64f9-b03d-4d17-a6d9-410e0e9e2d9g'

    @staticmethod
    def create_random_password(length=8, chars=string.ascii_letters + string.digits):
        return ''.join([choice(chars) for i in range(length)])

    @staticmethod
    def try_safe_eval(value):
        if isinstance(value, (list, dict, bool)) or value is None:
            return value
        value = str(value)
        if all([value]):
            if value.startswith('[') and value.endswith(']') or \
                    value.startswith('{') and value.endswith('}') or \
                    value in ['True', 'False']:
                value = eval(value)

            if value == 'true':
                value = True
            elif value == 'false':
                value = False
        else:
            raise ValueError('value can not be null')

        return value

    @staticmethod
    def get_now(time_format=True):
        if time_format:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            return datetime.now()

    @staticmethod
    def check_parameter(parameter, kwargs):
        for p in parameter:
            if p not in kwargs.keys():
                return False
        return True

    @staticmethod
    def get_request():
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        request = requests.Session()
        request.mount("https://", adapter)
        request.mount("http://", adapter)
        return request

    @staticmethod
    def get_gravatar_url(email, size=40):
        url = "https://cdn.v2ex.com/gravatar/"
        default = 'mm'
        return url + "%s?%s" % (
            hashlib.md5(email.lower().encode("utf-8")).hexdigest(),
            urllib.parse.urlencode({'d': default, 's': str(size)}))


class BlogTools(BaseUtil):

    @staticmethod
    def get_email_complex(email):
        # 通过@分开字符串
        mail_split_list = email.split('@')
        # 前面2位显示
        dis_mail_pre = mail_split_list[0][:4]
        # 其它位数隐藏
        hide_mail_pre = mail_split_list[0][2:]
        # 最后2位显示
        dis_mail_last = mail_split_list[-1][-3:]
        # 其它位数隐藏
        hide_mail_last = mail_split_list[-1][:-2]
        # 使用re.sub过滤
        result_hide_mail_pre = re.sub(hide_mail_pre, len(hide_mail_pre) * '*', hide_mail_pre)
        # 使用re.sub过滤
        result_hide_mail_last = re.sub(hide_mail_last, len(hide_mail_last) * '*', hide_mail_last)
        # 将结果集合起来
        desensitization_mail = dis_mail_pre + result_hide_mail_pre + '@' + result_hide_mail_last + dis_mail_last
        return desensitization_mail

    def get_author(self, request, email):
        if request.user and request.user.email == email:
            return email
        else:
            return self.get_email_complex(email)

    @staticmethod
    def get_random_banner():
        default_banner = os.listdir(BaseUtil.DEFAULT_BANNER_PATH)
        default_banner.remove('user')
        return '/static/images/banner/%s' % choice(default_banner)
