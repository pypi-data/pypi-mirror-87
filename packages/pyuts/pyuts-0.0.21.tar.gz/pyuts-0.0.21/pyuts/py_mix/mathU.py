# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class MathU(PyApiB):
    """
    数学相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def random(self, min=None, max=None, step=None):
        """
        生成一个随机数\n
        @Args:\n min：最小范围\n max: 最大范围\n step:随机步进范围\n
        """
        import random
        if min == None and max == None and step == None:
            return random.random()
        elif step == None:
            if isinstance(min, int) or isinstance(max, int):
                return random.randint(min, max)
            else:
                return random.uniform(min, max)
        else:
            return random.randrange(min, max, step)
          
    def randomArr(self, fromArr=None, getNum=0):
        if getNum==0 or fromArr == None or getNum >= len(fromArr):
            return []
        aa = []
        l = len(fromArr)
        while True:
            r = self.random(min=0,max=l-1)
            if fromArr[r] not in aa:
                aa.append(fromArr[r])
                if len(aa) == getNum:
                   break
        return sorted(aa)

    def __fitDatas(self, datas, key=None):
        if key != None:
            newDatas = list(map(lambda x:x[key],datas))  
            return self.__fitDatas(newDatas, None)
        return datas

    def aver(self, datas, key=None, maxNum=20):
        """ 平均值 """
        datas = self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        import numpy as np
        return np.mean(datas[-size:])
    
    def std(self, datas, key=None, maxNum=20):
        """ 标准差 """
        datas = self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        import numpy as np
        return np.std(datas[-size:])
    
    def boll(self, datas, key=None, maxNum=20):
        """ 布林 """
        datas= self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        mid = self.aver(datas[-size:])
        std = self.std(datas[-size:])
        top = mid + std + std
        bot = mid - std - std
        return [top, mid, bot]
    
    def min(self, datas, key=None, maxNum=20):
        """ 最小值 """
        datas= self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        return min(datas[-size:])
        
    def max(self, datas, key=None, maxNum=20):
        """ 最大值 """
        datas= self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        return max(datas[-size:])
    