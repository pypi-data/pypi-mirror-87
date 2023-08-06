from ..py_api_b import PyApiB
from ..py_file.fileU import FileU
from ..py_mix.envU import EnvU
import redis
import json
import random


class RedisDBU(PyApiB):
    """
    Redis数据库工具
    """
    HOST_KEY = "redis_host"
    PORT_KEY = "redis_port"
    USER_KEY = "redis_user"
    PSWD_KEY = "redis_pswd"
    DB_KEY = "redis_db"
    
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.dbIndex = -1
        self.initByEnv() or self.initByEnvFile()
        
    def initByEnv(self):
        _envU = EnvU()
        _host = _envU.get(self.HOST_KEY)
        if _host:
            _port = int(_envU.get(self.PORT_KEY,"1"))
            _user = _envU.get(self.USER_KEY)
            _pswd = _envU.get(self.PSWD_KEY)
            _db = _envU.get(self.DB_KEY)
            self.init(_host,_port,_user,_pswd,_db)
        
    def initByEnvFile(self, env_path='./dockers/.env'):
        _envU = FileU.produce().read_env(env_path)
        _host = _envU.get(self.HOST_KEY)
        if _host:
            _port = int(_envU.get(self.PORT_KEY,"1"))
            _user = _envU.get(self.USER_KEY)
            _pswd = _envU.get(self.PSWD_KEY)
            _db = _envU.get(self.DB_KEY)
            self.init(_host,_port,_user,_pswd,_db)

    def init(self, host=None, port=None, user=None, pswd=None, dbIndex=0):
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        self.selectDB(dbIndex=dbIndex)
        
    def selectDB(self, dbIndex=0):
        if self.dbIndex == dbIndex:
            return
        self.r:redis.Redis = redis.Redis(host=self.host, port=self.port, decode_responses=True, password=self.pswd, db=dbIndex)
        self.dbIndex = dbIndex
    
    def p(self, transaction=False):
        """ 
        同时大量写操作，请使用此管道方法
        用法：
        with pyuts.redisDBU().p() as p:
            xxx
            p.execute()
        """
        return self.r.pipeline(transaction=transaction)
    
    def set_str_list(self, key, values):
        """ 设置字符串列表 """
        nowLen = self.r.llen(key)
        toLen = len(values)
        if toLen <= 0:
            self.delete(key)
            return
        with self.p() as p:
            for i in range(toLen):
                if nowLen <= i:
                    nowLen += 1
                    p.rpush(key,values[i])
                else:
                    p.lset(key,i,values[i])
            p.ltrim(key,0,toLen-1)
            p.execute()
        
    def get_str_list(self, key):
        """ 获取字符串列表 """
        return self.r.lrange(key,0,-1)
        
    def set_json_list(self, key, values):
        """ 设置json列表 """
        vs = list(map(lambda x: json.dumps(x), values))
        self.set_str_list(key, vs)
        
    def get_json_list(self, key):
        """ 获取json列表 """
        values = self.get_str_list(key)
        vs = []
        for v in values:
            try:
                vs.append(json.loads(v))
            except Exception as identifier:
                pass
        return vs
    
    def lpop_str(self, key):
        try:
            return self.r.lpop(key)
        except Exception as e:
            return None
        
    def lpop_json(self, key):
        s = self.lpop_str(key)
        try:
            return json.loads(s)
        except Exception as identifier:
            return None
        
    def rpop_str(self, key):
        try:
            return self.r.rpop(key)
        except Exception as e:
            return None
        
    def rpop_json(self, key):
        s = self.rpop_str(key)
        try:
            return json.loads(s)
        except Exception as identifier:
            return None
        
    def rpush_str(self, key, value, maxCount=-1):
        try:
            if isinstance(value,list):
                if len(value) > 0:
                    with self.p() as p:
                        for v in value:
                            p.rpush(key, v)
                        if maxCount > 0:
                            p.ltrim(key, -maxCount, -1)
                        p.execute()
            else:
                self.r.rpush(key, value)
                if maxCount > 0:
                    self.r.ltrim(key, -maxCount, -1)
            return True
        except Exception as e:
            return False
        
    def rpush_json(self, key, value, maxCount=-1):
        try:
            if isinstance(value,list):
                vs = list(map(lambda x: json.dumps(x), value))
                self.rpush_str(key, vs, maxCount)
            else:
                self.rpush_str(key, json.dumps(value), maxCount)
            return True
        except Exception as e:
            return False
    
    def lrem_str(self, key, value, count=0):
        try:
            if isinstance(value,list):
                with self.p() as p:
                    for remJ in value:
                        p.lrem(key, json.dumps(remJ), count)
                    p.execute()
            else:
                self.r.lrem(key, value, count)
            return 1
        except Exception as e:
            return 0
        
    def lrem_json(self, key, value, count=0, byJsonKey=None):
        try:
            if isinstance(value, list):
                self.lrem_str(key, list(map(lambda x:json.dumps(x),value)), count)
            else:
                self.lrem_str(key, json.dumps(value), count)
        except Exception as e:
            return 0
        
    def random_get_str(self, key):
        """ 随机获取列表中的一个字符串元素 """
        nowLen = self.r.llen(key)
        index = random.randint(1,nowLen)
        try:
            return self.r.lindex(key, index)
        except Exception as e:
            return None
        
    def random_get_json(self, key):
        """ 随机获取列表中的一个字符串元素 """
        s = self.random_get_str(key)
        try:
            return json.loads(s)
        except Exception as identifier:
            return None
        
    def sadd(self, key, *values):
        """ 集合添加元素 """
        self.r.sadd(key,*values)
    
    def srandmember(self, key, number=1):
        """ 集合中随机获取numbers个元素 """
        return self.r.srandmember(key,number=number)
    
    def srem(self, key, *values):
        """ 集合中删除某些值 """
        try:
            return self.r.srem(key, *values)
        except Exception as identifier:
            return []

    def sismember(self, key, value):
        """ 检查value是否是key对应的集合的成员 """
        return self.r.sismember(key, value)
    
    def delete(self, key):
        """ 删除某个键 """
        try:
            self.r.delete(key)
        except Exception as identifier:
            pass
        
    def len(self, key):
        """ 获取键对应内容的长度 """
        _type = self.type(key)
        if _type == "list":
            return self.llen(key)
        elif _type == "set":
            return self.scard(key)
        elif _type == "zset":
            return self.zcard(key)
        elif _type == "hash":
            return self.hlen(key)
        elif _type == "string":
            return self.strlen(key)
        
    def strlen(self, key):
        """ 获取字符串长度 """
        return self.r.strlen(key)
    
    def llen(self, key):
        """ 获取列表长度 """
        return self.r.llen(key)
    
    def hlen(self, key):
        """ 获取散列表长度 """
        return self.r.hlen(key)
    
    def scard(self, key):
        """ 获取集合长度 """
        return self.r.scard(key)
    
    def zcard(self, key):
        """ 获取有序集合长度 """
        return self.r.zcard(key)
        
    def keys(self):
        """ 获取到所有的键 """
        return self.r.keys()
        
    def exists(self, *keys):
        """ 判断某个键是否存在 """
        return self.r.exists(*keys)
        
    def expire(self, key, time):
        """ 为某个键设置超时时间 """
        self.r.expire(key, time)
        
    def rename(self, key, toKey):
        """ 修改键的名字 """
        self.r.rename(key, toKey)
        
    def move(self, key, db):
        """ 将mykey从当前库移动到其他库中 """
        self.r.move(key, db)
        
    def randomkey(self):
        """ 随机获取一个键 """
        return self.r.randomkey()
    
    def type(self, key):
        """ 获取某个键对应的值的类型,注意此type非python中的type """
        return self.r.type(key)
    
    def get(self, key):
        """ 获取字符串值 """
        return self.r.get(key)
    
    
    