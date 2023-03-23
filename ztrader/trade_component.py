'''
the final purpose of this abstraction is to extract the core component 

that can be easily modified as an abstract input of the rest of the 

engine



'''

from datetime import date, timedelta


class FeatherReader():
    def __init__(self) -> None:
        pass


class Clock():
    def __init__(self, calendar, start_date, end_date):
        self.calendar = calendar

        self.start_date = start_date
        self.end_date = end_date
        pass

    def __iter__(self):
        self.daterange()

    def daterange(self):
        for n in range(int((self.end_date - self.start_date).days)):
            yield self.start_date + timedelta(n)


class DataPort():
    def __init__(self, reader) -> None:
        pass

    def can_trade_list(self, dt):
        pass

    def get_current(self):
        pass

    def get_history(self):
        pass


class FinanceDataPort():
    def __init__(self) -> None:
        pass


class BarData():
    def __init__(self, data_port, dt_func):
        self.data_port =data_port
        self.dt_func = dt_func
        pass

    def get_section(self, asset_list, freq, bar_num):
        pass

    def history(self, asset, freq, bar_num):
        pass

    def current(self, asset):
        pass


class FinanceData():
    def __init__(self, fin_data_port, dt_func):
        self.data_port = fin_data_port
        self.dt_func = dt_func
        pass

    def get_section():
        pass

    def history():
        pass

    def current():
        pass


class MarketData():
    def __init__(self, finance_data, bar_data):

        self.finance_data = finance_data
        self.bar_data = bar_data
        pass


    def get_section():
        pass


class Blotter():
    def __init__(self) -> None:
        self.orders = {}
        
        pass

    def order(self):
        pass

    
class Asset():
    def __init__(self) -> None:
        self.code = None
        self.name = None
        self.cur_price = None
        self.entry_price = None
        self.entry_share = None
        self.entry_date = None
        self.holding_day = 0


class PositionTracker():
    '''
        control the percentage of the total money to buying asset. it should 
        double communicate with cycle manager
    
    '''
    def __init__(self) -> None:
        self.permit_pos = 0.5

    def update(self, method=None, ref_targets=None):
        if method is None:
            return self.permit_pos
        
        else:
            self.permit_pos = method(self.permit_pos, ref) 


            return self.permit_pos


class CycleManager():
    def __init__(self, asset, timing_method):

        self.timing_method = timing_method


    def update_positions(self):
        self.hold_day+=1
        amount = self.timing_method(
            self.asset.entry_price,
            self.asset.entry_shares,
            self.asset.hold_day, 
            self.asset.price_history, 
            self.asset.current_price)
        
        self.hold_day += 1
        self.asset.hold_share += amount

        if amount<0:
            order = 'SELL'
        if amount>0:
            order = 'BUY'
        if amount==0:
            order = None
        
        return order, abs(amount)


class PortfolioManager():
    def __init__(self) -> None:
        self.assets = []

    def weighting(self, new_asset=None):
        pass


class Capital():
    def __init__(self, initial_cash, initial_position) -> None:
        self.cash = initial_cash
        self.position = initial_position
        self.cost = 0

    def update():
        # calculate holding capital
        c = 0
        for eq in self.assets:
            c += eq.cur_price * eq.hold_share
        
        self.capital = self.cash + c - self.cost - self.tax 

        pass




class StockSelector():
    def __init__(self):
        pass

    def select(self):
        pass




class PositionController():
    def __init__(self):
        pass


class StockPoolConstructor():
    def __init__(self):
        pass


class TimingStrategy():
    def __init__(self) -> None:
        pass


class Strategy():
    def __init__(
                self,
                pool_construct_method,
                stock_select_method,
                timing_algorithm,
                position_strategty,
                portfolio_weighting_algorithm,
                ):

        
        self.pool_construct_method = pool_construct_method
        self.stock_select_method = stock_select_method
        self.timing_algorithm = timing_algorithm

        self.position_strategty = position_strategty
        self.portfolio_weighting_algorithm = portfolio_weighting_algorithm

        self.action = None

        self.cycle_managers = []

        self.pool_constructor = StockPoolConstructor()
        self.stock_selector = StockSelector()
        self.porfolio = PortfolioManager()

        self.position_tracker = PositionTracker()
        self.capital_tracker = Capital()

        self.recorder = Recorder()
        pass
        
    def run_backtest(
                self, 
                market_data,
                market_infor,
                init_capital,
                start_date,
                end_date,
                order_mode,
                on_bar
                ):
        '''
        market_infor : including tax rate, equity type.
        order_mode : 尾盘买入或者开盘价买入
        on_bar : If False, action is on next bar
    

        '''
        # need to consider next bar action or action delate. update captial
        
        def select_and_order_new_asset():
            stock_pool = self.pool_constructor.cunstruct_stock_pool()

            if stock_pool is not None:
                self.select_and_weighting()

                self.order_targets(lots)

                for t in lots:
                    self.cycle_managers.append( self.cycle_manager(t) )
                    self.recorder.record(t, action)

                self.position_tracker.update(self.cycle_managers)      
            else:
                pass
        
        # main loop
        for date in self.clock:
            if self.cycle_managers==[]:
                select_and_order_new_asset()

            else:
                cycle_managers = []
                for cm in self.cycle_managers:
                    cm.update_positions()
                    self.recorder.record(t, action)

                    if not cm.position.is_empty:
                        cycle_managers.append(cm)
                
                self.cycle_managers = cycle_managers

                self.position_tracker.update(self.cycle_managers)
                
                if self.position_tracker.order_new_asset:
                    select_and_order_new_asset()

                else:
                    pass

            #tracking capital change
            self.capital_tracker.update(date)

    def select_and_weighting(self):
        stock_to_buy = self.stock_selector.select(stock_pool)
        # it need to insure that there is enough money to buy the
        # selected stock and need to confirm the order ordering:
        # buy after sell or sell after buy
        stock_to_buy = self.manage_order(stock_to_buy, budget)

        weights = self.portfolio.weighting(self.current_asset, stock_to_buy)
        positions = self.position_tracker.target_position()
        
        lots = self.position_tracker.calcualte_lots(positions, weights)

        return lots

    def run(self):
        pass



