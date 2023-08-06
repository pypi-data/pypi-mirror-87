# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
import scrapy
from scrapy.loader.processors import Identity, MapCompose


class ScrapyItemU(scrapy.Item, PyApiB):
    """
    scrapy相关封装工具的数据存储项基类
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    saveTableName = None
    """ 数据保存入库对应的表名，如果不指定，默认用item的类名 """
    
    saveDbName = None
    """ 数据保存入库对应的库名，如果不指定，默认用工程名 """
    
    @staticmethod
    def normal():
        """
        普通属性
        """
        return scrapy.Field()

    @staticmethod
    def identity():
        """
        特征属性
        """
        return scrapy.Field(output_processor=Identity())
