# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class JsonU(PyApiB):
    """
    json
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def fromString(self, string):
        import json
        return json.loads(string)

    def toString(self, json_data, ensure_ascii=False, indent=2):
        import json
        return json.dumps(json_data, ensure_ascii=ensure_ascii, indent=indent)

    def fromFile(self, filePath):
        from ..py_file.fileU import FileU
        return FileU.produce("JsonU").read_json(filePath)

    def toFile(self, json_data, filePath):
        from ..py_file.fileU import FileU
        return FileU.produce("JsonU").write_json(filePath, json_data)
