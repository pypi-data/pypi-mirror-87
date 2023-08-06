# -*- coding: UTF-8 -*-


def aliyun():
    from .aliyun import AliYun
    return AliYun.produce()


def baidu():
    from .baidu import Baidu
    return Baidu.produce()
