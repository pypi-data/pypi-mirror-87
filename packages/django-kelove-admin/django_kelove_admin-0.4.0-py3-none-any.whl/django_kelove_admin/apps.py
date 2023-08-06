# ==================================================================
#       文 件 名: apps.py
#       概    要: DjangoKeloveAdminConfig
#       作    者: IT小强 
#       创建时间: 8/4/20 9:05 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from . import SettingsRegister


class DjangoKeloveAdminConfig(AppConfig):
    """
    DjangoKeloveAdminConfig
    """

    label = 'django_kelove_admin'
    name = 'django_kelove_admin'
    verbose_name = _('kelove admin')


SettingsRegister.set('{app_name}.settings.GlobalSettingsForm'.format(app_name=DjangoKeloveAdminConfig.name))
SettingsRegister.set('{app_name}.settings.EmailSettingsForm'.format(app_name=DjangoKeloveAdminConfig.name))
