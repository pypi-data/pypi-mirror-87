# ==================================================================
#       文 件 名: __init__.py
#       概    要: KELOVE 内容管理系统
#       作    者: IT小强 
#       创建时间: 8/12/20 2:33 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

PACKAGE_VERSION = '0.2.2'

VERSION = tuple(PACKAGE_VERSION.split("."))

default_app_config = "django_kelove_cms.apps.DjangoKeloveCmsConfig"

DOCUMENT_TEMPLATE = 'document_templates'

CATEGORY_TEMPLATE = 'category_templates'

TAG_TEMPLATE = 'tag_templates'

DOCUMENT_TYPE_CHOICE_DOC = 'doc'
DOCUMENT_TYPE_CHOICE_PAGE = 'page'
DOCUMENT_TYPE_CHOICE_URL = 'url'
DOCUMENT_TYPE_CHOICE_WIKI = 'wiki'

CMS_BASE_FILTER = {
    'enabled': True,
    'status': 1,
}
