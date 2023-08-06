# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from .algorithmU import AlgorithmU
import sys
import multiprocessing


class CmdU(PyApiB):
    """
    命令行相关工具
    """

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def run(self, cmdline, cwd=None):
        import subprocess
        subprocess.Popen(cmdline, shell=True, cwd=cwd).wait()

    def getArgv(self, index, defV=None):
        if len(sys.argv) > index:
            return sys.argv[index]
        else:
            return defV