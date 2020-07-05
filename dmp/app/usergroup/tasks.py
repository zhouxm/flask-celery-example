# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app.meta.utiles.inspect_fill_rate_task import inspect_fill_rate
from app.meta.utiles.inspect_same_task import inspect_same
from app.meta.utiles.meta_map_task import entrance
from app import make_celery, create_app



cele = make_celery(create_app('development'))


@cele.task(name='group_upload')
def group_upload():
    """
    更新元数据地图
    调用时间:元数据采集完、系统上下线后、删除系统
    """
    core_system = os.environ.get('CORE_SYSTEM') or 4
    entrance(core_system)


@cele.task(name='group_create')
def group_create(system_name):
    """
    更新一致性检核
    调用时间:点击执行
    :param system_name:
    :return:
    """
    inspect_same(system_name)


@cele.task(name='update_fill_rate')
def update_fill_rate(system_name):
    """
    更新填充率检核
    调用时间:点击执行
    :param system_name:
    :return:
    """
    inspect_fill_rate(system_name)


if __name__ == '__main__':
    print(__name__)
