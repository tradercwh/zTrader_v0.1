'''
the final purpose of this abstraction is to extract the core component 

that can be easily modified as an abstract input of the rest of the 

engine

'''
from datetime import date, timedelta


#--------------------------------------------------------------------------------

class FeatherReader():
    def __init__(self) -> None:
        pass


class DataPort():
    def __init__(self, reader) -> None:
        pass


class FinanceDataPort():
    def __init__(self) -> None:
        pass


class BarData():
    def __init__(self, data_port, dt_func):
        self.data_port =data_port
        self.dt_func = dt_func
        pass


class FinanceData():
    def __init__(self, fin_data_port, dt_func):
        self.data_port = fin_data_port
        self.dt_func = dt_func
        pass


class MarketData():
    def __init__(self, finance_data, bar_data):

        self.finance_data = finance_data
        self.bar_data = bar_data
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

#--------------------------------------------------------------------------------

class PositionTracker():
    '''
        control the percentage of the total money to buying asset. it should 
        double communicate with cycle manager
    
    '''
    def __init__(self) -> None:
        self.permit_pos = 0.5


class CycleManager():
    def __init__(self, asset, timing_method):

        self.timing_method = timing_method


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


class StrategyConfig():
    def __init__(self, max_hold_num, max_hold_period, max_budget) -> None:
        self._max_hold_num = max_hold_num
        self._max_hold_period = max_hold_period
        self._max_budget = max_budget
        
    @property
    def max_hold_num(self):
        return self._max_hold_num

    @property
    def max_hold_period(self):
        return self._max_hold_num

    @property
    def max_budget(self):
        return self._max_budget
    

class Strategy():
    def __init__(self) -> None:
        pass

    def select_and_order_new_asset(self):
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

    def update_holding_position(self):
        cycle_managers = []
        for cm in self.cycle_managers:
            cm.update_positions()
            self.recorder.record(t, action)

            if not cm.position.is_empty:
                cycle_managers.append(cm)
        
        self.cycle_managers = cycle_managers


#--------------------------------------------------------------------------------


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
    def __init__(self, calendar, start_date, end_date):
        self.calendar = calendar

        self.start_date = start_date
        self.end_date = end_date
        pass


class T1BackTestEngine():
    def __init__(self, strategy) -> None:
        pass
        self.strategy = strategy

    def run(self):
        # main loop
        for date in self.clock:
            self.strategy.position_tracker.update()

            if self.strategy.cycle_managers==[]:
                self.strategy.select_and_order_new_asset()

            else:
                self.strategy.update_holding_position()
                #execute sell order before late

                #check available cash execute, buy order on bar late from last day and today
                
                if self.strategy.position_tracker.order_new_asset:
                    self.strategy.select_and_order_new_asset()
                else:
                    pass

            #tracking capital change
            self.capital_tracker.update(date)


if __name__ == '__main__':
    '''

        input of the backtest engine:
        1. data file reader
        2. equity pool construce algorithm
        3. equity selection algorithm
        4. position control algorithm
        5. portfolio weighting algorithm
        6. cycle managing algorithm 
        
        the pipeline:
        1. prepare data
        2. the algorithm above consume the data
        3. the engine output csv file and report about the backtest

    '''
    def pool_construct(context, market_data):
        '''
            return list
        '''

        assets = []
        return assets

    def stock_select(context, market_section_data, num):
        '''
            return list
        '''

        assets = []
        return assets
    

    # will be the handle_portfolio method in next version
    def portfolio_method(dt, assets_data):
        weights = {
            '600688':1
        }
        
        return weights

    def position_control(dt, anchor_date, *kargs):
        ratio = 1
        return ratio

    # self: dt, assets, availble, por
    def cycle_management(
            dt, 
            assets, 
            current, 
            history_data, 
            available, 
            portfolio_method,
            config, 
            *kargs):

        '''
            the method decide how much should buy and how to ajust position of current holding equity

            dt : current date
            assets : dictionary, include hold asset, and selected new asset
            current : current price data from other source
            history_data : bar data and finance data of assets

            available : cash, when available is negative, sell equity
            portfolio_method : determing equity share weighting
            config : other constant paramters
        
            pipeline : propose demand then execute 

            return : actual buying and selling order, dictionary

            case 1. if no sell order, and no available, no buy order will be executed.
            case 2. have sell order, no available,      execute all new buy order
            case 3. have sell order, have available     ...
            case 4. no sell order, have available       ...

            notice that the return allowed/legal order : the cost must less than available
            there is several choices:
            1. finding the combination that can buy most number of equity
            2. Buy the minimum cost first./Sort by cost size
            3. Buy the high score first.
            4. Buy new asset first.
            5. Adjust with ratio that most close to the original weights
        '''

        hold_equity = assets['hold']
        recmd_equity = assets['recommend']

        buy_demand = {}
        for eq in hold_equity:
            eq.entry_date
            eq.share_num
            # get eq current investment value
            # if there is sell signal, execute sell order

            # to decide whether be full position of equity or just holding
            # update buy_demand

        weights = portfolio_method(assets_to_buy)
        # calculate how much share should buy of the reommended stock according
        # to the weights and the buy_demand

        # calculate total money needed to buy the assets
        # if the money needed exceed the available money
        # adjust the order

        legal_order = {
            'id': '600688',
            'action':'BUY',
            'shares':2,
            'mode':next_bar_late
            }

        return legal_order
        

    bar_reader = FeatherReader()
    finance_reader = FeatherReader()

    bar_data = BarData(bar_reader)
    finance_data = FinanceData(finance_reader)

    market_data = MarketData(bar_data, finance_data)

    portforlio_manager = PortfolioManager(algo = portfolio_method)
    position_controller = PositionController(algo = position_control)

    pool_constructor = StockPoolConstructor(algo = pool_construct)
    equity_selector = StockSelector(algo = stock_select)
    cycle_manager = CycleManager(algo = cycle_management)

    blotter = Blotter()
    recorder = Recorder()

    strategy = Strategy(
        portforlio_manager = portforlio_manager,
        position_control = position_controller,
        pool_constructor = pool_constructor,
        equity_selector = equity_selector,
        cycle_manager = cycle_manager,
    )

    engine = T1BackTestEngine()
    pf_results = engine.run(
                    start_date = None,
                    end_date = None,
                    data = market_data,
                    strategy = strategy,
                    blotter = blotter,
                    recorder = recorder,
                    clock = None,
                    output_config = None
            )
