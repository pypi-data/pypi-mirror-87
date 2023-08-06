# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
# pip install PyExecJS
import execjs
from execjs._abstract_runtime_context import AbstractRuntimeContext


class JsU(PyApiB):
    """
    js工具， pip install PyExecJS
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def loadJsFile(self, filePath):
        from ..py_file.fileU import FileU
        fileU = FileU()
        jsStr = fileU.read_str(filePath)
        return self.loadJsStr(jsStr)
    
    def loadJsStr(self, jsStr):
        self.ctx = execjs.compile(jsStr)
        return self
        
    def _getJsRuntime(self)->AbstractRuntimeContext:
        return self.ctx
        
    def callFun(self, funName, *args):
        """ 调用函数 """
        return self._getJsRuntime().call(funName, *args)
        
    def getVal(self, valName):
        """ 获取变量值 """
        return self._getJsRuntime().eval(valName)
    
    