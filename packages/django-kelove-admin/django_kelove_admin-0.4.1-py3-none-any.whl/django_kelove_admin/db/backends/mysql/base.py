# ==================================================================
#       文 件 名: base.py
#       概    要: MySQL database backend for Django.
#       作    者: IT小强 
#       创建时间: 8/4/20 9:16 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.db.backends.mysql.base import *

from .schema import DatabaseSchemaEditor as MySqlDatabaseSchemaEditor


class DatabaseWrapper(DatabaseWrapper):
    SchemaEditorClass = MySqlDatabaseSchemaEditor
