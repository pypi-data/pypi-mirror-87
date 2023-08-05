# ==================================================================
#       文 件 名: views.py
#       概    要: 视图
#       作    者: IT小强 
#       创建时间: 8/12/20 4:18 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================


from hashlib import md5
from urllib.parse import quote, unquote

from django.shortcuts import render
from django.views.generic import View
from django_kelove_admin.util import load_object
from django.http import HttpResponseRedirect
from django.urls import reverse

from .settings import GlobalSettingsForm
from .util import get_tpl_path

from . import models, DOCUMENT_TEMPLATE, CATEGORY_TEMPLATE, TAG_TEMPLATE, CMS_BASE_FILTER, DOCUMENT_TYPE_CHOICE_URL


class BaseView(View):
    """
    视图基类
    """

    BASE_FILTER = CMS_BASE_FILTER

    is_home_page = False

    def __init__(self, *args, **kwargs):
        """
        初始化
        :param args:
        :param kwargs:
        """

        super().__init__(*args, **kwargs)

        # 获取全局配置
        self._global_settings: dict = GlobalSettingsForm.get()

        # 获取模板配置类
        self._template_settings_cls = load_object(self._global_settings.get('template_settings', None))

        # 获取模板配置
        self._template_settings: dict = self._template_settings_cls.get()

        # 页面标题处理
        self.page_title = []
        page_title = self._global_settings.get('page_title', '')
        if page_title:
            self.page_title.append(page_title)
        page_sub_title = self._global_settings.get('page_sub_title', '')
        if page_sub_title:
            self.page_title.append(page_sub_title)

        # 整合全部模板变量
        self._assign_data: dict = {
            **{
                'breadcrumb': [],
                'page_canonical': '',
                'page_robots': '',
                'page_nav_tag': '',
                'is_home_page': False,
            },
            **self._global_settings,
            **self._template_settings,
        }

        page_keywords = str(self._assign_data.get('page_keywords', ''))
        self._assign_data.update({
            'page_title': self.page_title,
            'page_keywords': page_keywords.split(',') if page_keywords else []
        })

        # 允许每个模板自定义变量
        self._assign_data.update(self._get_view_assign())

    def get(self, request, pk, page=1, **kwargs):
        """

        :param request:
        :param pk:
        :param page:
        :return:
        """

        self._assign_data['page_nav_tag'] = md5(quote(request.get_raw_uri()).encode()).hexdigest()

    def _render(self, request, template_name, context=None, content_type=None, status=None, using=None):
        if context is None:
            context = {}
        self._assign_data['page_title'] = ' | '.join(self._assign_data['page_title'][::-1])
        self._assign_data['page_keywords'] = ','.join(self._assign_data['page_keywords'])
        self._assign_data['is_home_page'] = self.is_home_page
        context['assign'] = self._assign_data
        return render(
            request=request,
            template_name=template_name,
            context=context,
            content_type=content_type,
            status=status,
            using=using
        )

    def _get_view_assign(self):
        view_assign = self._template_settings_cls.view_assign
        if isinstance(view_assign, str):
            view_assign = load_object(view_assign)
        if not isinstance(view_assign, dict):
            view_assign = view_assign(view_assign_settings=self._assign_data)
        return view_assign


class Tag(BaseView):

    def get(self, request, pk, page=1, **kwargs):
        """
        处理GET请求
        :param page:
        :param pk:
        :param request:
        :return:
        """

        url_key = self._global_settings['tag_url_key']
        data = models.Tag.objects.filter(
            **{**{url_key: pk}, **self.BASE_FILTER}
        ).get()

        # 页面标题
        self._assign_data['page_title'].append(data.title)
        # 页面关键词
        self._assign_data['page_keywords'].insert(0, data.title)
        # 导航标识
        self._assign_data['page_nav_tag'] = 'tag_' + str(data.pk)
        # 页面描述
        if data.description:
            self._assign_data['page_description'] = data.description
        return self._render(request, get_tpl_path(data, TAG_TEMPLATE), {
            "tag": data,
            "current_page": int(page),
            "current_url": '{scheme}://{host}{url}'.format(
                scheme=request.scheme,
                host=request.get_host(),
                url=data.get_url(page=page)
            ),
        })


class Category(BaseView):
    """
    分类
    """

    def get(self, request, pk, page=1, **kwargs):
        """
        处理GET请求
        :param page:
        :param pk:
        :param request:
        :return:
        """

        url_key = self._global_settings['category_url_key']

        data = models.Category.objects.filter(
            **{**{url_key: pk}, **self.BASE_FILTER}
        ).get()

        # 页面标题
        self._assign_data['page_title'].append(data.title)
        # 页面关键词
        self._assign_data['page_keywords'].insert(0, data.title)
        # 导航标识
        self._assign_data['page_nav_tag'] = 'category_' + str(data.pk)
        # 页面描述
        if data.description:
            self._assign_data['page_description'] = data.description
        elif data.content:
            self._assign_data['page_description'] = data.content[0:150]
        return self._render(request, get_tpl_path(data, CATEGORY_TEMPLATE), {
            "category": data,
            "current_page": int(page),
            "current_url": '{scheme}://{host}{url}'.format(
                scheme=request.scheme,
                host=request.get_host(),
                url=data.get_url(page=page)
            ),
        })


class Document(BaseView):
    """
    文章视图
    """

    def get(self, request, pk, page=1, **kwargs):
        """
        :param request:
        :param pk:
        :param page:
        :return:
        """

        # 获取url标识
        url_key = self._global_settings['document_url_key']

        # 获取文章基础数据
        document_data = self._get_document_data(request, pk, page, url_key, **kwargs)

        # 外链文章自动跳转
        if document_data['document'].type == DOCUMENT_TYPE_CHOICE_URL:
            return HttpResponseRedirect(document_data['document'].url)

        # 首页自动跳转
        home_page_doc_id = int(self._global_settings.get('home_page_doc_id', 0))
        if home_page_doc_id == document_data['document'].pk:
            return HttpResponseRedirect(reverse('django_kelove_cms:home'))

        # 搜索页自动跳转
        search_page_doc_id = int(self._global_settings.get('search_page_doc_id', 0))
        if search_page_doc_id == document_data['document'].pk:
            return HttpResponseRedirect(document_data['document'].get_search_url(
                page=page,
                query_string=request.META.get('QUERY_STRING', '')
            ))

        # 模板路经
        tpl_path = document_data['tpl_path']

        # 渲染模板
        return self._render(request, tpl_path, document_data)

    def _get_document_data(self, request, pk, page: int = 1, url_key: str = None, **kwargs):
        """
        获取文章基础数据
        :param request:
        :param pk:
        :param page:
        :param url_key:
        :param kwargs:
        :return:
        """

        if not url_key:
            url_key = self._global_settings['document_url_key']

        data = models.Document.objects.filter(
            **{**{url_key: pk}, **self.BASE_FILTER}
        ).select_related("category", "created_user", "updated_user").get()

        # 页面关键词
        data.tags = data_tags = data.tag.filter(**self.BASE_FILTER).order_by('sort', '-updated_time', '-id').all()

        # 导航标识
        self._assign_data['page_nav_tag'] = 'document_' + str(data.pk)
        # 页面标题
        self._assign_data['page_title'].append(data.title)
        # 页面关键词
        if data_tags:
            self._assign_data['page_keywords'] = list([i.title for i in data_tags])
        # 页面描述
        if data.description:
            self._assign_data['page_description'] = data.description
        elif data.content:
            self._assign_data['page_description'] = data.content[0:150]

        return {
            "document": data,
            "tpl_path": get_tpl_path(data, DOCUMENT_TEMPLATE),
            "current_page": int(page),
            "current_url": '{scheme}://{host}{url}'.format(
                scheme=request.scheme,
                host=request.get_host(),
                url=data.get_url(page=page)
            ),
        }


class Home(Document):
    """
    首页视图
    """

    is_home_page = True

    def get(self, request, pk=None, page=1, **kwargs):
        """
        首页GET请求处理
        :param request:
        :param pk:
        :param page:
        :param kwargs:
        :return:
        """

        # 获取到首页的文章ID
        pk = int(self._global_settings.get('home_page_doc_id', 0))

        # 获取文章基础数据
        document_data = self._get_document_data(request, pk, page, 'pk', **kwargs)

        # 模板路经
        tpl_path = document_data['tpl_path']

        # 渲染模板
        return self._render(request, tpl_path, document_data)


class Search(Document):
    """
    搜索视图
    """

    def get(self, request, pk=None, page=1, **kwargs):
        """
        搜索页GET请求处理
        :param request:
        :param pk:
        :param page:
        :param kwargs:
        :return:
        """

        # 获取到搜索页的文章ID
        pk = int(self._global_settings.get('search_page_doc_id', 0))

        # 获取文章基础数据
        document_data = self._get_document_data(request, pk, page, 'pk', **kwargs)

        # 模板路经
        tpl_path = document_data['tpl_path']

        # QUERY_STRING
        query_string = request.META.get('QUERY_STRING', '')

        # 获取搜索关键词
        kw = request.GET.get('kw', None)
        if not kw:
            kw = None
        else:
            kw = unquote(str(kw))
        # 渲染模板
        return self._render(request, tpl_path, {
            **document_data,
            **{
                'kw': kw,
                'query_string': query_string,
                "current_url": '{scheme}://{host}{url}'.format(
                    scheme=request.scheme,
                    host=request.get_host(),
                    url=document_data['document'].get_url(query_string=query_string, page=page)
                ),
            }
        })
