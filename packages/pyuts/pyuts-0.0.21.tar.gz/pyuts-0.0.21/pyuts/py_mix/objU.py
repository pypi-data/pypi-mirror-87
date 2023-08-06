# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class ObjU(PyApiB):
    """
    obj相关操作工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    # def find(self, item, filed):
    #     """ 查找数据项 """
    #     if item == None:
    #         return None
    #     if '.' in filed:
    #         fs = filed.split('.')
    #         newItem = self.find(item, fs[0])
    #         return self.find(newItem, filed[len(fs[0]) + 1:])
    #     else:
    #         if filed.isdigit() or (filed[:1] == '-' and filed[1:].isdigit()):
    #             try:
    #                 return item[int(filed)]
    #             except BaseException as e:
    #                 return None
    #         else:
    #             return item.get(filed)
    
    def find(self, item, filed):
        """ 查找数据项 """
        if "." in filed:
            nextfileds = filed.split(".")
            nextItem = self.find(item,nextfileds[0])
            return self.find(nextItem, filed[len(nextfileds[0])+1:])
        elif filed.isnumeric():
            return item[int(filed)] if item != None and (isinstance(item,list) or isinstance(item,tuple)) and int(filed) < len(item) else None
        elif len(filed)>1 and filed[:1] == '-' and filed[1:].isnumeric():
            return item[len(item)-(int(filed)%len(item))] if item != None and (isinstance(item,list) or isinstance(item,tuple))else None
        elif filed == "*" or filed == "**":
            return item
        else:
            if item == None:
                return None
            elif isinstance(item,list) or isinstance(item,tuple):
                return list(map(lambda x: None if x == None else self.find(x,filed), item))
            else:
                return None if item == None or not isinstance(item,dict) else item.get(filed)
            
    def update(self, item, filed, value):
        """ 更新数据项 """
        if item == None:
            return
        if '.' in filed:
            nextfileds = filed.split(".")
            nextItem = self.find(item,filed[:len(nextfileds[0])])
            if nextItem == None:
                if nextfileds[-1].isnumeric() or (len(nextfileds[-1])>1 and nextfileds[-1][:1] == '-' and nextfileds[-1][1:].isnumeric()) or nextfileds[-1] == "*":
                    nextItem = []
                else:
                    nextItem = {}
                self.update(item, filed[:len(nextfileds[0])], nextItem)
            self.update(nextItem,nextfileds[-1],value)
        elif filed.isnumeric():
            index = int(filed)
            if index < len(item):
                item[index] = value
            else:
                for i in range(0,(len(item)-index)):
                    item.append(None)
                item.append(value)
        elif len(filed)>1 and filed[:1] == '-' and filed[1:].isnumeric():
            item[int(filed)] = value
        elif filed == "*":
            for i in range(0,len(item)):
                item[i] = value
        elif filed == "**":
            for key in item:
                item[key] = value
        else:
            item[filed] = value
        
    # def update(self, item, filed, value):
    #     """ 更新数据项 """
    #     if item == None:
    #         return
    #     if '.' in filed:
    #         fs = filed.split('.')
    #         newItem = self.find(item, fs[0])
    #         if newItem == None:
    #             newV = {}
    #             if fs[1].isdigit():
    #                 newV = [None] * (int(fs[1])+1)
    #             if fs[1][:1] == '-' and fs[1][1:].isdigit():
    #                 newV = [None] * (int(fs[1][1:]))
    #             self.update(item, fs[0], newV)
    #             newItem = newV
    #         self.update(newItem, filed[len(fs[0]) + 1:], value)
    #     else:
    #         if filed.isdigit() or (filed[:1] == '-' and filed[1:].isdigit()):
    #             ss = int(filed)
    #             if ss < 0:
    #                 ss = -ss - 1
    #             if len(item) <= ss:
    #                 apNum = ss - len(item) + 1
    #                 for ii in range(0, apNum):
    #                     item.append(None)
    #             item[int(filed)] = value
    #         else:
    #             item[filed] = value

    def merge(self, fromItem, toItem, fromFiled, toFiled, formatFun=None):
        """ 复制数据项 """
        value = self.find(fromItem, fromFiled)
        if value == None:
            return
        if formatFun:
            value = formatFun(value)
        self.update(toItem, toFiled, value)

    def merge2(self, canCopy, fromItem, toItem, fromFiled, toFiled, formatFun=None):
        """ 复制数据项，与copy方法功能一样，唯一区别第一位加入开关参数 """
        if not canCopy:
            return
        self.merge(fromItem, toItem, fromFiled, toFiled, formatFun)

    def copy(self, data):
        import copy
        return copy.copy(data)
    
    def deepcopy(self, data):
        import copy
        return copy.deepcopy(data)
