# coding=utf-8
# pylint: disable=broad-except, import-error
import pymysql as mysql
from DBUtils.PooledDB import PooledDB



class SqlConnection(object):
    pool = dict()
    def __init__(self, host="172.29.129.8", port=3306, user="tester", passwd="Cnex!321", db_name="production_test"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.conn = self.__get_conn()
        self.cursor = self.conn.cursor()

    def __get_conn(self):
        if self.db_name not in SqlConnection.pool.keys():
            SqlConnection.pool[self.db_name] =  PooledDB(creator=mysql, mincached=1 , maxcached=20 ,
                                                         host=self.host , port=self.port, user=self.user,
                                                         passwd=self.passwd, db=self.db_name,
                                                         use_unicode=True,charset="utf8")
        return SqlConnection.pool[self.db_name].connection()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute_sql_command(self, command):
        results = list()
        try:
            self.conn.ping()
            self.cursor.execute(command)
            results = self.cursor.fetchall()
        except BaseException as message:
            print(message)
        return results