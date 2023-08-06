## hbase_thrift
安装依赖:
pip install elasticsearch==7.5.1 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

pip install setuptools==41.0.1  -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

pip install thriftpy2==0.4.8 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

安装和使用SDK：

1.使用pip进行安装(https://pypi.org/project/hbase-thrift-py-sdk)（推荐）


pip install hbase-thrift-py-sdk

2.原生的安装方式(或)：

1).卸载之前已经安装过这个sdk(如果是第一次安装 忽略)

pip uninstall hbase-thrift-py-sdk

2).解压，进入主目录下

3).安装

python setup.py install


4.使用相应功能

```
# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 10:01
# @Author  : Cocktail_py


from hbase_thrift.hbase_es import HBaseEs


def main():
    # 初始化hbase es组件

    db = HBaseEs(hbase_host="63.87.237.104:9090",
                 es_host_list=["192.168.18.149:19200", "192.168.18.150:19200", "192.168.18.151:19200"],
                 user_tuple=("username", "password"))
    # 查询数据
    # 参数            是否必填   参数类型        参数说明
    # body	         是		  字典类型        elasticsearch dsl
    # index	         是		  字符串类型      索引
    # columns	         否		  列表类型        查询结果返回的字段,如只需要返回简介 [“brief”]
    # is_scroll	     否		  int类型         是否支持滚动查询 0:不开启滚动查询 1:开始滚动查询
    # not_scroll_first 否		  int类型         是否第一次滚动查询 0:第一次滚动查询 1:非第一次滚动查询
    # scroll	         否		  字符串类型      滚动深度(默认200m)
    # sid	             否		  字符串类型      滚动查询指针
    # size	         否		  int类型        滚动查询需要返回的条数(默认100条)

    # 如果想要获取数仓数据is_processed=0, 获取数集is_processed=1(已废弃)

    """
    prefix:前缀:dw,dm,ods
    """
    # data = db.get(index="dm_gofish_test",body={
    #     "track_total_hits": True,
    #     "query": {"match_phrase": {
    #    "_id": "2"
    #  }}
    # }, columns=[], prefix="dm")
    # print(data)

    # # 添加数据(每条数据必须包含相应id,将数据以字典的形式放入到列表中,批量添加数据)
    # is_cover:是否需要全覆盖 0:重复数据不插入 1:全数据插入
    # result = db.add(index="dm_gofish_test", prefix="dm",data_list=[{"id": "62", "c_url": "https://www.baidu.com", "kw": "led", "kw1": "led1"},
    #                            {"id": "67", "c_url": "https://www.baidu.com", "kw": "led", "kw1": "led1"}], is_cover=0)
    # print(result)

    # 写入单条数据
    # index 索引名
    # prefix 前缀
    # data_dict={} # 每条数据都需要包含唯一id
    # data = {}
    # db.add(index="dw_gofish_many_product", prefix="dw", data_list=[data],is_cover=1)


    # #
    # # 修改(每条数据必须包含相应id,将该数据中需要修改的字段以字典的形式放入到列表中,批量修改数据)
    # # 当is_cover=1时,更新的数据以当前数据为准将以前旧的数据重新覆盖
    # # exist_update_not_exist_index是否存在更新不存在插入 exist_update_not_exist_index=1 存在更新则不存在插入
    # result = db.update(index="dw_gofish_media_comment",prefix="dw",data_list=[{"id": "17857215200076311", "comment_content": "A nyaralás alatt is meg lehet osztani az élményeket? 1"}],is_cover=0)
    
    # 单条数据更新
    result = db.single_update( index="dm_gofish_test", prefix="dm", p_key_name="id", data_dict={"id":99,"name":"99"}, is_cover=1, only_es=0)
    print(result)
    
    # # 删除(每个字典必须包含相应id,将该数据中需要删除的数据中的id以字典的形式放入到列表中,批量删除数据)
    # result = db.delete(index="dm_gofish_test",prefix="dm",
    #     data_list=[{"id": "2"}])

    # 单条插入 默认only_es=1 写入es不写入hbase; only_es=0 直插入hbase,不写入es
    # db.single_add("dm_gofish_test", "dm", data_dict={"id":"1","name":"tom"},only_es=0)

    # 批量写入hbase
    # db.hbase_batch_put(index="dm_gofish_test", prefix="dm",data_list=[{"id":"2","name":"jeey"},{"id":"3","name":"jky"}])

    # 批量删除hbase
    # db.hbase_batch_delete(index="dm_gofish_test", prefix="dm", data_list=[{"id":1},{"id":"2"}])

    # 获取hbase单条数据
    # db.hbase_query_single_line(index="dm_gofish_test", prefix="dm",id_=3)

    # 批量hbase单条数据
    # db.hbase_query_multi_lines(index="dm_gofish_test", prefix="dm", data_list=[{"id":3}])

    # 扫表hbase
    # index=None, prefix="", row_start=None, row_stop=None, row_prefix=None, filter_f=None,
    #                          limit=None, 
    # row_start起始row_key
    # row_stop结束row_key
    # row_prefix row_key的前缀
    # filter_f hbase的filter语法
    # limit 条数
    print(db.hbase_scan_table(index="dm_gofish_test",prefix="dm"))

if __name__ == '__main__':
    main()



```