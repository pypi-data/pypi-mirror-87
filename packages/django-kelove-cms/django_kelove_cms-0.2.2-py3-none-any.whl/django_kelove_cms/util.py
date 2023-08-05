# ==================================================================
#       文 件 名: util.py
#       概    要: 助手工具
#       作    者: IT小强 
#       创建时间: 8/12/20 3:10 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from uuid import uuid4

from django.urls import reverse

from django_kelove_admin.util import load_object

from . import DOCUMENT_TEMPLATE, DOCUMENT_TYPE_CHOICE_URL
from .settings import GlobalSettingsForm

__all__ = [
    'get_tpl_choices',
    'get_uuid_str',
    'get_current_tpl_form',
    'get_extension_data',
    'get_tpl_path',
    'get_page_limit',
]


def get_tpl_choices(key: str = DOCUMENT_TEMPLATE):
    """
    获取模板可选项
    :param key:标识 DOCUMENT_TEMPLATE | CATEGORY_TEMPLATE | TAG_TEMPLATE
    :return:
    """

    choices = ()
    global_settings_form = GlobalSettingsForm.get()
    template_settings = global_settings_form.get('template_settings', None)
    if not template_settings:
        return choices
    data: dict = getattr(load_object(template_settings), key, {})
    choices = ((k, v['template_title']) for k, v in data.items())
    return choices


def get_uuid_str(prefix: str = '') -> str:
    """
    生成uuid字符串
    :param prefix:
    :return:
    """

    _uuid_str = str(uuid4().hex)
    _uuid_str = 'u' + prefix + _uuid_str[:5] + _uuid_str[-4:]
    return _uuid_str.lower()


def get_current_tpl_form():
    """
    获取当前启用模板的配置类
    :return:
    """

    global_settings_form = GlobalSettingsForm.get()

    template_settings = global_settings_form.get('template_settings', None)

    return load_object(template_settings)


def get_extension_data(base_model_data, key, one_to_one_field):
    """
    获取扩展模型的数据
    :param base_model_data:
    :param key:
    :param one_to_one_field:
    :return:
    """

    data_extension = None

    # 获取模板配置类
    template_settings_cls = get_current_tpl_form()

    data: dict = getattr(template_settings_cls, key, {})
    data: dict = data.get(base_model_data.template, data.get('default', {}))
    inline_model = data.get('inline_model', None)

    if inline_model:
        if isinstance(inline_model, str):
            inline_model = load_object(inline_model)
        data_extension = inline_model.objects.filter(**{one_to_one_field: base_model_data})

    return data_extension


def get_tpl_path(base_model_data, key):
    """
    获取模板路经
    :param base_model_data:
    :param key:
    :return:
    """

    template_settings_cls = get_current_tpl_form()

    data: dict = getattr(template_settings_cls, key, {})
    data: dict = data.get(base_model_data.template, data.get('default', {}))

    return data.get('template_path', None)


def get_page_limit(page_limit: int = 0):
    """
    获取分页数量
    :param page_limit:
    :return:
    """

    default_page_limit = 10

    if page_limit < 1:
        global_settings_form = GlobalSettingsForm.get()
        page_limit = global_settings_form.get('page_limit', default_page_limit)
        if not page_limit:
            page_limit = 10
        page_limit = int(page_limit)
    return page_limit if page_limit >= 1 else default_page_limit
