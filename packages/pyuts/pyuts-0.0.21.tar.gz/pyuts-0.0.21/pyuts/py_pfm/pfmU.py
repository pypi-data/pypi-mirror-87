# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from .modelU import ModelU


class PfmU(PyApiB):
    """
    预测模型相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def create(self, modelFile) -> ModelU:
        return ModelU().init(modelFile)
