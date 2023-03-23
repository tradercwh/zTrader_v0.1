
'''

panel_data = get_panel_data_from_dfcf()

price_data = panel_data['price']

vol_data = panel_data['vol_infor']

trigger_func(panel_data)

trigger = Timer(interval, all_above)


'''

import pyttsx3

from threading import Timer
from functools import partial

from selenium import webdriver
from selenium.webdriver.common.by import By

PRICE = "price"
VOL_INFOR = "vol_infor"
SID = "stock_id"


EXCHANGE_NAME={
    'sz':['000', '002', '003'],
    'sh':['600', '601', '603','605']
}

def exchange_mapping(sid):
    head = sid[0:3]
    if head in EXCHANGE_NAME['sz']:
        return 'sz'
    if head in EXCHANGE_NAME['sh']:
        return 'sh'
    else:
        return None


def price_rate():
    '''
    '''
    pass


def price_threshold():
    '''
    '''
    pass


def atr_variation():
    '''
    '''
    pass


def macd_crossing():
    '''
    '''
    pass


def kdj():
    '''
    '''
    pass


def sid_fromfile(filepath):
    sid = [sid.strip for sid in open(filepath).readlines()]
    return sid


class PanelFetcher():
    def __init__(self):

        self.panel_datas={}
        self.stock_ids=[]

    def get_update(self, stock_id):
        pass


class DFCFScrawler(PanelFetcher):
    '''
        scrawling data from dong fang cai fu web site
    
    '''
    def __init__(self):
        super().__init__()
        
        self.HTML_BASE='http://quote.eastmoney.com/'
        
        self.ele_clalss = 'blinkred'

        self.drivers = []
        self.opt = webdriver.ChromeOptions()
        self.opt.headless = True

    def initialize(self, sids):

        for sid in sids:
            self.get_url(sid)
            
            d = webdriver.Chrome(options=self.opt)
            d.get(self.get_url(sid))
            
            self.drivers.update({sid : d})
        
    def get_update(self, stock_id):
        cur_panel_data = self.get_current_(stock_id)

        if stock_id not in self.stock_ids:
            self.panel_datas.update(
                {
                    SID : {
                        PRICE:[],
                        VOL_INFOR:[]
                    }
                })

            cur_price = cur_panel_data[PRICE]
            cur_vol_infor = cur_panel_data[VOL_INFOR]

            self.panel_datas[stock_id][PRICE].append(cur_price)
            self.panel_datas[stock_id][VOL_INFOR].append(cur_vol_infor)

    def get_url(self, stock_id):
        url_sid = self.HTML_BASE + exchange_mapping(stock_id) + stock_id + '.html'
        return url_sid

    def get_current_(self, stock_id):
        sid_url_driver = self.drivers['stock_id'] 
        ele = sid_url_driver.find_element(By.CLASS_NAME, self.ele_clalss)
        price = float(ele.text)

        


class PanelWatcher():
    def __init__(
        self,
        stock_ids,
        fetcher,
        trigger_funcs,
        time_interval,
        alarm_type=None,
        foreground_music=None
        ):

        self.stock_ids = stock_ids

        self.fetcher = fetcher
        self.trigger_funcs = trigger_funcs
        self.time_interval = time_interval

        self.alarm_type = alarm_type

    def initialize(self):
        self.fetcher.initialize()

    def start_(self):
        while True:
            self.verify_conditions()

    def verify_conditions(self):
        def loop_trigger():
            for sid in self.stock_ids:
                self.fetcher.get_update(sid)
                panel_data = self.fetcher.panel_datas[sid]
                for f in self.trigger_funcs:
                    if f(panel_data):
                        self.alarm(sid, f.__doc__)

        t = Timer(self.time_interval, loop_trigger)
        t.start()

    def alarm(self, sid, message):
        '''
            use multiprocess to play two sound
        '''


        def play_text(fgrd_sound):

            text = "{} {}".format(sid, message)
            

        def play_background():
            pass
        pass


if __name__ == "__main__":
    sid = sid_fromfile("watch_list.txt")
    fetcher = DFCFScrawler()
    trigger_funcs = [partial(price_rate)]
    time_interval = 10

    panel_watcher = PanelWatcher(
        sid,
        fetcher,
        trigger_funcs,
        time_interval
    )

    panel_watcher.start_()


