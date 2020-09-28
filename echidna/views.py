"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/28 7:54 下午
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.article.models import Article, Tag, Group


def index(request):
    page = request.GET.get('p', 1)
    if request.user.is_authenticated:
        article_info = Article.objects.all()
    else:
        article_info = Article.objects.filter(password__isnull=True, access_status=0)
    paginator = Paginator(article_info, 10)
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)

    tag_info = Tag.objects.all()
    return render(request, 'index.html', {'article_list': article_list, 'tag_info': tag_info})


def resume(request):
    return render(request, 'resume.html')


def project(request):
    return render(request, 'project.html')


def about(request):
    return render(request, 'about.html')


@login_required
def editor(request):
    return render(request, 'editor.html', {'tag_info': Tag.get_all_tag(), 'group_info': Group.get_all_group()})


def edit_article(request, article_id):
    article_info = get_object_or_404(Article, pk=article_id)
    return render(request, 'editor.html', {'tag_info': Tag.get_all_tag(),
                                           'group_info': Group.get_all_group(),
                                           'article_info': article_info})

