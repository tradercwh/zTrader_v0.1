'''
get dataframe from tushare api

'''

import tushare as ts
import pandas as pd
import os
import time

TOKEN='0b4d8d6fd5d5e5058e93a259a410f94f9f8b7279ab9247c9b81ac404'

ONE_MIN = 60000

REQ_LIM = 500
LINE_LIM = 8000

P5MIN_BAR_NUM = 48
P15MIN_BAR_NUM = 16
P30MIN_BAR_NUM = 8
P60MIN_BAR_NUM = 4

MIN_BAR_NUM = {
    "5min"  : P5MIN_BAR_NUM,
    "15min" : P15MIN_BAR_NUM,
    "30min" : P30MIN_BAR_NUM,
    "60min" : P60MIN_BAR_NUM
}

SAVE_ROOT = "B:\\stock_data\\price_volume"
DIR_NAME = {
    "5min"  :   "period_5min",
    "15min" :   "period_15min",
    "30min" :   "period_30min",
    "60min" :   "period_60min",
    "day"   :   "period_day",
    "week"  :   "period_week",
    "month" :   "period_month"
}


def get_trading_calendar():
    '''
        return the trading state of all history
    
    '''
    pass


def cal_trd_day_num(ts_code):
    '''
        return trading days of a stock since it marketing
    
    '''

    pass


def cal_line_num(day_num, period):
    return day_num * MIN_BAR_NUM[period]


def chunk_num(ts_code):
    dy_num = cal_trd_day_num(ts_code) 
    ln_num = cal_line_num(dy_num)

    if ln_num % LINE_LIM ==0:
        ck_num = ln_num // LINE_LIM
    else:
        ck_num = ln_num // LINE_LIM + 1

    return ln_num, ck_num


def cal_end_date(start_date, trd_day_num):
    '''
        given a start date, and day number after that, return the end date
    '''
    pass


def down_load_strategy(ts_code, period):
    ln_num, ck_num = chunk_num(ts_code)
    flags = []

    for i in range(ck_num):
        end_date = cal_end_date(start_date, LINE_LIM // P15MIN_BAR_NUM) 
        flags.append(end_date)

    min_to_use = ck_num // REQ_LIM + int( ck_num % REQ_LIM != 0 )

    return flags, min_to_use


def get_stock_list(tushare_pro_entry):
    data = tushare_pro_entry.query(
        'stock_basic', 
        exchange='', 
        list_status='L', 
        fields='ts_code,symbol,name,area,industry,list_date')

    return data


def cat_dfs(dfs):
    '''
        concat dataframe by rows
    
    '''

    pass


def dwn_daily_index():
    '''
        down load the index of SZZS
    '''

    pass


def daily_update():
    'loop and open feather file, cat newest df then save'

    pass


def dwn_to_feather(ts_code, start_data, end_date, period, output_dir):
    flags, min_to_use = down_load_strategy(ts_code, period)

    start_date = flags[0]
    flg_num = len(flags)

    cnt = 0
    dfs = []
    
    t0 = time.time()
    for i in range(flg_num-1):
        cnt += 1
        start_data = flags[i]
        end_date = flags[i+1]

        df_part = ts.pro_bar(
            ts_code=ts_code, 
            adj='qfq', 
            start_date=start_date, 
            end_date=end_date, 
            freq=period
            )

        dfs.append(df_part)

        tc = time.time()
        if tc-t0 < ONE_MIN and cnt >= REQ_LIM-1:
            time.sleep( ONE_MIN - (tc-t0 ) )
            t0=time.time() 
            cnt = 0

    df = cat_dfs(dfs)

    fl_name = ts_code.replace('.', '_') + '_' + period + '.feather'
    sv_path = os.path.join(output_dir, fl_name)

    df.to_feather(sv_path)


def download_all(period):
    pass


if __name__ == '__main__':
    ts.set_token(TOKEN)     
    pro = ts.pro_api(TOKEN)

    
    pass


