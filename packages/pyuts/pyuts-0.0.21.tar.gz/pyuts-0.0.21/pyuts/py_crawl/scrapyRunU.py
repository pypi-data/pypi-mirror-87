from ..py_api_b import PyApiB
from ..py_mix.datetimeU import DatetimeU
from ..py_mix.threadU import ThreadU
datatimeU = DatetimeU()
threadU = ThreadU()


class ScrapyRunU(PyApiB):
    """
    ScrapyRun相关封装工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.isEnd = False
        self.spiders = {}

    def run(self, args, opts):
        """ 执行逻辑 """
        pass

    def runSpider(self, spiderName, *args):
        """ 启动爬虫,结束后监听可以.addCallback(callBack) """
        spider = self.getSpider(spiderName)
        return self.process.crawl(spider, *args)

    def _setProcess(self, process):
        self.process = process
        return self

    def start(self):
        self.process.start(False)
        self._end()

    def _addSpiders(self, spiders):
        for sn in spiders:
            self.spiders[sn] = spiders[sn]
        return self
    
    def _addDB(self, db, dbName):
        self.db = db
        self.dbName = dbName
        return self

    def isNow(self, timeFormat='%Y-%m-%d %H:%M:%S'):
        return self.now() == self.now(timeFormat)

    def now(self, timeFormat='%Y-%m-%d %H:%M:%S'):
        return datatimeU.dataStr(timeFormat)

    def every_seconds(self):
        pass

    def _end(self):
        self.isEnd = True

    def loop_check(self):
        from ..py_mix.threadU import ThreadU
        ThreadU().asyncDo(self._loop_check).start()

    def _loop_check(self):
        import time
        self.oldTime = self.now()
        while not self.isEnd:
            time.sleep(0.3)
            n = self.now()
            if self.oldTime != n:
                self.oldTime = n
                threadU.asyncDo(self.every_seconds).start()

    def getSpiders(self):
        return self.spiders

    def getSpider(self, spiderName):
        return self.spiders.get(spiderName)

    def toJsonStr(self, data):
        import pyuts
        return pyuts.jsonU().toString(data, indent=None)
    
    def toJson(self, jsonStr):
        import pyuts
        return pyuts.jsonU().fromString(jsonStr)