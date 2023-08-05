# ==================================================================
#       文 件 名: conf.py
#       概    要: 配置管理
#       作    者: IT小强 
#       创建时间: 8/4/20 8:37 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================


from django.conf import settings as django_settings

from . import util


class Settings:
    """
    This is a simple class to take the place of the global settings object.

    An instance will contain all of our settings as attributes, with default
    values if they are not specified by the configuration.

    """

    DEFAULT_FIELD_SETTINGS_CKFINDER = {
        'displayFoldersPanel': True,
        'skin': 'neko',
        'connectorPath': 'django_kelove_admin:ckfinder_api',
        'chooseFiles': True,
        'plugins': ['ClearCache'],
    }

    DEFAULT_FIELD_SETTINGS_EDITOR_MD = {
        'imageUpload': False,
        'imageUploadURL': '',
        'readOnly': False,
        'theme': '',
        'previewTheme': '',
        'editorTheme': 'default',
        'autoFocus': False,
        'toolbarAutoFixed': False,
        'emoji': True,
        'codeFold': True,
        'tocDropdown': True,
        'mode': 'markdown',
        'tocm': True,
    }

    DEFAULT_FIELD_SETTINGS_JSON = {
        "mode": "code",
        "modes": ["code", "form", "text", "tree", "view", "preview"],
    }

    defaults: dict = {
        # admin管理注册（权限）
        'REGISTER_PERMISSION_ADMIN': True,
        # admin管理注册（内容类型）
        'REGISTER_CONTENT_TYPE_ADMIN': True,
        # admin管理注册（日志）
        'REGISTER_LOG_ENTRY_ADMIN': True,
        # ckfinder 配置
        'CKFINDER_CONFIG': {},
        # OTP 登录验证模板
        'OTP_LOGIN_TEMPLATE': 'kelove_admin/otp_login.html',
        # OTP 不验证的 view
        'ALLOWED_VIEW_FUNC': [
            'django.views.static.serve',
            'django.contrib.staticfiles.views.serve'
        ],
        # 数据库文档标题
        'DATABASE_DOC_TITLE': '数据库在线文档',
        # 数据库迁移是否写入默认值
        'DATABASE_INCLUDE_DEFAULT': False,
        # 外键约束类型
        'DATABASE_FOREIGN_DELETE_TYPE': 'django.db.models.deletion.PROTECT',
        # 是否强制外键约束
        'DATABASE_CONSTRAINT': False,
        # 创建人，更新人是否强制外键约束
        'DATABASE_CONSTRAINT_USER': False,
        # 创建人，更新人是否可编辑
        'DATABASE_USER_EDITABLE': False,
        # 状态字段可选项
        'DATABASE_STATUS_CHOICES': [(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')],
        # json 字段配置
        'FIELD_SETTINGS_JSON': DEFAULT_FIELD_SETTINGS_JSON,
        # ckfinder 字段配置
        'FIELD_SETTINGS_CKFINDER': DEFAULT_FIELD_SETTINGS_CKFINDER,
        # Markdown编辑器 字段配置
        # 添加以下配置，化身代码编辑器
        # 'watch': False,
        # 'toolbar': False,
        # 'mode': 'python'
        # 可选语言：
        #  text/html
        #  javascript
        #  php
        #  text/xml
        #  text/json
        #  clike
        #  javascript
        #  perl
        #  go
        #  python
        #  clike
        #  css
        #  ruby
        #
        'FIELD_SETTINGS_EDITOR_MD': DEFAULT_FIELD_SETTINGS_EDITOR_MD
    }

    prefix: str = 'KELOVE_'

    def __getattr__(self, name: str):

        true_name = name

        if not true_name.startswith(self.prefix):
            true_name = '{prefix}{name}'.format(prefix=self.prefix, name=name)

        if name in self.defaults:
            setting = getattr(django_settings, true_name, self.defaults[name])
        else:
            setting = getattr(django_settings, name)

        if name == 'DATABASE_FOREIGN_DELETE_TYPE' and isinstance(setting, str):
            setting = util.load_object(setting)

        return setting


settings = Settings()
