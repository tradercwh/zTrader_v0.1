import pandas as pd
import os
import random
import numpy as np
import datetime

import __init__
from manipulation_func import *
from common_var import *
from sector import *


class TradingDate():
    def get_points(self, freq) -> None:
        s1 = pd.date_range("9:30", "11:30", freq = freq)    
        s2 = pd.date_range("13:00", "15:00", freq = freq)


class FeatherReader():
    def read_(self, dir):
        file_list = self.get_file_list(dir)

        return self.get_raw_tables(file_list)

    def sample(self, dir, sids=None):
        if sids is None:
            file_list = self.get_file_list(dir)
            file_paths = [random.choice(file_list)]

            return self.get_raw_tables(file_paths)

        else:
            file_list = [os.path.join(dir, sid) for sid in sids]
            return self.get_raw_tables(file_list)

    def random_sample(self, dir, num=None):
        if num is None:
            num = 1

        file_list = self.get_file_list(dir)
        sub_file_list = random.sample(file_list, num)
        return self.get_raw_tables(sub_file_list)

    def get_file_list(dir):
        return [file for file in os.listdir(dir) if file.endswith('.feather')]

    def get_raw_tables(self, file_list):
        raw_tables ={}
        for file in file_list:
            file_path = os.path.join(dir, file)

            df = pd.read_feather(file_path)

            sid = os.path.basename(file_path)
            raw_tables.update({sid : df})
        return raw_tables

    
class DataPort():
    '''
          | id1     |   id2     | ...
    date1 |         |           |
    date2 |         |           |
    .
    .
    .
    .
    fields: O, H, L C, V, 
    '''
    def __init__(self, reader=None) -> None:
        self.default_mimic_stock_num = 1000

        self.default_start_date_minunte = datetime.datetime(2012,1,1, 9,30)
        self.default_end_date_minute =  datetime.datetime(2013,1,1, 15)

        self.default_start_date_daily = datetime.datetime(2012,1,1)
        self.default_end_date_daily =  datetime.datetime(2013,1,2)

        self.default_mimic_date_num =(self.default_end_date_daily - self.default_start_date_daily).days

        self.default_id = [str(i).zfill(6) for i in range(self.default_mimic_stock_num)]
    
        if reader is not None:
            self.reader = reader
        else:
            self.mimic = True
            
    def initialize(self, periods, fields):
        self.sep_sid_tables = {}
        self.sep_sid_tables_index = {}
        if not self.mimic:
            for period in periods:
                dir = self.get_dir(period)

                sid_table = self.reader.read(dir)

                field_tables = self.get_sep_field_table(sid_table)
                tables_index = self.get_standard_table_index(sid_table)

                self.sep_sid_tables.update({ period : field_tables })
        else:
            for period in periods:
                field_tables, tables_index = self.generate_data(period, fields)
                self.sep_sid_tables.update({ period : field_tables })
                self.sep_sid_tables_index.update({ period : tables_index })

    def get_sep_field_table(self):
        pass

    def get_dir(self):
        pass

    def get_current():
        pass

    def get_standard_table_index():
        pass

    def get_section(self, end_date, assets_name, field, bar_count, period):
        def get_row_indexer(period, field, end_date, bar_count):
            # print(self.sep_sid_tables_index[period][field][0:5])7
            table_index = self.sep_sid_tables_index[period][field]
            
            index = table_index.index(end_date) + 1
            first_index = max(index - bar_count+1, 0)

            row_indexer = table_index[ first_index : index+1 ]
            return row_indexer

        table = self.sep_sid_tables[period][field]
        row_indexer = get_row_indexer(period, field, end_date, bar_count)

        return table.loc[row_indexer, assets_name]

    def generate_data(self, period, fields):
        def get_period_code(period):
            if period in MIN_PERIOD:
                arg = { 'minutes' : int(period.replace('MIN', '')) }
            else:
                if 'D' in period:
                    arg = { 'days' : 1 }
            return arg
        
        def generate_date(start_date, end_date, period, bar_num):
            print(period)
            dates = []
            date = start_date
            delta = datetime.timedelta( **get_period_code(period) )
            session_delta = datetime.timedelta( hours = 18, minutes = 30) 
            rest_delta =  datetime.timedelta( hours = 1, minutes = 30) 

            while  date < end_date:
            # for i in range(self.default_mimic_date_num):            
                if date.hour==11 and date.minute==30:
                    date = date + rest_delta
                elif date.hour == 15:
                    date = date + session_delta
                else:
                    date = date + delta
                    dates.append( date )
            print(len(dates))
            return dates

        bar_num = self.cal_bar_num(period)
        
        tables = {}
        tables_index = {}
        for field in fields:
            if field in PRICE:
                low = 2
                high = 50
            if field == TOR:
                low = 0.1
                high = 5
            if field == V:
                low = 10000
                high = 1000000
            
            table = np.random.uniform(
                low = low, 
                high = high, 
                size = [
                        bar_num, 
                        self.default_mimic_stock_num
                    ]
            )
            
            if period in MIN_PERIOD:
                start_date = self.default_start_date_minunte
                end_date = self.default_end_date_minute
            else:
                start_date = self.default_start_date_daily
                end_date = self.default_end_date_daily

            dates = generate_date(
                start_date, 
                end_date, 
                period,
                bar_num
                )                        
            table = pd.DataFrame(data = table, 
                                 index = dates, 
                                 columns = self.default_id)
            tables[field] = table
            tables_index[field] = list(table.index)
        
        return tables, tables_index

    def cal_bar_num(self, period):
        return  self.default_mimic_date_num*DAY_BAR_NUM[period]
    
        
class FinanceDataPort():
    def __init__(self) -> None:
        pass


class BarData():
    def __init__(self, data_port, start_date,  daily_mode=T1):
        self.data_port =data_port
        self.mode = daily_mode
        # self.date = datetime.datetime.fromisoformat(start_date)
        
    def initialize(self, periods, fields, action_period):
        self.periods = periods
        self.fields = fields

        self.data_port.initialize(periods, fields)

        self.date = {}
        self.action_period = action_period

    def get_table(self, field, period, sector='ALL', start_date=None, end_date=None):
        pass

    def history(self, assets, field, bar_count, period, trailing=False):
        '''
        each table correspond to a field for example
        {   
            'H' : dataframe1, 
            'C' : dataframe2
            }, 
        dataframe with asset id as column and date as rows
        '''
        if not trailing:
            try:
                history_table = self.data_port.get_section(
                    self.date[period], 
                    assets, 
                    field, 
                    bar_count, 
                    period)
            except:
                print('No history data available')

                return None
        else:
            pass

        return history_table
    
    def action_bar(self, assets, field):
        try:
            return self.data_port.get_section(
                self.date['action_period'], 
                assets, 
                field=field, 
                bar_count=1, 
                period=self.action_period)
        except:
            print('No action data available')
            return None
    
    def current(self, assets, field, period):
        try:
            return self.data_port.get_section(
                self.date[period], 
                assets, 
                field=field, 
                bar_count=1, 
                period=period)
        except:
            print('No current data available')
            return None

    def history_multifreq(self, assets, field, bar_counts, periods=None):
        multi_freq_bar = {}
        
        if periods is None:
            periods = self.periods
        
        for p in periods:
            try:
                history_table = self.data_port.get_section(
                    self.date[p], 
                    assets, 
                    field, 
                    bar_counts[p], 
                    p)
                multi_freq_bar[p] = history_table
            except:
                multi_freq_bar[p] = None

        return multi_freq_bar

    def expand_to(self, period):
        pass

    def contained_in(self, period):
        pass
    
    def update_date(self, date, clock_period):
        # cur_date = date.date()
        hour = date.hour
        minute = date.minute
        # self.date = {}
        # clock period is daily
        self.date['action_period'] = date

        if self.mode is T0:
            if hour == 0:
                for period in self.periods:
                    #minute frequncy
                    if period in MIN_PERIOD:
                        self.date[period] = date.replace(hour = 15)
                    #daily period
                    else:
                        self.date[period] = date

            # clock period is minute
            else:
                for period in self.periods:
                    #minute frequncy
                    if period in MIN_PERIOD:
                        #period shorter than clock period
                        if is_inner_period(period, clock_period):
                            self.date[period] = date

                        #period longer than clock period
                        else:                        
                            if minute % get_minute(period)  == 0:
                                self.date[period] = date
                    #daily period
                    else:
                        self.date[period] = date
        else:
            for period in self.periods:
                #minute frequncy
                last_date = date + datetime.timedelta(days=-1)
                if period in MIN_PERIOD:
                    self.date[period] = last_date.replace(hour = 15, minute=0)
                #daily period
                else:
                    self.date[period] = last_date


class FinanceData():
    def __init__(self, fin_data_port, dt_func):
        self.data_port = fin_data_port
        self.dt_func = dt_func
        pass

    def last(self, assets, fields):
        pass


class MarketData():
    def __init__(self,  bar_data, finance_data=None):
        self.finance_data_ = finance_data
        self.bar_data_ = bar_data

    def matched_history(self):
        '''
            return date matched finance data and bar data
        '''
        pass

    def date_matching(self):
        pass

    @property
    def bar_data(self):
        return self.bar_data_
    
    @property
    def finance_data(self):
        return self.finance_data_
    
    def update_date(self, date, clock_period):
        self.bar_data_.update_date(date, clock_period)
    

class Asset():
    def __init__(self) -> None:
        self.code = None
        self.name = None
        
        self.entry_price = None
        self.entry_share = None
        self.entry_date = None
        self.holding_day = 0


if __name__ == '__main__':
    from backtest.backtest import Clock
    data_port = DataPort()

    start_date = '2012-04-01'
    end_date = '2012-04-02'

    bar_data = BarData(
        data_port=data_port, 
        start_date=start_date
        )
    
    market_data = MarketData( bar_data = bar_data )
    
    clock_period = 'D'
    clock = Clock(start_date=start_date, end_date=end_date, period=clock_period)

    market_data.bar_data.initialize(
        periods = ['15MIN', '30MIN', 'D'],
        fields= ['C', 'O', 'H', 'L', 'V', 'TOR'],
        action_period = clock_period
        )
    
    sid = '000001'
    print(market_data.bar_data.data_port.sep_sid_tables_index['D']['C'])
    for date in clock:
        market_data.update_date(date, clock_period)
        current_bar = market_data.bar_data.current(
            [sid], 
            period ='D',
            field = 'C'
            )
        
        history_bar = market_data.bar_data.history(
            [sid],  
            field = 'C', 
            period = '15MIN', 
            bar_count=3
            )
        
        action_bar = market_data.bar_data.action_bar(
            [sid],  
            field = 'C')
        print(date)
        print(market_data.bar_data_.date)

    
'''
1.7日内只有一日冲涨停,但未封板，次日低走5个点，横盘3-4日
2.连板（3~7）回落中间价格站稳（4~7日）。
3.

周线 月线 Trailing
'''
