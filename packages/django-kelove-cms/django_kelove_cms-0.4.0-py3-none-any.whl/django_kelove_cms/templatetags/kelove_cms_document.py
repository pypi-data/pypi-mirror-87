"""
kelove_cms_document.py 文档相关
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-09-02 11:33 AM
"""

from django import template
from django.core.paginator import Paginator
from django.db.models import Q

from .. import CMS_BASE_FILTER, models, util

register = template.Library()


def get_document_paginator(document, current_page: int = 1, page_limit: int = 0):
    """
    获取文档分页
    :param document: 文档查询集
    :param current_page: 当前页
    :param page_limit: 分页数量
    :return:
    """

    document = document.select_related("category", "created_user", "updated_user").all()
    paginator = Paginator(document, util.get_page_limit(page_limit))

    return paginator.page(current_page)


@register.simple_tag
def kelove_cms_all_paginator(current_page: int = 1, page_limit: int = 0, sort_field='-id'):
    """
    所有文档分页
    :param sort_field:
    :param current_page:
    :param page_limit:
    :return:
    """

    filter_list = []
    filter_dict = {}

    filter_data = {**filter_dict, **CMS_BASE_FILTER}

    document = models.Document.objects.filter(*filter_list, **filter_data).order_by(sort_field)

    return get_document_paginator(
        document=document,
        current_page=current_page,
        page_limit=page_limit,
    )


@register.simple_tag
def kelove_cms_search_paginator(kw, current_page: int = 1, page_limit: int = 0, sort_field='-id'):
    """
    搜索页文档分页
    :param sort_field:
    :param kw: 搜索关键词
    :param current_page:
    :param page_limit:
    :return:
    """

    if not kw:
        filter_list = []
        filter_dict = {"title": ''}
    else:
        kw = str(kw)
        filter_list = [
            Q(title__icontains=kw) | Q(name__icontains=kw) | Q(content__icontains=kw) | Q(description__icontains=kw)
        ]
        filter_dict = {}

    filter_data = {**filter_dict, **CMS_BASE_FILTER}

    document = models.Document.objects.filter(*filter_list, **filter_data).order_by(sort_field)

    return get_document_paginator(
        document=document,
        current_page=current_page,
        page_limit=page_limit,
    )


@register.simple_tag
def kelove_cms_category_paginator(obj, current_page: int = 1, page_limit: int = 0, sort_field='-id'):
    """
    分类页文档分页
    :param sort_field:
    :param obj:
    :param current_page:
    :param page_limit:
    :return:
    """

    filter_data = {**{"category": obj}, **CMS_BASE_FILTER}

    document = models.Document.objects.filter(**filter_data).order_by(sort_field)

    return get_document_paginator(
        document=document,
        current_page=current_page,
        page_limit=page_limit,
    )


@register.simple_tag
def kelove_cms_tag_paginator(obj, current_page: int = 1, page_limit: int = 0, sort_field='-id'):
    """
    标签页文档分页
    :param sort_field:
    :param obj:
    :param current_page:
    :param page_limit:
    :return:
    """

    filter_data = {**{"tag": obj}, **CMS_BASE_FILTER}

    document = models.Document.objects.filter(**filter_data).order_by(sort_field)

    return get_document_paginator(
        document=document,
        current_page=current_page,
        page_limit=page_limit,
    )


@register.simple_tag
def kelove_cms_document_prev(obj):
    """
    获取上一篇文章
    :return:
    """

    return models.Document.objects.filter(
        pk__lt=obj.pk,
        category=obj.category,
        **CMS_BASE_FILTER
    ).order_by('-id').first()


@register.simple_tag
def kelove_cms_document_next(obj):
    """
    获取下一篇文章
    :return:
    """

    return models.Document.objects.filter(
        pk__gt=obj.pk,
        category=obj.category,
        **CMS_BASE_FILTER
    ).order_by('id').first()


@register.simple_tag
def kelove_cms_document_archives():
    """
    归档专用
    :return:
    """

    data = models.Document.objects.filter(
        **CMS_BASE_FILTER
    ).order_by('-created_time', '-id').all()

    archives = {}

    for item in data:
        c_time = item.created_time
        c_year = str(c_time.year)
        c_month = str(c_time.month)
        c_day = str(c_time.day)
        c_year_data = archives.get(c_year, None)
        if not isinstance(c_year_data, dict):
            archives[c_year] = {}
        c_month_data = archives[c_year].get(c_month, None)
        if not isinstance(c_month_data, dict):
            archives[c_year][c_month] = {}
        c_day_data = archives[c_year][c_month].get(c_day, None)
        if not isinstance(c_day_data, list):
            archives[c_year][c_month][c_day] = []
        archives[c_year][c_month][c_day].append(item)

    return archives
