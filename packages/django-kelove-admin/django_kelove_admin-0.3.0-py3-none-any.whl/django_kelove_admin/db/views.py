# ==================================================================
#       文 件 名: views.py
#       概    要: 视图
#       作    者: IT小强 
#       创建时间: 8/4/20 9:36 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.shortcuts import render

from .backends.mysql.doc import Doc as MySQLDoc
from ..conf import settings


def mysql_doc(request):
    """
    MySQL数据库在线文档
    :param request:
    :return:
    """

    doc_title = settings.DATABASE_DOC_TITLE
    doc = MySQLDoc()
    doc_data = doc.get_database_doc_data()

    return render(request, 'kelove_admin/database_doc.html', {"apps": doc_data, 'title': doc_title})
