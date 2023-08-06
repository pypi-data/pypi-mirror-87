# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class VideoU(PyApiB):
    """
    视频文件格式相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        pass

    def formatTo(self, videoPath, toVideoPath, rmEnd=False):
        import ffmpy
        ff = ffmpy.FFmpeg(inputs={videoPath: None},
                          outputs={toVideoPath: None})
        ff.run()
        if rmEnd:
            import os
            os.remove(videoPath)
