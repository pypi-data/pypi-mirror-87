# ==================================================================
#       文 件 名: forms.py
#       概    要: 表单
#       作    者: IT小强 
#       创建时间: 8/12/20 5:50 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import random

from django import forms
from django.utils.translation import gettext_lazy as _

from django_kelove_admin.forms.fields import EditorMdField, CkFinderField

from . import models
from .settings import GlobalSettingsForm


def get_field_settings():
    return {'height': random.randint(10, 600)}


class BaseForm(forms.ModelForm):
    """
    表单基类
    """

    def __init__(self, *args, **kwargs):
        self.global_settings = GlobalSettingsForm.get()
        super().__init__(*args, **kwargs)

    def get_content_field(self, field_name: str = '', field_title: str = ''):
        """
        获取内容字段
        :return:
        """

        form_editor = self.global_settings.get('form_editor', 'default')
        if form_editor == 'markdown':
            # 文档内容
            self.base_fields[field_name] = self.fields[field_name] = EditorMdField(
                label=_(field_title),
                initial='',
                required=False
            )

    def get_file_field(self, field_name: str = '', field_title: str = ''):
        """
        获取文件上传字段
        :return:
        """

        file_selector = self.global_settings.get('file_selector', 'default')

        if file_selector == 'ckfinder':
            self.base_fields[field_name] = self.fields[field_name] = CkFinderField(
                label=_(field_title),
                initial='',
                required=False
            )


class NavForm(BaseForm):
    """
    导航管理表单
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_file_field('image', '导航图片')

    def clean(self):
        cleaned_data = super().clean()

        # 获取当前实例的导航分组
        nav_group = cleaned_data.get('nav_group', None)

        # 获取当前实例的导航分组主键值
        if nav_group:
            nav_group_pk = nav_group.pk
        else:
            nav_group_pk = 0

        # 获取当前实例的父级
        parent = cleaned_data.get('parent', None)

        # 获取当前实例的父级的分组
        if parent:
            parent_nav_group = parent.nav_group
        else:
            parent_nav_group = None

        # 获取当前实例的父级的分组主键值
        if parent_nav_group:
            parent_nav_group_pk = parent_nav_group.pk
        else:
            parent_nav_group_pk = 0

        if parent:  # 父级存在即非顶级节点
            if parent_nav_group_pk != nav_group_pk:  # 判断当前实例的分组是否与上级的分组一致
                raise forms.ValidationError(_('当前导航与上级导航分组不一致'))
        else:
            try:
                self.instance.get_descendants(include_self=False).update(nav_group=nav_group)
            except ValueError:
                pass

        return cleaned_data

    class Meta:
        exclude = []
        model = models.Nav


class CategoryForm(BaseForm):
    """
    分类管理表单
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_content_field('content', '分类内容')
        self.get_file_field('image', '分类图片')

    class Meta:
        exclude = []
        model = models.Category


class DocumentForm(BaseForm):
    """
    文档管理表单
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_content_field('content', '文档内容')
        self.get_file_field('image', '文档图片')

    def clean(self):
        cleaned_data = super().clean()

        # 获取当前实例的分类
        category = cleaned_data.get('category', None)

        # 获取当前实例的分类主键值
        if category:
            category_pk = category.pk
        else:
            category_pk = 0

        # 获取当前实例的父级
        parent = cleaned_data.get('parent', None)

        # 获取当前实例的父级的分类
        if parent:
            parent_category = parent.category
        else:
            parent_category = None

        # 获取当前实例的父级的分类主键值
        if parent_category:
            parent_category_pk = parent_category.pk
        else:
            parent_category_pk = 0

        if parent:  # 父级存在即非顶级节点
            if parent_category_pk != category_pk:  # 判断当前实例的分类是否与上级的分类一致
                raise forms.ValidationError(_('当前文档与上级文档分类不一致'))
        else:
            try:
                self.instance.get_descendants(include_self=False).update(category=parent_category)
            except ValueError:
                pass

        return cleaned_data

    class Meta:
        exclude = []
        model = models.Document
