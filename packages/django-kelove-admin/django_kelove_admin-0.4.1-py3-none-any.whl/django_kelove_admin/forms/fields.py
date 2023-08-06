# ==================================================================
#       文 件 名: fields.py
#       概    要: 表单字段
#       作    者: IT小强 
#       创建时间: 8/4/20 10:09 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.forms import fields

from .widgets import JSONWidget, CkFinderWidget, EditorMdWidget


class JSONField(fields.JSONField):
    """
    JSON 表单字段
    """

    def __init__(self, *, field_settings=None, **kwargs):
        self.field_settings = field_settings
        kwargs['widget'] = JSONWidget(attrs={'field_settings': field_settings})
        super().__init__(**kwargs)


class CkFinderField(fields.CharField):
    """
    CkFinder 文件选择器表单字段
    """

    def __init__(self, *, field_settings=None, **kwargs):
        self.field_settings = field_settings
        kwargs['widget'] = CkFinderWidget(attrs={'field_settings': field_settings})
        super().__init__(**kwargs)


class EditorMdField(fields.CharField):
    """
    Markdown 编辑器 表单字段
    """

    def __init__(self, *, field_settings=None, **kwargs):
        self.field_settings = field_settings
        kwargs['widget'] = EditorMdWidget(attrs={'field_settings': field_settings})
        super().__init__(**kwargs)
