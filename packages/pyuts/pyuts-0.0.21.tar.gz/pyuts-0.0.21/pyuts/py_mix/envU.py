# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class EnvU(PyApiB):
    """
    环境变量相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def get(self,key,default=None):
        """ 获取环境变量的值 """
        import os
        value = default
        if key in os.environ:
            value = os.environ[key]
        return value