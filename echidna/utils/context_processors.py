"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/29 10:44 上午
"""

from .blog_setting_tools import Settings


def settings(request):
    return {
        'settings': Settings.get_settings()
    }
