# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class ThreadU(PyApiB):
    """
    线程相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    @staticmethod
    def asyncDo(fn, *args, **kwargs):
        threadU = ThreadU()
        threadU.__bind(fn, *args, **kwargs)
        return threadU

    def __bind(self, fn, *args, **kwargs):
        import threading
        if args or kwargs:
            self.thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        else:
            self.thread = threading.Thread(target=fn)

    def start(self):
        self.thread.start()

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        import time
        import inspect
        import ctypes
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

    def stop(self):
        self._async_raise(self.thread.ident, SystemExit)

    