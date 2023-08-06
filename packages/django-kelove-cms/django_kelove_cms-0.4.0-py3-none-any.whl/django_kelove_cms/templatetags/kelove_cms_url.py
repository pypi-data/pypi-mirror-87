"""
kelove_cms_url.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-09-02 12:06 PM
"""

from django import template

from ..models import Document

register = template.Library()


@register.simple_tag
def kelove_cms_document_url(obj, page=0):
    return obj.get_url(page=page)


@register.simple_tag
def kelove_cms_category_url(obj, page=0):
    return obj.get_url(page=page)


@register.simple_tag
def kelove_cms_tag_url(obj, page=0):
    return obj.get_url(page=page)


@register.simple_tag
def kelove_cms_search_url(query_string: str = '', page=0):
    return Document.get_search_url(query_string=query_string, page=page)


@register.simple_tag
def kelove_cms_type_url(url_type: str, obj, page=0):
    """
    根据实例类型获取相应的URL
    :param url_type:
    :param obj:
    :param page:
    :return:
    """

    if url_type == 'search':
        return Document.get_search_url(query_string=obj, page=page)
    else:
        return obj.get_url(page=page)
