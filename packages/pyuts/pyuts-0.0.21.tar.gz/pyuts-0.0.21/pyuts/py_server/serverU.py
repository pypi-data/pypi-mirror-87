# -*- coding: UTF-8 -*-
from .httpServerU import HttpServerU
from ..py_api_b import PyApiB


class ServerU(PyApiB):
    """
    服务器端相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def http(self, port=80) -> HttpServerU:
        return HttpServerU(port)