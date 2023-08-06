# -*- coding: UTF-8 -*-


class PyApiB:
    """
    所有需要对外提供的类，都需要承继此类
    """
    instances = {}

    @staticmethod
    def _produce(key, cls):
        if not key:
            key = f"{cls.__name__}_default"
        else:
            key = f"{cls.__name__}{key}"
        if key not in PyApiB.instances:
            PyApiB.instances[key] = cls()
        return PyApiB.instances[key]

    def __init__(self):
        pass