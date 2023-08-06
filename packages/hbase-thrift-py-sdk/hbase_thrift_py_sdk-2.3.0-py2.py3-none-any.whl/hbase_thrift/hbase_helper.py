# -*- coding: utf-8 -*-
# @Time    : 2020/7/28 14:02
# @Author  :
"""
https://blog.csdn.net/Cocktail_py/article/details/102730839
No protocol version header
./hbase-daemon.sh start thrift

"""
from . import ConnectionPool

# DEFAULT_TRANSPORT = 'buffered'
# DEFAULT_COMPAT = '0.98'
# DEFAULT_PROTOCOL = 'binary'
DEFAULT_TRANSPORT = 'framed'
DEFAULT_COMPAT = '0.98'
DEFAULT_PROTOCOL = 'compact'


class HBaseHelper(object):

    def __init__(self, host, table_prefix=None, compat=DEFAULT_COMPAT,
                 transport=DEFAULT_TRANSPORT, protocol=DEFAULT_PROTOCOL):
        """
                host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=None,
                         autoconnect=True, table_prefix=None,
                         table_prefix_separator=b'_', compat=DEFAULT_COMPAT,
                         transport=DEFAULT_TRANSPORT, protocol=DEFAULT_PROTOCOL
                :return:
                """
        self.host = host
        self.compat = compat
        self.table_prefix = table_prefix
        self.transport = transport
        self.protocol = protocol
        self.conn = self.connect()

    def connect(self):

        conn = ConnectionPool(host=self.host, timeout=None,
                              autoconnect=True, compat=DEFAULT_COMPAT,
                              transport=DEFAULT_TRANSPORT, protocol=DEFAULT_PROTOCOL)
        return conn

    def table_name(self, index, prefix):
        table = '{namespace}:{columnFamily}'.format(namespace=prefix,
                                                    columnFamily=index.replace("%s_" % prefix, ""))
        return table

    def query_single_line(self, index, prefix, row_key, columns=None):
        """
        返回单行数据，返回tuple
        :param index:索引名
        :param row_key: 相应的id
        :param prefix:前缀:dw,dm,ods
        :param columns:
        :return:
        """
        table = self.table_name(index, prefix)
        with self.connect().connection() as connection:
            hb_dict = dict(connection.table(table).row(row_key, columns=columns))
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in hb_dict.items()}

    def single_put(self, row_key_name, index, prefix, column, data):
        """
        插入单条数据
        :param index: 索引名
        :param prefix: 前缀
        :param dict data: the data to store
        :return:
        """
        table = self.table_name(index, prefix)
        with self.connect().connection() as connection:
            da_nw = {'{column}:{k}'.format(column=column, k=k): v for k, v in data.items()}
            row_key = da_nw.pop('{column}:{k}'.format(column=column, k=row_key_name))
            connection.table(table).put(row_key,
                                        data=da_nw)

    def single_delete(self, index, prefix, row_key):
        """
        删除单行数据
        :param table:
        :param row_key:
        :return:
        """
        table = self.table_name(index, prefix)
        with self.connect().connection() as connection:
            connection.table(table).delete(row_key)


    def batch_put(self, row_key_name, index, column, datas, prefix="", batch_size=2000):
        """
        批量插入数据
        :param index: 索引名
        :param row_key_name: rk名字
        :param column: 列名
        :param datas: 数据集 [{k1:v1,k2:v2}]
        :param prefix: 前缀:dw,dm,ods
        :param batch_size: 每次批量插入多少条
        :return:
        """
        table = self.table_name(index, prefix)
        with self.connect().connection() as connection:
            datas_new = [datas[i:i + batch_size] for i in range(0, len(datas), batch_size)]
            for x in datas_new:
                with connection.table(table).batch(batch_size=batch_size) as batch:
                    for da in x:
                        da_nw = {'{column}:{k}'.format(column=column, k=k): v for k, v in da.items()}
                        row_key = da_nw.pop('{column}:{k}'.format(column=column, k=row_key_name))
                        batch.put(row_key, da_nw)

    def query_multi_lines(self, row_keys, index=None, prefix="", columns=None):
        """
        返回多行数据，返回dict
        :param index: 索引名
        :param prefix: 前缀:dw,dm,ods
        :param row_keys: 对应的rk列表 ["rk1","rk2","rk3"]
        :param columns: 需要获取的列名
        :param list row_keys: list of row keys
        :return:
        """

        table = self.table_name(index, prefix)
        with self.connect().connection() as connection:
            hb_dict = dict(connection.table(table).rows(row_keys, columns=columns))
        return {k1.decode('utf-8'): {k2.decode('utf-8'): v2.decode('utf-8') for k2, v2 in v1.items()} for k1, v1 in
                hb_dict.items()}

    def batch_delete(self, row_keys, index=None, prefix=""):
        """
        批量删除数据
        :param row_keys:
        :param index:
        :param prefix:前缀:dw,dm,ods
        :return:
        """
        table = self.table_name(index, prefix)
        with self.connect().connection() as connection:
            with connection.table(table).batch() as bat:
                for rk in row_keys:
                    bat.delete(rk)

    def scan_table(self, row_start, row_stop, row_prefix, index=None, prefix="",
                   filter_f=None, limit=None):
        """
        扫描一张表
        :param index: 索引名
        :param prefix:前缀:dw,dm,ods
        :param row_start: 开始rk
        :param row_stop: 结束rk
        :param row_prefix: rk的前缀
        :param filter_f: 过滤器:"SingleColumnValueFilter ('info', 'media', =, 'binary:6')",例如,info列族下的media=2的数据
        # "ColumnPrefixFilter('your_prsifx_str') AND TimestampsFilter(your_timestamp)"
        :param limit: 条数
        :return:
        """
        table = self.table_name(index, prefix)
        with self.connect().connection() as connection:
            scan = connection.table(table).scan(row_start=row_start, row_stop=row_stop, row_prefix=row_prefix,
                                                filter=filter_f, limit=limit)
            hb_dict = dict(scan)

        return {k1.decode('utf-8'): {k2.decode('utf-8'): v2.decode('utf-8') for k2, v2 in v1.items()} for k1, v1 in
                hb_dict.items()}

