# -*- coding: UTF-8 -*-
import json
import tornado.web
import inspect
from ..py_api_b import PyApiB


class HttpHandlerU(tornado.web.RequestHandler, PyApiB):
    """
    HTTP服务器端接口基类
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    getPath: str = None
    """ 
    复写get方法时需要给getPath付值，如：/test 
    """
    postPath: str = None
    """ 复写post方法时需要给postPath付值，如：/test """

    def returnData(self, data=None, code=200, msg='OK'):
        """
        返回数据
        
        Args:

        """
        self.write(
            json.dumps({
                'code': code,
                'msg': msg,
                'data': {} if data == None else data
            }))
        self.finish()