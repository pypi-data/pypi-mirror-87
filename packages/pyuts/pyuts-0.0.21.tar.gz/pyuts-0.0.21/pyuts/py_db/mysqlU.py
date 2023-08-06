from ..py_api_b import PyApiB
# pip install PyMySQL
from .mysqlDBU import MysqlDBU


class MysqlU(PyApiB):
    """
    mysql数据库工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.init()

    def init(self, host=None, port=27017, user=None, pswd=None):
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        return self
      
    def getDB(self, dbName, charset='utf8') -> MysqlDBU:
        """ 获取数据库 """
        return MysqlDBU.produce(dbName).init(self.host, self.port, self.user, self.pswd, dbName,charset)
      
    # def execute_sql(self, sql, commit=False):
    #     '''执行sql语句'''
    #     try:
    #         self._curs.execute(sql)
    #     except Exception as e:
    #         pprint(sql)
    #         raise e
    #     if commit:
    #         self._conn.commit()

                