# ==================================================================
#       文 件 名: settings.py
#       概    要: 配置管理
#       作    者: IT小强 
#       创建时间: 8/12/20 2:37 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django import forms
from django.utils.translation import gettext_lazy as _

from django_kelove_admin import SettingsRegister
from django_kelove_admin.forms.fields import JSONField
from django_kelove_admin.settings import SettingsForm
from django_kelove_admin.util import load_object


def get_template_settings_choices():
    """
    获取可用的CMS模板
    :return:
    """

    page_tpl_choices = SettingsRegister.get()

    template_settings_choices = []
    for i in page_tpl_choices:
        obj = None
        try:
            obj = load_object(i)
        except (ImportError, AttributeError):
            pass
        if not obj:
            continue

        is_cms_template = getattr(obj, 'is_cms_template', False)
        if not is_cms_template:
            continue
        template_settings_choices.append([obj.get_settings_key(), obj.get_settings_title()])
    return template_settings_choices


class GlobalSettingsForm(SettingsForm):
    """
    全局配置
    """

    settings_title = _('内容管理全局配置')

    def __init__(self, data=None, files=None, **kwargs):
        super().__init__(data, files, **kwargs)
        self.update_choices('template_settings', get_template_settings_choices())

    URL_KEY_CHOICES = (
        ('id', 'ID'),
        ('name', '标识'),
    )

    FORM_EDITOR_CHOICES = (
        ('default', '默认'),
        ('markdown', 'Markdown编辑器'),
    )

    FILE_SELECTOR_CHOICES = (
        ('default', '默认'),
        ('ckfinder', 'CKFinder文件管理器'),
    )

    template_settings = forms.ChoiceField(
        choices=[],
        initial='',
        label=_('前端模板'),
    )

    form_editor = forms.ChoiceField(
        initial='default',
        label=_("内容编辑器"),
        choices=FORM_EDITOR_CHOICES
    )

    file_selector = forms.ChoiceField(
        initial='default',
        label=_("文件选择器"),
        choices=FILE_SELECTOR_CHOICES
    )

    home_page_doc_id = forms.IntegerField(
        initial=1,
        label=_("首页文章ID"),
        help_text=_('此处填写将要作为首页的文章ID，可在文章管理列表获取到ID')
    )

    search_page_doc_id = forms.IntegerField(
        initial=2,
        label=_("搜索页文章ID"),
        help_text=_('此处填写将要作为搜索页的文章ID，可在文章管理列表获取到ID')
    )

    page_limit = forms.IntegerField(
        initial=10,
        label=_("分页数量")
    )

    page_title = forms.CharField(
        initial='',
        required=False,
        label=_("页面标题")
    )

    page_sub_title = forms.CharField(
        initial='',
        required=False,
        label=_("页面副标题")
    )

    page_keywords = forms.CharField(
        initial='',
        required=False,
        label=_("页面关键词"),
        widget=forms.Textarea,
        help_text=_('多个关键词之间使用英文逗号分割')
    )

    page_description = forms.CharField(
        initial='',
        required=False,
        label=_("页面描述"),
        widget=forms.Textarea,
        help_text=_('页面描述不宜超过200字')
    )

    document_url_key = forms.ChoiceField(
        initial='id',
        label=_("文章页面路由标识"),
        choices=URL_KEY_CHOICES
    )

    category_url_key = forms.ChoiceField(
        initial='id',
        label=_("分类页面路由标识"),
        choices=URL_KEY_CHOICES
    )

    tag_url_key = forms.ChoiceField(
        initial='id',
        label=_("标签页面路由标识"),
        choices=URL_KEY_CHOICES
    )

    page_beian = forms.CharField(
        initial='',
        required=False,
        label=_("备案号"),
    )

    page_beian_url = forms.CharField(
        initial='http://www.beian.miit.gov.cn',
        required=False,
        label=_("备案号链接地址"),
        help_text=_("一般为：") + 'http://www.beian.miit.gov.cn'
    )

    page_copyright = forms.CharField(
        initial='',
        required=False,
        label=_("站点版权信息"),
        widget=forms.Textarea,
    )

    page_favicon_icon = forms.CharField(
        initial='',
        required=False,
        label=_('站点小图标favicon.ico'),
    )
