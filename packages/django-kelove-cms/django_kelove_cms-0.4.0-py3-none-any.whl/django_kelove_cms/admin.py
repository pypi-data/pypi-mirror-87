# ==================================================================
#       文 件 名: admin.py
#       概    要: 后台管理
#       作    者: IT小强 
#       创建时间: 8/12/20 3:20 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.contrib.admin import register
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_kelove_admin.util import load_object

from import_export.admin import ImportExportMixin
from mptt.admin import TreeRelatedFieldListFilter

from django_kelove_admin.admin import ModelAdminWithUser, ModelAdminMPTTWithUser
from mptt.exceptions import InvalidMove

from . import models, forms, TAG_TEMPLATE, CATEGORY_TEMPLATE, DOCUMENT_TEMPLATE
from .settings import GlobalSettingsForm


def get_inlines(request, obj, inlines_type, default_inlines=None):
    if default_inlines is None:
        default_inlines = []
    template_name = request.GET.get('kelove_tpl', None)
    if not template_name:
        template_name = getattr(obj, 'template', None)
    global_settings_form = GlobalSettingsForm.get()
    template_settings = global_settings_form.get('template_settings', None)
    if not template_settings:
        return default_inlines

    return load_object(template_settings).get_inline(
        template_name=template_name,
        inlines_type=inlines_type,
        default_inlines=default_inlines
    )


@register(models.NavGroup)
class NavGroup(ImportExportMixin, ModelAdminWithUser):
    """
    导航分组管理
    """

    list_display = (
        'id',
        'title',
        'sort',
        'created_user',
        'created_time',
        'updated_user',
        'updated_time',
        'enabled',
        'status'
    )

    list_display_links = ('id', 'title')

    list_filter = ('status', 'enabled', 'created_time', 'updated_time')

    search_fields = ('title',)

    fieldsets = (
        (
            _('基础信息'),
            {
                'fields': (
                    'title',
                )
            }
        ),
        (
            _('扩展信息'),
            {
                'classes': ('collapse',),
                'fields': ('enabled', 'status', 'sort',)
            }
        ),
    )


@register(models.Nav)
class Nav(ImportExportMixin, ModelAdminMPTTWithUser):
    """
    导航管理
    """

    form = forms.NavForm

    mptt_level_indent = 20
    mptt_indent_field = "title"
    list_display = (
        'id',
        'mptt_title',
        'title',
        'nav_group',
        'nav_url',
        'nav_tag',
        'sort',
        'created_user',
        'created_time',
        'updated_user',
        'updated_time',
        'enabled',
        'status',
        'action_list'
    )

    list_display_links = ('id', 'mptt_title')

    list_filter = ('nav_group', 'status', 'enabled', 'created_time', 'updated_time')

    search_fields = ('title', 'description')

    raw_id_fields = ('category', 'tag', 'document')

    fieldsets = (
        (
            _('导航内容'),
            {
                'fields': (
                    'title',
                    'nav_group',
                    'parent',
                    'url',
                )
            }
        ),
        (
            _('基础信息'),
            {
                'classes': ('collapse',),
                'fields': (
                    'category',
                    'document',
                    'tag',
                    'image',
                    'icon',
                    'description'
                )
            }
        ),
        (
            _('扩展信息'),
            {
                'classes': ('collapse',),
                'fields': ('enabled', 'status', 'sort',)
            }
        ),
    )

    def action_list(self, obj):
        return mark_safe('<a href="{url}" target="_blank">{title}</a>'.format(
            url=obj.nav_url(),
            title='浏览'
        ))

    action_list.short_description = '操作'

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except InvalidMove:
            pass


@register(models.Tag)
class Tag(ImportExportMixin, ModelAdminWithUser):
    """
    标签管理
    """

    list_display = (
        'id',
        'name',
        'title',
        'template',
        'sort',
        'created_user',
        'created_time',
        'updated_user',
        'updated_time',
        'enabled',
        'status',
        'action_list'
    )
    list_display_links = ('id', 'name', 'title')
    list_filter = (
        'template',
        'status',
        'enabled',
        'created_time',
        'updated_time'
    )
    search_fields = ('title', 'name', 'description')

    fieldsets = (
        (
            _('基础信息'),
            {
                'fields': (
                    'template',
                    'name',
                    'title',
                    'description'
                )
            }
        ),
        (
            _('扩展信息'),
            {
                'classes': ('collapse',),
                'fields': ('enabled', 'status', 'sort',)
            }
        ),
    )

    default_inlines = []

    def action_list(self, obj):
        return mark_safe('<a href="{url}" target="_blank">{title}</a>'.format(
            url=obj.get_url(),
            title='浏览'
        ))

    action_list.short_description = '操作'

    def get_inlines(self, request, obj):
        self.inlines = get_inlines(
            request=request,
            obj=obj,
            inlines_type=TAG_TEMPLATE,
            default_inlines=self.default_inlines
        )
        return super().get_inlines(request, obj)

    class Media:
        js = ('kelove_cms/template-select.js',)


@register(models.Category)
class Category(ImportExportMixin, ModelAdminMPTTWithUser):
    """
    分类管理
    """

    form = forms.CategoryForm

    raw_id_fields = ('parent',)

    default_inlines = []

    mptt_level_indent = 30
    mptt_indent_field = "title"

    list_display = (
        'id',
        'mptt_title',
        'name',
        'title',
        'template',
        'image',
        'icon',
        'level',
        'sort',
        'created_user',
        'created_time',
        'updated_user',
        'updated_time',
        'enabled',
        'status',
        'action_list'
    )
    list_display_links = ('id', 'name', 'mptt_title')
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
        'template',
        'status',
        'enabled',
        'created_time',
        'updated_time'
    )
    search_fields = ('title', 'name', 'description')

    fieldsets = (
        (
            _('分类内容'),
            {
                'fields': (
                    'title',
                    'template',
                    'parent',
                )
            }
        ),
        (
            _('基础信息'),
            {
                'classes': ('collapse',),
                'fields': ('name', 'description', 'image', 'icon', 'content')
            }
        ),
        (
            _('扩展信息'),
            {
                'classes': ('collapse',),
                'fields': ('enabled', 'status', 'sort',)
            }
        ),
    )

    def action_list(self, obj):
        return mark_safe('<a href="{url}" target="_blank">{title}</a>'.format(
            url=obj.get_url(),
            title='浏览'
        ))

    action_list.short_description = '操作'

    def get_inlines(self, request, obj):
        self.inlines = get_inlines(
            request=request,
            obj=obj,
            inlines_type=CATEGORY_TEMPLATE,
            default_inlines=self.default_inlines
        )
        return super().get_inlines(request, obj)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except InvalidMove:
            pass

    class Media:
        js = ('kelove_cms/template-select.js',)


@register(models.Document)
class Document(ImportExportMixin, ModelAdminMPTTWithUser):
    """
    文章管理
    """

    raw_id_fields = ('parent', 'category')

    form = forms.DocumentForm

    default_inlines = []

    list_display = (
        'id',
        'mptt_title',
        'name',
        'title',
        'category',
        'type',
        'template',
        'image',
        'icon',
        'sort',
        'created_user',
        'created_time',
        'updated_user',
        'updated_time',
        'enabled',
        'status',
        'action_list'
    )
    list_display_links = ('id', 'name', 'mptt_title')
    list_filter = (
        ('category', TreeRelatedFieldListFilter),
        'type',
        'template',
        'status',
        'enabled',
        'created_time',
        'updated_time'
    )
    search_fields = ('title', 'name', 'description')

    fieldsets = (
        (
            _('文档内容'),
            {
                'fields': (
                    'title',
                    'template',
                    'category',
                    'content',
                )
            }
        ),
        (
            _('基础信息'),
            {
                'classes': ('collapse',),
                'fields': (
                    'description',
                    'name',
                    'parent',
                    'type',
                    'url',
                    'tag',
                    'image',
                    'icon',
                )
            }
        ),
        (
            _('扩展信息'),
            {
                'classes': ('collapse',),
                'fields': ('enabled', 'status', 'sort',)
            }
        ),
    )

    filter_horizontal = ('tag',)

    def action_list(self, obj):
        return mark_safe('<a href="{url}" target="_blank">{title}</a>'.format(
            url=obj.get_url(),
            title='浏览'
        ))

    action_list.short_description = '操作'

    def get_inlines(self, request, obj):
        self.inlines = get_inlines(
            request=request,
            obj=obj,
            inlines_type=DOCUMENT_TEMPLATE,
            default_inlines=self.default_inlines
        )

        return super().get_inlines(request, obj)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except InvalidMove:
            pass

    class Media:
        js = ('kelove_cms/template-select.js',)
