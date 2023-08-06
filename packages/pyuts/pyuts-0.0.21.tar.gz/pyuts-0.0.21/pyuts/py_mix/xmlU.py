# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from ..py_file.fileU import FileU
import xmltodict
import json


class XmlU(PyApiB):
    """
    XML
    pip install xmltodict
    """
    
    
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def parseByFile(self, filePath):
        xmlStr = FileU.produce().read_str(filePath)
        return self.parseByStr(xmlStr)
    
    def parseByStr(self, xmlStr, **kwargs):
        xmlObj = xmltodict.parse(xmlStr, **kwargs)
        return json.loads(json.dumps(xmlObj))
    