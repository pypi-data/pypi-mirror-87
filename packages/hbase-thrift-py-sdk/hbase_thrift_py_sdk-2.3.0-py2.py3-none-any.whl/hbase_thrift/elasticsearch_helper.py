# -*- coding: utf-8 -*-
# @Time    : 2020/7/27 19:31
# @Author  :
# https://blog.csdn.net/Cocktail_py/article/details/99740388

from elasticsearch import helpers


def bulk_insearch_es(es, p_key, datas=[], index="dw_gofish_article"):
    """
    批量插入es
    :param p_key: 主键名称
    :param datas: 数据列表
    :param index: 索引
    :param doc_type: 文档
    :return:
    """

    def gender_data():
        for idx, da in enumerate(datas):
            p_k = da.get(p_key)
            yield {
                "_index": index,
                "_id": p_k,
                "_source": da,
                "_retry_on_conflict": 5,
            }

    result = helpers.bulk(es, gender_data())
    return result
