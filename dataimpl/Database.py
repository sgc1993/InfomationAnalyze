import pyodbc
import py2neo
import configparser
import os
settings_file = os.path.join( os.path.dirname(__file__),"settings.conf")
#数据库连接、操作类
class MSSQL:
    def __init__(self):
        settings = self.__load_configuration__(settings_file)
        self.host = settings['MSSQL_SERVER']
        self.db = settings['MSSQL_DB']
        self.user = settings['MSSQL_USER']
        self.pwd = settings['MSSQL_PWD']
    #连接数据库，获得数据库对象
    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(self.host,self.db,self.user,self.pwd))
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur
    #执行查询sql语句,返回查询结果列表
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList
    #执行非查询sql语句，无返回结果
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def __load_configuration__(self, config_file):
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(config_file)
        settings = {}
        settings['MSSQL_SERVER'] = config.get('connection_settings','MSSQL_SERVER').strip("'").strip("\"")
        settings['MSSQL_DB'] = config.get('connection_settings','MSSQL_DB').strip("'").strip("\"")
        settings['MSSQL_USER'] = config.get('connection_settings','MSSQL_USER').strip("'").strip("\"")
        settings['MSSQL_PWD'] = config.get('connection_settings','MSSQL_PWD').strip("'").strip("\"")
        return settings

class Neo4j:

    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd

    def __GetConnect(self):
        self.graph = py2neo.Graph(self.host, self.user, self.pwd)

if __name__ == '__main__':
    mssql = MSSQL()
    result = mssql.ExecQuery("select * from Expert")
    print(result[0])
