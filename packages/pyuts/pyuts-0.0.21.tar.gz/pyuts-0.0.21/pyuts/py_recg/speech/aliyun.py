# -*- coding: UTF-8 -*-
# https://nls-portal.console.aliyun.com/applist


class AliYun:
    instances = {}
    
    
    def __init__(self):
        pass

    
    @staticmethod
    def produce(key=None):
        if not key:
            key = "default"
        if key not in AliYun.instances:
            AliYun.instances[key] = AliYun()
        return AliYun.instances[key]
    
    
    
    