# Generated by Django 3.1 on 2020-09-01 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_kelove_cms.util
import django_kelove_cms.validators
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.IntegerField(choices=[(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')], default=1, help_text='状态{"-1": "草稿", "0": "待审", "1": "通过", "2": "驳回"}', verbose_name='状态')),
                ('enabled', models.BooleanField(db_index=True, default=True, verbose_name='是否启用')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('level', models.PositiveIntegerField(editable=False, verbose_name='级别')),
                ('name', models.CharField(blank=True, default=django_kelove_cms.util.get_uuid_str, help_text='标识至少需要2个字符，且须以字母开头，以字母或数字结尾，只能包含小写字母数字和-', max_length=191, unique=True, validators=[django_kelove_cms.validators.NameValidator()], verbose_name='分类标识')),
                ('title', models.CharField(default='', max_length=191, unique=True, verbose_name='分类名称')),
                ('template', models.CharField(choices=[], default='', max_length=191, verbose_name='分类模板')),
                ('image', models.CharField(blank=True, default='', max_length=191, verbose_name='分类图片')),
                ('icon', models.CharField(blank=True, default='', max_length=191, verbose_name='分类图标')),
                ('description', models.TextField(blank=True, default='', verbose_name='分类描述')),
                ('content', models.TextField(blank=True, default='', help_text='分类作为单页使用时可填写该内容', verbose_name='分类内容')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('created_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_category_created_user_set', to=settings.AUTH_USER_MODEL, verbose_name='创建用户')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.category', verbose_name='上级分类')),
                ('updated_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_category_updated_user_set', to=settings.AUTH_USER_MODEL, verbose_name='更新用户')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类管理',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.IntegerField(choices=[(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')], default=1, help_text='状态{"-1": "草稿", "0": "待审", "1": "通过", "2": "驳回"}', verbose_name='状态')),
                ('enabled', models.BooleanField(db_index=True, default=True, verbose_name='是否启用')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('level', models.PositiveIntegerField(editable=False, verbose_name='级别')),
                ('name', models.CharField(blank=True, default=django_kelove_cms.util.get_uuid_str, help_text='标识至少需要2个字符，且须以字母开头，以字母或数字结尾，只能包含小写字母数字和-', max_length=191, unique=True, validators=[django_kelove_cms.validators.NameValidator()], verbose_name='文档标识')),
                ('title', models.CharField(default='', max_length=191, unique=True, verbose_name='文档名称')),
                ('description', models.TextField(blank=True, default='', verbose_name='文档描述')),
                ('type', models.CharField(choices=[('doc', '文章'), ('page', '单页'), ('url', '外链'), ('wiki', '手册')], default='doc', max_length=191, verbose_name='文档类型')),
                ('url', models.URLField(blank=True, default='', help_text='文档类型为外链时必须', max_length=191, verbose_name='文档链接')),
                ('template', models.CharField(choices=[], default='', max_length=191, verbose_name='文档模板')),
                ('image', models.CharField(blank=True, default='', max_length=191, verbose_name='文档图片')),
                ('icon', models.CharField(blank=True, default='', max_length=191, verbose_name='文档图标')),
                ('content', models.TextField(blank=True, default='', verbose_name='文档内容')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('category', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.category', verbose_name='文档分类')),
                ('created_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_document_created_user_set', to=settings.AUTH_USER_MODEL, verbose_name='创建用户')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.document', verbose_name='上级文档')),
            ],
            options={
                'verbose_name': '文档',
                'verbose_name_plural': '文档管理',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.IntegerField(choices=[(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')], default=1, help_text='状态{"-1": "草稿", "0": "待审", "1": "通过", "2": "驳回"}', verbose_name='状态')),
                ('enabled', models.BooleanField(db_index=True, default=True, verbose_name='是否启用')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('name', models.CharField(blank=True, default=django_kelove_cms.util.get_uuid_str, help_text='标识至少需要2个字符，且须以字母开头，以字母或数字结尾，只能包含小写字母数字和-', max_length=191, unique=True, validators=[django_kelove_cms.validators.NameValidator()], verbose_name='标签标识')),
                ('title', models.CharField(max_length=191, unique=True, verbose_name='标签名称')),
                ('template', models.CharField(choices=[], default='', max_length=191, verbose_name='标签模板')),
                ('description', models.TextField(blank=True, default='', verbose_name='标签描述')),
                ('created_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_tag_created_user_set', to=settings.AUTH_USER_MODEL, verbose_name='创建用户')),
                ('updated_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_tag_updated_user_set', to=settings.AUTH_USER_MODEL, verbose_name='更新用户')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签管理',
            },
        ),
        migrations.CreateModel(
            name='NavGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.IntegerField(choices=[(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')], default=1, help_text='状态{"-1": "草稿", "0": "待审", "1": "通过", "2": "驳回"}', verbose_name='状态')),
                ('enabled', models.BooleanField(db_index=True, default=True, verbose_name='是否启用')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('title', models.CharField(default='', max_length=191, verbose_name='导航分组名称')),
                ('created_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_navgroup_created_user_set', to=settings.AUTH_USER_MODEL, verbose_name='创建用户')),
                ('updated_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_navgroup_updated_user_set', to=settings.AUTH_USER_MODEL, verbose_name='更新用户')),
            ],
            options={
                'verbose_name': '导航分组',
                'verbose_name_plural': '导航分组',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.IntegerField(choices=[(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')], default=1, help_text='状态{"-1": "草稿", "0": "待审", "1": "通过", "2": "驳回"}', verbose_name='状态')),
                ('enabled', models.BooleanField(db_index=True, default=True, verbose_name='是否启用')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('level', models.PositiveIntegerField(editable=False, verbose_name='级别')),
                ('title', models.CharField(default='', max_length=191, verbose_name='导航名称')),
                ('image', models.CharField(blank=True, default='', max_length=191, verbose_name='导航图片')),
                ('icon', models.CharField(blank=True, default='', max_length=191, verbose_name='导航图标')),
                ('url', models.URLField(blank=True, default='', max_length=191, verbose_name='导航链接')),
                ('description', models.TextField(blank=True, default='', verbose_name='导航描述')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('category', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.category', verbose_name='关联分类')),
                ('created_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_nav_created_user_set', to=settings.AUTH_USER_MODEL, verbose_name='创建用户')),
                ('document', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.document', verbose_name='关联文档')),
                ('nav_group', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.navgroup', verbose_name='导航分组')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.nav', verbose_name='上级导航')),
                ('tag', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_kelove_cms.tag', verbose_name='关联标签')),
                ('updated_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_nav_updated_user_set', to=settings.AUTH_USER_MODEL, verbose_name='更新用户')),
            ],
            options={
                'verbose_name': '导航',
                'verbose_name_plural': '导航管理',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='tag',
            field=models.ManyToManyField(blank=True, to='django_kelove_cms.Tag', verbose_name='文档标签'),
        ),
        migrations.AddField(
            model_name='document',
            name='updated_user',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='django_kelove_cms_document_updated_user_set', to=settings.AUTH_USER_MODEL, verbose_name='更新用户'),
        ),
    ]
