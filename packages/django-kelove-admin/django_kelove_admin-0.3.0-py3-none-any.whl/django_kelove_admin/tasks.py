"""
tasks.py
依赖 celery
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-11-26 09:12
"""

from celery import shared_task

from django.core.cache import cache


@shared_task
def django_cache_clear():
    """
    清除全部缓存
    :return:
    """

    cache.clear()
