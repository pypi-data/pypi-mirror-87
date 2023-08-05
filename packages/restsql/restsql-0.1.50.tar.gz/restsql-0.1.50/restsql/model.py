# -*- coding:utf-8 -*-
from peewee import ModelBase, TextField, DoubleField, BooleanField, Database, SqliteDatabase, IntegerField
from restsql.table import Table, StringField, NumberField, BoolField, IntField
from copy import deepcopy


class ModelMeta(ModelBase):
    """
    转换用户自定义表到peewee指定格式
    """

    def __new__(mcs, name, bases, attrs):
        base_attrs = deepcopy(attrs)
        meta = base_attrs.get('Meta', None)
        for field, field_type in meta.fields.items():
            if isinstance(field_type, StringField):
                base_attrs[field] = TextField()
            elif isinstance(field_type, IntField):
                base_attrs[field] = IntegerField()
            elif isinstance(field_type, NumberField):
                base_attrs[field] = DoubleField()
            elif isinstance(field_type, BoolField):
                base_attrs[field] = BooleanField()
        del meta.fields  # 删除该类属性，否则进入base.new中fields属性会产生冲突
        return super(ModelMeta, mcs).__new__(mcs, name, bases, base_attrs)
