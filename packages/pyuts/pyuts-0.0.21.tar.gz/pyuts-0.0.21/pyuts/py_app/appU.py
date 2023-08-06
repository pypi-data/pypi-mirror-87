# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
import sys, os
import importlib
from PyQt5.QtWidgets import QApplication, QMainWindow
from quamash import QEventLoop, QThreadExecutor
import asyncio


logiBase = [QMainWindow]

class AppU(PyApiB):
    """
    PC界面相关工具
    # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
    # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
    # pip install -i https://mirrors.aliyun.com/pypi/simple/ quamash
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.wins = {}
        
    
    def compile(self, appModule):
        """ 打包模块下所有ui文件为py文件 """
        cwd = os.path.dirname(os.path.abspath(appModule.__file__))
        files = os.listdir(cwd)
        for i in files:
            if not i.startswith('_') and i.endswith('.ui'):
                print(i)
    
    def init(self, appModule):
        self.app = QApplication(sys.argv)
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        cwd = os.path.dirname(os.path.abspath(appModule.__file__))
        files = os.listdir(cwd)
        for i in files:
            if not i.startswith('_') and os.path.isdir(f"{cwd}/{i}") and os.path.exists(f"{cwd}/{i}/__init__.py"):
                viewName = i
                uipyCls,logipyCls = None,None
                viewModule = importlib.import_module(f".{i}", appModule.__package__)
                vfs = os.listdir(f"{cwd}/{i}")
                for vf in vfs:
                    if len(vf) > 3 and vf[-3:] == ".py":
                        mdl = importlib.import_module(f".{vf[:-3]}", viewModule.__package__)
                        if vf[:3] == "Ui_":
                            # uipy
                            names = [x for x in mdl.__dict__ if x.startswith("Ui_")]
                            uipyCls = getattr(mdl, names[0])
                        elif vf[:1] != "_":
                            # logipy
                            names = [x for x in mdl.__dict__ if not x.startswith("_")]
                            logiClss = []
                            for n in names:
                                nn = getattr(mdl, n) 
                                if hasattr(nn, '__mro__') and any(list(map(lambda x: x in nn.__mro__,logiBase))):
                                    if f"{appModule.__package__}.{i}.{vf[:-3]}" == nn.__module__:
                                        logiClss.append(nn)
                            if logiClss:
                                logipyCls = logiClss[0]
                if uipyCls and logipyCls:
                     self.addWindow(viewName, logipyCls, uipyCls)
        return self
        
    def waitEnd(self):
        """ 等待app用户操作结束 """
        sys.exit(self.app.exec_())
        
    def getApp(self):
        """ 获取QApplication的实例 """
        return self.app
    
    def addWindow(self, windowName, logipyCls, uipyCls):
        self.wins[windowName] = [logipyCls, uipyCls]
    
    def loadWindow(self, windowName):
        logipyCls, uipyCls = self.wins.get(windowName,(None, None))
        if not logipyCls or not uipyCls:
            return None
        win = logipyCls()
        lg = uipyCls()
        lg.setupUi(win)
        return win
    
    def showWindow(self, windowName):
        """ 显示窗口
        @windowName: 如果init(appModule),此字段为子目录的名称
        """
        self.win = self.loadWindow(windowName)
        if self.win:
            self.win.show()
            

        