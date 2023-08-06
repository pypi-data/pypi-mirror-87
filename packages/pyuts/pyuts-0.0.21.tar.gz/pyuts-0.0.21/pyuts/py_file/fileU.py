# -*- coding: UTF-8 -*-
import time
import shutil
import random
import os
import json
from ..py_api_b import PyApiB


class FileU(PyApiB):
    """
    文件相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        pass
    
    def fixPath(self, path):
        if path and path[:1] == '~':
            return f'{os.path.expanduser("~")}{path[1:]}'
        return path

    # 新建文件夹
    # @param path 路径

    def mkdir(self, path):
        if not self.is_exists(path):
            os.makedirs(path, exist_ok=True)

    # 准备基目录文件夹
    # @param file_path 路径

    def prepare_basedir(self, file_path):
        to_base_path = file_path[:-len(self.path_to_filename(file_path))]
        self.mkdir(to_base_path)

    # 是否存在
    # @param path 路径

    def is_exists(self, path):
        return os.path.exists(path)

    # 文件名加上随时数或时间
    # @param file_name
    # @param is_add_time
    # @param is_add_random
    def fix_file_name(self, file_name, is_add_time=False, is_add_random=False):
        if is_add_random or is_add_time:
            end = file_name.split(".")[-1]
            fn = file_name[:-(len(end) + 1)]
            mid = ""
            if is_add_time:
                t = int(time.time() * 100)
                mid = f"{mid}_{t}"
            if is_add_random:
                rd = int(random.random() * 10000)
                mid = f"{mid}_{rd}"
            file_name = f"{fn}{mid}.{end}"
        return file_name

    # 获取路径或文件名的后缀，例如： xxx.png,返回png
    # @param path_or_file_name 路径

    def suffix(self, path_or_file_name):
        return path_or_file_name.split(".")[-1]

    # 获取文件路径对应的文件名，即 "/" 后面的字符串
    # @param path 路径

    def path_to_filename(self, path):
        return path.split("/")[-1]

    # json数据写入文件中
    # @param path 路径
    # @param json_data json数据
    def write_json(self, path, json_data, model="w"):
        path = self.fixPath(path)
        self.prepare_basedir(path)
        with open(path, model) as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

    def write_str(self, path, str_data, model="w", encoding="utf-8"):
        path = self.fixPath(path)
        self.prepare_basedir(path)
        with open(path, model, encoding=encoding) as f:
            f.write(str_data)

    def read_str(self, path, model='r', encoding="utf-8"):
        path = self.fixPath(path)
        if not self.is_exists(path):
            return ''
        with open(path, 'r') as load_f:
            return load_f.read()

    # 文件中加载json数据
    # @param path 路径

    def read_json(self, path):
        path = self.fixPath(path)
        if not self.is_exists(path):
            return {}
        with open(path, 'r') as load_f:
            json_data = json.load(load_f)
        return json_data

    # 删除
    # @param path 路径

    def remove(self, path):
        path = self.fixPath(path)
        if not self.is_exists(path):
            return
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    # 复制
    # @param path 源路径
    # @param to_path 路径
    # @param symlinks 是否只是链接

    def copy(self, path, to_path, symlinks=False):
        path = self.fixPath(path)
        to_path = self.fixPath(to_path)
        if not self.is_exists(path):
            return
        if os.path.isdir(path):
            self.prepare_basedir(to_path)
            shutil.copyfile(path, to_path, follow_symlinks=symlinks)
        else:
            shutil.copytree(path, to_path, symlinks=symlinks)
            
            
    def move(self, path, to_path):
        path = self.fixPath(path)
        to_path = self.fixPath(to_path)
        if not self.is_exists(path):
            return
        shutil.move(path, to_path)


    def read_env(self, env_path='./dockers/.env'):
        envStr = self.read_str(env_path)
        envs = envStr.splitlines()
        res = {}
        for env in envs:
            if '=' in env:
                vvs = env.split('=')
                res[vvs[0].strip()] = vvs[1].strip()
        return res