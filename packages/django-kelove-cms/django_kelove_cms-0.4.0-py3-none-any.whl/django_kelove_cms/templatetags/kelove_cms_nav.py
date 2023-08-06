"""
kelove_cms_nav.py 导航相关
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-09-02 11:52 AM
"""

from django import template

from .. import CMS_BASE_FILTER, models

register = template.Library()


@register.simple_tag
def kelove_cms_navs(nav_group_id: int):
    """
    根据导航组ID获取导航
    :param nav_group_id:
    :return:
    """

    try:
        nav_group_id = int(nav_group_id)
    except ValueError:
        return None

    return models.Nav.objects.filter(
        nav_group=nav_group_id,
        **CMS_BASE_FILTER
    ).select_related("category", "tag", "document", "nav_group").all()
