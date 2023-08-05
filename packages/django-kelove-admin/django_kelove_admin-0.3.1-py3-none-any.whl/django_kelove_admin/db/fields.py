# ==================================================================
#       文 件 名: fields.py
#       概    要: 模型字段
#       作    者: IT小强 
#       创建时间: 8/4/20 10:31 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..forms import fields


class JSONField(models.JSONField):
    """
    JSON 编辑器字段
    """

    def __init__(self, field_settings=None, default=dict, **kwargs):
        self.field_settings = field_settings
        super().__init__(default=default, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = fields.JSONField
        kwargs['field_settings'] = self.field_settings
        return super().formfield(**kwargs)


class CkFinderField(models.CharField):
    """
    CkFinder 文件选择器字段
    """

    description = _("CkFinder 文件选择器字段")

    def __init__(self, field_settings=None, **kwargs):
        self.field_settings = field_settings
        super().__init__(**kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = fields.CkFinderField
        kwargs['field_settings'] = self.field_settings
        return super().formfield(**kwargs)


class EditorMdField(models.TextField):
    """
    Markdown 编辑器字段
    """

    description = _("Markdown 编辑器字段")

    def __init__(self, field_settings=None, **kwargs):
        self.field_settings = field_settings
        super().__init__(**kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = fields.EditorMdField
        kwargs['field_settings'] = self.field_settings
        return super().formfield(**kwargs)
