'''

the app run automatically after trading hour

'''

BEIJING_TIME_FLAG=15


import datetime


import __init__
from trade_component import *


stock_selector = StockSelector()


def main():
    '''

        1.update market data

        2.check whether there is stock position go to zero. if so return 

        recommendation stock with number set in configure file.  
    
    '''
    time_n = datetime.datetime.now()
    hr_n = time_n.hour
    
    if hr_n >= BEIJING_TIME_FLAG:
        print(" running stock selector ")

        stock_selector.select()

    pass



if __name__=='__main__':
    main()
