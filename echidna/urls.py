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
from . import views
from django.urls import path, re_path, include
from .utils import http_403_handle, http_404_handle, http_500_handle

urlpatterns = [
    re_path('^$', views.index, name='index'),

    re_path('^project$', views.project, name='project'),
    re_path('^about$', views.about, name='about'),

    re_path(r'^editor$', views.editor, name='editor'),
    re_path(r'^editor/(?P<article_id>\S*)/', views.edit_article, name='edit_article'),

    re_path('^article/', include('apps.article.urls.urls_web')),

    re_path('^api/article/', include('apps.article.urls.urls_api')),
    re_path('^api/user/', include('apps.user.urls')),


]

handler403 = http_403_handle
handler404 = http_404_handle
handler500 = http_500_handle
