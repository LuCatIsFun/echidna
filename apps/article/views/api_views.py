import os
import hashlib
import shortuuid

from uuslug import slugify

from django.db.models import Q
from django.shortcuts import get_object_or_404, reverse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from apps.article import models, serializer
from echidna.utils import BlogTools


class Article(APIView):
    tools = BlogTools()
    COMMENT_STATUS = ['true', True, 'false', False]

    def post(self, request):
        """
        创建文章
        """

        content = request.data.get('content')
        title = request.data.get('title')
        tags = request.data.get('tags')
        groups = request.data.get('groups')
        access_status = request.data.get('access_status')
        password = request.data.get('password')
        show_comment = request.data.get('show_comment')
        allow_comment = request.data.get('allow_comment')

        banner = request.data.get('banner')
        if not all([banner]):
            banner = self.tools.get_random_banner()
        if not all([title]):
            return request.response.FAILED(msg='创建文章失败，标题不能为空')
        else:
            if models.Article.objects.filter(Q(title=title) | Q(slug=slugify(title))):
                return request.response.FAILED(msg='创建文章失败，标题已存在')

            if show_comment in self.COMMENT_STATUS and allow_comment in self.COMMENT_STATUS:
                show_comment = self.tools.try_safe_eval(show_comment)
                allow_comment = self.tools.try_safe_eval(allow_comment)
                assert isinstance(show_comment, bool) and isinstance(allow_comment, bool), '评论状态异常'
            else:
                return request.response(response_code=400)

            try:
                access_status = int(access_status)
                if access_status not in models.Article.ACCESS_STATUS_DICT:
                    return request.response(response_code=400)
            except:
                return request.response(response_code=400)
            else:
                if access_status == 2:
                    if not all([password]):
                        return request.response.FAILED(msg='创建文章失败，可见性设置为密码访问时，密码不能为空哦~')
                else:
                    password = None

        article_id = shortuuid.uuid()
        article_info = models.Article.objects.create(id=article_id, title=title,
                                                     show_comment=show_comment, allow_comment=allow_comment,
                                                     access_status=access_status, password=password,
                                                     banner=banner, content=content)

        if tags:
            article_info.set_tag(tag_name=self.tools.try_safe_eval(tags))
        if groups:
            article_info.set_group(group_name=self.tools.try_safe_eval(groups))

        return request.response.SUCCESS(msg='文章创建成功', article_id=article_id,
                                        redirect=reverse('edit_article', kwargs={'article_id': article_id}))


class ArticleDetail(APIView):
    permission_classes = (IsAuthenticated,)
    tools = BlogTools()

    def get(self, request, article_id):
        article_info = get_object_or_404(models.Article, pk=article_id)
        return request.response.SUCCESS(data=serializer.ArticleSerializer(instance=article_info, many=False).data)

    def put(self, request, article_id):
        content = request.data.get('content')
        title = request.data.get('title')
        tags = request.data.get('tags')
        groups = request.data.get('groups')
        access_status = request.data.get('access_status')
        password = request.data.get('password')
        show_comment = request.data.get('show_comment')
        allow_comment = request.data.get('allow_comment')

        banner = request.data.get('banner')

        article_info = get_object_or_404(models.Article, pk=article_id)

        if not all([banner]):
            banner = self.tools.get_random_banner()
        if not all([title]):
            return request.response.FAILED(msg='更新文章失败，标题不能为空')
        else:
            if models.Article.objects.filter(Q(title=title) | Q(slug=slugify(title)) & ~Q(id=article_id)):
                return request.response.FAILED(msg='更新文章失败，标题与其他已存在文章重复')
            if show_comment in Article.COMMENT_STATUS and allow_comment in Article.COMMENT_STATUS:
                show_comment = self.tools.try_safe_eval(show_comment)
                allow_comment = self.tools.try_safe_eval(allow_comment)
                assert isinstance(show_comment, bool) and isinstance(allow_comment, bool), '评论状态异常'
            else:
                return request.response(response_code=400)

            try:
                access_status = int(access_status)
                if access_status not in models.Article.ACCESS_STATUS_DICT:
                    return request.response(response_code=400)
            except:
                return request.response(response_code=400)
            else:
                if access_status == 2:
                    if not all([password]):
                        return request.response.FAILED(msg='更新文章失败，可见性设置为密码访问时，密码不能为空哦~')
                else:
                    password = None

        models.Article.objects.filter(id=article_id).update(title=title,
                                                            show_comment=show_comment, allow_comment=allow_comment,
                                                            access_status=access_status, password=password,
                                                            banner=banner, content=content)

        if tags:
            article_info.set_tag(tag_name=self.tools.try_safe_eval(tags))
        if groups:
            article_info.set_group(group_name=self.tools.try_safe_eval(groups))

        return request.response.SUCCESS(msg='文章更新成功')


class ArticleVerify(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, article_id):
        password = request.data.get('password')
        if not all([password]):
            return request.response(response_code=400)

        article_info = get_object_or_404(models.Article, pk=article_id)
        if article_info.password:
            status = password == article_info.password
        else:
            status = True
        return request.response.SUCCESS(status=status)


class ArticleDraft(APIView):
    """
    文章草稿
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        article_id = request.GET.get('article_id')
        save_type = request.GET.get('type')

        draft_info = models.Draft.objects.filter(article_id=article_id, type=save_type).order_by('-create_date_time')
        return request.response.SUCCESS(list=serializer.DraftListSerializer(instance=draft_info, many=True).data)

    def post(self, request):
        title = request.data.get('title')
        article_id = request.data.get('article_id')
        content = request.data.get('content')
        save_type = request.data.get('type')
        note = request.data.get('note')

        if not all([content]):
            return request.response.FAILED(msg="保存的草稿内容不能为空哦~")

        models.Draft.save_draft(article_id=article_id, content=content, note=note, save_type=save_type, title=title)
        return request.response.SUCCESS(msg="保存草稿成功")


class ArticleDraftDetail(APIView):
    """
    文章草稿详情
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        article_id = request.GET.get('article_id')
        save_type = request.GET.get('type')
        draft_id = request.GET.get('draft_id')

        try:
            save_type = int(save_type)
        except:
            return request.response(response_code=400)

        if save_type != 2:
            if not all([draft_id]):
                return request.response(response_code=400)
            draft_info = get_object_or_404(models.Draft, pk=draft_id)
        else:
            draft_info = models.Draft.objects.filter(article_id=article_id, type=save_type).first()
            if not draft_info:
                return request.response.FAILED(msg="当前文章没有热草稿哦")

        return request.response.SUCCESS(data=serializer.DraftListSerializer(instance=draft_info, many=False).data)


class ArticleUploadBanner(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    IMAGE_SUPPORT_TYPE = ['jpg', 'jpeg', 'png']

    def post(self, request):
        file_obj = request.FILES.get('file', None)

        if all([file_obj]):
            file_type_split = file_obj.name.split('.')

            if len(file_type_split) < 2:
                return request.response(response_code=400, msg='文件名格式非法，请确保文件名类似为"xxx.jpg"')
            else:
                file_type = file_type_split[-1].lower()
                if file_type not in self.IMAGE_SUPPORT_TYPE:
                    return request.response(response_code=400, msg='文件格式非法，当前仅支持图片')
            md5_obj = hashlib.md5()
            md5_obj.update(file_obj.read())
            file_name = "%s.%s" % (md5_obj.hexdigest(), file_type)
            file_path = os.path.join(BlogTools.BANNER_PATH, file_name)

            if not os.path.isfile(file_path):
                with open(file_path, 'wb+') as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
            file_path = '/%s' % '/'.join(file_path.split('/')[-5:])
            return request.response.SUCCESS(msg='上传成功', url=file_path)
        else:
            return request.response(response_code=400, msg='未能获取到资源，请尝试重新上传')
