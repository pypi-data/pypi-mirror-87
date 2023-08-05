# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase

from restsql.impalet import ImpalaClient, ImpalaDatabase


class EnumDataBase:
    PG = 'PostgreSQL'
    MYSQL = 'MySql'
    SQLITE = 'SQLite'
    ES = 'Elasticsearch'
    IMPALA = 'Impala'


class DbSetting:
    """
    db_setting类。存储各个数据源的配置信息，用于连接、peewee查询。这里应该用builder模式但是py下的构造着模式有些奇怪，就改动了下。
    """

    def __init__(self, name, db_type, host, db_name=None, port=None, user=None, password=None, schema=None,
                 tables=None, black_tables=None, black_fields=None):
        """
        db_setting初始化器。
        :param name: 该db_setting的name。用于区分db_setting.
        :param db_type: 数据库类型。由EnumDataBase枚举类定义。
        :param host: 数据库host。
        :param db_name: 数据库名。
        :param port: 端口名。
        :param user: 用户名。用于连接数据库。
        :param password: 密码。用户连接数据库。
        :param schema: 模式。用于pgsql数据源。
        :param tables: 表。用户自定义相关表。是继承自Table类的类的list。
        :param black_tables: 黑名单表。使用自动维护时有用。是string的list。
        :param black_fields: 黑名单字段。使用自动维护时有用。是字典，结构为{'表名': ['需忽视字段名', ], }
        """
        if tables is None:
            tables = []
        if black_fields is None:
            black_fields = {}
        if black_tables is None:
            black_tables = []
        self.name = name
        # self.db_name = db_name
        self.db_type = db_type
        # self.host = host
        # self.port = port
        # self.user = user
        # self.password = password
        self.schema = schema
        if isinstance(tables, list):
            self.tables = tables
        else:
            raise RuntimeError("List of class(extended from Table) needed.")
        if isinstance(black_tables, list):
            self.black_tables = black_tables
        else:
            raise RuntimeError("List of string(tables' name) needed.")
        if isinstance(black_fields, dict):
            self.black_fields = black_fields
        else:
            raise RuntimeError("Dict of table_name: [field_name] needed.")
        if db_type == EnumDataBase.SQLITE:
            self.db = SqliteDatabase(host)
        elif db_type == EnumDataBase.PG:
            if db_name is None or port is None or user is None or password is None:
                raise RuntimeError("Empty elements in PgSQL")
            self.db = PostgresqlDatabase(
                db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
        elif db_type == EnumDataBase.MYSQL:
            if db_name is None or port is None or user is None or password is None:
                raise RuntimeError("Empty elements in PgSQL")
            self.db = MySQLDatabase(
                db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
        elif db_type == EnumDataBase.IMPALA:
            if db_name is None or port is None:
                raise RuntimeError("Empty elements in Impala")
            self.db = ImpalaDatabase("impala")
            self.impala_client = ImpalaClient(host, port, db_name)
        elif db_type == EnumDataBase.ES:
            self.db = Elasticsearch(host)


class _DbSettings:
    """
    线程不安全的DbSettings类，系统中作为单例管理
    使用前put、add添加新的db_setting
    使用时get_by_name将锁上当前db_setting并返回
    使用后一定要return_by_name返回当前db_setting以释放锁
    """

    def __init__(self):
        self._db_settings = {}

    def get_all_name(self):
        """
        获取当前db_settings中所有db_setting的name的list
        :return: List of db_settings' name
        """
        return self._db_settings.keys()

    def put(self, *db_setting_tuple):
        """
        向db_settings中直接添加db_setting实例
        :param db_setting_tuple: db_setting的可变参数列表
        :return: None
        """
        for db_setting in db_setting_tuple:
            if not isinstance(db_setting, DbSetting):
                raise RuntimeError("DbSetting needed!")
            self._db_settings[db_setting.name] = db_setting

    def add(self, name, db_type, host, db_name=None, port=None, user=None, password=None, schema=None,
            tables=None, black_tables=None, black_fields=None):
        """
        向db_settings中添加新的db_setting类。
        :param name: 该db_setting的name。用于区分db_setting.
        :param db_type: 数据库类型。由EnumDataBase枚举类定义。
        :param host: 数据库host。
        :param db_name: 数据库名。
        :param port: 端口名。
        :param user: 用户名。用于连接数据库。
        :param password: 密码。用户连接数据库。
        :param schema: 模式。用于pgsql数据源。
        :param tables: 表。用户自定义相关表。是继承自Table类的类的list。
        :param black_tables: 黑名单表。使用自动维护时有用。是string的list。
        :param black_fields: 黑名单字段。使用自动维护时有用。是字典，结构为{'表名': ['需忽视字段名', ], }
        :return: None
        """
        self._db_settings[name] = DbSetting(name, db_type, host, db_name, port, user, password, schema, tables,
                                            black_tables, black_fields)

    def remove_by_name(self, name):
        """
        根据提供的db_setting's name删除db_setting
        :param name: 待删除db_setting的name
        :return: None
        """
        if name in self._db_settings:
            del self._db_settings[name]

    def get_by_name(self, name):
        """
        根据提供的db_setting的name获取db_setting。
        注意：需手动维护锁
        :param name: 待获取db_setting的name
        :return: db_setting
        """
        if name in self._db_settings:
            return self._db_settings[name]


#  以单例的方式生成db_settings
db_settings = _DbSettings()
