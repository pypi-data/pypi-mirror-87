# -*- coding: UTF-8 -*-
import time, datetime
from ..py_api_b import PyApiB


class DatetimeU(PyApiB):
    """
    时间日期相关工具 \n
    
    时间格式类型: \n
        %y 两位数的年份表示（00-99）\n
        %Y 四位数的年份表示（000-9999）\n
        %m 月份（01-12）\n
        %d 月内中的一天（0-31）\n
        %H 24小时制小时数（0-23）\n
        %I 12小时制小时数（01-12）\n
        %M 分钟数（00=59）\n
        %S 秒（00-59）\n
        %a 本地简化星期名称\n
        %A 本地完整星期名称\n
        %b 本地简化的月份名称\n
        %B 本地完整的月份名称\n
        %c 本地相应的日期表示和时间表示\n
        %j 年内的一天（001-366）\n
        %p 本地A.M.或P.M.的等价符\n
        %U 一年中的星期数（00-53）星期天为星期的开始\n
        %w 星期（0-6），星期天为星期的开始\n
        %W 一年中的星期数（00-53）星期一为星期的开始\n
        %x 本地相应的日期表示\n
        %X 本地相应的时间表示\n
        %Z 当前时区的名称\n
        %% %号本身\n
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def changeFormate(self, dataStr, fromFormate, toFormate):
        '''
        时间日期字符串格式转化\n
        @Args: \n
        dataStr:str 需要转化的日期字符串，例如：2020-01-01 08:00:00 \n
        fromFormate:str 原字符串格式，例如：%Y-%m-%d %H:%M:%S \n
        toFormate:str 转化为字符串格式，例如：%Y年%m月%d日 %H:%M:%S \n
        '''
        sec = self.seconds(dataStr, fromFormate)
        return self.dataStr(toFormate, sec)

    def seconds(self, dataStr, formate=None):
        if not formate:
            formate = '%Y-%m-%d %H:%M:%S'
        return time.mktime(
            datetime.datetime.strptime(dataStr, formate).timetuple())

    def dataStr(self, formate=None, seconds=None, addDays=0, addHours=0, addMinutes=0, addSeconds=0):
        '''
        时间日期字符串格式转化\n
        @Args: \n
        formate:str 格式，例如：%Y-%m-%d %H:%M:%S \n
        seconds:float 时间秒数，例如：time.time() \n
        '''
        if not formate:
            formate = '%Y-%m-%d %H:%M:%S'
        if not seconds:
            seconds = time.time()
        if addDays != 0:
            seconds = seconds + addDays * 86400
        if addHours != 0:
            seconds = seconds + addHours * 3600
        if addMinutes != 0:
            seconds = seconds + addMinutes * 60
        if addSeconds != 0:
            seconds = seconds + addSeconds
        return time.strftime(formate, time.localtime(seconds))
      
    def isNowFormat(self, timeFormat='%Y-%m-%d %H:%M:%S'):
        return self.now() == self.now(timeFormat)
    
    def isNow(self, doTime='Y|m|d|H|M|S|w'):
        if '|' not in doTime:
            return self.isNowFormat(doTime)
        else:
            dots = doTime.split('|')
            tfs = '%Y|%m|%d|%H|%M|%S|%w'.split('|')
            for i in range(0,len(dots)):
                dot = dots[i]
                if dot == None or not isinstance(dot,str) or len(dot)<=0:
                    continue
                ds = []
                if dot.isnumeric():
                    ds = [dot]
                elif len(dot)>2 and '[' in dot[:1] and ']' in dot[-1:]:
                    ds = dot[1:-1].split(',')
                else:
                    continue
                pV = int(self.dataStr(tfs[i]))
                if not any(map(lambda x: int(x)==pV,ds)):
                    return False
            return True
          
              

    def nowStr(self, timeFormat='%Y-%m-%d %H:%M:%S')->str:
        return self.dataStr(timeFormat)

    def now(self)->datetime.datetime:
        return datetime.datetime.now()