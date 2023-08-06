# ==================================================================
#       文 件 名: doc.py
#       概    要: 数据库文档生成基类
#       作    者: IT小强 
#       创建时间: 8/4/20 9:19 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.db import connection
from django.apps import apps


class Doc:
    """
    数据库文档生成基类
    """

    def __init__(self):
        self.cursor = connection.cursor()

    def get_db_fields_info(self, table_name, cur_fields):
        """
        获取数据库中的字段信息
        :param table_name:
        :param cur_fields:
        :return:
        """
        pass

    def get_fields(self, table_name, fields):
        """
        获取数据表全部字段信息
        :param fields:
        :param table_name:
        :return:
        """
        cur_fields = {}

        # 获取模型信息
        for item in fields:
            cur_fields[item.column] = {
                # 字段注释
                'comment': item.help_text if item.help_text else item.verbose_name,
                # 字段默认值
                'default': item.get_default(),
                # 获取关联表
                'relation_table_name': item.related_model._meta.db_table if item.is_relation else ''
            }

        # 获取数据库查询信息并合并
        return self.get_db_fields_info(table_name, cur_fields)

    def get_tables(self, app):
        """
        获取指定模块下的全部模型
        :param app:
        :return:
        """
        data = {}
        for model in apps.get_app_config(app).get_models():
            table_name = model._meta.db_table  # 表名

            cur_table_info = {
                'name': table_name,
                'title': model._meta.verbose_name,
                'fields': self.get_fields(table_name, model._meta.fields)
            }
            if cur_table_info['fields']:
                data[cur_table_info['name']] = cur_table_info
        return data

    def get_database_doc_data(self, apps_list=None):
        """
        获取应用数据库文档数据
        :param apps_list:
        :return:
        """
        data = {}

        if apps_list is None:
            apps_list = [item for item in apps.all_models.keys()]

        for app in apps_list:
            cur_app_info = {
                'name': app,
                'title': apps.get_app_config(app).verbose_name,
                'tables': self.get_tables(app)
            }
            if cur_app_info['tables']:
                data[app] = cur_app_info
        return data
