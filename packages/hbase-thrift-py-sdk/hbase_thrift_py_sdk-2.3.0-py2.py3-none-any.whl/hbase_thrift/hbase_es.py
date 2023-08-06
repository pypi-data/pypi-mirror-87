# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 16:30
# @Author  :

from elasticsearch import Elasticsearch, helpers, ConnectionPool, exceptions
from .hbase_helper import HBaseHelper
from .elasticsearch_helper import bulk_insearch_es

COLUMN = "info"


class HBaseEs(object):
    def __init__(self, hbase_host, es_host_list=[], user_tuple=()):
        self.hbase_host = hbase_host
        self.es_host_list = es_host_list
        self.user_tuple = user_tuple
        self.__conneteshbase()

    def __conneteshbase(self):
        self.es = Elasticsearch(self.es_host_list,
                                http_auth=self.user_tuple, timeout=180, max_retries=20,
                                retry_on_timeout=True, connection_pool_class=ConnectionPool)
        self.hbase = HBaseHelper(host=self.hbase_host)

    def __es_bulk(self, _op_type, index, data_list, name):
        """
        es批量操作方法
        :param _op_type: 操作类型
        :param index: 相应索引
        :param data_list: 相应数据
        :return:
        """
        bulk_list = [
            {
                '_op_type': _op_type,
                '_index': index,
                '_id': da.get("id"),
                "_retry_on_conflict": 5,
                "{}".format(name): da
            } for da in data_list

        ]
        return bulk_list

    def get(self, index, body, columns=[], prefix="", is_scroll=0, not_scroll_first=0, scroll="500m", sid="",
            size=100, only_es=0):
        """

        :param index:索引
        :param body: es dsl语法
        :param columns: 需要获取的字段如 ["c_url","kw"]
         :param prefix:前缀:dw,dm,ods
        :param is_scroll:是否支持滚动搜索 1支持 0不支持
        :param not_scroll_first: 不是第一次滚动 1不是第一次滚动 0是第一次滚动
        :param scroll: 滚动深度(默认200m)
        :param sid: 滚动游标
        :param size:滚动查询需要返回的条数
        :return:
        """
        scroll_size = 0
        body["_source"] = False
        if only_es == 1:
            body["_source"] = columns
        body["track_total_hits"] = True
        if is_scroll != 1:
            result = self.es.search(index=index, body=body)
        else:

            if not_scroll_first != 1:
                result = self.es.search(
                    index=index,
                    scroll=scroll,
                    size=size,
                    # es中的查询语法
                    body=body
                )
                sid = result['_scroll_id']
            else:
                result = self.es.scroll(scroll_id=sid, scroll=scroll)
            scroll_size = len(result['hits']['hits'])
        hits = result.get('hits')
        aggregations = result.get('aggregations', 0)
        total = hits.get("total")
        datas = hits.get('hits')
        sort = []
        if datas:
            sort = datas[-1].get("sort")
            rk_list = [da.get('_id') for da in datas]
        else:
            try:
                self.es.clear_scroll(
                    scroll_id=sid)
            except:
                pass
            sid = ""
            rk_list = []
        if only_es == 1:
            return {
                "data": {"total": total, "list": datas, "aggregations": aggregations, "sid": sid,
                         "scroll_size": scroll_size, "sort": sort}, 'msg': 'successful',
                'status': 200}
        if columns:
            columns = ["{column}:{k}".format(column=COLUMN, k=k) for k in columns]
        hbase_dict = self.hbase.query_multi_lines(row_keys=rk_list, index=index, prefix=prefix,
                                                  columns=columns)
        nw_list = []
        for k, v in hbase_dict.items():
            k_dict = {"id": k}
            data_dict = {k1.replace("%s:" % COLUMN, ""): v1 for k1, v1 in v.items()}
            data_dict.update(k_dict)
            nw_list.append(data_dict)
        return {
            "data": {"total": total, "list": nw_list, "aggregations": aggregations, "sid": sid,
                     "scroll_size": scroll_size, "sort": sort}, 'msg': 'successful',
            'status': 200}

    def add(self, index, prefix="", p_key_name="id", data_list=[], is_cover=1, only_es=0):
        """
        批量添加数据
         :param index:索引
         :param prefix:前缀:dw,dm,ods
        :param p_key_name:
        :param data_list:
        :param is_cover:是否覆盖默认为1表示覆盖 0表示不覆盖
        :return:
        """
        if only_es == 1:
            pass
        else:
            if is_cover == 0:
                rk_list = [da.get("id") for da in data_list]
                hbase_dict = self.hbase.query_multi_lines(row_keys=rk_list, index=index, prefix=prefix,
                                                          columns=[])
                data_list = [da for da in data_list if da.get("id") not in hbase_dict]
                data_hbase_list = [{k: str(v) for k, v in da.items()} for da in data_list]
            else:
                data_hbase_list = [{k: str(v) for k, v in da.items()} for da in data_list]

            self.hbase.batch_put(row_key_name=p_key_name, index=index, column=COLUMN, datas=data_hbase_list,
                                 prefix=prefix,
                                 batch_size=250)
        bulk_insearch_es(self.es, p_key_name, datas=data_list, index=index)
        return {'msg': 'successful', 'status': 200}

    def single_add(self, index, prefix, p_key_name="id", data_dict={}, only_es=1):
        """
        写入单条数据
        :param index: 索引名
        :param prefix: 前缀
        :param data_dict: 相应的单条数据 {"k1":"v1","k2":"v2"...}
        :param only_es: 是否只使用es
        :return:
        """
        id_ = data_dict.get("id", "")
        if not id_:
            raise Exception("id not found")
        id_ = str(id_)
        if not isinstance(data_dict, dict):
            raise Exception("data_dict must dict type")
        if only_es == 1:
            result = self.es.index(index, data_dict, id=id_)

        else:
            result = self.hbase.single_put(p_key_name, index, prefix, column=COLUMN,
                                           data={k: str(v) for k, v in data_dict.items()})
        return {'msg': 'successful', 'status': 200, "result": result}

    def update(self, index, prefix="", p_key_name="id", data_list=[], is_cover=0, only_es=0,
               exist_update_not_exist_index=0):
        """
        :param index:索引
         :param prefix:前缀:dw,dm,ods
        :param is_cover: 是否覆盖
        :param only_es: 是否只对es更新操作 only_es=1只对es进行更新操作
        :param exist_update_not_exist_index: 是否存在更新不存在插入 exist_update_not_exist_index=1 存在更新不存在插入
        :param p_key_name:
        :param data_list:
        :return:
        """
        exist_list = []
        not_exist_list = []
        _op_type = 'update'
        name = "doc"
        if is_cover == 1:
            _op_type = 'index'
            if only_es == 1:
                pass
            else:
                row_keys = [p.get(p_key_name) for p in data_list]
                self.hbase.batch_delete(row_keys, index=index)
        else:
            if exist_update_not_exist_index == 1:
                rk_list = [da.get("id") for da in data_list]
                # # 是否存在列表
                data_list_exit_list = []
                data_list_not_exit_list = []
                bulk_list = []
                result = self.es.mget(body={"ids": rk_list}, index=index)
                es_ids = [da.get("_id") for da in result.get("docs") if da.get('found')]
                for da in data_list:
                    id_ = da.get("id")
                    if id_ not in es_ids:
                        data_list_not_exit_list.append(da)
                        not_exist_list.append(id_)
                    else:
                        data_list_exit_list.append(da)
                        exist_list.append(id_)
                if only_es == 1:
                    pass
                else:
                    data_hbase_list = [{k: str(v) for k, v in da.items()} for da in data_list]
                    self.hbase.batch_put(row_key_name=p_key_name, index=index, column=COLUMN, datas=data_hbase_list,
                                         prefix=prefix,
                                         batch_size=250)
                bulk_list.extend(self.__es_bulk('index', index, data_list_not_exit_list, name="_source"))
                bulk_list.extend(self.__es_bulk('update', index, data_list_exit_list, name="doc"))
                helpers.bulk(self.es, bulk_list)

                return {
                    'msg': 'update successful', 'status': 200,
                    "update": {"exist": exist_list, "not_exist": not_exist_list}}
        if only_es == 1:
            pass
        else:
            data_hbase_list = [{k: str(v) for k, v in da.items()} for da in data_list]
            self.hbase.batch_put(row_key_name=p_key_name, index=index, column=COLUMN, datas=data_hbase_list,
                                 prefix=prefix,
                                 batch_size=250)
        if _op_type == 'update':
            name = "doc"
        if _op_type == 'index':
            name = "_source"
        bulk_list = self.__es_bulk(_op_type, index, data_list, name)
        helpers.bulk(self.es, bulk_list)

        return {
            'msg': 'update successful', 'status': 200, "update": {"exist": exist_list, "not_exist": not_exist_list}}

    def single_update(self, index, prefix="", p_key_name="id", data_dict={}, is_cover=0, only_es=0,
                      exist_update_not_exist_index=0):
        """
        单条数据更新
        :param index: 索引名
        :param prefix: 前缀名
        :param p_key_name: 主键名
        :param data_dict: 相应数据 字典形式
        :param is_cover: 是否整条数据覆盖
        :param only_es: 是否只对es进行操作
        :param exist_update_not_exist_index: 是否存在更新不存在插入 exist_update_not_exist_index=1 存在更新不存在插入
        :return:
        """
        exist_list = []
        not_exist_list = []
        id_ = data_dict.get(p_key_name, "")
        if not id_:
            raise Exception("id not found")
        id_ = str(id_)
        body = {
            "doc": data_dict
        }
        if is_cover == 1:
            if only_es == 1:
                pass
            else:
                self.hbase.single_delete(index, prefix, id_)
                self.hbase.single_put(p_key_name, index, prefix, column=COLUMN,
                                      data={k: str(v) for k, v in data_dict.items()})
            result = self.es.index(index=index, body=data_dict, id=id_)
        else:
            if exist_update_not_exist_index == 1:
                if only_es == 1:
                    pass
                else:
                    self.hbase.single_put(p_key_name, index, prefix, column=COLUMN,
                                          data={k: str(v) for k, v in data_dict.items()})
                try:
                    self.es.get(index=index, id=id_)
                    result = self.es.update(index=index, id=id_, body=body)
                    exist_list.append(id_)
                except exceptions.NotFoundError:
                    result = self.es.index(index=index, body=data_dict, id=id_)
                    not_exist_list.append(id_)

            # 从hbase中获取数据
            else:
                if only_es == 1:
                    pass
                else:
                    self.hbase.single_put(p_key_name, index, prefix, column=COLUMN,
                                          data={k: str(v) for k, v in data_dict.items()})
                result = self.es.update(index=index, id=id_, body=body)
        return {'msg': 'single update successful', 'status': 200, "result": result,
                "update": {"exist": exist_list, "not_exist": not_exist_list}}

    def delete(self, index, prefix="", p_key_name="id", data_list=[], only_es=0):
        """
        批量删除方法
        :param index:索引
        :param prefix:前缀:dw,dm,ods
        :param p_key_name:
        :param data_list:
        :return:
        """
        _op_type = 'delete'
        if only_es == 1:
            pass
        else:
            row_keys = [p.get(p_key_name) for p in data_list]
            self.hbase.batch_delete(row_keys, index=index, prefix=prefix)
        bulk_list = [
            {
                '_op_type': _op_type,
                '_index': index,
                '_id': da.get("id"),
            } for da in data_list

        ]
        helpers.bulk(self.es, bulk_list)

        return {
            'msg': 'delete successful', 'status': 200}

    def hbase_batch_put(self, index, prefix="", data_list=[], batch_size=250, p_key_name="id"):
        """
                批量插入hbase数据
                :param index: 索引名
                :param row_key_name: rk名字
                :param data_list: 数据集 [{k1:v1,k2:v2}]
                :param prefix: 前缀:dw,dm,ods
                :param batch_size: 每次批量插入多少条
                :return:
                """
        data_hbase_list = [{k: str(v) for k, v in da.items()} for da in data_list]
        self.hbase.batch_put(p_key_name, index, COLUMN, data_hbase_list, prefix=prefix, batch_size=batch_size)
        return {
            'msg': 'hbase batch put successful', 'status': 200}

    def hbase_query_single_line(self, index, prefix, id_, columns=None, p_key_name="id"):
        """
                返回hbase单行数据
                :param index:索引名
                :param prefix: 前缀:dw,dm,ods
                :param id_: 对应的数据id
                :param columns:
                :return:
                """
        hbase_d = self.hbase.query_single_line(index, prefix, row_key=str(id_), columns=columns)
        hbase_dict = {}
        hbase_dict[p_key_name] = id_
        hbase_dict.update({k1.replace("%s:" % COLUMN, ""): v1 for k1, v1 in hbase_d.items()})
        return hbase_dict

    def hbase_query_multi_lines(self, index=None, prefix="", data_list=[], columns=None, p_key_name="id"):
        """
               返回hbase多行数据，返回dict
               :param index: 索引名
               :param prefix: 前缀:dw,dm,ods
               :param data_list: 对应的rk列表 ["rk1","rk2","rk3"]
               :param columns: 需要获取的列名
               :param p_key_name: id名
               :return:
               """

        rk_list = [str(da.get(p_key_name)) for da in data_list]
        if columns:
            columns = ["{column}:{k}".format(column=COLUMN, k=k) for k in columns]
        hbase_dict = self.hbase.query_multi_lines(rk_list, index=index, prefix=prefix, columns=columns)
        nw_list = []
        for k, v in hbase_dict.items():
            k_dict = {p_key_name: k}
            data_dict = {k1.replace("%s:" % COLUMN, ""): v1 for k1, v1 in v.items()}
            k_dict.update(data_dict)
            nw_list.append(k_dict)
        return nw_list

    def hbase_batch_delete(self, index=None, prefix="", data_list=[], p_key_name="id"):
        """
              批量删除数据
              :param index:
              :param prefix:前缀:dw,dm,ods
              :return:
              """
        row_keys = [str(p.get(p_key_name)) for p in data_list]
        self.hbase.batch_delete(row_keys, index=index, prefix=prefix)
        return {
            'msg': 'delete successful', 'status': 200}

    def hbase_scan_table(self, index=None, prefix="", row_start=None, row_stop=None, row_prefix=None, filter_f=None,
                         limit=None, p_key_name="id"):
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

        hbase_dict = self.hbase.scan_table(row_start, row_stop, row_prefix, index=index, prefix=prefix,
                                           filter_f=filter_f, limit=limit)
        nw_list = []
        for k, v in hbase_dict.items():
            k_dict = {p_key_name: k}
            data_dict = {k1.replace("%s:" % COLUMN, ""): v1 for k1, v1 in v.items()}
            k_dict.update(data_dict)
            nw_list.append(k_dict)
        return nw_list
