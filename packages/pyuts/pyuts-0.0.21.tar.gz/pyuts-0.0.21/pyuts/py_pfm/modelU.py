# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from ..py_mix.mathU import MathU
from ..py_mix.jsonU import JsonU
from ..py_mix.sortU import SortU
sortU = SortU()
jsonU = JsonU()
mathU = MathU()


class ModelData:
    def __init__(self, modelFile):
        self.modelFile = modelFile
        self.signDatas = {}
        self._trainedDatas = {}
        self.bb_p = None
        
        
    def __getSignData(self, sign='default'):
        if sign not in self.signDatas:
            self.signDatas[sign] = {}
        return self.signDatas[sign]
        
    def __bindPrice(self, date, price, sign='default'):
        signData = self.__getSignData(sign)
        if 'prices' not in signData:
            signData['prices'] = {}
        if date not in signData['prices']:
            signData['prices'][date] = price
            signData['prices'] = sortU.sortByKey(signData['prices'], -1)
        
    def __prices(self, sign='default'):
        signData = self.__getSignData(sign)
        if 'prices' not in signData:
            signData['prices'] = {}
        return list(signData['prices'].values())
    
    def __try(self, prices):
        std = mathU.std(prices[:-2],maxNum=20)
        p = prices[-1]
        if self.bb_p == None:
            aver5 = mathU.aver(prices[:-2],maxNum=5)
            if p < aver5:
                self.bb_p = p
        else:
            if self.bb_p > p + std * 0.25:
                print(f"{self.bb_p}  {p}")
                self.bb_p = None
                return True
        return False
        
    def trained(self, date, price, sign='default'):
        self.__bindPrice(date, price, sign)
        prices = self.__prices(sign)
        if self.__try(prices):
            print(f"{date} buy:{price}")
        
    
    def predict(self, date, sign='default'):
        return 1.00


class ModelU(PyApiB):
    """
    模型相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def init(self, modelFile):
        self.modelData = ModelData(modelFile)
        return self

    def fit(self, date, price, sign='default'):
        if isinstance(price, str):
            price = float(price)
        self.modelData.trained(date, price, sign)

    def predict(self, date, sign='default'):
        return self.modelData.predict(date, sign)
    