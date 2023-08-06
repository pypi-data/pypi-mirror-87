# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class ModuleU(PyApiB):
    """
    模块相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def importClsByKV(self, module,key,value):
        """ 引入模块内类存在属性key的值为value的类 """
        import importlib
        import os
        handlers = module
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
                clss = {}
                clss.update({k: getattr(mdl, k) for k in names})
                for cn in clss:
                    vv = getattr(clss[cn],key,None)
                    if vv == value:
                        return clss[cn]
        return None
    
    