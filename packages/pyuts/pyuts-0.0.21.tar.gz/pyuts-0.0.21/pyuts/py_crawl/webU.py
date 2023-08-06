# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
import os
from .chromeU import ChromeU
from .scrapyU import ScrapyU


class WebU(PyApiB):
    """
    网页浏览器模拟工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.driver = None
        self.windowSize = [1920, 1080]
        self.imagesEnable = False
        self.isHide = True

    def setHide(self, isHide=True):
        self.isHide = isHide
        return self

    def setImgEnable(self, imagesEnable=False):
        self.imagesEnable = imagesEnable
        return self

    def setSize(self, width=1920, height=1080):
        self.windowSize = [width, height]
        return self

    def chrome(self) -> ChromeU:
        return ChromeU().setConfig(self.windowSize, self.imagesEnable,
                                   self.isHide)

    def scrapy(self) -> ScrapyU:
        return ScrapyU()
