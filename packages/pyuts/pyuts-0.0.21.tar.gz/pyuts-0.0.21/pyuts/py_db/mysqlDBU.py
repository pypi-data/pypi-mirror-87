from ..py_api_b import PyApiB
# pip install PyMySQL
# pip install DBUtils
import string
import datetime
import pymysql
import pymysql.cursors
from DBUtils.PooledDB import PooledDB
from DBUtils.SteadyDB import SteadyDBConnection, SteadyDBCursor
from ..py_mix.envU import EnvU
envU = EnvU()


class MysqlDB:

    def __init__(self, host, port, user, pswd, charset, dbName, maxconnections=0, mincached=0, maxcached=0, maxshared=0, blocking=True, maxusage=None, setsession=None, ping=0):
        """ 获取数据库连接池
        
        @dbName 数据库名称 \n
        @maxconnections 连接池允许的最大连接数，0和None表示不限制连接数 \n
        @mincached 初始化时，链接池中至少创建的空闲的链接，0表示不创建 \n
        @maxcached 链接池中最多闲置的链接，0和None不限制 \n
        @blocking 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错 \n
        @maxusage 一个链接最多被重复使用的次数，None表示无限制\n
        @setsession 开始会话前执行的命令列表。如：[“set datestyle to …”, “set time zone …”] \n
        @ping ping MySQL服务端，检查是否服务可用。(0 = None = never;1 = default = whenever it is requested;2 = when a cursor is created;4 = when a query is executed;7 = always) \n
        """
        self.pool:PooledDB = PooledDB(
                creator=pymysql,
                maxconnections=maxconnections,
                mincached=mincached,
                maxcached=maxcached,
                maxshared=maxshared,
                blocking=blocking,
                maxusage=maxusage,
                setsession=[] if setsession == None else setsession,
                ping=ping,
                host=host,
                port=int(port) if isinstance(port,str) else port,
                user=user,
                password=pswd,
                database=dbName,
                charset=charset
            )
        
    def getWaitList(self) -> dict:
        """ 等待提交的队列 {sign:[connect,cursor]} """
        waitList = getattr(self,"waitList",None)
        if waitList == None:
            waitList = {}
            setattr(self,"waitList",waitList)
        return waitList
        
    def conn(self) -> SteadyDBConnection:
        return self.pool.connection()
      
    def __get_cursor(self, conn:SteadyDBConnection, rtType='stream') -> SteadyDBCursor:
        """ 获取光标，用于输入命令 """
        _cursor = None
        if rtType == 'stream':
            return conn.cursor(pymysql.cursors.SSCursor)  # 返回流式游标,查询大量数据时不占用内存(返回数据形式是元组)
        elif rtType == 'dict':
            return conn.cursor(pymysql.cursors.DictCursor)  # 返回字典形式游标,查询出的数据以字典形式返回
        elif rtType == 'default':
            return conn.cursor()
        else:
            # raise Exception("cursor rtType error")
            return conn.cursor()
    
    def __get_conn_cursor(self, sign="", rtType="dict") -> (SteadyDBConnection,SteadyDBCursor):
        """ 获取输入光标
        
        sign:特殊提交标记，“”或None，表示直接提交，其它表示不直接提交，需调用commit(commitSign)才提交
        """
        conn = None
        cursor = None
        if sign:
            if sign in self.getWaitList():
                conn, cursor = self.getWaitList()[sign]
            else:
                raise Exception("execute_sql sign error!")
        if conn == None:
            conn = self.conn()
            cursor = self.__get_cursor(conn, rtType)
        return (conn,cursor)
    
    def _get_where_str(self, where, key=None, rela="=", ao="AND"):
        if where == None and key == None:
            return ""
        if where == None and key != None:
            if rela == "!=":
                return f"{key} is not NULL"
            else:
                return f"{key} is NULL"
        if isinstance(where,dict):
            vvs = []
            for wk in where:
                _ao = ao
                if wk[:1] == "$":
                    if wk[1:] in ["gt","GT"]:
                        rela = ">"
                    elif wk[1:] in ["gte","GTE"]:
                        rela = ">="
                    elif wk[1:] in ["lt","LT"]:
                        rela = "<"
                    elif wk[1:] in ["lte","LTE"]:
                        rela = "<="
                    elif wk[1:] in ["ne","NE"]:
                        rela = "!="
                    elif wk[1:] in ["eq","EQ"]:
                        rela = "="
                    elif wk[1:] in ["in","IN"]:
                        rela = "IN"
                    elif wk[1:] in ["len","LEN"]:
                        key = f"CHAR_LEN({key})"
                    elif wk[1:] in ["or","OR"]:
                        _ao = "OR"
                else:
                    key = wk
                value = where[wk]
                vvs.append(self._get_where_str(value,key,rela,_ao))
            return f" {ao} ".join(vvs)
        elif isinstance(where,list):
            vvs = list(map(lambda x: self._get_where_str(x,key,rela,ao),where))
            res = f" {ao} ".join(vvs)
            if ao in ["OR","or"]:
                res = f"({res})"
            return res
        elif isinstance(where,str):
            if key == None:
                return where
            elif len(where) > 2 and where[:1] == "{" and where[-1:] == "}":
                return f"{key}{rela}{where[1:-1]}"
            else:
                return f"{key}{rela}'{where}'"
        else:
            return f"{key}{rela}{where}"
        return ""
        
      
    def _get_find_filt(self, filt:dict):
        if filt == None:
            return "*"
        retStr = ""
        for fk in filt:
            if filt[fk] == 1:
                retStr = f"{retStr},{fk}"
        if len(retStr) > 1:
            retStr = retStr[1:]
        return retStr
      
    def _append_find_sort(self, whereStr, sort:dict):
        if sort == None:
            return whereStr
        retStr = "ORDER BY "
        for s in sort:
            if sort[s] == 1:
                retStr = f"{retStr}{s} ASC,"
            elif sort[s] == -1:
                retStr = f"{retStr}{s} DESC,"
        if retStr[-1:] == ",":
            retStr = retStr[:-1]
        return f"{whereStr} {retStr}"
    
    def _append_find_limit(self, tbName, whereStr, limit):
        # 如果对于有where 条件，又想走索引用limit的，必须设计一个索引，将where 放第一位，limit用到的主键放第2位，而且只能select 主键！
        # https://www.jb51.net/article/31868.htm
        # select * from collect where id in (select id from collect where vtype=1 limit 90000,10)
        if not limit:
            return whereStr
        startIndex = 0
        pageSize = 0
        if isinstance(limit, int):
            pageSize = limit
        elif isinstance(limit, list) or isinstance(limit, tuple):
            if len(limit) == 1:
                pageSize = limit[0]
            elif len(limit) == 2:
                startIndex = limit[0]
                pageSize = limit[1]
        if startIndex == 0 and pageSize == 0:
            return whereStr
        orderBy = ""
        if " ORDER BY " in whereStr:
            tt = whereStr.split(" ORDER BY ")
            whereStr = tt[0]
            orderBy = f" ORDER BY {tt[1]}"
        return f" id in (SELECT id from {tbName} where {whereStr}){orderBy} limit {startIndex},{pageSize}"
    
    def __cursor_close(self, cursor):
        try:
            cursor.close()
        except:
            pass
        
    def __cursor_rollback(self, cursor):
        try:
            cursor.rollback()
        except:
            pass
          
    def __newSign(self) -> string:
        import random
        return ''.join(random.sample(string.ascii_letters + string.digits, 32))
    
    def __fix_value_str(self, value):
        if value == None:
            return "NULL"
        elif isinstance(value,str):
            return f"'{value}'"
        elif isinstance(value,datetime.datetime):
            return f"'{str(value)}'"
        else:
            return str(value)
    
    def _parse_kv(self, data:dict, filt:dict=None):
        """ 分别提交key和value的数组 """
        keys = []
        vals = []
        for k in data:
            if not (filt and filt.get(k,1) == 0):
                keys.append(k)
                vals.append(self.__fix_value_str(data[k]))
        return keys,vals
        
    def begin(self, rtType='dict') -> string:
        """ 开启同一批命令的标记
        
        rtType: 同一批操作命令返回结果类型，stream：返回流式游标,查询大量数据时不占用内存(返回数据形式是元组)，dict：返回字典形式游标,查询出的数据以字典形式返回
        """
        sign = self.__newSign()
        conn = self.conn()
        cursor = self.__get_cursor(conn,rtType)
        self.getWaitList()[sign] = (conn,cursor)
        return sign
    
    def _commit(self,conn, cursor):
        """ 提交并关闭光标 """
        conn.commit()
        cursor.close()
        
    def commit(self,sign):
        """ 提交
        
        sign: 提交标记，由begin()返回
        """
        if sign not in self.getWaitList():
            return
        conn, cursor = self.getWaitList()[sign]
        self._commit(conn, cursor)
        del self.getWaitList()[sign]
    
    def find_one(self, tbName:str, where, filt:dict=None, sign="", rtType="dict", justSQL=False):
        """ 查找一条数据
        
        tbName:str 表名
        
        where:[str|dict] 查找条件;
            格式str:语法与sql条件语句一样;
            格式dict:语法与Mongodb一样。查看转化结果可以调用:#_get_where_str(where)
                例如:#{"year":{"$gt":1878,"$lt":2000},"name":{"$eq":"{nickName}"}}
                    #== year>1878 AND year<2000 AND name=nickName
                    #{"name":{"$len":{"$lt":100},"$ne":None},"year":{"$or":[{"$gte":1900},{"$lt":1000}]}}
                    #== CHAR_LEN(name)<100 AND CHAR_LEN(name) is not NULL AND (year>=1900 OR year<1000)
        
        filt:dict 查找的字段,None表示全选出，其中单字段1表示选出,0表示不选出.查看转化结果可以调用:#_get_find_filt(where)
                例如:#None
                    #== *
                    #{"id":1,"nickName":0,"name":1}
                    #== id,name
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        rtType:str 返回结果类型,如果已传sign,此字段无效，将以begin(rtType)所传的rtType为主
                   stream：返回流式游标,查询大量数据时不占用内存(返回数据形式是元组)，dict：返回字典形式游标,查询出的数据以字典形式返回
        
        justSQL:boolean 是否只返回sql不操作数据库，可用于sql拼接
        
        """
        import string
        _filtStr = self._get_find_filt(filt)
        _whereStr = self._get_where_str(where)
        sql = f"SELECT {_filtStr} FROM {tbName} WHERE {_whereStr};"
        print(sql)
        if justSQL:
            return sql
        else:
            return self.query_one(sql,sign,rtType, False)
      
    def find_all(self, tbName:str, where, filt:dict=None, limit=None, sort:dict=None, sign="", rtType="dict", justSQL=False):
        """ 查找所有条数据
        
        tbName:str 表名

        where:(str|dict) 查找条件;
            格式str:语法与sql条件语句一样;
            格式dict:语法与Mongodb一样。查看转化结果可以调用:#_get_where_str(where)
                例如:#{"year":{"$gt":1878,"$lt":2000},"name":{"$eq":"{nickName}"}}
                    #== year>1878 AND year<2000 AND name=nickName
                    #{"name":{"$len":{"$lt":100},"$ne":None},"year":{"$or":[{"$gte":1900},{"$lt":1000}]}}
                    #== CHAR_LEN(name)<100 AND CHAR_LEN(name) is not NULL AND (year>=1900 OR year<1000)
        
        filt:dict 查找的字段,None表示全选出，其中单字段1表示选出,0表示不选出.查看转化结果可以调用:#_get_find_filt(where)
                例如:#None
                    #== *
                    #{"id":1,"nickName":0,"name":1}
                    #== id,name
        
        limit:(list|tuple|int) 限制长度。相关说明或性能问题，详见：_append_find_limit
                例如：100或[100]或(100) 相当于 limit 100;[10000,100]或(10000,100) 相当于 limit 10000,100
        
        sort:dict 排序，1:ASC,-1:DESC\n例如：{"date":-1,"level":1} 相当于 date DESC,level ASC
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        rtType:str 返回结果类型,如果已传sign,此字段无效，将以begin(rtType)所传的rtType为主
                   stream：返回流式游标,查询大量数据时不占用内存(返回数据形式是元组)，dict：返回字典形式游标,查询出的数据以字典形式返回
        
        justSQL:boolean 是否只返回sql不操作数据库，可用于sql拼接
        """
        _filtStr = self._get_find_filt(filt)
        _whereStr = self._get_where_str(where)
        _whereStr = self._append_find_sort(_whereStr, sort)
        _whereStr = self._append_find_limit(tbName,_whereStr,limit)
        sql = f"SELECT {_filtStr} FROM {tbName} WHERE {_whereStr};"
        if justSQL:
            return sql
        else:
            return self.query_all(sql, sign, rtType, False)
    
    def insert_one(self, tbName:str, data:dict, filt:dict=None, sign="", justSQL=False):
        """ 插入一条数据
        
        tbName:str 表名

        data:dict 要更新的数据列表
        
        filt:dict 查找的字段,None表示全选出，其中单字段1表示选出,0表示不选出.查看转化结果可以调用:#_get_find_filt(where)
                例如:#None
                    #== *
                    #{"id":1,"nickName":0,"name":1}
                    #== id,name
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        justSQL:boolean 是否只返回sql不操作数据库，可用于sql拼接
        """
        keys, vals = self._parse_kv(data, filt)
        sql = f"INSERT INTO {tbName} ({','.join(keys)}) VALUES ({','.join(vals)});"
        if justSQL:
            return sql
        else:
            return self.query_one(sql, sign, commit=sign in ["",None])
        
    def insert_all(self, tbName:str, data:list, filt:dict=None, sign="", ignoreExist=True, justSQL=False):
        """ 同时插入多条数据，
        
        tbName:str 表名

        data:list 要更新的数据列表
        
        filt:dict 查找的字段,None表示全选出，其中单字段1表示选出,0表示不选出.查看转化结果可以调用:#_get_find_filt(where)
                例如:#None
                    #== *
                    #{"id":1,"nickName":0,"name":1}
                    #== id,name
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        ignoreExist:boolean 是否忽略键值已经存在的数据，默认为True
        
        justSQL:boolean 是否只返回sql不操作数据库，可用于sql拼接
        """
        if not data:
            return []
        one = data[0]
        keys, val = self._parse_kv(one, filt)
        _values_strs = list(map(lambda x: f"({','.join(self._parse_kv(x, filt)[1])})", data))
        _values_str = ','.join(_values_strs)
        ignoreStr = "ignore " if ignoreExist else ""
        sql = f"INSERT {ignoreStr}INTO {tbName} ({','.join(keys)}) VALUES {_values_str};"
        if justSQL:
            return sql
        else:
            return self.query_all(sql, sign, commit=sign in ["",None])
    
    def update_one(self, tbName:str, data:dict, where, filt:dict=None, sign="", justSQL=False):
        """ 更新一条数据 
        
        tbName:str 表名

        data:dict 要更新的数据
        
        where:(str|dict) 查找条件;
            格式str:语法与sql条件语句一样;
            格式dict:语法与Mongodb一样。查看转化结果可以调用:#_get_where_str(where)
                例如:#{"year":{"$gt":1878,"$lt":2000},"name":{"$eq":"{nickName}"}}
                    #== year>1878 AND year<2000 AND name=nickName
                    #{"name":{"$len":{"$lt":100},"$ne":None},"year":{"$or":[{"$gte":1900},{"$lt":1000}]}}
                    #== CHAR_LEN(name)<100 AND CHAR_LEN(name) is not NULL AND (year>=1900 OR year<1000)
        
        filt:dict 查找的字段,None表示全选出，其中单字段1表示选出,0表示不选出.查看转化结果可以调用:#_get_find_filt(where)
                例如:#None
                    #== *
                    #{"id":1,"nickName":0,"name":1}
                    #== id,name
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        justSQL:boolean 是否只返回sql不操作数据库，可用于sql拼接
        """
        keys, vals = self._parse_kv(data, filt)
        _whereStr = self._get_where_str(where)
        _setStrs = list(map(lambda x: f"{keys[x]}={vals[x]}",range(len(keys))))
        sql = f"UPDATE {tbName} SET {','.join(_setStrs)} WHERE {_whereStr};"
        if justSQL:
            return sql
        else:
            return self.query_one(sql, sign, commit=sign in ["",None])
        
    
    def update_all_by_key(self, tbName:str, data:list, key:str="id", filt:dict=None, sign="", justSQL=False):
        """ 更新所有数据，PS:请确保所有数据中都有key对应的字段
        
        tbName:str 表名

        data:list 要更新的数据列表
        
        key:str 生成where对应的键，如果多个键，中间以“逗号”隔开
        
        filt:dict 查找的字段,None表示全选出，其中单字段1表示选出,0表示不选出.查看转化结果可以调用:#_get_find_filt(where)
                例如:#None
                    #== *
                    #{"id":1,"nickName":0,"name":1}
                    #== id,name
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        justSQL:boolean 是否只返回sql不操作数据库，可用于sql拼接
        """
        keys = []
        if ',' in key:
            keys = key.split(",")
        else:
            keys.append(key)
        _update_keys = []
        if len(data) > 0:
            for _d in data[0]:
                if (_d not in keys) and ((not filt) or filt.get(_d,0) == 1):
                    _update_keys.append(_d)
        _in_wheres = list(map(lambda x: f"({','.join(list(map(lambda y: self.__fix_value_str(x.get(y)),keys)))})",data))
        _where_str = f"({','.join(keys)}) IN ({','.join(_in_wheres)})"
        _set_strs = []
        for _update_key in _update_keys:
            _set_str = f"{_update_key} = CASE"
            for i in range(len(data)):
                _set_str = f"{_set_str} WHEN ({','.join(keys)})={_in_wheres[i]} THEN {self.__fix_value_str(data[i].get(_update_key))}"
            _set_str = f"{_set_str} END"
            _set_strs.append(_set_str)
        _set_str = ",".join(_set_strs)
        sql = f"UPDATE {tbName} SET {_set_str} WHERE {_where_str}"
        if justSQL:
            return sql
        else:
            return None
        
    def upsert_all_by_key(self, tbName:str, data:list, filt:dict=None, sign="", justSQL=False):
        """ 如果键不存在则插入，存在则更新。
        
        tbName:str 表名

        data:list 要更新的数据列表
        
        filt:dict 查找的字段,None表示全选出，其中单字段1表示选出,0表示不选出.查看转化结果可以调用:#_get_find_filt(where)
                例如:#None
                    #== *
                    #{"id":1,"nickName":0,"name":1}
                    #== id,name
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        justSQL:boolean 是否只返回sql不操作数据库，可用于sql拼接
        """
        keys = []
        _update_keys = []
        if len(data) > 0:
            for _d in data[0]:
                if (_d not in keys) and ((not filt) or filt.get(_d,0) == 1):
                    _update_keys.append(_d)
        _useKeys = keys + _update_keys
        _values_strs = list(map(lambda x: f"({','.join(list(map(lambda y: self.__fix_value_str(x.get(y)),_useKeys)))})",data))
        _values_str = ','.join(_values_strs)
        _keys_str = f"({','.join(_useKeys)})"
        _update_strs = list(map(lambda x: f"{x}=VALUES({x})",_update_keys))
        _update_str = ','.join(_update_strs)
        sql = f"INSERT INTO {tbName} {_keys_str} VALUES {_values_str} ON DUPLICATE KEY UPDATE {_update_str};"
        if justSQL:
            return sql
        else:
            return self.query_all(sql, sign, commit=sign in ["",None])

    
    def query_all(self, sql, sign="", rtType="dict", commit=False):
        """ 执行sql语句，返回列表数据
        
        sql:str 需执行的sql语句
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        rtType:str 返回结果类型,如果已传sign,此字段无效，将以begin(rtType)所传的rtType为主
                   stream：返回流式游标,查询大量数据时不占用内存(返回数据形式是元组)，dict：返回字典形式游标,查询出的数据以字典形式返回
        
        commit:boolean 是否提交
        """
        conn, cursor = self.__get_conn_cursor(sign, rtType)
        result = None
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if commit:
                self._commit(conn, cursor)
            elif not sign:
                self.__cursor_close(cursor)
        except BaseException as e:
            print(e)
            self.__cursor_rollback(cursor)
            self.__cursor_close(cursor)
        return result
      
    def query_one(self, sql, sign="", rtType="dict", commit=False):
        """ 执行sql语句，返回列表数据
        
        sql:str 需执行的sql语句
        
        sign:str 同一批输入命令的标记，开启同一批命令返回的标记，可以通过调用begin(rtType)返回，不传表示立即执行，传了，则需调用commit(sign)后才生效
        
        rtType:str 返回结果类型,如果已传sign,此字段无效，将以begin(rtType)所传的rtType为主
                   stream：返回流式游标,查询大量数据时不占用内存(返回数据形式是元组)，dict：返回字典形式游标,查询出的数据以字典形式返回
        
        commit:boolean 是否提交
        """
        conn, cursor = self.__get_conn_cursor(sign, rtType)
        result = None
        lastrowid = None
        try:
            cursor.execute(sql)
            lastrowid = cursor.lastrowid
            result = cursor.fetchone()
            if commit:
                self._commit(conn, cursor)
            elif not sign:
                self.__cursor_close(cursor)
        except BaseException as e:
            print(e)
            self.__cursor_rollback(cursor)
            self.__cursor_close(cursor)
        return result if result else lastrowid

class MysqlDBU(PyApiB):
    """
    mysql数据库操作工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        self.dbPools = {}
        self.host = envU.get("mysql_host")
        self.port = envU.get("mysql_port")
        self.user = envU.get("mysql_user")
        self.pswd = envU.get("mysql_pswd")
        self.charset = envU.get("mysql_charset","utf8")
        
    def init(self, host, port, user="", pswd="", charset="utf8"):
        self.host = host
        self.port = str(port)
        self.user = user
        self.pswd = pswd
        self.charset = charset
        return self
    
    def getDB(self,dbName,maxconnections=0,mincached=0,maxcached=0,maxshared=0,blocking=True,maxusage=None,setsession=None,ping=0) -> MysqlDB:
        """ 获取数据库
        
        @dbName 数据库名称 \n
        @maxconnections 连接池允许的最大连接数，0和None表示不限制连接数 \n
        @mincached 初始化时，链接池中至少创建的空闲的链接，0表示不创建 \n
        @maxcached 链接池中最多闲置的链接，0和None不限制 \n
        @blocking 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错 \n
        @maxusage 一个链接最多被重复使用的次数，None表示无限制\n
        @setsession 开始会话前执行的命令列表。如：[“set datestyle to …”, “set time zone …”] \n
        @ping ping MySQL服务端，检查是否服务可用。(0 = None = never;1 = default = whenever it is requested;2 = when a cursor is created;4 = when a query is executed;7 = always) \n
        """
        if dbName in self.dbPools:
            return self.dbPools[dbName]
        db = MysqlDB(self.host,self.port,self.user,self.pswd,self.charset,dbName,maxconnections,mincached,maxcached,maxshared,blocking,maxusage,setsession,ping)
        self.dbPools[dbName] = db
        return db
      
        
    