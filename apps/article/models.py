import re
import math
import json
import shortuuid

from html import unescape
from random import choice
from django.db import models
import django.utils.timezone as timezone

from uuslug import slugify

MONTH_MAP = {
    1: '一',
    2: '二',
    3: '三',
    4: '四',
    5: '五',
    6: '六',
    7: '七',
    8: '八',
    9: '九',
    10: '十',
    11: '十一',
    12: '十二',
    0: '未知'
}


# 文章
class Article(models.Model):
    ACCESS_STATUS = (
        (0, '公开'),
        (1, '私有'),
        (2, '密码'),

    )
    ACCESS_STATUS_DICT = {
        0: "公开",
        1: "私有",
        2: "密码"
    }

    id = models.CharField(max_length=30, primary_key=True)
    slug = models.SlugField(editable=False)

    # article meta data
    title = models.CharField(max_length=200, verbose_name='标题')
    banner = models.CharField(max_length=300, verbose_name='文章标题图片')
    content = models.TextField(verbose_name="内容")
    read_count = models.IntegerField(default=0, verbose_name="阅读量")

    # comment
    show_comment = models.BooleanField(default=True, verbose_name="展示评论")
    allow_comment = models.BooleanField(default=True, verbose_name="允许评论")

    # permission
    access_status = models.IntegerField(default=0, choices=ACCESS_STATUS, verbose_name="权限类型")
    password = models.CharField(verbose_name="文章密码", max_length=100, default=None, blank=True, null=True)

    create_date_time = models.DateTimeField(default=timezone.now)
    update_date_time = models.DateTimeField(auto_now=True)

    @property
    def need_password(self):
        return all([self.password])

    @property
    def get_chinese_month(self):
        return MONTH_MAP.get(self.create_date_time.month, 0)

    def get_content_replace_line_break(self):
        return json.dumps(self.content, ensure_ascii=False)

    @property
    def get_text(self):
        """
            获取文章纯文字，不包括html标签
        :return:
        """
        html = unescape(self.content) # 转义Html，这样类似于 &nbsp;这样的标签会被去除
        assert (isinstance(html, str))
        summary = re.sub(r'<.*?>', u'', html)  # 去除html标签
        return ''.join(summary.split())

    def digest(self, count=100):
        """
            获取文章概要，默认前100字
        :param count:
        :return:
        """
        content_text = self.get_text
        all_content = False if len(content_text) > count else True
        return {
            'all': all_content,
            'detail': content_text[0:count]
        }

    @property
    def read_time(self):
        """
            阅读分钟数，按每分钟400字
        :return:
        """
        sec = math.ceil(len(self.get_text) / 400)
        return sec if sec > 1 else 1

    @property
    def word_count(self):
        return len(self.get_text)

    @property
    def tag(self):
        """
            获取本文章tag列表
        :return:
        """
        return [
            Tag.objects.filter(id=t.tag_id).first().name
            for t in ArticleToTags.objects.filter(article_id=self.id)
        ]

    @property
    def group(self):
        """
            获取本文章分组列表
        :return:
        """
        return [
            Group.objects.filter(id=t.group_id).first().name
            for t in ArticleToGroup.objects.filter(article_id=self.id)
        ]

    def add_tag(self, **kwargs):
        """
            可传入 tag_id 或 tag_name 增加tag
            >>> self.add_tag(tag_name="123") # 增加一个名为123的tag
            >>> self.add_tag(tag_id="123") # 增加一个ID为123的tag

            >>> self.add_tag(tag_name=["123", "456"]) # 增加名为123，456的tag


        :param tag_name:
        :param tag_id:
        :return:
        """
        return self._set_tag('add', **kwargs)

    def add_group(self, **kwargs):
        """
            增加分组，功能类比增加标签
        """
        return self._set_group('add', **kwargs)

    def delete_tag(self, **kwargs):
        """
            可传入 tag_id 或 tag_name 删除tag
        :param tag_name:
        :param tag_id:
        :return:
        """
        return self._set_tag('delete', **kwargs)

    def delete_group(self, **kwargs):
        """
        删除分组，功能类比删除标签
        """
        return self._set_group('delete', **kwargs)

    def set_tag(self, **kwargs):
        """
            将tag更新传入的tag，不在传入列表中的tag将被删除

            >>> self.set_tag(tag_name=["123", "456"]) # 将文章标签设置为123,456

        :param kwargs:
        :return:
        """
        self.delete_all_tag()
        return self.add_tag(**kwargs)

    def set_group(self, **kwargs):
        self.delete_all_group()
        return self.add_group(**kwargs)

    @property
    def get_all_tag(self):
        """
            获取所有tag
        :return:
        """
        return Tag.get_all_tag()

    @property
    def get_all_group(self):
        """
            获取所有tag
        :return:
        """
        return Group.get_all_group()

    def delete_all_tag(self):
        ArticleToTags.objects.filter(article_id=self.id).delete()

    def delete_all_group(self):
        ArticleToGroup.objects.filter(article_id=self.id).delete()

    def _set_group(self, action, **kwargs):
        assert 'group_id' in kwargs.keys() or 'group_name' in kwargs.keys(), 'parameters "group_id" or "group_name" ' \
                                                                             'set at least one '
        if 'group_id' in kwargs.keys():
            query = 'id'
            k = 'group_id'
        else:
            query = 'name'
            k = 'group_name'

        assert isinstance(kwargs[k], (list, str)), 'type must be str or list'

        if type(kwargs[k]) == str:
            kwargs[k] = [kwargs[k]]
        for group in kwargs[k]:
            if not all([group]):
                continue
            query_parameter = {
                query: group
            }
            group_info = Group.objects.filter(**query_parameter)
            if group_info:
                group_obj = group_info.first()
                if action == 'add':
                    if not ArticleToGroup.objects.filter(group_id=group_obj.id,
                                                         article_id=self.id):
                        ArticleToGroup.objects.create(id=shortuuid.uuid(), group_id=group_obj.id,
                                                      article_id=self.id)
                elif action == 'delete':
                    ArticleToGroup.objects.filter(group_id=group_obj.id, article_id=self.id).delete()
            else:
                # 如果被操作的tag数据不存在，判断是否是用户想根据名称新增tag
                if action == 'add' and query == 'name':
                    group_id = shortuuid.uuid()
                    Group.objects.create(id=group_id, name=group)
                    ArticleToGroup.objects.create(id=shortuuid.uuid(), group_id=group_id, article_id=self.id)

    def _set_tag(self, action, **kwargs):
        """
            接收tag_id或tag的名称，动态设置查询条件增加或删除
        :param action:
        :param kwargs:
        :return:
        """
        assert 'tag_id' in kwargs.keys() or 'tag_name' in kwargs.keys(), 'parameters "tag_id" or "tag_name" set at ' \
                                                                         'least one'
        if 'tag_id' in kwargs.keys():
            query = 'id'
            k = 'tag_id'
        else:
            query = 'name'
            k = 'tag_name'

        assert isinstance(kwargs[k], (list, str)), 'type must be str or list'

        if type(kwargs[k]) == str:
            kwargs[k] = [kwargs[k]]
        for tag in kwargs[k]:
            if not all([tag]):
                continue
            query_parameter = {
                query: tag
            }
            tag_info = Tag.objects.filter(**query_parameter)
            if tag_info:
                if action == 'add':
                    if not ArticleToTags.objects.filter(tag_id=tag_info.first().id,
                                                        article_id=self.id):
                        ArticleToTags.objects.create(id=shortuuid.uuid(), tag_id=tag_info.first().id,
                                                     article_id=self.id)
                elif action == 'delete':
                    ArticleToTags.objects.filter(tag_id=tag_info.first().id, article_id=self.id).delete()
            else:
                # 如果被操作的tag数据不存在，判断是否是用户想根据名称新增tag
                if action == 'add' and query == 'name':
                    tag_id = shortuuid.uuid()
                    Tag.objects.create(id=tag_id, name=tag, color=Tag.random_color())
                    ArticleToTags.objects.create(id=shortuuid.uuid(), tag_id=tag_id, article_id=self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    class Meta:
        default_permissions = ()
        ordering = ['-create_date_time']


# 比较讨厌数据库层面的硬关联，这里做了文章和tag的关系表
class ArticleToTags(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    tag_id = models.CharField(max_length=30, verbose_name="标签ID")
    article_id = models.CharField(max_length=30, verbose_name="文章ID")

    class Meta:
        default_permissions = ()


# Tag
class Tag(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200, verbose_name='tag名称')
    color = models.CharField(max_length=30, verbose_name='颜色')
    create_date_time = models.DateTimeField(default=timezone.now)

    @staticmethod
    def get_all_tag():
        """
            获取所有tag
        :return:
        """
        return [
            tag.name
            for tag in Tag.objects.all()
        ]

    @staticmethod
    def random_color():
        color_list = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
        return choice(color_list)

    class Meta:
        default_permissions = ()
        ordering = ['name']


# 草稿
class Draft(models.Model):
    TYPE = (
        (0, '自动保存'),
        (1, '手动保存'),
        (2, '热保存'),

    )
    TYPE_DICT = {
        0: "自动保存",
        1: "手动保存",
        2: "热保存"
    }

    id = models.CharField(max_length=30, primary_key=True)
    article_id = models.CharField(max_length=30, verbose_name='文章ID', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='标题', null=True, blank=True)
    content = models.TextField(verbose_name="草稿内容")
    type = models.IntegerField(default=0, choices=TYPE, verbose_name="类型")
    note = models.CharField(max_length=200, verbose_name="备注", null=True, blank=True)
    create_date_time = models.DateTimeField(default=timezone.now)

    MAX_KEEP_DRAFT = 10

    @staticmethod
    def save_draft(article_id, content, save_type, title, note=None):
        """
            保存草稿
        :return:
        """
        save_type = int(save_type)
        draft_info = Draft.objects.filter(article_id=article_id, type=save_type).order_by('-create_date_time')

        if save_type in [0, 1]:
            if save_type == 0 and not note:
                note = '自动保存'

            # 删除多余草稿
            if (len(draft_info) + 1) > Draft.MAX_KEEP_DRAFT:
                Draft.objects.filter(article_id=article_id,
                                     type=save_type,
                                     create_date_time__lte=draft_info[
                                         Draft.MAX_KEEP_DRAFT - 1].create_date_time).delete()
            Draft.objects.create(id=shortuuid.uuid(), type=save_type, article_id=article_id,
                                 content=content, title=title, note=note)
        else:
            if draft_info:
                draft_info = draft_info.first()
                draft_info.content = content
                draft_info.title = title
                draft_info.save()
            else:
                Draft.objects.create(id=shortuuid.uuid(), article_id=article_id,
                                     type=save_type,
                                     title=title,
                                     note="热保存",
                                     content=content)

        return True

    class Meta:
        default_permissions = ()
        ordering = ['-create_date_time']


# Group
class Group(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200, verbose_name='tag名称')
    create_date_time = models.DateTimeField(default=timezone.now)

    @staticmethod
    def get_all_group():
        """
            获取所有tag
        :return:
        """
        return [
            group.name
            for group in Group.objects.all()
        ]

    class Meta:
        default_permissions = ()
        ordering = ['name']


# 文章和分组的关系表
class ArticleToGroup(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    group_id = models.CharField(max_length=30, verbose_name="分组ID")
    article_id = models.CharField(max_length=30, verbose_name="文章ID")

    class Meta:
        default_permissions = ()
