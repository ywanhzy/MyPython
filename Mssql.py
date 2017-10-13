# -*- coding: utf-8 -*-

import sys
import pymssql


class Mssql:
    def __init__(self, config):
        if not config:
            config = {'host': '.', 'user': 'sa', 'pwd': '2510556', 'db': 'EzgFilmDB'}
        self.cf = config

    def __Connect(self):
        if not self.cf['db']:
            print "没有设置数据库信息"
            sys.exit(1)
        try:
            self.conn = pymssql.connect(host=self.cf['host'], user=self.cf['user'], password=self.cf['pwd'],
                                        database=self.cf['db'],charset="utf8")
            cur = self.conn.cursor()
        except Exception as e:
            print "connect--Error decoding config file: %s" % str(e.message)
            sys.exit(1)
        return cur

    def select(self, sql):
        try:
            cur = self.__Connect()
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            self.conn.close()
            return rows
        except Exception, err:
            print "select--Error decoding config file: %s" % str(err)
            sys.exit(1)

    def insert(self, sql):
        try:
            cur = self.__Connect()
            cur.execute(sql)
            cur.close()
            self.conn.commit()
            self.conn.close()
        except Exception, err:
            print "insert--Error decoding config file: %s" % str(err)
            sys.exit(1)

def main():
    config = {'host': '.', 'user': 'sa', 'pwd': '2510556', 'db': 'EzgFilmDB'}
    #config = {'host': '192.168.1.206', 'user': 'sa', 'pwd': 'c5adcde3a!', 'db': 'Ezg_OA'}

    mssql = Mssql(config)

    # insert sql
    # sql = "insert into [dbo].[Client_User] values('2','2','2','2','2018-05-20','你好啊','大大大','嘻嘻嘻','哈哈哈')"
    # mssql.insert(sql)

    # select sql
    sql = "select top 3 *  from [dbo].[Client_User]"
    rows = mssql.select(sql)

    for i in rows:
        print i[8]


if __name__ == "__main__":
    main()