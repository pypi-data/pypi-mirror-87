# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from adbutils import adb


class AdbU(PyApiB):
    """
    adb相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def devices(self):
        """ 获取所有可用的设备 """
        return adb.devices()

    def device(self, serial=None):
        """ 获取设备,当只有一个设备时，可以不填serial """
        return adb.device()

    def screenshot(self, savePath='screen.jpg', serial=None):
        d = self.device(serial)
        remote_tmp_path = "/data/local/tmp/screenshot.png"
        d.shell(["rm", remote_tmp_path])
        d.shell(["screencap", "-p", remote_tmp_path])
        d.sync.pull(remote_tmp_path, savePath)

    def click(self, x, y, serial=None):
        d = self.device(serial)
        d.click(x, y)
        
    def swipe(self, x1, y1, x2, y2, ss,serial=None):
        """ swipe from(10, 10) to(200, 200) 0.5s """
        d = self.device(serial)
        d.swipe(x1, y1, x2, y2, ss)
        
    def window_size(self, serial=None):
        d = self.device(serial)
        return d.window_size()
    
    def rotation(self, serial=None):
        d = self.device(serial)
        return d.rotation()
    
    def keyHome(self, serial=None):
        self.keyEvent("HOME",serial)
    
    def keyBack(self, serial=None):
        self.keyEvent("BACK",serial)
        
    def keyEvent(self, keyEvent, serial=None):
        d = self.device(serial)
        d.keyevent(keyEvent)
        
    def send_keys(self, keys, serial=None):
        d = self.device(serial)
        d.send_keys(keys)
        
    def is_screen_on(self, serial=None):
        d = self.device(serial)
        d.is_screen_on()
        
    def open_browser(self, url, serial=None):
        d = self.device(serial)
        d.open_browser(url)
        
    def startScreenRecord(self, serial=None):
        """ 开始录屏并返回一个句柄 """
        d = self.device(serial)
        r = d.screenrecord(no_autostart=True)
        r.start()
        return r
        
    def stopScreenRecord(self, startRecordH, savePath='./video.mp4'):
        """ 停止录屏,startRecordH为录屏句柄 """
        startRecordH.stop_and_pull(savePath)
    
