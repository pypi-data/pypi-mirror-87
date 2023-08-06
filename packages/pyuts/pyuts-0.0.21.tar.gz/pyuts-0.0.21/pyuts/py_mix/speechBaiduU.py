from ..py_api_b import PyApiB
import os


# https://console.bce.baidu.com/ai/?fromai=1#/ai/speech/app/detail~appId=1444134
class SpeechU(PyApiB):
    """
    语言转化相关工具，文本转语音
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        from aip import AipSpeech
        appId='18321292'
        apiKey='6dXV7j8sWfQYvZRWjOBKqSEw'
        secretKey='lEKw7nK02K7FN21NRSwFYUX1s1YMuPNv'
        self.client = AipSpeech(appId, apiKey, secretKey)
        
    def __split(self, text, maxByte=1024):
        import re
        if len(text.encode()) <= maxByte:
            return text
        wordlist = re.split('！|。|？',text)
        newText = ''
        count = 0
        for word in wordlist:
            count = count + len(word.encode())
            if count > maxByte:
                return newText
            newText = newText + word + '。'
        return ''
        
    def __toVoice(self, text, savePath, option, isAppend=False):
        import time
        newText = self.__split(text, 1020)
        if len(newText) < len(text):
            self.__toVoice(newText, savePath, option, isAppend)
            self.__toVoice(text[len(newText):], savePath, option, True)
        else:
            time.sleep(2)
            result = self.client.synthesis(text, 'zh', 1, option)
            if not isinstance(result, dict):
                with open(savePath, 'ab' if isAppend else 'wb') as f:
                    f.write(result)
                    f.close()
            else:
                print(result)
                time.sleep(2)

        
    def toVoice(self, text, savePath=None, cuid=None, spd=5, pit=5, vol=15, per=1):
        """
        文本转化为音频\n
        @Args:\n
        text:需要转化的文本\n
        savePath:保存路径\n
        cuid:用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内\n
        spd:语速，取值0-9，默认为5中语速\n
        pit:音调，取值0-9，默认为5中语调\n
        vol:音量，取值0-15，默认为5中音量\n
        per:发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女\n
        """
        if savePath == None:
            savePath = 'auido.mp3'
        option = {'spd': spd, 'pit': pit, 'vol':vol, 'per': per}
        if cuid:
            option['cuid'] = cuid
        self.__toVoice(text, savePath, option)
            
    