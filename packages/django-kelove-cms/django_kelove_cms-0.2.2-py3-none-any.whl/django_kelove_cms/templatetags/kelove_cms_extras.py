# ==================================================================
#       文 件 名: kelove_cms_extras.py
#       概    要: CMS 扩展标签
#       作    者: IT小强 
#       创建时间: 8/13/20 2:35 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from json import dumps
from random import randint

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def kelove_cms_has_permission(user, permission):
    """
    权限检查
    :param user:
    :param permission:
    :return:
    """

    return user.has_perm(permission)


@register.simple_tag
def kelove_cms_randint(a: int, b: int) -> int:
    """
    生成随机整数
    :param a:
    :param b:
    :return:
    """

    return randint(a, b)


@register.simple_tag
def kelove_cms_to_json(data) -> str:
    """
    python 对象转json字符串
    :param data:
    :return:
    """

    return mark_safe(dumps(data))
