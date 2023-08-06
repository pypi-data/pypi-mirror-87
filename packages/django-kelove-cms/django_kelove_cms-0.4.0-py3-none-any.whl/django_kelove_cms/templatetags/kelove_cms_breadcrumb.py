"""
kelove_cms_breadcrumb.py 面包屑导航
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-09-02 11:55 AM
"""

from django import template

register = template.Library()


@register.simple_tag
def kelove_cms_document_breadcrumb(obj):
    """
    文档面包屑导航
    :param obj:
    :return:
    """

    breadcrumb = []

    category = obj.category
    if category:
        breadcrumb = [{
            'title': i.title,
            'icon': i.icon,
            'url': i.get_url(),
        } for i in category.get_ancestors(include_self=True, ascending=False)]

    breadcrumb.append({
        'title': obj.title,
        'icon': 'fa-file',
        'url': obj.get_url(),
    })

    return breadcrumb


@register.simple_tag
def kelove_cms_category_breadcrumb(obj):
    """
    分类面包屑导航
    :param obj:
    :return:
    """

    breadcrumb = [{
        'title': i.title,
        'icon': i.icon,
        'url': i.get_url(),
    } for i in obj.get_ancestors(include_self=True, ascending=False)]

    return breadcrumb


@register.simple_tag
def kelove_cms_tag_breadcrumb(obj):
    """
    标签面包屑导航
    :param obj:
    :return:
    """

    breadcrumb = [{
        'title': obj.title,
        'icon': 'fa-tag',
        'url': obj.get_url(),
    }]

    return breadcrumb
