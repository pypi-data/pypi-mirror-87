# ==================================================================
#       文 件 名: schema.py
#       概    要: MySQL database backend for Django.
#       作    者: IT小强 
#       创建时间: 8/4/20 9:16 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from abc import ABC
from inspect import isfunction

from django.db.backends.mysql.schema import DatabaseSchemaEditor as MySqlDatabaseSchemaEditor

from django_kelove_admin.conf import settings


class DatabaseSchemaEditor(MySqlDatabaseSchemaEditor, ABC):

    def column_sql(self, model, field, include_default=False):
        """
        重写 字段sql生成方法
        :param model:
        :param field:
        :param include_default:
        :return:
        """

        # 字段默认值是否写入到sql语句中处理，可在settings.py中配置
        include_default_fun = self.connection.settings_dict.get(
            'INCLUDE_DEFAULT',
            settings.DATABASE_INCLUDE_DEFAULT
        )

        if isinstance(include_default_fun, bool):
            include_default = include_default_fun
        elif isfunction(include_default_fun):
            include_default = include_default_fun(model, field, include_default, self.connection)
        else:
            include_default = bool(include_default_fun)

        # 生成sql
        sql, params = super().column_sql(model, field, include_default)

        if not isinstance(sql, str):
            return sql, params

        # 写入字段注释
        comment = ''
        if field.help_text:
            comment = field.help_text
        elif field.verbose_name:
            comment = field.verbose_name
        sql += ' COMMENT "%s"' % comment.replace('"', r'\"')
        return sql, params

    def table_sql(self, model):
        """
        重写表sql生成方法
        :param model:
        :return:
        """
        sql, params = super().table_sql(model)
        if model._meta.verbose_name:
            sql += " COMMENT '%s'" % model._meta.verbose_name
        return sql, params
