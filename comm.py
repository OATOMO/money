# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         comm
# Description:  
# Date:         2020/9/24
# -----------------------------------------------------------------------------
import psycopg2
pgHost = '172.16.2.53'
pgPort = 5432
pgDB = 'economicanalysis'
pgUSER = 'economic'
pgPW = 'economic@ynty1'


def initPgDB(dbName, user, passwd, host, port):
    conn = psycopg2.connect(database=dbName,
                            user=user,
                            password=passwd,
                            host=host,
                            port=port,
                            connect_timeout=3)
    # cur = conn.cursor()
    return conn


def upsertRow(conn, tableName, keyList, valueList, unique):
    if len(keyList) != len(valueList):  # 无法判断就返回存在,不让其添加
        return
    sqlStr = "INSERT INTO {tabName} ({keyStr}) VALUES ( {sStr} )" \
             " on conflict ({unique_name}) do update set {uniqueStr};;"
    # sqlStr = "insert into test values (1,'test',now()) on conflict (id) do update set info=excluded.info,crt_time=excluded.crt_time;"
    sStr = ''
    keyStr = ''
    uniqueStr = ''
    for i in range(len(keyList)):
        sStr += '%s,'
        keyStr += ('"' + keyList[i] + '",')
        if keyList != 'order_id':
            uniqueStr += '{field}=excluded.{field},'.format(field=keyList[i])
    sStr = sStr.rstrip(',')
    keyStr = keyStr.rstrip(',')
    uniqueStr = uniqueStr.rstrip(',')
    sql = sqlStr.format(tabName=tableName, keyStr=keyStr, sStr=sStr, unique_name=unique, uniqueStr=uniqueStr)
    # print(sql)
    cur = conn.cursor()
    cur.execute(sql, (valueList))
    conn.commit()


def insertRow(conn, tableName, keyList, valueList):
    if len(keyList) != len(valueList):  # 无法判断就返回存在,不让其添加
        return
    # sql = "INSERT INTO population (id,time,in,out) VALUES ( %s,%s,%s,%s)"
    sqlStr = "INSERT INTO {tabName} ({keyStr}) VALUES ( {sStr} ) ON CONFLICT DO NOTHING;;"
    sStr = ''
    keyStr = ''
    for i in range(len(keyList)):
        sStr += '%s,'
        keyStr += ('"' + keyList[i] + '",')
    sStr = sStr.rstrip(',')
    keyStr = keyStr.rstrip(',')
    sql = sqlStr.format(tabName=tableName, keyStr=keyStr, sStr=sStr)
    # print(sql)
    cur = conn.cursor()
    cur.execute(sql, (valueList))
    conn.commit()


# 多行插入
def insertRows(conn, tableName, keyList, valueLists):
    if type(valueLists[0]) != list:
        return
    if len(keyList) != len(valueLists[0]):  # 无法判断就返回存在,不让其添加
        return
    # sql = "INSERT INTO population (id,time,in,out) VALUES ( %s,%s,%s,%s)"
    sqlStr = "INSERT INTO {tabName} ({keyStr}) VALUES  {vStr}  ON CONFLICT DO NOTHING;;"
    sStr = ''
    keyStr = ''
    for i in range(len(keyList)):
        sStr += '%s,'
        keyStr += ('"' + keyList[i] + '",')
    sStr = sStr.rstrip(',')
    rowsStr = ''
    for row in valueLists:
        rowsStr += '(\''+'\',\''.join(row)+'\'),'
    rowsStr = rowsStr.rstrip(',')
    rowsStr = rowsStr.replace('\'NULL\'', 'NULL')
    keyStr = keyStr.rstrip(',')
    sql = sqlStr.format(tabName=tableName, keyStr=keyStr, vStr=rowsStr)
    # print(sql)
    cur = conn.cursor()
    cur.execute(sql, (valueLists))
    conn.commit()


def getAllCode(conn):
    sql = "select * from stock_code where trade_status='1'"
    codes = []
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for code in result:
            codes.append(code)
        # todo
        # return codes[200:230]
        return codes
    except psycopg2.errors.InvalidDatetimeFormat:
        return []


def list2lower(l):
    r = []
    for i in l:
        r.append(i.lower())
    return r


def fullList(l):
    r = []
    for i in l:
        if i == '':
            r.append(None)
        else:
            r.append(i)
    return r


def fullList_str(l):
    r = []
    for i in l:
        if i == '':
            r.append('NULL')
        else:
            r.append(i)
    return r