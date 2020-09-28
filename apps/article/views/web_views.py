import shortuuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ratelimit.decorators import ratelimit

from apps.article.models import Article
from apps.article.utils import verify_article_password


@ratelimit(key='ip', rate='2/1s', method='GET', block=True)
def article(request, slug: str) -> render:
    """
    文章
    :param slug:
    :param request:
    :return:
    """
    article_info = get_object_or_404(Article, slug=slug)

    # check password
    if article_info.access_status == 2:
        if article_info.password:
            if not request.user.is_authenticated:
                if not verify_article_password(request, password=article_info.password, article_id=article_info.id):
                    return render(request, 'article_no_password.html', {'article_info': article_info})
    elif article_info.access_status == 1:
        if not request.user.is_authenticated:
            return request.response.FAILED(msg="糟糕，没有权限访问 😳")

    article_info.read_count += 1
    article_info.save()
    return render(request, 'article.html', {'article_info': article_info})
