# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from .algorithmU import AlgorithmU
import threading
import multiprocessing
import random
import time
import inspect
import ctypes


class AsyncU(PyApiB):
    """
    异步相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def asyncRun(self, target, args=None, asyncKey=None, isProcess=False):
        if asyncKey == None:
            asyncKey = AlgorithmU.produce("cmdU").md5(str(random.randint(0,9999999999999)))
        if isProcess:
            multiprocessing.Process(target=target,args=(() if not args else args),name=asyncKey).start()
        else:
            threading.Thread(target=target, args=(() if not args else args), name=asyncKey).start()
        return asyncKey
    
    def getRunningProcessKeys(self) -> list:
        keys = []
        children = multiprocessing.active_children()
        for child in children:
            keys.append(child.name)
        return keys
    
    def getRunningThreadKeys(self) -> list:
        keys = []
        children = threading.enumerate()
        for child in children:
            keys.append(child.name)
        return keys
    
    def getRunningKeys(self) -> list:
        keys = []
        keys += self.getRunningProcessKeys()
        keys += self.getRunningThreadKeys()
        return keys
    
    def stopAsyncProcess(self, asyncKey):
        children = multiprocessing.active_children()
        for child in children:
            if isinstance(asyncKey,str) and child.name == asyncKey or isinstance(asyncKey,list) and child.name in asyncKey:
                try:
                    child.terminate()
                except Exception as identifier:
                    pass
                
                
    def stopAsyncThread(self, asyncKey):
        children = threading.enumerate()
        for child in children:
            if isinstance(asyncKey,str) and child.name == asyncKey or isinstance(asyncKey,list) and child.name in asyncKey:
                try:
                    self._async_raise(child.ident, SystemExit)
                except Exception as identifier:
                    pass
        
    def stopAsync(self, asyncKey):
        """ 停掉异步，asyncKey:[str|list]"""
        self.stopAsyncProcess(asyncKey)
        self.stopAsyncThread(asyncKey)
    
    def stopAllAsyncProcess(self):
        for child in multiprocessing.active_children():
            try:
                child.terminate()
            except Exception as identifier:
                pass
            
    def stopAllAsyncThread(self):
        children = threading.enumerate()
        for child in children:
            try:
                self._async_raise(child.ident, SystemExit)
            except Exception as identifier:
                pass
            
    def stopAllAsync(self):
        self.stopAllAsyncProcess()
        self.stopAllAsyncThread()
    
    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")