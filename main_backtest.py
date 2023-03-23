'''
1. parsing configure
2. call func:
    1. initialize dataport
    2. set backtest engine
    3. set clock
    4. load algorithms
'''

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-cf', '--config')


from ztrader.backtest.backtest import T1Engine, Clock
from ztrader.data_api.data import DataPort, MarketData, BarData
from ztrader.algorithms.strategy import T1Strategy
from ztrader.algorithms.utils import load_algo_func

from utils import parse_config, visulize_func


config_file = parser.config

ele = parse_config( config_file )

funcs = ele['algo_funcs']
capital_base = ele['capital_base']
start_date = ele['start_date']
end_date = ele['end_date']
clock_period = ele['clock_period']

bar_periods = ele['bar_periods']
bar_feilds = ele['bar_feilds']
reader = ele['data_reader']
visual = ele['visual']

data_port = DataPort(reader=reader)

bar_data = BarData(
        data_port=data_port, 
        start_date=start_date
        )

market_data = MarketData( bar_data = bar_data )

clock = Clock(start_date=start_date, end_date=end_date, period=clock_period)

market_data.bar_data.initialize(
        periods = bar_periods,
        fields= bar_feilds,
        action_period = clock_period
        )

stratgey = T1Strategy(market_data=market_data,
                       capital_base=capital_base, 
                       **funcs)

backtest_engin = T1Engine(
    strategy=stratgey,
    clock=clock
)

perfs = backtest_engin.run()
visulize_func(perfs)

