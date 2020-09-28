"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/9/24 11:01 上午
"""

from rest_framework import serializers

from apps.article.models import Draft, Article


class DraftListSerializer(serializers.ModelSerializer):
    create_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Draft
        ordering = ['-create_date_time']
        fields = '__all__'
        # exclude = ('content_key',)


class ArticleSerializer(serializers.ModelSerializer):
    create_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    tag = serializers.ListField()
    group = serializers.ListField()

    class Meta:
        model = Article
        ordering = ['-create_date_time']
        fields = '__all__'
