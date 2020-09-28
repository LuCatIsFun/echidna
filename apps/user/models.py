import datetime
import hashlib

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# 继承自带user类，增加拓展字段
class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('user', u'普通用户'),
        ('admin', u'管理员'),
    )
    mobile = models.CharField(max_length=30, blank=True, verbose_name='电话')
    role = models.CharField(max_length=30, choices=USER_ROLE_CHOICES, default='user', verbose_name='用户角色')
    avatar = models.CharField(max_length=500, verbose_name='头像地址')
    nickname = models.CharField(max_length=30, blank=True, verbose_name=u'昵称')
    token = models.CharField(max_length=64, blank=True, null=True, verbose_name='认证token')
    expired_date_time = models.DateTimeField(default=timezone.now, verbose_name="失效时间")
    dead_date_time = models.DateTimeField(default=timezone.now, verbose_name="最长可用时间")

    @staticmethod
    def generate_token():
        now = str(datetime.datetime.now())
        md5 = hashlib.md5()
        md5.update(bytes(now + settings.SECRET_KEY, encoding='utf-8'))
        return md5.hexdigest()

    def create_token(self):
        """
            删除现有token，重新创建新token

        :return:
        """
        self.token = None
        token, expired_date_time = self.flush_token()
        return token, expired_date_time

    def flush_token(self):
        """
            刷新token，token最大可用时间无法超过最长可用时间，如果不存在则创建新token
        :return:
        """

        if self.token:
            expired_date_time = datetime.datetime.now() + datetime.timedelta(days=settings.TOKEN_EXPIRED_TIME)

            if self.expired_date_time >= self.dead_date_time:
                self.token = None
            elif expired_date_time >= self.dead_date_time:
                self.expired_date_time = self.dead_date_time
            else:
                self.expired_date_time = expired_date_time

            token = self.token
        else:
            token = self.generate_token()
            now = datetime.datetime.now()
            self.token = token
            self.expired_date_time = now + datetime.timedelta(days=settings.TOKEN_EXPIRED_TIME)
            self.dead_date_time = now + datetime.timedelta(days=30)

        self.save()
        return token, self.expired_date_time

    def __unicode__(self):
        return self.nickname

    def __str__(self):
        return self.nickname

    class Meta:
        default_permissions = ()
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
