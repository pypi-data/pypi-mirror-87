# -*- coding: UTF-8 -*-
import json
import tornado.web
import inspect
from .httpHandlerU import HttpHandlerU
from ..py_api_b import PyApiB


class HttpServerU(PyApiB):
    """
    HTTP服务器端相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self, port=80):
        self.__port = int(port)
        self.handlers = {}

    def addHandlers(self, handlers):
        import importlib
        import os
        cwd = os.path.dirname(os.path.abspath(handlers.__file__))
        files = os.listdir(cwd)
        for i in files:
            if not i.startswith('_') and i.endswith('.py'):
                m = '.' + i[:-3]
                mdl = importlib.import_module(m, handlers.__package__)
                if "__all__" in mdl.__dict__:
                    names = mdl.__dict__["__all__"]
                else:
                    names = [x for x in mdl.__dict__ if not x.startswith("_")]
                need_import_cls = {}
                need_import_cls.update({k: getattr(mdl, k) for k in names})
                for c in need_import_cls:
                    if need_import_cls[c].__base__.__name__ == 'HttpHandlerU':
                        self.addHandler(need_import_cls[c])
        return self

    def addHandler(self, handler: HttpHandlerU):
        if handler.getPath:
            getParams = inspect.signature(handler.get).parameters
            handlerUrl = handler.getPath
            for getParam in getParams:
                if getParam not in ['self', 'args', 'kwargs']:
                    handlerUrl = f"{handlerUrl}/(?P<{getParam}>.*)"
            self.handlers[handlerUrl] = handler
        if handler.postPath:
            postParams = inspect.signature(handler.post).parameters
            handlerUrl = handler.postPath
            for postParam in postParams:
                if postParam not in ['self', 'args', 'kwargs']:
                    handlerUrl = f"{handlerUrl}/(?P<{postParam}>.*)"
            self.handlers[handlerUrl] = handler
        return self

    def __make_app(self):
        hs = []
        for url_path in self.handlers:
            h = (url_path, self.handlers[url_path])
            hs.append(h)
        return tornado.web.Application(hs)

    def start(self):
        app = self.__make_app()
        app.listen(self.__port)
        tornado.ioloop.IOLoop.current().start()
