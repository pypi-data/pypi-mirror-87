# ==================================================================
#       文 件 名: util.py
#       概    要: 助手工具
#       作    者: IT小强 
#       创建时间: 8/4/20 10:42 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import json
from importlib import import_module

from django.utils.translation import gettext_lazy as _


def json_value_to_python(value):
    """
    格式化json数据
    :param value:
    :return:
    """

    if isinstance(value, dict) or isinstance(value, list):
        return value

    if isinstance(value, tuple) or isinstance(value, set):
        return list(value)

    if isinstance(value, str):
        return json.loads(value)

    raise ValueError(_('“%s“不是有效的json值') % str(value))


def load_object(path: str):
    """
    Load an object given its absolute object path, and return it.
    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    dot = path.rindex('.')
    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)
    return getattr(mod, name)
