# ==================================================================
#       文 件 名: template_settings.py
#       概    要: 模板配置
#       作    者: IT小强 
#       创建时间: 8/12/20 4:05 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django_kelove_admin.settings import SettingsForm
from django_kelove_admin.util import load_object

from . import DOCUMENT_TEMPLATE, CATEGORY_TEMPLATE, TAG_TEMPLATE


class TemplateSettingsForm(SettingsForm):
    """
    模板配置基类
    """

    is_cms_template = True

    # 自定义模板渲染变量（值为字典或者字符串，字符串表示回调函数）

    # def view_assign(view_assign_settings=None):
    #     if view_assign_settings is None:
    #         view_assign_settings = {}
    #     return {
    #         'top_nav': models.Nav.objects.filter(
    #             nav_group=view_assign_settings.get('top_nav', 1)
    #         ).all(),
    #         'aq01': '01就01'
    #     }
    # view_assign = 'django_kelove_cms_kelove.assign.view_assign'
    view_assign = {}

    # document_templates = {
    #     'default_tpl': {
    #         'template_name': 'default_tpl',
    #         'template_title': '默认模板',
    #         'template_path': 'django_kelove_cms_kelove/home/document/default.html',
    #         'inline_model': 'django_kelove_cms_kelove.models.Doc',
    #         'inline_model_admin': 'django_kelove_cms_kelove.admin.DocInline',
    #     },
    #     'default_tpl2': {
    #         'template_name': 'default_tpl2',
    #         'template_title': '默认模板2',
    #         'template_path': 'django_kelove_cms_kelove/home/document/default.html',
    #         'inline_model': None,
    #         'inline_model_admin': None,
    #     },
    # }

    document_templates = {}

    category_templates = {}

    tag_templates = {}

    _allow_type = {DOCUMENT_TEMPLATE, CATEGORY_TEMPLATE, TAG_TEMPLATE}

    @classmethod
    def get_inline(cls, template_name, inlines_type=DOCUMENT_TEMPLATE, default_inlines=None):
        """
        获取 inline_model_admin
        :param template_name:
        :param inlines_type:
        :param default_inlines:
        :return:
        """

        if inlines_type not in cls._allow_type:
            raise ValueError('inlines type must in ' + str(cls._allow_type))

        if default_inlines is None:
            default_inlines = []

        templates = getattr(cls, inlines_type, {})
        if not templates:
            return default_inlines

        try:
            template = templates.get(template_name, list(templates.values())[0])
        except KeyError:
            template = None

        if (not template) or (not isinstance(template, dict)):
            return default_inlines

        inline_model_admin = template.get('inline_model_admin', None)
        if not inline_model_admin:
            return default_inlines

        if isinstance(inline_model_admin, str):
            inline_model_admin = load_object(inline_model_admin)

        return list(set(default_inlines + [inline_model_admin]))
