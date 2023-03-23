''''
    three things to record:
        1. each atom order
        2. sessionize order of each asset
        3. total daily packet (perf)
        
'''
from __future__ import division

from collections import namedtuple, OrderedDict
from ..utils import dates_funcs


class Asset():
    def __init__(self,
                 sid,
                 asset_name,
                 exchange_info,
                 start_date,
                 end_date,
                 entry_date):
        self.sid = sid
        self.asset_name = asset_name 
        self.exchange_info = exchange_info
        self.start_date = start_date
        self.end_date = end_date
        self.entry_date = entry_date


class ConfirmOrder():
    def __init__(self, asset, amount, price, dt, close):
        self.asset = asset
        self.amount = amount
        self.price = price
        self.dt = dt
        self.close = close

    def to_dict(self):
        order_type = 'BUY' if self.amount >0 else 'SELL'
        
        return {
            'asset': self.asset.sid,
            'amount': self.amount,
            'price': self.price,
            'date': self.dt,
            'close': self.close,
            'order type' : order_type
        }


class Position(dict):
    '''
    holdings: {
            'id':{
            'entry_date':,
            'order':{
                'dt1' : {   
                            'transaction_price' :,
                            'amount' :,
                            'closed_price':,
                        },
                'dt2' : ...
                }
            }
        }

    '''
    def __init__(self, asset, *args, **kwargs):
        self.asset = asset

        self.amount = 0
        self.cost = 0
        self.retrive = 0

        self.orders = {}

        self.close = 0

    def amount_(self):
        return self.amount 

    def update(self, order):
        self.amount += order.amount

        self.close = order.close

        self.cost_delta = 0
        self.retrive_delta = 0

        self.delta = order.amount * order.price

        if order.amount > 0:
            self.cost += self.delta 
        
        if order.amount < 0:
            self.retrive += (-self.delta)

        if self.orders == {}:
            self.orders['entry_date'] =  order.dt
        
            self.orders['order'] = {}

        self.orders['order'].update(
            { 
                order.dt : {
                        'price' : order.price,
                        'amount' : order.amount,
                        'close' : order.close
                }
            }
        )
        
    def __repr__(self) -> str:
        message = 'amout : {}\ncost : {}\nclearance : {}\nclose price : {}'\
            .format(self.amount, self.cost, self.is_clearance(), self.close)
        return message
        
    def is_clearance(self):
        return self.amount == 0


class Positions(dict):
    def __init__(self, *args, **kwargs):
        self.cost = 0
        self.retrive = 0
        
    def __missing__(self, asset):
        return Position(asset)
    

class Portfolio():
    def __init__(self, start_date=None, capital_base=0.0):
        self.starting_cash = capital_base
        self.portfolio_value = capital_base
        self.returns = 0.0
        self.cash = capital_base
        self.positions = Positions()
        self.start_date = start_date
        self.positions_value = 0.0

    def get_portfolio(self):
        pass

    def weighting(self, new_asset=None):
        pass

    def __repr__(self):
        message = ''


class PositionTracker():
    '''
        cash flow book
        {
            'asset':{
                'dt':{
                    'cost':,
                    'retrive':,
                        },
            'dt2':{}
            },
        }

        约定：投入以及回收资金按照成交价格计算，市值按照当天收盘价计算
        投入/回收：手数*成交价格
        市值:更新手数后的手数*收盘价

    '''
    def __init__(self, capital_base) -> None:
        # self.positions = OrderedDict()
        # self.cost_book = {}
        self.portfolio = Portfolio(capital_base=capital_base)

        self.positions = self.portfolio.positions

        self.cash_ = self.portfolio.cash
        self.portfolio_value_ = self.portfolio.portfolio_value
        self.positions_value_ = self.portfolio.positions_value
        self.profit_ = 0

        self.daily_packet = {
            'cash' : [],
            'positions_value' : [],
            'portfolio_value' : [],
            'daily_return' : [],
            'profit' : [],
            'date' :[]
        }

        self.processed_transaction = {}
        self.trading_sessions = {}

        self.cost = 0
        self.retrive = 0

    def update_portfolio(self, clock_date):
        self.daily_packet['cash'].append(self.cash_)
        self.daily_packet['positions_value'].append(self.positions_value_)
        self.daily_packet['portfolio_value'].append(self.portfolio_value_)
        self.daily_packet['profit'].append(self.profit_)
        self.daily_packet['date'].append(clock_date)

        daily_return = self.portfolio_value_/self.portfolio.portfolio_value - 1
        self.daily_packet['daily_return'].append(daily_return)

        self.last_porfolio_value_ = self.portfolio_value_

        self.portfolio.cash = self.cash_
        self.portfolio.positions_value = self.positions_value_
        self.portfolio.portfolio_value = self.portfolio_value_

    def cumulate_portfolio(self):
        # update after hour
        cost = self.calcualte_cost()
        retrive = self.calculate_retrive()
        positions = self.calculate_positions_value()

        self.cash_ = self.cash_ - cost + retrive
        self.portfolio_value_ = self.cash_ + positions
        self.positions_value_ = positions
        self.profit_ = retrive + self.positions_value_ - cost

    def execute_transaction(self, order):
        if order.dt not in self.processed_transaction.keys():
            self.processed_transaction[order.dt]=[]
        # else:
        self.processed_transaction[order.dt].append(order.to_dict())

        asset = order.asset

        self.positions[asset] = self.positions[asset]
        position = self.positions[asset]

        position.update(order)  

        self.cumulate_portfolio()

        if position.is_clearance():
            print(position.orders.keys())
            entry_date = position.orders['entry_date']
            empty_date = order.dt

            if asset.sid not in self.trading_sessions.keys():
                self.trading_sessions[asset.sid] = {}

            self.trading_sessions[asset.sid][(entry_date, empty_date)] = position.orders['order']

            self.positions.pop(asset)

        self.cost += 0
        self.retrive += 0
        # self.cash_flow_book.update({})
    
    def calculate_retrive(self):
        retrive = 0.0
        for asset in self.positions:
            p = self.positions[asset]
            if p.delta > 0:
                retrive += abs(p.delta)
        return retrive

    def calcualte_cost(self):
        c = 0.0
        for asset in self.positions:
            p = self.positions[asset]
            if p.delta < 0:
                c += abs(p.delta)
        return c   

    def calculate_positions_value(self):
        v = 0.0
        for asset in self.positions:
            p = self.positions[asset]
            v += p.amount*p.close
        return v
    
    def record_daily(self, dt, data):
        self.daily_packet
        pass

    def __repr__(self) -> str:
        template = "cash : {cash}\n"\
                    "positions value : {positions_value}\n"\
                    "portfolio value : {portfolio_value}\n"\
                    "================================"
        
        return template.format(
            cash = self.portfolio.cash,
            positions_value = self.portfolio.positions_value,
            portfolio_value = self.portfolio.portfolio_value
        )

    def get_transaction_record(self, format='RAW'):
        if format == 'RAW':
            return self.processed_transaction
        
        if format == 'ASSET':
            '''
            {
                asset_id:{
                    'dt1':{},
                    'dt2':{},
                    ...
                }                    
            }
                
            '''
            # asset priority reorganized in asset name indexing
            record_ = {}
            for dt, orders in self.processed_transaction.items():
                for order in orders:
                    asset_id = order['asset']
                    if asset_id not in record_.keys():
                        record_[asset_id] = {}

                    record_[asset_id][dt] = {
                        'amount' : order['amount'],
                        'price' : order['price'],
                        'close' : order['close']
                    }

            return record_
        
    def get_trading_session(self):
        return self.trading_sessions
        

class TransactionStat():
    '''
        statistica about transaction action of each session and total
    '''
    def __init__(self) -> None:
        pass

    def position_stat(self, asset_trns, asset_close):
        # calcualte current position value, cost and retrive
        amount_ = 0
        cost_ = 0
        retrive_ = 0

        perf = {}
        transactions = []
        for (start_date, end_date) in asset_trns.keys():
            trns = asset_trns[(start_date, end_date)]

            session = {}
            session['amount'] = []
            session['price'] = []
            session['close'] = []
            session['position_value'] = []
            session['cost'] = []
            session['retrive'] = []
            session['dates'] = []
            session['profit'] = []

            amount = 0
            cost = 0
            retrive = 0
            action_price = trns[start_date]['price']
            
            for dt in dates_funcs.date_range(start_date, end_date):
                close = asset_close[dt]
                # print(dt)
                try:
                    action_price = trns[dt]['price']
                    price = trns[dt]['price']
                    delta_= trns[dt]['amount']
                    amount += delta_
                    # amount_ += delta_

                    if delta_ > 0:
                        cost += delta_ * price
                        # cost_ += delta_ * price
                    else:
                        retrive += (-delta_ *price)
                        # retrive += (-delta_ * price)
                except:
                    action_price = 0
                    pass
                
                session['amount'].append(amount)
                session['price'].append(action_price)
                session['close'].append(close)
                session['position_value'].append(amount * close)
                session['cost'].append(cost)
                session['retrive'].append(retrive)
                session['dates'].append(dt)
                session['profit'].append( amount * close + retrive - cost )

            transactions.append(session)
        
        return transactions, perf

    def from_file(self):
        pass

    def read_excel(self):
        pass

    def read_csv(self):
        pass            
    
    def to_csv():
        pass

    def to_excel():
        pass

    def to_tdx(self, trading_sessions):
        pass
        