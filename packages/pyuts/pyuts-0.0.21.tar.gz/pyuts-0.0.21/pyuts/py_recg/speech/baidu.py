# -*- coding: UTF-8 -*-


class Baidu:
    instances = {}
    
    
    def __init__(self):
        pass

    
    @staticmethod
    def produce(key=None):
        if not key:
            key = "default"
        if key not in Baidu.instances:
            Baidu.instances[key] = Baidu()
        return Baidu.instances[key]
    