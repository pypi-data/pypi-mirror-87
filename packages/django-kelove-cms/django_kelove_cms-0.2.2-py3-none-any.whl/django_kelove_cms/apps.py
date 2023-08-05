# ==================================================================
#       文 件 名: apps.py
#       概    要: DjangoKeloveCmsConfig
#       作    者: IT小强 
#       创建时间: 8/12/20 2:34 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================


from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from django_kelove_admin import SettingsRegister


class DjangoKeloveCmsConfig(AppConfig):
    """
    DjangoKeloveCmsConfig
    """

    label = 'django_kelove_cms'
    name = 'django_kelove_cms'
    verbose_name = _('Kelove 内容管理')


SettingsRegister.set('{app_name}.settings.GlobalSettingsForm'.format(app_name=DjangoKeloveCmsConfig.name))
