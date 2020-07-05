# 任务-：
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import json
import logging
import os
from urllib.parse import urlparse
from pymysql import connect as mysql_connect


class MetaMap(object):

    def __init__(self, system_id):

        self.system_id, self.links = system_id, set()

        connect_params = os.environ.get(
            'DATABASE_URI') or 'mysql+mysqlconnector://deployop:P@ssw0rd@100.69.216.42:3306/metadata'
        conn_info = urlparse(connect_params)
        db_name = conn_info.path.replace("/", '')
        connect_params = {"host": conn_info.hostname, "port": conn_info.port,
                          "user": conn_info.username, "password": conn_info.password, "database": db_name}
        self.conn = mysql_connect(**connect_params)
        self.cursor = self.conn.cursor()

        self.sql_list = ("SELECT DISTINCT tb_code FROM tbl_info_table WHERE system_id='{}';",
                         "SELECT DISTINCT tgt_obj_id FROM tbl_data_rel_t WHERE src_obj_id='{}';",
                         "SELECT DISTINCT system_id FROM tbl_info_table WHERE tb_code='{}';",
                         "SELECT system_id,system_name FROM tbl_info_system WHERE system_id IN({});")

    def son_recursion(self, src_obj_id, system_ids):
        """递归实现影响树 source => target"""

        self.cursor.execute(self.sql_list[1].format(src_obj_id))
        crs = self.cursor.fetchall()
        if not crs:
            return

        tgt_obj_ids = set(map(lambda x: x[0], crs))
        for s in tgt_obj_ids:
            self.cursor.execute(self.sql_list[2].format(s))
            info = self.cursor.fetchall()
            sys_ids = set(map(lambda x: x[0], info))
            a_link = {x for x in itertools.product(system_ids, sys_ids) if x[0] != x[1]}  # 笛卡尔积
            self.links.update(a_link)

            self.son_recursion(s, sys_ids)

    def map_tree(self):
        """
        对核心系统下的每个tb_code做影响分析 在让上下层的system_ids 做笛卡尔积
        :return:
        """
        try:

            try:
                self.cursor.execute(self.sql_list[0].format(self.system_id))
                tb_codes = self.cursor.fetchall()
            except Exception as e:
                logging.info(e)
                raise Exception('查询系统不存在')

            codes = set(map(lambda x: x[0], tb_codes))
            codes = filter(lambda x: x.isnumeric(), codes)

            for code in codes:
                sys_ids = {self.system_id}
                try:
                    self.son_recursion(code, sys_ids)
                except Exception as e:
                    logging.info(e)
                    raise Exception('递归出错了')

            # 组织格式
            get_ids = {i for l in self.links for i in l}
            system_ids = ','.join(list(map(str, get_ids)))
            self.cursor.execute(self.sql_list[3].format(system_ids))
            info = self.cursor.fetchall()
            nodes = list(map(lambda x: {'id': x[0], 'name': x[1]}, info))

            # 降维  {()()()}
            rest_ids = {node.get('id') for node in nodes}
            drop_ids = get_ids - rest_ids
            rest_links = set()
            for item in self.links:
                if set(item) & drop_ids:
                    continue
                else:
                    rest_links.add(item)

            links = [{"source": l[0], "target": l[1]} for l in rest_links]
            meta_map = {"nodes": nodes, "links": links}

            # 缓存到redis
            from app import redis_store
            try:
                redis_store.set("meta_map", json.dumps(meta_map))
            except Exception as e:
                logging.info(e)
                raise Exception('连接redis出错了')
        except Exception as e:
            logging.info(e)
            logging.info('更新元数据地图失败')

        self.conn.close()
        self.cursor.close()


def entrance(core_system=4):
    mm = MetaMap(core_system)
    mm.map_tree()
    logging.info('更新元数据地图成功')


if __name__ == '__main__':
    entrance()
