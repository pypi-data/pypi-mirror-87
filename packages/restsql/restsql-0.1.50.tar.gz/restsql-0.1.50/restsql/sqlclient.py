# -*- coding:utf-8 -*-
import datetime
import logging
import re
import sys

import pandas as pd
import six
from peewee import Model, fn, JOIN

from restsql.dbsetting import EnumDataBase, db_settings
from restsql.model import ModelMeta
from restsql.table import Table

logger = logging.getLogger("restsql")


class SubQuery(object):
    # 单个sql子句查询
    def __init__(self, query, join_type, database, on=None, export=None, limit=1000):
        self.query = query
        self.join_type = join_type
        self.database = database
        self.table = self._get_table()
        self.on = on
        self.export = export
        self.alias = self._get_alias(export)
        # self.schema = schema
        self._result = None
        self.query['from'] = self.query['from'].split('.', 1)[1]
        self.limit = limit
        self.join_querys = []

    def attach_joins(self, *join_querys):
        """
        用于连接joins表，加速query
        """
        self.join_querys = self.join_querys + list(join_querys)

    @staticmethod
    def _get_alias(export):
        if export is None:
            return {}
        else:
            alias_result = {}
            for item in export:
                raw = item.split('@')[0]
                alias = item.split('@')[1]
                alias_result[raw] = alias
            return alias_result

    def _get_table(self):
        table_name = self.query['from'].split(".", 1)[-1]
        for table in self.database.tables:
            if table_name == table.table_name:
                return table
        return None

    def get_model(self):
        """
        更改为内置属性的方式。在访问extract_xxx_xxx系列函数前调用。
        """
        # if not isinstance(self.database.db, Database):
        #     raise RuntimeError('db is not Database instance')
        if self.table.__bases__[0] != Table:
            raise RuntimeError('schema is not Table class')

        class NewModel(six.with_metaclass(ModelMeta, Model)):
            class Meta:
                database = self.database.db
                table_name = self.table.table_name
                fields = self.table.fields
                schema = getattr(self.database, 'schema', None)

        self.db_model = NewModel

    def extract_select_params(self):
        """
        从Model中提取出select
        """
        selects = self.query['fields'] + self.query['aggregation']
        select_params = []
        for expression in selects:
            if '__' in expression:
                field, operator = expression.split('__')
                if operator in ['count', 'sum', 'avg', 'max', 'min']:
                    param = getattr(fn, operator)(getattr(self.db_model, field)).alias(expression)
                    select_params.append(param)
                elif operator == 'count_distinct':
                    # count_distinct需要特殊处理，peewee库中没有专门的处理方法
                    param = fn.Count(fn.Distinct(getattr(self.db_model, field))).alias(expression)
                    select_params.append(param)
                else:
                    raise RuntimeError('operator {} is invalid'.format(operator))
            else:
                select_params.append(getattr(self.db_model, expression))
        return select_params

    def extract_where_params(self):
        filters = self.query.get('filter', {})
        where_params = []
        for filter_k, filter_v in filters.items():
            if '__' in filter_k:
                field, operator = filter_k.split('__')
                if operator == 'gt':
                    # where_expression = (getattr(model, field) > filter_v)
                    where_params.append(getattr(self.db_model, field) > filter_v)
                elif operator == 'lt':
                    where_params.append(getattr(self.db_model, field) < filter_v)
                elif operator == 'gte':
                    where_params.append(getattr(self.db_model, field) >= filter_v)
                elif operator == 'lte':
                    where_params.append(getattr(self.db_model, field) <= filter_v)
                elif operator == 'contains':
                    where_params.append(getattr(self.db_model, field).contains(filter_v))
                elif operator == 'startswith':
                    where_params.append(getattr(self.db_model, field).startswith(filter_v))
                elif operator == 'endswith':
                    where_params.append(getattr(self.db_model, field).endswith(filter_v))
                elif operator == 'range':
                    if isinstance(filter_v, list) and len(filter_v) == 2:
                        where_params.append(getattr(self.db_model, field).between(*filter_v))
                    else:
                        if isinstance(filter_v, list):
                            raise RuntimeError('the length of Range list should be 2')
                        else:
                            raise RuntimeError('Range value should be a list')
                elif operator == 'in':
                    if isinstance(filter_v, list):
                        where_params.append(getattr(self.db_model, field).in_(filter_v))
                    else:
                        raise RuntimeError('In value should be list')
                else:
                    raise RuntimeError('filter {} is invalid'.format(operator))
            else:
                where_params.append(getattr(self.db_model, filter_k) == filter_v)
        return where_params

    def extract_group_by_params(self):
        groups = self.query.get('group_by', [])
        group_params = [getattr(self.db_model, field) for field in groups]
        return group_params

    def _get_peewee_query(self):
        """
        用于拼凑peewee查询Model，获得一个ModelSelect
        TODO: 暂时以分支方式保留es的单查询支持
        """
        if len(self.join_querys) != 0:
            self.get_model()
            for join_query in self.join_querys:
                join_query.get_model()

            # select params
            select_params = self.extract_select_params()
            for join_query in self.join_querys:
                select_params = select_params + join_query.extract_select_params()

            # where params
            where_params = self.extract_where_params()
            for join_query in self.join_querys:
                where_params = where_params + join_query.extract_where_params()

            # group by params
            group_params = self.extract_group_by_params()
            for join_query in self.join_querys:
                group_params = group_params + join_query.extract_group_by_params()

            results = self.db_model.select(*select_params)
            join_table = {
                "left_join": JOIN.LEFT_OUTER,
                "inner_join": JOIN.INNER,
                "full_join": JOIN.FULL
            }
            for join_query in self.join_querys:
                main_on_field = join_query.on.keys()[0]
                sub_on_field = join_query.on.values()[0]
                results = results.join(dest=join_query.db_model, join_type=join_table[join_query.join_type], on=(
                        getattr(self.db_model, main_on_field) == getattr(join_query.db_model, sub_on_field)))
            if len(where_params) > 0:
                # filter
                results = results.where(*where_params)
            if len(group_params) > 0:
                # group by
                results = results.group_by(*group_params)
            limit = self.query.get('limit', 1000)
            results = results.limit(limit)
            return results
        else:  # Original
            self.get_model()
            limit = self.query.get('limit', 1000)

            # get select params
            select_params = self.extract_select_params()

            # get where params
            where_params = self.extract_where_params()

            # get group by params
            group_params = self.extract_group_by_params()
            # select
            results = self.db_model.select(*select_params)
            if len(where_params) > 0:
                # filter
                results = results.where(*where_params)
            if len(group_params) > 0:
                # group by
                results = results.group_by(*group_params)
            results = results.limit(limit)
            return results

    def _query_sql(self):
        """
        真正query。将获取到的元组处理join的重命名。
        """
        query = self._get_peewee_query()
        time1 = datetime.datetime.now()
        results = pd.DataFrame(query.dicts())
        time2 = datetime.datetime.now()
        if len(self.join_querys) > 0:
            sub_selects = []
            alias = {}
            for join_query in self.join_querys:
                sub_selects = sub_selects + join_query.query['fields'] + join_query.query['aggregation']
                alias.update(join_query.alias)
            if len(alias.keys()) != 0:
                results.rename(alias, axis="columns", inplace=True)
            self._result = results
        else:
            if len(self.alias.keys()) != 0:
                results.rename(self.alias, axis="columns", inplace=True)
            self._result = results
        time3 = datetime.datetime.now()
        # print "Query1: {}".format(time2 - time1)
        # print "Query3: {}".format(time3 - time2)

    def _query_impala(self):
        client = self.database.impala_client
        sql, params = self._get_peewee_query().sql()
        logger.info("IMPALA: Original SQL is: %s [%s]", sql, params)
        self._result = pd.DataFrame(client.run_sql((sql, params)))

    def _query_es(self):
        results = []
        es_client = self.database.db
        dsl = self._json_to_dsl()
        index = dsl['from']
        del dsl['from']
        raw_result = es_client.search(index=index, body=dsl)
        # result = {}
        if 'aggs' in raw_result or 'aggregations' in raw_result:
            if raw_result.get('aggregations'):
                results = raw_result['aggregations']['groupby']['buckets']
            else:
                results = raw_result['agg']['groupby']['buckets']
            for it in results:
                pair = it['key'].split(';')
                for pair_item in pair:
                    it.update({pair_item.split(':')[0]: pair_item.split(':')[1]})
                del it['key']
                del it['doc_count']  # TODO: 暂时没用的一个字段
                for field, value in it.items():
                    if isinstance(value, dict) and 'value' in value:
                        if self.alias is None:
                            it[field] = value['value']
                        else:
                            if field in self.alias.keys():
                                it[self.alias[field]] = value['value']
        elif 'hits' in raw_result and 'hits' in raw_result['hits']:
            if self.alias is None:
                results = list(map(lambda x: x['_source'], raw_result['hits']['hits']))
            # for it in results:
            else:
                for it in raw_result['hits']['hits']:
                    record = it['_source']
                    result = {}
                    for field in record.keys():
                        if field in self.alias.keys():
                            result[self.alias[field]] = record[field]
                    results.append(result)
        self._result = pd.DataFrame(results)

    def _json_to_dsl(self):
        if self.query['from'] is None or self.query['from'] == '':
            raise SyntaxError('Check query whether contains the "from" field')
        limit = self.query.get("limit", 1000)
        dsl = {
            'size': limit,
            'query': {
                'bool': {
                    'must': []
                }
            },
            'sort': [],
            '_source': {
                'includes': []
            },
            'aggs': {
                'groupby': {
                    'terms': {
                        'script': {
                            'source': ''
                        }
                    },
                    'aggs': {}
                }
            },
            'from': self.query['from']
        }
        dsl['_source']['includes'] = self.query['fields']
        dsl_where = dsl['query']['bool']['must']
        dsl_group_by = ''
        dsl_aggs = dsl['aggs']['groupby']['aggs']
        dsl_sort = dsl['sort']

        # 处理filter
        for field, value in self.query['filter'].items():
            if '__' not in field:
                dsl_where.append({
                    'term': {
                        field: value
                    }
                })
            else:
                op = field.split('__')[1]
                field_name = field.split('__')[0]
                if op == 'gt':
                    dsl_where.append({
                        'range': {
                            field_name: {'gt': value}
                        }
                    })
                elif op == 'lt':
                    dsl_where.append({
                        'range': {
                            field_name: {'lt': value}
                        }
                    })
                elif op == 'gte':
                    dsl_where.append({
                        'range': {
                            field_name: {'gte': value}
                        }
                    })
                elif op == 'lte':
                    dsl_where.append({
                        'range': {
                            field_name: {'lte': value}
                        }
                    })
                elif op == 'contains':
                    """"
                    TODO: 本来想用match/match_phrase来进行模糊匹配，但是由于这两种查询由于分词的缘故，现有的
                          分词情况并不能完美的模拟sql中的like，所以暂时采用正则查询。正则查询的效率很低。
                    dsl_where.append({
                        'match_phrase': {
                            field_name: {
                                'query': value
                            }
                        }
                    })
                    """
                    dsl_where.append({
                        'wildcard': {field_name: ''.join(['*', value, '*'])}
                    })
                elif op == 'startswith':
                    dsl_where.append({
                        'prefix': {field_name: value}
                    })
                elif op == 'endswith':
                    dsl_where.append({
                        'wildcard': {field_name: ''.join(['*', value])}
                    })
                elif op == 'range':
                    if len(value) != 2:
                        raise SyntaxError('Check your "range" query')
                    dsl_where.append({
                        'range': {
                            field_name: {'gte': value[0], 'lte': value[1]}
                        }
                    })
                elif op == 'in':
                    dsl_where.append({
                        'terms': {field_name: value}
                    })
                else:
                    raise SyntaxError('cat not support op: {0}, field: {1}'.format(op, field))
        if self.query.get('group_by'):
            # 处理 group by
            """
            由于ES 6.x以下版本不支持 composite 语法，所以这里采用script方式来实现group by，用来兼容不同版本ES这部分语法的差异性
            script中source的格式：key:value;key:value
            定义成这个样子是方便后面从查询结果中提取数据
            """
            for field in self.query['group_by']:
                dsl_group_by = ''.join(
                    [dsl_group_by, "'", field, "'", " + ':' + ", "doc['", field, "'].value", " + ';' + "])
            dsl_group_by = dsl_group_by[:len(dsl_group_by) - len(" + ';' + ")]  # 去掉结尾的 " + ';' + "
            dsl['aggs']['groupby']['terms']['script']['source'] = dsl_group_by
            # 处理 aggregation
            for field in self.query['aggregation']:
                field_name, op = field.split('__')[0], field.split('__')[1]
                func_map = {'count': 'value_count', 'sum': 'sum', 'avg': 'avg', 'max': 'max', 'min': 'min',
                            'count_distinct': 'cardinality'}
                if op in func_map:
                    dsl_aggs[field] = {func_map[op]: {'field': field_name}}
                else:
                    raise SyntaxError('cat not support aggregation operation: {}'.format(op))
        else:
            del dsl['aggs']

        # 处理 sort
        if self.query.get('sort'):
            for sort_it in self.query['sort']:
                is_reverse = sort_it.find('-')
                if is_reverse != 0:
                    dsl_sort.append({
                        sort_it: {'order': 'asc'}
                    })
                else:
                    field = ''.join(sort_it.split('-')[1:])
                    dsl_sort.append({
                        field: {'order': 'desc'}
                    })
        else:
            del dsl['sort']
        return dsl

    def do_query(self):
        """
        执行query。将区分db_type分别调用各自执行函数
        """
        db_type = self.database.db_type
        if db_type in [EnumDataBase.MYSQL, EnumDataBase.PG, EnumDataBase.SQLITE]:
            self._query_sql()
        elif db_type == EnumDataBase.ES:
            self._query_es()
        elif db_type == EnumDataBase.IMPALA:
            self._query_impala()

    @property
    def result(self):
        return self._result


class RestSqlClient(object):
    """
    RestSQL的核心类。所有输入输出都由此类处理。
    """

    def __init__(self):
        """
        初始化一个Client。
        """
        pass

    def _get_db_setting_by_from_part(self, db_setting_table_name):
        """
        从from部分获取db_setting实例。
        """
        try:
            db_setting_name, table_name = db_setting_table_name.split('.', 1)
        except ValueError:
            raise RuntimeError('table_name {} is not invalid'.format(db_setting_table_name))
        return db_settings.get_by_name(db_setting_name)

    def query(self, query):
        """
        query接口
        """

        # 1、拆分sql
        subquery_list = []
        main_subquery = query['select']
        main_db = self._get_db_setting_by_from_part(main_subquery['from'])
        main_query = SubQuery(query=main_subquery, join_type='main', database=main_db)
        subquery_list.append(main_query)
        for join in query['join']:  # 目前的方案是所有的join分query。后续优化方向是同源query下放到数据库。
            join_subquery = join['query']['select']
            join_db = self._get_db_setting_by_from_part(join_subquery['from'])
            sub_query = SubQuery(query=join_subquery, join_type=join['type'], database=join_db, on=join['on'],
                                 export=join['export'])
            if main_db == join_db:
                main_query.attach_joins(sub_query)
            else:
                subquery_list.append(sub_query)

        #  TODO: 将同源且非es的查询attach到main中
        time2 = datetime.datetime.now()
        # 2、查询sql
        data_frame = None
        for subquery in subquery_list:
            subquery.do_query()
            if subquery.join_type == 'main':
                # 取出主查询结果，方便下一步合并
                data_frame = subquery.result
        time3 = datetime.datetime.now()

        # 3、合并
        join_type_map = {
            'left_join': 'left',
            'inner_join': 'inner',
            'full_join': 'outer'
        }
        for subquery in subquery_list:
            if subquery.join_type in join_type_map.keys():
                df = subquery.result
                data_frame = data_frame.merge(df, left_on=subquery.on.keys(),
                                              right_on=subquery.on.values(),
                                              how=join_type_map[subquery.join_type])

        # 4、sort
        sort_list = query.get('sort', None)
        if sort_list and data_frame.to_dict():
            sort_methods = []
            for index, value in enumerate(sort_list):
                if value.startswith('-'):
                    # it = value[1:]
                    sort_list[index] = value[1:]  # 去掉-
                    sort_methods.append(False)
                else:
                    sort_methods.append(True)
            data_frame = data_frame.sort_values(by=sort_list, ascending=sort_methods)

        # 5、合并后limit处理
        limit = query.get('limit', 1000)
        data_frame = data_frame[0:limit]
        data_frame = data_frame.fillna('null')

        time6 = datetime.datetime.now()

        # 6、整个语句的fields提取及alias处理
        alias_map = {}
        for field in query['fields']:
            if field.find('@') != -1:
                alias_map.update({field.split('@')[0]: field.split('@')[1]})

        columns_list = data_frame.columns.tolist()
        exclude_list = []
        for raw, alias in alias_map.items():
            if raw not in columns_list:
                if ('+' in raw) or ('-' in raw) or ('*' in raw) or ('/' in raw):  # 表达式
                    var_list = list(set(self._extract_var(raw)))
                    for var in var_list:
                        raw = raw.replace(var, 'data_frame[\'{}\']'.format(var))
                    try:
                        data_frame[alias] = eval(raw)
                    except:
                        logger.warning("Failed when calculating %s: %s", raw, sys.exc_info()[0])
                        raise RuntimeError('Failed when calculating {}: {}'.format(raw, sys.exc_info()[0]))
                else:  # 多余字段
                    data_frame.drop(raw, axis="columns", inplace=True)
            else:
                if alias == 'exclude':  # 用于计算，最后删除
                    exclude_list.append(raw)
                else:  # 需要重命名
                    data_frame.rename({raw: alias}, axis="columns", inplace=True)
        for exclude_raw in exclude_list:  # 删除exclude部分
            data_frame.drop(exclude_raw, axis="columns", inplace=True)
        for excess_key in columns_list:  # 删除fields中不存在的字段
            if excess_key not in alias_map.keys():
                data_frame.drop(excess_key, axis="columns", inplace=True)
        time7 = datetime.datetime.now()
        # print "query耗时: {}".format(time3 - time2)
        # print "整理耗时: {}".format(time7 - time6)
        return data_frame.to_dict(orient='records')

    @staticmethod
    def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def _extract_var(expression):
        """
        将计算表达式中的变量提取出来
        :param expression:  (a+b)*(c-d)
        :return: [a,b,c,d]
        """
        return re.findall('[^\+,\-,\*,\/,(,)]+', expression)
