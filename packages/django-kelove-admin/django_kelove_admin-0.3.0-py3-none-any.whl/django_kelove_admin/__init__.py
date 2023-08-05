# ==================================================================
#       文 件 名: __init__.py
#       概    要: DJANGO 后台管理 增强
#       作    者: IT小强 
#       创建时间: 8/4/20 8:36 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
import json

from django.contrib.auth import user_logged_in, user_login_failed

PACKAGE_VERSION = '0.3.0'

VERSION = tuple(PACKAGE_VERSION.split("."))

default_app_config = "django_kelove_admin.apps.DjangoKeloveAdminConfig"


class SettingsRegister:
    """
    配置注册
    """

    settings = []

    @classmethod
    def set(cls, settings_cls):
        if not isinstance(settings_cls, str):
            raise ValueError('settings_cls type must be a string')
        cls.settings.append(settings_cls)

    @classmethod
    def get(cls):
        return cls.settings


def _user_logged_in_log(sender, request, user, **kwargs):
    """
   记录登录成功日志
   """
    from .models import LoginLog, LOGIN_SUCCESS
    LoginLog.objects.log_action(
        request=request,
        user=user,
        action=LOGIN_SUCCESS,
        content=''
    )


def _user_logged_failed_log(sender, credentials, request, **kwargs):
    """
    记录登录失败日志
    """
    from .models import LoginLog, LOGIN_FAILED
    LoginLog.objects.log_action(
        request=request,
        action=LOGIN_FAILED,
        content=json.dumps(credentials)
    )


user_logged_in.connect(_user_logged_in_log)
user_login_failed.connect(_user_logged_failed_log)
