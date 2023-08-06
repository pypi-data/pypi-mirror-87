# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class ProxyCrawlerU(PyApiB):
    """
    代理相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def getProxys(self) -> list:
        """ 获取和解析代理
        {"host":"xx.xx.xx.xx","port":"xxxx","user":"","pswd":""}
        """
        return []
    
    