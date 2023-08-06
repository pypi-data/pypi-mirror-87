from ..py_api_b import PyApiB
from pymongo import MongoClient, ReplaceOne, UpdateOne
from ..py_file.fileU import FileU
from ..py_mix.envU import EnvU


class MongoDBU(PyApiB):
    """
    Mongo数据库工具
    """
    HOST_KEY = "mongo_host"
    PORT_KEY = "mongo_port"
    USER_KEY = "mongo_user"
    PSWD_KEY = "mongo_pswd"
    
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.initByEnv() or self.initByEnvFile()
        
    def initByEnv(self):
        _envU = EnvU()
        _host = _envU.get(self.HOST_KEY)
        if _host:
            _port = int(_envU.get(self.PORT_KEY,"1"))
            _user = _envU.get(self.USER_KEY)
            _pswd = _envU.get(self.PSWD_KEY)
            self.init(_host,_port,_user,_pswd)
            return True
        return False
        
    def initByEnvFile(self, env_path='./dockers/.env'):
        _envU = FileU.produce().read_env(env_path)
        _host = _envU.get(self.HOST_KEY)
        if _host:
            _port = int(_envU.get(self.PORT_KEY,"1"))
            _user = _envU.get(self.USER_KEY)
            _pswd = _envU.get(self.PSWD_KEY)
            self.init(_host,_port,_user,_pswd)
            return True
        return False

    def init(self, host=None, port=None, user=None, pswd=None):
        self.session = None
        if user:
            self.mongo = MongoClient(f"mongodb://{user}:{pswd}@{host}:{port}")
        elif host:
            self.mongo = MongoClient(host, port)
        else:
            self.mongo = None
        return self

    def getDatabase(self, dbName):
        return self.mongo.get_database(dbName)

    def getTable(self, dbName, tableName):
        db = self.getDatabase(dbName)
        tb = db.get_collection(tableName)
        return tb

    # # 数据复制
    # @staticmethod
    # def copy(from_client,
    #          to_client,
    #          from_db_name,
    #          to_db_name,
    #          tb_name=None,
    #          from_where=None):
    #     from_db = from_client.getDatabase(from_db_name)
    #     to_db = to_client.getDatabase(to_db_name)
    #     if tb_name:
    #         ds = from_db.get_collection(tb_name).find(from_where)
    #         to_db.get_collection(tb_name).delete_many({})
    #         to_db.get_collection(tb_name).insert(ds)
    #     else:
    #         tbnames = from_db.list_collection_names()
    #         for tbname in tbnames:
    #             if tbname == 'operation':
    #                 continue
    #             MongoDB.copy(from_client, to_client, from_db_name, to_db_name,
    #                          tbname, from_where)

    # 事务相关session
    def _getSession(self):
        if not self.session:
            self.session = self.mongo.start_session()
        return self.session

    # 事务开启
    def startTransaction(self):
        self._getSession().start_transaction()

    # 事务提交
    def commitTransaction(self):
        self._getSession().commit_transaction()
        self.session = None

    # 回滚事务
    def abortTransaction(self):
        self._getSession().abort_transaction()
        self.session = None

    def _next_inc_id(self, dbName, tableName):
        return str(
            self.getTable(dbName, "ids").find_and_modify(
                query={"table_name": tableName},
                update={"$inc": {
                    "id": 1
                }},
                upsert=True,
                new=True)['id'])
        
    def insertManyIfNotExist(self, dbName, tableName, datas):
        if isinstance(datas, list):
            _ids = list(map(lambda x:x.get("id"),datas))
            _inserts = []
            _lobjs = self.getTable(dbName, tableName).find({'id':{'$in':_ids}}, {'id':1})
            _lids = list(map(lambda x:x.get("id"),_lobjs))
            for i in range(0,len(datas)):
                if datas[i]['id'] not in _lids:
                    _inserts.append(datas[i])
            if len(_inserts) > 0:
                self.getTable(dbName, tableName).insert_many(_inserts)
                
    def upsertManyById(self, dbName, tableName, datas):
        # reqs = []
        # for _data in datas:
        #     reqs.append(UpdateOne({'id':_data['id']},_data,upsert=True))
        # self.getTable(dbName,tableName).bulk_write(reqs)
        bo = self.getTable(dbName,tableName).initialize_ordered_bulk_op()
        for _data in datas:
            bo.find({'id':_data['id']}).upsert().update({'$set': _data})
        bo.execute()

    # 插入数据
    def insert(self, dbName, tableName, data):
        if isinstance(data, list):  # 多条数据
            ids = []
            if len(data) > 0:
                for d in data:
                    if 'id' in d:
                        ids.append(d['id'])
                    else:
                        d['id'] = self._next_inc_id(dbName, tableName)
                        ids.append(id)
                self.getTable(dbName,
                               tableName).insert_many(data,
                                                      session=self.session)
            return ids
        elif isinstance(data, dict):  # 一条数据
            if 'id' not in data:
                data['id'] = self._next_inc_id(dbName, tableName)
            self.getTable(dbName, tableName).insert_one({**data},
                                                         session=self.session)
            return data['id']
        else:
            return None

    # 删除一项数据
    def delete_one(self, dbName, tableName, where):
        self.getTable(dbName, tableName).delete_one(where)

    def delete_many(self, dbName, tableName, where=None):
        if where == None:
            where = {}
            self.getTable(dbName, tableName).delete_many(where)

    def drop(self, dbName):
        self.mongo.drop_database(dbName)

    def update(self, dbName, tableName, where, data, is_unset=False):
        action = '$set'
        if is_unset:
            action = '$unset'
        if isinstance(data, list):  # 多条数据
            self.getTable(dbName, tableName).update_many(where,
                                                          {action: data},
                                                          session=self.session)
        elif isinstance(data, dict):  # 一条数据
            self.getTable(dbName, tableName).update_one(where, {action: data},
                                                         session=self.session)
        else:
            return

    def bind_id(self, dbName, tableName, where, data):
        if isinstance(data, list):  # 多条数据
            size = len(data)
            for i in range(0, size):
                data[i] = self.bind_id(dbName, tableName, where, data[i])
        elif isinstance(data, dict):  # 一条数据
            one = self.find_one(dbName, tableName, where)
            if one:
                data['id'] = one['id']
            else:
                data['id'] = self._next_inc_id(dbName, tableName)
        return data

    # 更新或者插入一条数据
    def upsert_one(self, dbName, tableName, where, data):
        id = None
        if where:
            self.getTable(dbName, tableName).update_one(where, {'$set': data},
                                                         upsert=True,
                                                         session=self.session)
        else:
            id = self.insert(dbName, tableName, data)
        return id

    # 设置外键
    def _set_foreign_key(self, dbName, from_tb, from_key, to_tb, to_key):
        data = {
            'from_tb': from_tb,
            'from_key': from_key,
            'to_tb': to_tb,
            'to_key': to_key
        }
        self.upsert_one(dbName, "foreignkeys", {
            'from_tb': from_tb,
            'from_key': from_key
        }, data)

    # 拼接外键数据
    def _add_foreign_data(self,
                          dbName,
                          table_name,
                          data,
                          filters=None,
                          add_foreign_key_deep=0):
        froms = self.find(dbName, "foreignkeys", {'from_tb': table_name})
        for f in froms:
            data = self.__add_foreign_data_by_from(dbName, f['from_tb'],
                                                   f['from_key'], f['to_tb'],
                                                   f['to_key'], data, filters,
                                                   add_foreign_key_deep)
        return data

    def __add_foreign_data_by_from(self,
                                   dbName,
                                   from_tb,
                                   from_key,
                                   to_tb,
                                   to_key,
                                   data,
                                   filters=None,
                                   add_foreign_key_deep=0):
        index = from_key.find('.')
        if index == -1:
            if from_key in data and data[from_key]:
                if isinstance(data[from_key], list):
                    ddd = []
                    for di in data[from_key]:
                        ddd_one = self.find_one(
                            dbName,
                            to_tb, {to_key: di},
                            filters={
                                **filters, from_tb: 0
                            },
                            add_foreign_key_deep=add_foreign_key_deep - 1)
                        if ddd_one:
                            ddd.append(ddd_one)
                    data[from_key] = ddd
                else:
                    data[from_key] = self.find_one(
                        dbName,
                        to_tb, {to_key: data[from_key]},
                        filters={
                            **filters, from_tb: 0
                        },
                        add_foreign_key_deep=add_foreign_key_deep - 1)
        else:
            key = from_key[:index]
            next_key = from_key[index + 1:]
            if key == '0':
                size = len(data)
                for i in range(0, size):
                    data[i] = self.__add_foreign_data_by_from(
                        dbName, from_tb, next_key, to_tb, to_key, data[i],
                        filters, add_foreign_key_deep)
            elif key in data:
                data[key] = self.__add_foreign_data_by_from(
                    dbName, from_tb, next_key, to_tb, to_key, data[key],
                    filters, add_foreign_key_deep)
        return data

    def find(self,
             dbName,
             tableName,
             where=None,
             filters=None,
             add_foreign_key_deep=0,
             page=-1,
             size=100,
             sort=None):
        if filters == None:
            filters = {'_id': 0}
        else:
            filters['_id'] = 0
        d = self.getTable(dbName, tableName).find(where, filters)
        if sort:
            d = d.sort(list(map(lambda x:(x,int(sort[x])),sort)))
        if page >= 0:
            d = d.limit(size).skip(size * page)
        data = list(d)
        if add_foreign_key_deep > 0:
            size = len(data)
            for i in range(0, size):
                data[i] = self._add_foreign_data(dbName, tableName, data[i],
                                                 filters, add_foreign_key_deep)
        return data

    def find_one(self,
                 dbName,
                 tableName,
                 where=None,
                 filters=None,
                 add_foreign_key_deep=0):
        if filters == None:
            filters = {'_id': 0}
        else:
            filters['_id'] = 0
        data = self.getTable(dbName, tableName).find_one(where, filters)
        if add_foreign_key_deep > 0:
            self._add_foreign_data(dbName, tableName, data, filters,
                                   add_foreign_key_deep)
        return data

    def count(self, dbName, tableName, where=None):
        return self.getTable(dbName, tableName).count(where,
                                                       session=self.session)

    def aggregate(self, dbName, tableName, match):
        return list(self.getTable(dbName, tableName).aggregate(match))