"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/29 10:59 上午
"""
import environ
from .base import BaseUtil
from django.conf import settings


class Settings(BaseUtil):

    @staticmethod
    def auto_theme():
        if 7 <= BaseUtil.get_now(time_format=False).hour <= 17:
            return 'light'
        else:
            return 'dark'

    @staticmethod
    def get_settings():
        env = settings.ENV
        return {
            # 网站信息
            'theme': env.str('theme', Settings.auto_theme()),  # 主题，默认为自动
            'title': env.str('title', '多娜茶,干杯 🍻'),        # 左上logo文字,
            'description': env.str('description', '干了这杯多娜茶'),        # 左上logo文字
            'copyright': env.str('copyright', 'Echidna ©2020 Created by Li yao'),    # 版权
            'background_image': env.str('background_image', '/static/img/image_header.jpg'),
            'disqus_url': env.str('disqus_url', None),

            # 个人信息
            'author': env.str('author', 'Echidna'),        # 作者
            'avatar': env.str('avatar', '/static/images/avatar.jpg'),        # 头像
            'position': env.str('position', '嫉妒魔女'),                 # 职位
            'email': env.str('email', None),
            'location': env.str('location', None),
            'birthday': env.str('birthday', None),
            'phone': env.str('phone', None),

            # 社交
            'facebook': env.str('facebook', None),
            'twitter': env.str('twitter', None),
            'github': env.str('github', None),
        }
