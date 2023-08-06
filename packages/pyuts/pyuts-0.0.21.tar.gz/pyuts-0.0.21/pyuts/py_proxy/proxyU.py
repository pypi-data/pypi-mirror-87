# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from ..py_crawl.httpU import HttpU
from .proxyCrawlerU import ProxyCrawlerU
from ..py_mix.ctrlCU import CtrlCU
from ..py_mix.asyncU import AsyncU
from ..py_file.fileU import FileU
from ..py_db.redisDBU import RedisDBU
from ..py_db.mongoDBU import MongoDBU
import time
CHECK_BAIDU = "https://www.baidu.com"
DBName = "proxy"
CHECKED_TBNAME = "checked"

class ProxyU(PyApiB):
    """
    代理相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        self.redis = RedisDBU()
        self.mongoDB = MongoDBU()
        self.redisPreKey = "proxyU"
        self.ctrlCU = None
    
    def addProxyCrawler(self,crawlerName:str, crawler:ProxyCrawlerU):
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        proxy_crawlers[crawlerName] = crawler
        setattr(self,'proxy_crawlers',proxy_crawlers)
        
    def getProxyMeta(self):
        """ 获取一个代理 """
        type = "checked"
        key = f"{self.redisPreKey}:{type}"
        meta = self.redis.srandmember(key)
        if meta and len(meta)>0:
            return meta[0]
        return None
    
    def proxyToMeta(self, proxy):
        """ dict的代理转meta格式 """
        if proxy.get("user") and proxy.get("host") and proxy.get("port"):
            meta = f"http://{proxy.get('user')}:{proxy.get('pswd')}@{proxy.get('host')}:{proxy.get('port')}"
        elif proxy.get("host") and proxy.get("port"):
            meta = f"http://{proxy.get('host')}:{proxy.get('port')}"
        return meta
    
    def metaToProxy(self, meta):
        """ meta格式转dict代理 """
        if "//" in meta:
            pInfo = meta.split("//")[1]
            user,pswd = "",""
            if "@" in pInfo:
                up, pInfo = pInfo.split("@")
                if ":" in up:
                    user,pswd = up.split(":")
                else:
                    user = up
            if ":" in pInfo:
                host, port = pInfo.split(":")
                return {"host":host,"port":port,"user":user,"pswd":pswd}
        return {}
        
    def __readLocalMetas(self, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        return self.redis.get_str_list(key)
        
    def __saveLocalMetas(self, metas, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        self.redis.set_str_list(key, metas[-maxLen:])
        
    def __pushLocalMetas(self, metas, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        self.redis.rpush_str(key,metas,maxLen)
        
    def __isMetaSame(self, meta1, meta2):
        m1,m2 = meta1,meta2
        if isinstance(meta1,dict):
            m1 = meta1.get('meta')
        if isinstance(meta2,dict):
            m2 = meta2.get('meta')
        return m1 == m2
    
    def __isInMetas(self, meta1, metas):
        return any(list(map(lambda x: self.__isMetaSame(meta1, x),metas)))
        
    def __upsertCheckedMeta(self, meta, maxLen=1000):
        """ 更新有效的代理入mongoDB,并同步一份至redis """
        key = f"{self.redisPreKey}:checked"
        self.mongoDB.upsert_one(DBName,CHECKED_TBNAME,{"meta":meta.get("meta")},meta)
        self.redis.sadd(key,meta.get("meta"))
        
    def __removeCheckedFromRedis(self, *metaStrs):
        """ 从redis的checked中删除一个代理 """
        key = f"{self.redisPreKey}:checked"
        self.redis.srem(key,*metaStrs)
        
    def __filtHasChecked(self, proxys):
        key = f"{self.redisPreKey}:checked"
        ms = self.redis.srandmember(key)
        newProxys = []
        for proxy in proxys:
            meta = f"http://{proxy.get('user')}:{proxy.get('pswd')}@{proxy.get('host')}:{proxy.get('port')}"
            if meta not in ms:
                newProxys.append(proxy)
        return newProxys
        
    def __popLocalMeta(self, type="source"):
        key = f"{self.redisPreKey}:{type}"
        return self.redis.rpop_str(key)
        
    def __saveToWaitCheck(self, proxys):
        # 将没有在等待队列中的元素搬到等待队列
        waitCheckMetas = self.__readLocalMetas("waitCheck")
        needPushs = []
        for proxy in proxys:
            meta = ""
            if isinstance(proxy,str):
                meta = proxy
            else:
                meta = self.proxyToMeta(proxy)
            if not self.__isInMetas(meta, waitCheckMetas):
                needPushs.append(meta)
        if needPushs:
            print(f"tranProxys:{len(needPushs)}")
            self.__pushLocalMetas(needPushs, "waitCheck")
            
    def __popWaitCheck(self):
        return self.__popLocalMeta("waitCheck")
        
    def crawlProxyAndSave(self, crawlerName):
        """ 采集名称为crawlerName的爬虫，并保存所获得的代理 """
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        crawler = proxy_crawlers.get(crawlerName)
        if crawler:
            proxys = crawler().getProxys()
            print(f"crawlProxyAndSave:{len(proxys)}")
            proxys = self.__filtHasChecked(proxys)
            self.__saveToWaitCheck(proxys)
        
    def crawlProxysAndSave(self):
        """ 采集所有爬虫，并保存所获得的代理 """
        asyncU:AsyncU = AsyncU.produce("ProxyU")
        runKeys = asyncU.getRunningKeys()
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        for k in proxy_crawlers:
            if k not in runKeys:
                asyncU.asyncRun(target=self.crawlProxyAndSave,args=(k,), asyncKey=k, isProcess=False)
    
    def loopCrawl(self, crawlDuring):
        """ 循环采集所有爬虫，并保存所获得的代理 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        while not ctrlCU.isExit():
            wkey = ctrlCU.wantSleep()
            self.crawlProxysAndSave()
            ctrlCU.toSleep(crawlDuring,wkey)
        
    def checkOneProxy(self, proxyMeta=None, timeout=60, checkUrl=CHECK_BAIDU):
        """ 检测一次代理的可用性，并保存入checked。proxyMeta如果为空，则从等待队列中pop一个代理 """
        if proxyMeta == None:
            proxyMeta = self.__popWaitCheck()
        # print(f"check {proxyMeta}")
        if proxyMeta:
            res = HttpU().get(checkUrl,proxyMeta=proxyMeta,timeout=timeout)
            if str(res.get('code')) == "200":
                meta = {"meta":proxyMeta,"ut":time.time()}
                self.__upsertCheckedMeta(meta)
            else:
                print(f"check {proxyMeta} NoPass!!")
            return True
        else:
            return False
                
    def loopCheckOneProxy(self, timeout=20, checkUrl=CHECK_BAIDU):
        """ 一个线程循环检测等待队列中代理的可用性，并保存入checked。 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        while not ctrlCU.isExit():
            res = False
            try:
                res = self.checkOneProxy(timeout=timeout,checkUrl=checkUrl)
            except Exception as e:
                print("checkOneProxy Failed!!!")
            if not res:
                time.sleep(5)
            else:
                time.sleep(1)
            
    def tranExpire(self, expireTime=3600):
        """ 转移过期的入待查队列 """
        nowTime = time.time()
        self.mongoDB.delete_many(DBName,CHECKED_TBNAME,{"ut":{"$lte":(nowTime-expireTime*5)}})
        needChecks = self.mongoDB.find(DBName,CHECKED_TBNAME,{"ut":{"$lte":(nowTime-expireTime)}})
        if needChecks:
            metas = list(map(lambda x: x.get("meta"),needChecks))
            self.__saveToWaitCheck(metas)
            self.__removeCheckedFromRedis(*metas)
        
    def loopTranExpire(self,expireTime=3600):
        """ 定时转移过期的入待查队列 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        while not ctrlCU.isExit():
            time.sleep(60)
            self.tranExpire(expireTime)
        
    def loopCheck(self,checkUrl=CHECK_BAIDU,checkTimeout=20,checkThreadNum=16,expireTime=3600):
        """ 多线程循环检测等待队列中代理的可用性，并保存入checked。 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        asyncU:AsyncU = AsyncU.produce("ProxyU")
        asyncU.asyncRun(target=self.loopTranExpire, asyncKey="loopTranExpire", isProcess=False)
        for c in range(checkThreadNum):
            asyncU.asyncRun(target=self.loopCheckOneProxy,args=(checkTimeout,checkUrl,), asyncKey=f"loopChechProxys_{c}", isProcess=False)
        
    def loopCrawlAndCheck(self,crawlDuring=20,checkUrl=CHECK_BAIDU,checkTimeout=20,checkThreadNum=16,expireTime=3600):
        """ 总入口，启动所有采集和检测进程 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        self.loopCheck(checkUrl, checkTimeout,checkThreadNum,expireTime)
        self.loopCrawl(crawlDuring)
        