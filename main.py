# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         text
# Description:  
# Date:         2020/9/23
# -----------------------------------------------------------------------------
"""   baostock
每日最新数据更新时间：
当前交易日17:30，完成日K线数据入库；
当前交易日20:30，完成分钟K线数据入库；
第二自然日1:30，完成前交易日“其它财务报告数据”入库；
"""
import baostock as bs
import pandas as pd
import comm
import argparse
from tqdm import tqdm


pgHost = '172.16.2.53'
pgPort = 5432
pgDB = 'economicanalysis'
pgUSER = 'economic'
pgPW = 'economic@ynty1'


def download_data(date):
    bs.login()
    # 获取指定日期的指数、股票数据
    stock_rs = bs.query_all_stock(date)
    stock_df = stock_rs.get_data()
    data_df = pd.DataFrame()
    for i, row in stock_df.iterrows():
        print(row['code'], row['code_name'], row['tradeStatus'])
    return
    for code in stock_df["code"]:
        print("Downloading :" + code)
        k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,amount,pctChg", date, date)
        data_df = data_df.append(k_rs.get_data())
    bs.logout()
    data_df.to_csv("./demo_assignDayData.csv", encoding="gbk", index=False)
    print(data_df)


# def get_d_kLine(conn, start, end):
#     data_df = get_kLine(conn, start, end, 'd')
#     pbar = tqdm(total=data_df.shape[0], desc='入库中')
#     for i, row in data_df.iterrows():
#         k = comm.list2lower(row.index.tolist())
#         v = row.values.tolist()
#         comm.insertRow(conn, 'stock_d_k_line', k, comm.fullList(v))
#         pbar.update(1)
#     print('{start}~{end} 日k线数据入库完成'.format(start=date, end=date))

def get_d_kLine(conn, start, end):
    write_n = 1000
    data_df = get_kLine(conn, start, end, 'd')
    pbar = tqdm(total=data_df.shape[0], desc='入库中')
    vList = []
    k = []
    for i, row in data_df.iterrows():
        k = comm.list2lower(row.index.tolist())
        if len(vList) >= write_n:
            comm.insertRows(conn, 'stock_d_k_line', k, vList)
            vList = []
        v = row.values.tolist()
        vList.append(comm.fullList_str(v))
        pbar.update(1)
    comm.insertRows(conn, 'stock_d_k_line', k, vList)
    print('{start}~{end} 日k线数据入库完成'.format(start=date, end=date))


# @type: day (日K线),week (周k线),minute (分钟k线)
def get_kLine(conn, start, end, ktype):
    data_df = pd.DataFrame()
    Parameter = {
        'd': 'date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,' \
                        'tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST',
        'w': 'date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg',
        'm': 'date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg',
        '5': 'date,time,code,open,high,low,close,volume,amount,adjustflag'}
    if ktype not in Parameter.keys():
        return
    codes = comm.getAllCode(conn)
    for item in tqdm(codes, desc='拉取中'):
        code = item[0]
        name = item[1]
        # frequency：数据类型，默认为d，日k线；d = 日k线、w = 周、m = 月、5 = 5,分钟、
        # 15 = 15,分钟、30 = 30,分钟、60 = 60,分钟k线数据
        # adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权
        rs = bs.query_history_k_data_plus(code, Parameter[ktype], start, end, ktype, '3')
        data_df = data_df.append(rs.get_data())
        # print('query_history_k_data_plus respond error_code:' + rs.error_code)
        # print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
    return data_df


# 更新证券代码
def updateCode(conn, date):
    stock_rs = bs.query_all_stock(date)
    stock_df = stock_rs.get_data()
    kList = ['code', 'code_name', 'trade_status']
    for i, row in stock_df.iterrows():
        item = [row['code'], row['code_name'], row['tradeStatus']]
        comm.upsertRow(conn, 'stock_code', kList, item, 'code')


# 更新行业分类
def updateIndustry(conn, date):
    data_df = pd.DataFrame()
    codes = comm.getAllCode(conn)
    for item in tqdm(codes, desc='拉取行业分类'):
        code = item[0]
        name = item[1]
        rs = bs.query_stock_industry(code)
        data_df = data_df.append(rs.get_data())
    pbar = tqdm(total=data_df.shape[0], desc='行业分类入库中')
    for i, row in data_df.iterrows():
        k = comm.list2lower(row.index.tolist())
        v = row.values.tolist()
        comm.upsertRow(conn, 'stock_industry', k, v, 'code')
        pbar.update(1)


def parse_ages():
    parser = argparse.ArgumentParser(description="自动同步银联数据")
    parser.add_argument('--start', default='', help=' date : [yyyy-mm-dd]', type=str)
    parser.add_argument('--end', default='', help=' date : [yyyy-mm-dd]', type=str)
    parser.add_argument('--date', default='', help=' date : [yyyy-mm-dd]', type=str)
    parser.add_argument('--mode', default='kLine', help=' type : [kLine] [update-code] [industry]')
    return parser.parse_args()


def init():
    conn = comm.initPgDB(pgDB, pgUSER, pgPW, pgHost, pgPort)
    cur = conn.cursor()
    cur.execute("SET TIME ZONE 'Asia/Chongqing';")
    conn.commit()
    bs.login()
    return conn


if __name__ == '__main__':
    conn = init()
    ages = parse_ages()
    date = ages.date
    start = ages.start
    end = ages.end
    mode = ages.mode
    if mode == 'update-code':
        updateCode(conn, date)
    elif mode == 'kLine':
        if start == '' and end == '' and date == '':
            print('参数没有有效日期')
            exit(0)
        if start == '' or end == '':
            start = date; end = date
        # 获取指定日期全部股票的日K线数据
        get_d_kLine(conn, start, end)
    elif mode == 'industry':
        updateIndustry(conn, date)
