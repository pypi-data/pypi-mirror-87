from ..py_api_b import PyApiB
from PyQt5.QtWidgets import QMainWindow
import sys


class WindowU(QMainWindow, PyApiB):
    """
    PC界面相关工具
    # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
    # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    # def __init__(self):
    #     super(WindowU, self).__init__()
    
    def show(self):
        super().show()
        # self.destroyed.connect(self.onDestroyed())
    
    def onDestroyed(self):
        print("onDestroyed")
        sys.exit()
    