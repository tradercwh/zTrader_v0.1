'''
    clock only support minute and daily level frequency
    minute : date + 15 : 00 / 9 : 30
    daily  : date 00 : 00 
'''

import pandas as pd
import datetime

import os
import sys
sys.path.append(os.getcwd())
from common_var import *


class Blotter():
    def __init__(self) -> None:
        self.orders = {}        
        pass

    def order(self):
        pass


class Recorder():
    def __init__(self) -> None:
        pass


class Clock():
    def __init__(self, 
                 start_date, 
                 end_date, 
                 period):
        self.period = period

        if period in MIN_PERIOD:
            self.start_date = datetime.datetime.fromisoformat( start_date+' 09:30' )
            self.end_date = datetime.datetime.fromisoformat( end_date +' 15:00:00' )
        else:
            self.start_date = datetime.datetime.fromisoformat( start_date )
            self.end_date = datetime.datetime.fromisoformat( end_date )

        self.delta = datetime.timedelta( **self.get_arg() )
        self.session_delta = datetime.timedelta( hours = 18, minutes = 30) 
        self.rest_delta =  datetime.timedelta( hours = 1, minutes = 30) 

    def get_date_ele(self, datestr):
        date_ele = datestr.split('-')
        year = int( date_ele[0] )
        month = int( date_ele[1] )
        day = int( date_ele[2] )

        return year, month, day 

    def get_arg(self):
        if self.period in MIN_PERIOD:
            arg = { 'minutes' : int(self.period.replace('MIN', '')) }
        else:
            if 'D' in self.period:
                arg = { 'days' : 1 }
        return arg

    def __iter__(self):
        # year, month, day = self.get_date_ele(self.start_date)
        # self.date = datetime.datetime(year, month, day, 9, 30)
        self.date = self.start_date 
        return self

    def __next__(self):
        date = self.date
        if self.date <= self.end_date:
            # print(self.date)
            # print(self.end_date)
            if self.date.hour==11 and self.date.minute==30:
                self.date = self.date + self.rest_delta
            elif self.date.hour == 15:
                self.date = self.date + self.session_delta
            # else:
            self.date = self.date + self.delta
            return date
        else:
            raise StopIteration


class T1Engine():
    def __init__(self, strategy, market_data, clock) -> None:
        self.strategy = strategy
        self.blotter = strategy.blotter
        self.positions_tracker = strategy.positions_tracker
        
        self.market_data = market_data

        self.clock = clock

        self.recorder = Recorder()

    def run(self):
        for date in self.clock:
            self.market_data.update_date(
                ate)

            last_date = self.last_date(date)
            
            self.strategy.prepare_data()
            self.strategy.set_holding_position()
            self.strategy.select_stock()

            self.strategy.handle_portfolio()

            self.strategy.set_position()
            # self.portfolio.update_close_price()
            self.recorder.record(date)


if __name__ == '__main__':
    clock  = Clock(start_date='2018-09-16', end_date='2018-09-17', period='D')
    for date in clock:
        print(date)
        pass

