# ==================================================================
#       文 件 名: doc.py
#       概    要: MySQL数据库文档生成
#       作    者: IT小强 
#       创建时间: 8/4/20 9:20 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from ..base import doc


class Doc(doc.Doc):
    """
    MySQL数据库文档生成
    """

    COLUMNS_SQL = 'SHOW FULL COLUMNS FROM `{table_name}`'

    def get_db_fields_info(self, table_name, cur_fields):
        """
        获取数据库中的字段信息
        :param table_name:
        :param cur_fields:
        :return:
        """

        sql = self.COLUMNS_SQL.format(table_name=table_name)
        self.cursor.execute(sql)
        for filed_info in self.cursor.fetchall():
            filed_name = filed_info[0]
            # db_default_value = filed_info[5]
            # default_value = cur_fields[filed_name]['default']
            # comment = cur_fields[filed_name]['comment']

            cur_filed_info = {
                'field': filed_name,
                'type': filed_info[1],
                'collation': filed_info[2],
                'null': filed_info[3],
                'key': filed_info[4],
                # 'default': db_default_value if db_default_value else default_value,
                'extra': filed_info[6],
                'privileges': filed_info[7],
                # 'comment': comment if comment else filed_info[8]
            }
            cur_fields[filed_name].update(cur_filed_info)
        return cur_fields
