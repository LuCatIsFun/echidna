"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/9/23 4:12 下午
"""

__all__ = ['verify_article_password']


def verify_article_password(request, password, article_id):
    return request.COOKIES.get("%s_password" % article_id) == password
