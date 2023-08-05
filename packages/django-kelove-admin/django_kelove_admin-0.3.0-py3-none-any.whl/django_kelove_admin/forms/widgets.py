# ==================================================================
#       文 件 名: widgets.py
#       概    要: 表单组件
#       作    者: IT小强 
#       创建时间: 8/4/20 10:09 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import json
from inspect import isfunction

from django.forms import Widget, Media
from django.urls import reverse, NoReverseMatch

from ..conf import settings


class BaseWidget(Widget):
    """
    表单组件基类
    """

    field_settings_key = 'BASE'

    field_settings = {}

    def __init__(self, attrs=None):
        attrs = attrs if isinstance(attrs, dict) else {}
        field_settings = self.get_field_settings(attrs.get('field_settings', {}))
        attrs['field_settings'] = json.dumps(field_settings)
        super().__init__(attrs)

    @classmethod
    def get_field_settings(cls, field_settings=None) -> dict:
        """
        配置信息统一获取
        :param field_settings:
        :return:
        """

        return {
            **cls.field_settings,
            **cls.get_field_settings_default(),
            **cls.get_field_settings_custom(field_settings=field_settings)
        }

    @classmethod
    def get_field_settings_default(cls):
        """
        获取默认配置
        :return:
        """

        field_settings = getattr(settings, 'FIELD_SETTINGS_' + cls.field_settings_key, {})
        if not isinstance(field_settings, dict):
            field_settings = {}
        return field_settings

    @classmethod
    def get_field_settings_custom(cls, field_settings=None):
        """
        获取自定义配置
        :return:
        """

        if isfunction(field_settings):
            field_settings = field_settings()

        if not isinstance(field_settings, dict):
            field_settings = {}

        return field_settings


class JSONWidget(BaseWidget):
    """
    JSON 表单组件
    https://github.com/josdejong/jsoneditor
    """

    field_settings_key = 'JSON'

    template_name = 'kelove_admin/forms/json.html'

    def format_value(self, value):
        if value == '' or value is None:
            return None
        if not isinstance(value, str):
            value = json.dumps(value)
        return value

    def _get_media(self):
        return Media(
            css={
                "all": (
                    'kelove_admin/jsoneditor/jsoneditor.min.css',
                    'kelove_admin/jsoneditor/style.css',
                )
            },
            js=(
                'kelove_admin/jsoneditor/jsoneditor.min.js',
                'kelove_admin/jsoneditor/script.js',
            )
        )

    media = property(_get_media)


class CkFinderWidget(BaseWidget):
    """
    CkFinder 文件选择器 表单组件
    """

    field_settings_key = 'CKFINDER'

    template_name = 'kelove_admin/forms/ckfinder.html'

    IMAGE_EXT = ['png', 'jpg', 'gif', 'ico', 'jpeg', 'svg', 'bmp']

    @classmethod
    def get_field_settings(cls, field_settings=None) -> dict:
        """
        重构，添加上传路经处理
        :param field_settings:
        :return:
        """

        field_settings = {
            **cls.field_settings,
            **cls.get_field_settings_default(),
            **cls.get_field_settings_admin(),
            **cls.get_field_settings_custom(field_settings=field_settings)
        }

        connector_path = field_settings['connectorPath']
        try:
            connector_path = reverse(connector_path)
        except NoReverseMatch:
            pass

        field_settings['connectorPath'] = connector_path

        if 'license_key' in field_settings.keys():
            field_settings.pop('license_key')

        if 'license_name' in field_settings.keys():
            field_settings.pop('license_name')

        return field_settings

    @classmethod
    def get_field_settings_admin(cls):
        """
        获取后台配置
        :return:
        """

        from ..settings import GlobalSettingsForm

        global_settings = GlobalSettingsForm.get()
        field_settings = global_settings.get('ckfinder_selector_settings', {})
        if not isinstance(field_settings, dict):
            field_settings = {}

        return field_settings

    def _get_media(self):
        return Media(
            css={
                "all": (
                    'kelove_admin/ckfinder/style.css',
                )
            },
            js=(
                'kelove_admin/ckfinder/ckfinder.js',
                'kelove_admin/ckfinder/script.js',
            )
        )

    media = property(_get_media)


class EditorMdWidget(BaseWidget):
    """
    EditorMd 表单组件
    https://github.com/pandao/editor.md
    """

    field_settings_key = 'EDITOR_MD'

    template_name = 'kelove_admin/forms/editor_md.html'

    @classmethod
    def get_field_settings(cls, field_settings=None) -> dict:
        """
        重构，添加上传路经处理
        :param field_settings:
        :return:
        """

        field_settings = {
            **cls.field_settings,
            **cls.get_field_settings_default(),
            **cls.get_field_settings_admin(),
            **cls.get_field_settings_custom(field_settings=field_settings)
        }

        if not field_settings['imageUpload']:
            return field_settings

        if isinstance(field_settings['imageUploadURL'], dict):
            field_settings['imageUploadURL'] = CkFinderWidget.get_field_settings(field_settings['imageUploadURL'])
        else:
            image_upload_url = str(field_settings['imageUploadURL'])
            try:
                image_upload_url = reverse(image_upload_url)
            except NoReverseMatch:
                pass
            field_settings['imageUploadURL'] = image_upload_url

        return field_settings

    @classmethod
    def get_field_settings_admin(cls):
        """
        获取后台配置
        :return:
        """

        from ..settings import GlobalSettingsForm

        global_settings = GlobalSettingsForm.get()
        field_settings = global_settings.get('markdown_editor_settings', {})
        if not isinstance(field_settings, dict):
            field_settings = {}

        return field_settings

    def _get_media(self):
        return Media(
            css={
                "all": (
                    'kelove_admin/editor_md/css/editormd.min.css',
                    'kelove_admin/editor_md/style.css',
                )
            },
            js=(
                'kelove_admin/jquery/jquery-3.5.1.min.js',
                'kelove_admin/editor_md/editormd.min.js',
                'kelove_admin/ckfinder/ckfinder.js',
                'kelove_admin/editor_md/script.js',
            )
        )

    media = property(_get_media)
