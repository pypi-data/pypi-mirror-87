## RestSQL介绍

[点此查看](https://git.code.oa.com/tencent_cloud_mobile_tools/Athena/blob/develop/doc/interface/rest-sql-protocol/rest-sql-protocol.md)

## 示例
```python
# -*- coding:utf-8 -*-
import time

from restsql import RestSqlClient
from restsql.model import Table, StringField
from restsql.dbsetting import EnumDataBase, DbSetting

# 自定义表格
class Kv100(Table):
    table_name = 'kudu_kv_100'
    fields = {
        'app_id': StringField(),
        'device_id': StringField(),
        'time': StringField(),
        'entrance_id': StringField(),
        'user_id': StringField(),
    }

# db_settings初始化
db_settings = [
    DbSetting(
        name='impala_athena',
        db_type=EnumDataBase.IMPALA,
        host='127.0.0.1',
        port=21050,
        db_name='tencent',
        tables=[Kv100],  # 手动添加自定义表格
        black_tables=["funnel", "kv_100", "kv_100_compact", "kv_100_fixed", "kv_100_fixed_old", "kv_100_fixed_test1",
                      "kv_100_fixed_test2", "kv_100_json_compact", "kv_3", "kv_3_compact", "kv_3_fixed",
                      "kv_3_json_compact", "kv_4", "kv_4_compact", "kv_4_fixed", "kv_4_json_compact", "kv_4_orc",
                      "kv_7", "kv_7_compact", "kv_7_fixed", "kv_7_json_compact", "metrics", "metrics_old",
                      "metrics_old1", "pattern_distinct_slice", "po_id_history", "po_id_label", "po_id_source",
                      "resource_flow", "retain_predict", "tencent_kv_100", "tencent_kv_3", "tencent_kv_4",
                      "tencent_kv_7", "tmp_new_usr", "uba_debug_explode_df", "uba_debug_sankey_error_nodes",
                      "uba_debug_sankey_join_links", "uba_debug_sankey_links", "uba_inner_kv_4_fixed",
                      "uba_inner_page_rank", "uba_inner_sankey_links", "uba_inner_sankey_nodes",
                      "uba_inner_sankey_nodes_rank", "uba_kv4_join_3", "uba_res_action_profile",
                      "uba_res_device_metrics", "uba_res_heat_map", "uba_res_page_actions", "uba_res_page_degree",
                      "uba_res_page_markov", "uba_res_page_profile", "uba_res_page_route", "uba_res_sankey_links",
                      "uba_res_sankey_nodes", "uba_res_user_cluster", "uba_res_user_cluster_page_degree",
                      "uba_res_user_cluster_profile", "uba_res_user_clustering", "uba_user_page_degree", "uin_9707_tmp",
                      "user_features", "user_features_9707", "user_features_9707_merged_user",
                      "user_features_9707_user", "user_features_merged", "user_features_qapm", "user_features_qapm_pub",
                      "user_features_qapm_pub_user"],  # 让schema_manager忽视这些table
    ),
]

restsql = RestSqlClient(db_settings=db_settings, middlewares=[])
schema_manager = restsql.get_schema_manager()  # 从RestSqlClient获得一个schema_manager，注意，请保证它为单例
schema_manager.active_daemon()  # 激活守护进程以自动刷新schema


def query_impala():
    query = {
        'select': {
            'from': 'impala_athena.kudu_kv_100',
            'fields': ['app_id', 'device_id', 'user_id', 'time'],
            'filter': {'time__gte': '\'2020-11-03T00:00:00.000Z\'',
                       'time__lte': '\'2020-11-03T00:00:01.000Z\''},
            'aggregation': [],
            'group_by': []
        },
        'join': [],
        'sort': [],
        'fields': ['app_id@aid', 'device_id@did', 'user_id@uid', 'time@time'],
        'limit': 10
    }

    results = restsql.query(query)
    print(results)


if __name__ == "__main__":
    while True:
        query_impala()
        time.sleep(10)
```

## 概念介绍

### db_settings

DbSetting类初始化器：
* name: 该db_setting的name。用于区分db_setting.
* db_type: 数据库类型。由EnumDataBase枚举类定义。
* host: 数据库host。
* db_name: 数据库名。
* port: 端口名。
* user: 用户名。用于连接数据库。
* password: 密码。用户连接数据库。
* schema: 模式。用于pgsql数据源。
* tables: 表。用户自定义相关表。是继承自Table类的类的list。
* black_tables: 黑名单表。使用自动维护时有用。是string的list。
* black_fields: 黑名单字段。使用自动维护时有用。是字典，结构为{'表名': ['需忽视字段名', ], }

### middleware

暂时未实现

查询前对query的处理模块，例如格式检查，也可以对query做自定义修改。暂时只支持自定义的形式，后续会默认添加基本的格式检查


## 发布

1. 打包: `python setup.py sdist build`。
2. 上传: 
    * 安装twine工具: `pip install twine`
    * 发布: `twine upload dist/*`


## Todo List

- [x] Impala不兼容
- [x] alias和raw相同时的冲突
- [x] Impala查询时`IndexError: tuple index out of range`
- [x] 添加表格
    * kudu_kv_100
    * kudu_kv_3
    * kudu_kv_4
    * kudu_kv_7
    * kudu_uba_res_device_metrics
- [x] 前端bug: table格式查询的重载入时存在不会默认隐藏无关栏的bug
- [x] 前端bug: 自动填充时间字段需加入引号
- [x] 添加前端仓库
- [x] 添加后端仓库
- [] 添加schema manager以自动刷新schema
- [] 改为进程安全的db_settings
- [] 优化join。同源join下放到数据库中。
