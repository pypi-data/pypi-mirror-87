from ..py_api_b import PyApiB
import os
import time


# https://developer.baidu.com/vcast
class SpeechU(PyApiB):
    """
    语言转化相关工具，文本转语音
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        from .. import WebU
        webU = WebU.produce('speech')
        self.chrome = webU.setHide(True).setImgEnable(True).chrome()
        
    def __split(self, text, maxByte=1024):
        import re
        if len(text) <= maxByte:
            return text
        wordlist = re.split('！|。|？',text)
        newText = ''
        count = 0
        for word in wordlist:
            count = count + len(word)
            if count > maxByte:
                return newText
            newText = newText + word + '。'
        return ''
        
    def __toVoice(self, chrome, bodyElement, title, text, savePath, index=0):
        newText = self.__split(text, 4900)
        if len(newText)>0:
            if index > 0:
                title = f"{title}_{index}"
                savePath = f"{savePath[:-4]}{index}{savePath[-4:]}"
            tts = bodyElement.find_elements_by_tag_name('textarea')
            tts[0].send_keys(title)
            time.sleep(1)
            tts[1].send_keys(newText)
            time.sleep(1)
            commitBtn = bodyElement.find_element_by_class_name('generate-voice-button')
            chrome.click(commitBtn)
            time.sleep(1)
            address = ''
            while len(address) == 0:
                time.sleep(2)
                addE = bodyElement.find_element_by_class_name('shiting_href')
                if addE and addE.get_attribute('href'):
                    address = addE.get_attribute('href')
            print(address)
            chrome.downloadFile(address, savePath)
        if newText != text:
            self.__toVoice(chrome, bodyElement, title, text[len(newText):], savePath, index+1)
            
        
    def toVoice(self, title, text, savePath=None, spd=1, per=1):
        """
        文本转化为音频\n
        @Args:\n
        text:需要转化的文本\n
        savePath:保存路径\n
        spd:语速，取值0-2，0:慢速，1：正常，2：快速\n
        per:发音人选择, 0为情感女声，1为情感男声，2为非情感女声，3为非情感男声\n
        """
        if savePath == None:
            savePath = 'auido.mp3'
        
        vcast = self.chrome.loadUrl('https://developer.baidu.com/vcast')
        pers = vcast.find_elements_by_class_name('voice-radio-click')
        self.chrome.click(pers[per])
        time.sleep(1)
        spds = vcast.find_elements_by_class_name('speed-box')
        self.chrome.click(spds[spd])
        time.sleep(1)
        self.__toVoice(self.chrome, vcast, title, text, savePath)
    