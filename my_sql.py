# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         my_sql
# Description:  
# Date:         2020/9/29
# -----------------------------------------------------------------------------
# 搜索所有证券代码
import psycopg2


def sql_select_all_code(conn):
    sql = "select * from stock_code where trade_status='1'"
    codes = []
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for code in result:
            codes.append({'label': code[1], 'value': code[0]})
        return codes
    except psycopg2.errors.InvalidDatetimeFormat:
        return []


def sql_code_kline(conn, code, start, end):
    sql = "select text(date) as date,close from stock_d_k_line where code='{code}' and \
        date>=date('{start}') and date<date('{end}')+interval '1 year' order by date;".format(
        code=code, start=start, end=end)
    cur = conn.cursor()
    data = []
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for i in result:
            data.append({'date': i[0], 'close': i[1]})
        return data
    except psycopg2.errors.InvalidDatetimeFormat:
        return []


def sql_kline_valid_date(conn):
    sql = "select distinct to_char(date_trunc('year',date),'YYYY') as date from \
        (select distinct date from stock_d_k_line order by date)x;"
    cur = conn.cursor()
    data = []
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for i in result:
            data.append(i[0])
        return data
    except psycopg2.errors.InvalidDatetimeFormat:
        return []

