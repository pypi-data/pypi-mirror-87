# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class ProxyInfoU(PyApiB):
    """
    代理信息相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def init(self, host=None, port=None, user=None, pswd=None):
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        
        
    