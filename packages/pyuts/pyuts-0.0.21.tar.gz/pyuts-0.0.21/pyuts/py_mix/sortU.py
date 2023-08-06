# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class SortU(PyApiB):
    """
    排序相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __compare(self, p, r, byDict=None):
        if isinstance(p, dict) and byDict != None:
            for byKey in byDict:
                if byKey in p and byKey in r:
                    if p[byKey] == r[byKey]:
                        continue
                    else:
                        return -1 if (p[byKey] < r[byKey]) == (byDict[byKey] < 0) else 1
                else:
                    continue
            return 0
        if isinstance(byDict, int):
            return -1 if (p < r) == (byDict < 0) else 1
        else:
            return -1 if p < r else 1


    def sortArray(self, datas, byDict=None):
        """ 排序数组 """
        if datas == None or len(datas) < 2:
            return datas
        from functools import cmp_to_key
        datas = sorted(datas,key=cmp_to_key(lambda a,b:self.__compare(a, b, byDict)))
        return datas

    def sortByKey(self, dataDict, direct=1):
        if not dataDict:
            return dataDict
        keys = list(dataDict.keys())
        keys = self.sortArray(keys, direct)
        newData = {}
        for key in keys:
            newData[key] = dataDict[key]
        return newData

    def changeToKVArray(self, dataDict):
        kvArray = []
        for key in dataDict:
            kvArray.append({'key':key,'value':dataDict[key]})
        return kvArray