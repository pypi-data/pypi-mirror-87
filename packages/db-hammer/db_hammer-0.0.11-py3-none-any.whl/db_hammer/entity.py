from enum import Enum


def table(name=None):
    """数据据保存的表名"""

    def decorate(clazz):
        if name is None:
            setattr(clazz, "__table_name", clazz.__name__)
        else:
            setattr(clazz, "__table_name", name)

        return clazz

    return decorate


def primary_key(keys):
    """配置主键"""
    if isinstance(keys, str):
        keys = str(keys).split(",")

    def decorate(clazz):
        setattr(clazz, "__primary_key", keys)
        return clazz

    return decorate


def columns(**kwargs):
    """数据库保存时列名定义"""
    def decorate(clazz):
        __columns = {}
        for k in kwargs:
            __columns[k] = kwargs[k]
        setattr(clazz, "__columns", __columns)
        return clazz
    return decorate
