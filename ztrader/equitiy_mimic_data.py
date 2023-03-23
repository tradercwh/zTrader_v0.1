'''
'''

import random
import numpy as np
import pandas as pd
from functools import partial

from datetime import date, timedelta

#dates function
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def custom_data_generator(initial_price_range, period_num):
    p = random.uniform(initial_price_range[0], initial_price_range[1])

    ps = []
    for i in range(period_num):       
        ps.append(p)
        rise_ratio = 0.1*random.uniform(-1, 1)
        
        p = p * ( 1 + rise_ratio )

    return ps


def geometric_brownian():
    pass
    

def equity_table_imitator(
    symbols,
    dates,
    gen_func,
    field = None, 
    saved_dir = None
    ):
    '''
    Parameters:

    ---------------
    
    symbols : id of equity.
    dates : data date.
    field : single field name
    gen_func : a data generator function
    saved_dir : output_dir

    '''
    d = {}
    num = len(symbols)

    #fd for field data
    fd_num = len(dates)

    for i in range(num):
        fds = gen_func[i](fd_num)
        sid = symbols[i]

        d.update({ sid : fds})

    data_frame = pd.DataFrame(data=d, index = dates)

    if saved_dir is not None:
        data_frame.to_feather(saved_dir)

    return data_frame


def test_func(gen):
    for p in gen:
        print(p)


if __name__ == '__main__':

    start_date = date(2013, 1, 1)
    end_date = date(2015, 6, 2)
    dates = list(daterange(start_date, end_date))
    gen =  partial(custom_data_generator, [5, 30])
    gen(10)
    df_h = equity_table_imitator(
        symbols=['600688'],
        dates=dates,
        gen_func=[gen]
    )

    df_l = equity_table_imitator(
        symbols=['600688'],
        dates=dates,
        gen_func=[gen]
    )

    df_o = equity_table_imitator(
        symbols=['600688'],
        dates=dates,
        gen_func=[gen]
    )

    df_c = equity_table_imitator(
        symbols=['600688'],
        dates=dates,
        gen_func=[gen]
    )


    mimic_data={
        "H" : df_h,
        "L" : df_l,
        "O" : df_o,
        "C" : df_c
    }


    
    # print(df)


    # test_func(gen)
    
    
    # for single_date in daterange(start_date, end_date):
    #     print(single_date.strftime("%Y-%m-%d"))


    # pass


