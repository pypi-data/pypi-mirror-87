# -*- coding: UTF-8 -*-
import sys
import importlib
from .py_api_b import PyApiB
import os
"""
用于生成__init__.py文件内容。提交时调用：rm -f ./pyuts/__init__.py && python3 -m pyuts.__setup__,如果代码有变化，会重新生成__init__.py
"""

def load_module(handlers):
    cwd = os.path.dirname(os.path.abspath(handlers.__file__))
    files = os.listdir(cwd)
    need_import = {}
    for i in files:
        if not i.startswith('_') and i.endswith('.py'):
            m = '.' + i[:-3]
            mdl = importlib.import_module(m, handlers.__package__)
            if "__all__" in mdl.__dict__:
                names = mdl.__dict__["__all__"]
            else:
                names = [x for x in mdl.__dict__ if not x.startswith("_")]
            need_import_cls = {}
            need_import_cls.update({k: getattr(mdl, k) for k in names})
            for c in need_import_cls:
                if hasattr(need_import_cls[c], '__mro__'):
                    if PyApiB != need_import_cls[
                            c] and PyApiB in need_import_cls[c].__mro__:
                        need_import[
                            need_import_cls[c].__module__] = need_import_cls[c]
    return need_import


def firstLower(str):
    return f"{str[:1].lower()}{str[1:]}"


def appendDoc(str, doc):
    str = f"{str}        '''\n"
    if doc == None:
        doc = ''
    docs = doc.split('\n')
    for d in docs:
        str = f"{str}        {d.lstrip()}\n"
    str = f"{str}        '''\n"
    return str


initFile = "# -*- coding: UTF-8 -*-\n"
pwd = os.path.dirname(os.path.abspath(__file__))
fs = os.listdir(pwd)
all_class = {}
for i in fs:
    if os.path.isdir(f"{pwd}/{i}") and i.startswith('py_'):
        m = '.' + i
        mdl = importlib.import_module(m, __package__)
        all_class.update(load_module(mdl))
for mcls_name in all_class:
    cls_name = all_class[mcls_name].__name__
    moduleName = mcls_name
    # print(moduleName)
    initFile = f"{initFile}try:\n"
    initFile = f"{initFile}    from {moduleName} import {cls_name}\n\n"
    initFile = f"{initFile}    def {firstLower(cls_name)}(key=None) -> {cls_name}:\n"
    initFile = appendDoc(initFile, all_class[mcls_name].__doc__)
    initFile = f"{initFile}        return {cls_name}.produce(key)\n"
    initFile = f"{initFile}except ImportError as e:\n"
    initFile = f"{initFile}    print(e)\n\n"

from pyuts.py_file.fileU import FileU
# print(initFile)
FileU().write_str("pyuts/__init__.py", initFile)