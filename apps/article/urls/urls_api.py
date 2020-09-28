"""echidna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from .. import views

urlpatterns = [
    re_path(r"^upload/banner/", views.ArticleUploadBanner.as_view(), name='ArticleUploadBanner'),

    re_path(r"editor/(?P<article_id>\S*)/", views.ArticleDetail.as_view(), name='edit_article_api'),
    re_path(r"draft/detail/", views.ArticleDraftDetail.as_view(), name='ArticleDraftDetail'),

    re_path(r"(?P<article_id>\S*)/verify/", views.ArticleVerify.as_view(), name='ArticleVerify'),


    re_path(r"^draft/", views.ArticleDraft.as_view(), name='ArticleDraft'),

    re_path(r'', views.Article.as_view(), name='article_api'),

]
