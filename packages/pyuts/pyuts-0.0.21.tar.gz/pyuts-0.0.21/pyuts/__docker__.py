# -*- coding: UTF-8 -*-
import sys
from .py_file.fileU import FileU
"""
用于生成docker文件内容。提交时调用：python -m pyuts.__docker__
"""
if len(sys.argv) < 2:
    exit()
fileU = FileU()
dcbase = fileU.read_str('./pyuts/dockers/docker_compose.ymlbase')
services = ''
env_strs = ''
for name in sys.argv[1:]:
    if name in ['mongodb']:
        service = fileU.read_str(f'./pyuts/dockers/service_{name}.ymlbase')
        services = services + service
        env_str = fileU.read_str(f'./pyuts/dockers/service_{name}.envbase')
        env_strs = env_strs + env_str
dcStr = dcbase.format(service=services)
fileU.write_str('./dockers/docker-compose.yml', dcStr)
fileU.write_str('./dockers/.env', env_strs)
