# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class RecordU(PyApiB):
    """
    ???
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.isRecoding = False

    def m3u8(self,
             url,
             savePath,
             auto_increase=True,
             startTime=None,
             endTime=None):
        from pyuts.py_mix.datetimeU import DatetimeU
        nowTime = DatetimeU.produce('recordU').dataStr('%H:%M')
        if nowTime < startTime or nowTime > endTime:
            return
        if self.isRecoding:
            return
        self.isRecoding = True
        savePath = savePath.format(
            time=DatetimeU.produce('recordU').dataStr('%Y-%m-%d_%H_%M_%S'))
        import requests
        import os
        saveTSPath = f"{savePath}_tmp"
        if os.path.exists(saveTSPath):
            lfs = os.listdir(saveTSPath)
            for lf in lfs:
                os.remove(f"{saveTSPath}/{lf}")
        else:
            os.mkdir(saveTSPath)
        try:
            all_content = requests.get(url, stream=True).text
            if "#EXTM3U" not in all_content:
                return
            if "EXT-X-STREAM-INF" not in all_content:
                return
            contents = all_content.split('\n')
            for content in contents:
                if '.m3u8' in content:
                    self._save_m3u8_ts(content, saveTSPath, auto_increase,
                                       endTime)
        except BaseException as e:
            pass
        finally:
            self.merge_tslist(saveTSPath, savePath + '.ts', True)
            from pyuts.py_file.videoU import VideoU
            VideoU.produce('recordU').formatTo(savePath + '.ts', savePath,
                                               True)
            self.isRecoding = False

    def merge_tslist(self, tslist, savePath, rmTslist=True):
        box = self._get_sorted_ts(tslist)
        with open(savePath, 'ab') as f:
            for ts_file in box:
                with open(f"{tslist}/{ts_file}", 'rb') as ts:
                    f.write(ts.read())
        if rmTslist:
            from pyuts.py_file.fileU import FileU
            fileU = FileU.produce('recordU')
            fileU.remove(tslist)

    def _get_sorted_ts(self, user_path):
        from glob import glob
        import os
        ts_list = glob(os.path.join(user_path, '*.ts'))
        boxer = []
        for ts in ts_list:
            if os.path.exists(ts):
                file = os.path.splitext(os.path.basename(ts))
                boxer.append(f"{file[0]}{file[1]}")
        boxer.sort()
        return boxer

    def _save_m3u8_ts(self, url, savePath, auto_increase=False, endTime=None):
        import requests
        import os
        baseUrl = url.rsplit("/", 1)[0]
        tsUrls = []
        all_content = requests.get(url, stream=True).text
        contents = all_content.split('\n')
        isEXTINF = False
        for content in contents:
            if isEXTINF:
                isEXTINF = False
                # tsFilePath = f"{savePath}/{content.rsplit('/', 1)[1].rsplit('?', 1)[0]}"
                # if os.path.exists(tsFilePath):
                #     continue
                tsUrls.append({'url': f"{baseUrl}/{content}"})
                # asyncio.run(self._download_file(f"{baseUrl}/{content}", tsFilePath))
            if 'EXTINF' in content:
                isEXTINF = True
        if not auto_increase:
            for tsUrl in tsUrls:
                self._download_file(
                    tsUrl['url'],
                    f"{savePath}/{tsUrl['url'].rsplit('/', 1)[1].rsplit('?', 1)[0]}"
                )
        elif len(tsUrls) > 0:
            tsUrl = tsUrls[0]['url']
            needIncrease = False
            from pyuts.py_mix.datetimeU import DatetimeU
            while True:
                nowTime = DatetimeU.produce('recordU').dataStr('%H:%M')
                if nowTime > endTime:
                    break
                if needIncrease:
                    tsId = tsUrl.rsplit('/', 1)[1].rsplit('.ts', 1)[0]
                    newTsId = int(tsId) + 1
                    newTsUrl = f"{tsUrl.rsplit('/', 1)[0]}/{newTsId}.ts{tsUrl.rsplit('/', 1)[1].rsplit('.ts', 1)[1]}"
                    tsUrl = newTsUrl
                needIncrease = self._download_file(
                    tsUrl,
                    f"{savePath}/{tsUrl.rsplit('/', 1)[1].rsplit('?', 1)[0]}")

    def _download_file(self, url, savePath):
        import os
        import requests
        import time
        if os.path.exists(savePath):
            return
        r = requests.get(url, stream=True)
        if r.status_code == 404:
            return False
        f = open(savePath, "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        return True
