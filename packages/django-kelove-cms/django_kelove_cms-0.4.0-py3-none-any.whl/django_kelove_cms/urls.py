# ==================================================================
#       文 件 名: urls.py
#       概    要: 路由配置
#       作    者: IT小强 
#       创建时间: 8/12/20 4:16 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.conf.urls import url
from django.urls import path
from django.conf import settings

from . import views

from .apps import DjangoKeloveCmsConfig

__all__ = ['urlpatterns', 'app_name']

app_name = DjangoKeloveCmsConfig.name

KELOVE_CMS_URL_SETTINGS = {**{
    "home_page": r'^page/(?P<page>[\w-]+)/$',

    "tag_url": r'^tag/(?P<pk>[\w-]+)/page/(?P<page>[\w-]+)/$',
    "tag_home_url": r'^tag/(?P<pk>[\w-]+)/$',

    "category_url": r'^category/(?P<pk>[\w-]+)/page/(?P<page>[\w-]+)/$',
    "category_home_url": r'^category/(?P<pk>[\w-]+)/$',

    "document_url": r'^(?P<pk>[\w-]+)/page/(?P<page>[\w-]+)/$',
    "document_home_url": r'^(?P<pk>[\w-]+).html$',

    "search_url": r'^search/page/(?P<page>[\w-]+)/$',
    "search_home_url": r'^search/$',
}, **dict(getattr(settings, 'KELOVE_CMS_URL_SETTINGS', {}))}

urlpatterns = [
    # 首页
    path('', views.Home.as_view(), name='home'),
    url(KELOVE_CMS_URL_SETTINGS['home_page'], views.Home.as_view(), name='home_page'),
    # 搜索
    url(KELOVE_CMS_URL_SETTINGS['search_url'], views.Search.as_view(), name='search'),
    url(KELOVE_CMS_URL_SETTINGS['search_home_url'], views.Search.as_view(), name='search_home'),
    # 标签
    url(KELOVE_CMS_URL_SETTINGS['tag_url'], views.Tag.as_view(), name='tag'),
    url(KELOVE_CMS_URL_SETTINGS['tag_home_url'], views.Tag.as_view(), name='tag_home'),
    # 分类
    url(KELOVE_CMS_URL_SETTINGS['category_url'], views.Category.as_view(), name='category'),
    url(KELOVE_CMS_URL_SETTINGS['category_home_url'], views.Category.as_view(), name='category_home'),
    # 文档
    url(KELOVE_CMS_URL_SETTINGS['document_url'], views.Document.as_view(), name='document'),
    url(KELOVE_CMS_URL_SETTINGS['document_home_url'], views.Document.as_view(), name='document_home'),
]
