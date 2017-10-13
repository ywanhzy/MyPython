#coding=utf-8

import Mssql
import Email

#---------操作Mssql数据库----start---
def doMsSql():
    config = {'host': '.', 'user': 'sa', 'pwd': '2510556', 'db': 'EzgFilmDB'}
    mssql = Mssql.Mssql(config)
    sql = "select top 3 *  from [dbo].[Client_User]"
    rows = mssql.select(sql)
    for i in rows:
        print i[8]
# ---------操作Mssql数据库---end----

# doMsSql()

Email.sendEmail()