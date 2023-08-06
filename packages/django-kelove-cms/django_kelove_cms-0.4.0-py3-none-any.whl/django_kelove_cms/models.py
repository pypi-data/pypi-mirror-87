# ==================================================================
#       文 件 名: models.py
#       概    要: 模型
#       作    者: IT小强 
#       创建时间: 8/12/20 2:48 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from hashlib import md5
from urllib.parse import unquote, quote

from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models

from mptt.fields import TreeForeignKey

from django_kelove_admin.models import AllModel, MPTTModel
from django_kelove_admin.conf import settings

from . import DOCUMENT_TEMPLATE, CATEGORY_TEMPLATE, TAG_TEMPLATE, DOCUMENT_TYPE_CHOICE_DOC, DOCUMENT_TYPE_CHOICE_WIKI, \
    DOCUMENT_TYPE_CHOICE_URL, DOCUMENT_TYPE_CHOICE_PAGE
from .settings import GlobalSettingsForm
from .util import get_uuid_str, get_tpl_choices
from .validators import NameValidator

DATABASE_FOREIGN_DELETE_TYPE = getattr(settings, 'DATABASE_FOREIGN_DELETE_TYPE', models.PROTECT)

DATABASE_CONSTRAINT = getattr(settings, 'DATABASE_CONSTRAINT', False)


def get_pk_value(obj, key: str, default='pk'):
    global_settings = GlobalSettingsForm.get()
    url_key = global_settings.get(key, default)
    url_key = url_key if url_key else default

    if url_key != 'pk':
        pk_value = getattr(obj, url_key)
    else:
        try:
            pk_value = getattr(obj, url_key)
        except AttributeError:
            pk_value = getattr(obj, 'id')
    return pk_value


class NavGroup(AllModel):
    """
    导航分组
    """

    # 导航分组名称
    title = models.CharField(
        verbose_name=_('导航分组名称'),
        max_length=191,
        null=False,
        blank=False,
        default='',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('导航分组')
        verbose_name_plural = _('导航分组')


class Nav(MPTTModel, AllModel):
    """
    导航
    """

    category = TreeForeignKey(
        'Category',
        verbose_name=_('关联分类'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=True,
        blank=True,
        default=None
    )

    tag = models.ForeignKey(
        'Tag',
        verbose_name=_('关联标签'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=True,
        blank=True,
        default=None
    )

    document = models.ForeignKey(
        'Document',
        verbose_name=_('关联文档'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=True,
        blank=True,
        default=None
    )

    # 导航分组
    nav_group = models.ForeignKey(
        'NavGroup',
        verbose_name=_('导航分组'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=False,
        blank=False
    )

    # 上级导航
    parent = TreeForeignKey(
        'self',
        verbose_name=_('上级导航'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=True,
        blank=True,
        default=None
    )

    # 导航名称
    title = models.CharField(
        verbose_name=_('导航名称'),
        max_length=191,
        default=''
    )

    # 导航图片
    image = models.CharField(
        verbose_name=_('导航图片'),
        max_length=191,
        default='',
        blank=True
    )

    # 导航图标
    icon = models.CharField(
        verbose_name=_('导航图标'),
        max_length=191,
        default='',
        blank=True
    )

    # 导航链接
    url = models.URLField(
        verbose_name=_('导航链接'),
        max_length=191,
        default='',
        blank=True
    )

    # 导航描述
    description = models.TextField(
        verbose_name=_('导航描述'),
        default='',
        null=False,
        blank=True
    )

    def mptt_title(self):
        return format_html(
            '{} {}',
            self.level * '---',
            self.title
        )

    mptt_title.short_description = _('层级关系')

    def nav_url(self):
        """
        导航完整链接
        :return:
        """

        if self.document is not None:
            return self.document.get_url()

        if self.category is not None:
            return self.category.get_url()

        if self.tag is not None:
            return self.tag.get_url()

        return unquote(self.url)

    nav_url.short_description = _('导航完整链接')

    def nav_tag(self):
        """
        导航标识
        :return:
        """

        if self.document is not None:
            return 'document_' + str(self.document.pk)

        if self.category is not None:
            return 'category_' + str(self.category.pk)

        if self.tag is not None:
            return 'tag_' + str(self.tag.pk)

        return md5(quote(self.url).encode()).hexdigest()

    nav_tag.short_description = _('导航标识')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('导航')
        verbose_name_plural = _('导航管理')

    class MPTTMeta:
        order_insertion_by = ['sort']


class Tag(AllModel):
    """
    标签
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tpl_choices = tuple(get_tpl_choices(TAG_TEMPLATE))
        self._meta.get_field('template').choices = tpl_choices
        if len(tpl_choices) >= 1:
            self._meta.get_field('template').default = tpl_choices[0][0]

    # 标签标识
    name = models.CharField(
        unique=True,
        verbose_name=_('标签标识'),
        max_length=191,
        null=False,
        blank=True,
        default=get_uuid_str,
        validators=[NameValidator()],
        help_text=NameValidator.message,
    )

    # 标签名称
    title = models.CharField(
        unique=True,
        verbose_name=_('标签名称'),
        max_length=191,
        null=False,
        blank=False
    )

    # 标签模板
    template = models.CharField(
        verbose_name=_('标签模板'),
        choices=[],
        default='',
        max_length=191,
        null=False,
        blank=False,
    )

    # 标签描述
    description = models.TextField(
        verbose_name=_('标签描述'),
        default='',
        blank=True,
        null=False,
    )

    def get_url(self, page=0, query_string: str = ''):
        """
        获取URL地址
        :param query_string:
        :param page:
        :return:
        """

        pk_value = get_pk_value(self, 'tag_url_key')

        if page == '__PAGE__' or int(page) > 1:
            return reverse('django_kelove_cms:tag', kwargs={'pk': pk_value, 'page': page})
        else:
            return reverse('django_kelove_cms:tag_home', kwargs={'pk': pk_value})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('标签')
        verbose_name_plural = _('标签管理')


class Category(MPTTModel, AllModel):
    """
    分类
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tpl_choices = tuple(get_tpl_choices(CATEGORY_TEMPLATE))
        self._meta.get_field('template').choices = tpl_choices
        if len(tpl_choices) >= 1:
            self._meta.get_field('template').default = tpl_choices[0][0]

    # 上级分类
    parent = TreeForeignKey(
        'self',
        verbose_name=_('上级分类'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=True,
        blank=True,
        default=None
    )

    # 分类标识
    name = models.CharField(
        unique=True,
        verbose_name=_('分类标识'),
        max_length=191,
        null=False,
        blank=True,
        default=get_uuid_str,
        validators=[NameValidator()],
        help_text=NameValidator.message,
    )

    # 分类名称
    title = models.CharField(
        unique=True,
        verbose_name=_('分类名称'),
        max_length=191,
        default='',
        null=False,
        blank=False
    )

    # 分类模板
    template = models.CharField(
        verbose_name=_('分类模板'),
        max_length=191,
        choices=[],
        default='',
        blank=False,
        null=False,
    )

    # 分类图片
    image = models.CharField(
        verbose_name=_('分类图片'),
        max_length=191,
        default='',
        blank=True,
        null=False,
    )

    # 分类图标
    icon = models.CharField(
        verbose_name=_('分类图标'),
        max_length=191,
        default='',
        blank=True,
        null=False,
    )

    # 分类描述
    description = models.TextField(
        verbose_name=_('分类描述'),
        default='',
        blank=True,
        null=False,
    )

    # 分类内容
    content = models.TextField(
        verbose_name=_('分类内容'),
        default='',
        blank=True,
        null=False,
        help_text=_('分类作为单页使用时可填写该内容')
    )

    def mptt_title(self):
        return format_html(
            '{} {}',
            self.level * '---',
            self.title
        )

    mptt_title.short_description = _('层级关系')

    def get_url(self, page=0, query_string: str = ''):
        """
        获取URL地址
        :param query_string:
        :param page:
        :return:
        """

        pk_value = get_pk_value(self, 'category_url_key')

        if page == '__PAGE__' or int(page) > 1:
            return reverse('django_kelove_cms:category', kwargs={'pk': pk_value, 'page': page})
        else:
            return reverse('django_kelove_cms:category_home', kwargs={'pk': pk_value})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('分类')
        verbose_name_plural = _('分类管理')

    class MPTTMeta:
        order_insertion_by = ['sort']


class Document(MPTTModel, AllModel):
    """
    文档
    """

    TYPE_CHOICES = (
        (DOCUMENT_TYPE_CHOICE_DOC, _('文章')),
        (DOCUMENT_TYPE_CHOICE_PAGE, _('单页')),
        (DOCUMENT_TYPE_CHOICE_URL, _('外链')),
        (DOCUMENT_TYPE_CHOICE_WIKI, _('手册')),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tpl_choices = tuple(get_tpl_choices(DOCUMENT_TEMPLATE))
        self._meta.get_field('template').choices = tpl_choices
        if len(tpl_choices) >= 1:
            self._meta.get_field('template').default = tpl_choices[0][0]

    # 文档分类
    category = TreeForeignKey(
        'Category',
        verbose_name=_('文档分类'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=True,
        blank=True,
    )

    # 上级文档
    parent = TreeForeignKey(
        'self',
        verbose_name=_('上级文档'),
        on_delete=DATABASE_FOREIGN_DELETE_TYPE,
        db_constraint=DATABASE_CONSTRAINT,
        null=True,
        blank=True,
        default=None
    )

    # 文档标签
    tag = models.ManyToManyField(
        'Tag',
        verbose_name=_('文档标签'),
        blank=True,
    )

    # 文档标识
    name = models.CharField(
        unique=True,
        verbose_name=_('文档标识'),
        max_length=191,
        null=False,
        blank=True,
        default=get_uuid_str,
        validators=[NameValidator()],
        help_text=NameValidator.message,
    )

    # 文档名称
    title = models.CharField(
        unique=True,
        verbose_name=_('文档名称'),
        max_length=191,
        default='',
        null=False,
        blank=False
    )

    # 文档描述
    description = models.TextField(
        verbose_name=_('文档描述'),
        default='',
        blank=True,
        null=False,
    )

    # 文档类型
    type = models.CharField(
        verbose_name=_('文档类型'),
        choices=TYPE_CHOICES,
        default=DOCUMENT_TYPE_CHOICE_DOC,
        max_length=191,
        null=False,
        blank=False,
    )

    # 文档链接
    url = models.URLField(
        verbose_name=_('文档链接'),
        max_length=191,
        default='',
        blank=True,
        help_text=_('文档类型为外链时必须')
    )

    # 文档模板
    template = models.CharField(
        verbose_name=_('文档模板'),
        choices=[],
        default='',
        max_length=191,
        null=False,
        blank=False,
    )

    # 文档图片
    image = models.CharField(
        verbose_name=_('文档图片'),
        max_length=191,
        default='',
        blank=True,
        null=False,
    )

    # 文档图标
    icon = models.CharField(
        verbose_name=_('文档图标'),
        max_length=191,
        default='',
        blank=True,
        null=False,
    )

    # 文档内容
    content = models.TextField(
        verbose_name=_('文档内容'),
        default='',
        blank=True,
        null=False,
    )

    def mptt_title(self):
        return format_html(
            '{} {}',
            self.level * '---',
            self.title
        )

    mptt_title.short_description = _('层级关系')

    def get_url(self, page=0, query_string: str = ''):
        """
        获取URL地址
        :param query_string:
        :param page:
        :return:
        """

        pk_value = get_pk_value(self, 'document_url_key')
        global_settings_form = GlobalSettingsForm.get()

        # 外链文章自动转换
        if self.type == DOCUMENT_TYPE_CHOICE_URL:
            return self.url

        # 首页自动转换
        home_page_doc_id = int(global_settings_form.get('home_page_doc_id', 0))
        if home_page_doc_id == self.pk:
            if page == '__PAGE__' or int(page) > 1:
                return reverse('django_kelove_cms:home_page', kwargs={'page': page})
            else:
                return reverse('django_kelove_cms:home')

        # 搜索页自动转换
        search_page_doc_id = int(global_settings_form.get('search_page_doc_id', 0))
        if search_page_doc_id == self.pk:
            return self.get_search_url(query_string=query_string, page=page)

        if page == '__PAGE__' or int(page) > 1:
            return reverse('django_kelove_cms:document', kwargs={'pk': pk_value, 'page': page})
        else:
            return reverse('django_kelove_cms:document_home', kwargs={'pk': pk_value})

    @staticmethod
    def get_search_url(query_string: str = '', page=0):
        """
        搜索路由
        :param query_string:
        :param page:
        :return:
        """

        query_string = '?' + query_string if query_string else ''

        if page == '__PAGE__' or int(page) > 1:
            return reverse('django_kelove_cms:search', kwargs={'page': page}) + query_string
        else:
            return reverse('django_kelove_cms:search_home', kwargs={}) + query_string

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('文档')
        verbose_name_plural = _('文档管理')

    class MPTTMeta:
        order_insertion_by = ['sort']
