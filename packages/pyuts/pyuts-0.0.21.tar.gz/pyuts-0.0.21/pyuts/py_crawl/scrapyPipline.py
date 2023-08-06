# -*- coding: UTF-8 -*-
import pyuts
from pyuts import MongoDBU


class ScrapyprojectnamePipeline(object):
    """
    scrapyPipline相关封装工具
    """
    
    def __init__(self):
        host = pyuts.envU().get('mongo_host')
        port = int(pyuts.envU().get('mongo_port','1'))
        user = pyuts.envU().get('mongo_user')
        pswd = pyuts.envU().get('mongo_pswd')
        # 创建MONGODB数据库链接
        self.client = MongoDBU().init(host, port, user, pswd)
        self.saveSignList = {}

    def process_item(self, item, spider):
        _saveSign = getattr(spider,'saveSign')
        if item.__class__.__name__ == 'ScrapySaveItem':
            if _saveSign == item['saveSign']:
                _saveType = item['type']
                if _saveType == 'begin':
                    self.saveSignList[_saveSign] = []
                elif _saveType == 'commit':
                    _saves = self.saveSignList[_saveSign]
                    del self.saveSignList[_saveSign]
                    if len(_saves) > 0:
                        db_name = _saves[0]['db_name']
                        tb_name = _saves[0]['tb_name']
                        _saveDatas = list(map(lambda x:x['data'],_saves))
                        # print(_saveDatas)
                        import time
                        tt = time.time()
                        _optionType = item['optionType']
                        if _optionType == 'insert':
                            self.client.insertManyIfNotExist(db_name,tb_name,_saveDatas)
                        elif _optionType == 'upsert':
                            self.client.upsertManyById(db_name,tb_name,_saveDatas)
                        elif len(_optionType) >= 8 and _optionType[:8] == 'jsonfile':
                            ops = _optionType.split('@')
                            savePath = f'../jsonfiles/{db_name}/{tb_name}/{_saveSign}.json'
                            if len(ops) > 1:
                                savePath = ops[1]
                            pyuts.fileU().write_json(savePath,_saveDatas)
                        print(f'UserTime:{time.time()-tt}')
            return item
        data = dict(item)
        tb_name = getattr(item,'saveTableName')
        if tb_name == None:
            tb_name = item.__class__.__name__
        db_name = getattr(item,'saveDbName')
        if db_name == None:
            from scrapy.utils.project import get_project_settings
            settings = get_project_settings()
            db_name = settings["BOT_NAME"]
        if _saveSign in self.saveSignList:
            self.saveSignList[_saveSign].append({'data':data,'db_name':db_name,'tb_name':tb_name})
        else:
            self.client.upsert_one(db_name, tb_name, {'id': data['id']}, data)
        return item

    def open_spider(self, spider):
        spider.myPipline = self
        spider.state = 'running'

    def close_spider(self, spider):
        spider.myPipline = None
        spider.state = 'close'