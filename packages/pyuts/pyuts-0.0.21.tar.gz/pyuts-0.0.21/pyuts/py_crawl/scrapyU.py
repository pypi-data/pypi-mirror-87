# -*- coding: UTF-8 -*-
from .scrapySpiderU import ScrapySpiderU
from ..py_mix.threadU import ThreadU
from ..py_api_b import PyApiB
import os
import importlib
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
threadU = ThreadU()


class ScrapyU(PyApiB):
    """
    scrapy相关封装工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.spiders = {}
        self.client = None
        self.process = None
        self._isEnd = False
        
    def runCmd(self, projectName, command, *args, **kwargs):
        import os
        os.environ['SCRAPY_PROJECT'] = projectName
        from ..py_mix.cmdU import CmdU
        cmdU = CmdU()
        cmdLine = f'scrapy {command}'
        for arg in args:
            cmdLine = f'{cmdLine} {arg}'
        cmdU.run(cmdLine,cwd=f'./{projectName}')
        print(f'{projectName} runCmd {cmdLine}')
        
    def runSpider(self, projectName, spiderName, *args, **kwargs):
        import os
        os.environ['SCRAPY_PROJECT'] = projectName
        from ..py_mix.cmdU import CmdU
        cmdU = CmdU()
        cmdLine = f'scrapy crawl {spiderName}'
        for arg in args:
            cmdLine = f'{cmdLine} {arg}'
        cmdU.run(cmdLine,cwd=f'./{projectName}')
        print(f'{projectName} runSpider {cmdLine}')

    def addSettings(self, settings, priority='project'):
        """ 添加设置文件 """
        dont = ['__name__', '__doc__', '__package__', '__loader__',
                '__spec__', '__file__', '__cached__', '__builtins__', 'pyuts', '__env']
        for key in settings.__dict__:
            if key in dont:
                continue
            self.addSetting(key, settings.__dict__[key], priority)
        return self

    def addSetting(self, name, value, priority='project'):
        if value:
            self.__fixSetting(name, value, priority)
            settings.set(name, value, priority)
        return self

    def __fixSetting(self, name, value, priority='project'):
        if name == 'ITEM_PIPELINES':
            for v in value:
                clzName = v.split('.')[-1]
                pipmodule = importlib.import_module(v[:-len(clzName)-1])
                piplineCls = getattr(pipmodule, clzName)
                setattr(piplineCls, 'scrapyU', self)
        elif name == 'SPIDER_MODULES':
            for sp in value:
                spiders = importlib.import_module(sp)
                self.addSpiders(spiders)

    def getDB(self):
        client = getattr(self, 'client', None)
        if client == None:
            mongo_host = settings.get('mongo_host')
            mongo_port = settings.get('mongo_port')
            mongo_user = settings.get('mongo_user')
            mongo_pswd = settings.get('mongo_pswd')
            from ..py_db.mongoDBU import MongoDBU
            client = MongoDBU().init(mongo_host, mongo_port, mongo_user, mongo_pswd)
            setattr(self, 'client', client)
        return client

    def getDBName(self):
        dbName = getattr(self, 'dbName', None)
        if dbName == None:
            dbName = settings.get('mongo_db_name')
            setattr(self, 'dbName', dbName)
        return dbName

    def addSpiders(self, spiders, debugMode=False):
        import importlib
        import os
        cwd = os.path.dirname(os.path.abspath(spiders.__file__))
        files = os.listdir(cwd)
        for i in files:
            if not i.startswith('_') and i.endswith('.py'):
                m = '.' + i[:-3]
                mdl = importlib.import_module(m, spiders.__package__)
                if "__all__" in mdl.__dict__:
                    names = mdl.__dict__["__all__"]
                else:
                    names = [x for x in mdl.__dict__ if not x.startswith("_")]
                need_import_cls = {}
                need_import_cls.update({k: getattr(mdl, k) for k in names})
                for c in need_import_cls:
                    if hasattr(need_import_cls[c], '__mro__'):
                        if ScrapySpiderU != need_import_cls[
                                c] and ScrapySpiderU in need_import_cls[
                                    c].__mro__:
                            self.addSpider(need_import_cls[c], debugMode)
        return self

    def addSpider(self, spider, debugMode=False):
        if spider.enable:
            self.spiders[spider.name] = spider
        return self

    def start(self, scrapyRunClz, args=None, opts=None, isScheduleDo=True):
        import time
        if not self.spiders:
            return
        from scrapy.crawler import CrawlerProcess
        self.process = CrawlerProcess(settings, False)
        scrapyRun = scrapyRunClz()._setProcess(self.process)._addSpiders(self.spiders)._addDB(self.getDB(),self.getDBName())
        scrapyRun.loop_check()
        scrapyRun.run(args, opts)
        scrapyRun.start()

    def _start(self, _spiders):
        if len(_spiders) == 0:
            return
        for spider in _spiders:
            self._startSpider(spider)

    def _startSpider(self, spider, args=None):
        self.process.crawl(spider, args)
