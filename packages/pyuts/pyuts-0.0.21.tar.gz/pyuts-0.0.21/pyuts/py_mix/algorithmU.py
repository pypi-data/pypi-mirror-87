# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
import urllib.parse

class AlgorithmU(PyApiB):
    """
    算法相关工具
    """

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
      
    def md5(self, data):
        """ to md5 """
        import hashlib
        return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
      
    def sha256(self, data):
        """ to sha256 """
        import hashlib
        return hashlib.sha256(bytes(data,encoding='utf-8')).hexdigest()
      
    def base64encodeB(self,data):
        """ to base64 """
        import base64
        return base64.b64encode(data).decode("utf-8")
      
    def base64encode(self,data):
        """ to base64 """
        return self.base64encodeB(data.encode("utf-8"))
      
    def base64decode(self,data):
        """ from base64 """
        return self.base64decodeB(data).decode("utf-8")
    
    def base64decodeB(self, data):
        """ from base64 """
        import base64
        return base64.b64decode(data)
      
    def stepStr(self, dataStr, step=0, isFiltOut=False):
        bdataStr = bytes(dataStr,encoding='utf8')
        bdataStrs = []
        for b in bdataStr:
            bb = b+step
            if bb > 128:
                if isFiltOut:
                    continue
                while bb > 128:
                    bb -= 128
            elif bb < 0:
                if isFiltOut:
                    continue
                while bb < 0:
                    bb += 128
            bdataStrs.append(bb)
        return str(bytes(bdataStrs),'utf8')
    
    def urlEncode(self, dataStr):
        return urllib.parse.quote(dataStr)
    
    def urlDecode(self, dataStr):
        return urllib.parse.unquote(dataStr)