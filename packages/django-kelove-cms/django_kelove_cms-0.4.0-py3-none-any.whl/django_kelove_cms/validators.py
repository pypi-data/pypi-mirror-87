# ==================================================================
#       文 件 名: validators.py
#       概    要: 验证器
#       作    者: IT小强 
#       创建时间: 8/13/20 5:47 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class NameValidator(validators.RegexValidator):
    """
    标识验证器
    """

    regex = r'^[a-z]{1}[a-z0-9-_]*[a-z0-9]{1}$'
    message = _('标识至少需要2个字符，且须以字母开头，以字母或数字结尾，只能包含小写字母数字和-')
    flags = 0
