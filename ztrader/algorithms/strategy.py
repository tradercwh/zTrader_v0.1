
from protocal import PositionTracker


class T1Strategy():
    '''
        the available cash and set position method need bar data up to now.
    '''
    def __init__(
                self, 
                market_data, 
                capital_base = None,
                set_position=None,
                set_holding_position=None,
                select_stock=None,
                portfolio_weighting=None,
                record_attribute=None,
                other_arg = None 
                ):
        self.positions_tracker = PositionTracker()
        
        self.market_data = market_data
        self.assets_data = None

        # temp dictionary for proposed sell/buy order
        self.temp_buy_order = []
        self.temp_sell_order = []
        
        self.stock_selected = []
        self.asset_to_order = []

        self.executed_orders = []

        self.set_position = set_position
        self.set_holding_position = set_holding_position
        self.select_stock = select_stock
        self.portfolio_weighting = portfolio_weighting

        self.record_attribute_ = record_attribute

    def prepare_data(self):
        holded_assets = self.positions_tracker.holdings

        self.assets_data = \
            self.market_data.bar_data.data_history_t1(self.holded_asset)
        
        self.assets_transaction = \
            self.positions_tracker.holdings_record[holded_assets]
        
    def set_holding_position_(self):
        for asset in self.portfolio.assets:
            # query last holding history and 
            # data history with given bar num
            #             
            asset_order = \
                self.set_holding_position( self.asset_data, self.assets_transaction ) 

            if asset_order.type == 'SELL':
                self.temp_sell_order.update( { asset : asset_order })

            if asset_order.type == 'BUY':
                self.temp_buy_order.update( { asset : asset_order } )

    def select_stock_(self):
        self.stock_selected.update(
            { self.dt : self.select_stock(self.market_data) }
            )
        
    def portfolio_weighting_(self, assets):
        assets_data = self.get_assets_history(assets)
        self.weighting = self.portfolio_weighting(assets_data)

    def handle_portfolio_(self):
        def lighten_positions():
            # ======================
            # adjust positions after sell 
            # order executed onbar
            # 
            # calculate total selling 
            # value and average value
            # 
            # calculate share amount to 
            # sell for each holding assets
            # ======================
            # 
            # update last day pvalue after sell 
            # on bar estimated from last bar        
            p_value = self.positions_tracker.position_value

            # last day estimated target value 
            tp_value = self.target_position_value 
            if tp_value < p_value:

                lighten_value = p_value - tp_value
                lighten_orders =
                
                
                self.lighten_on_average(lighten_value)

                return lighten_orders
            else:
                return None

        if self.trade_day >= 2:
            for order in self.temp_sell_order:
                self.execute_transaction(order)

            lighten_orders = lighten_positions()
            # ======================
            # execute end bar sell order
            # ======================
            for order in lighten_orders:
                # if True:
                self.execute_transaction(order)

        weights = self.portfolio_weighting_(
            self.assets_to_order, 
            self.market_data.bar_data)
        # ======================
        # adjust the buy order 
        # and execute
        # ======================

        available = self.positions_tracker.cash
    
        if available>0:
            self.temp_buy_order = self.calculate_buy_order(
                weights, 
                self.temp_buy_order, 
                self.stock_selected[self.dt]
                )
            
        # ======================
        # execute buy orders
        # ======================
        for order in self.temp_buy_order:
            self.execute_transaction(order)

    def set_position_(self):
        position_ratio = \
            self.set_position(self, self.market_data.ref_data)
        
        self.target_position_value = \
            self.positions_tracker.calculate_position(position_ratio)

    def lighten_on_average(self, lighten_value):
        #execute all sell order update portfolio
        #how to determine selling price ???
        holdings_num = self.holdings_num
        avg = math.ceil(lighten_value/ holdings_num)

        orders = {
            asset : \
                self.calculate_sell_order(asset, avg) for \
                    asset in self.portfolio.asset}

        return orders

    def get_assets_history(self, assets):
        assets_data = {asset : 
                self.market_data.bar_data.data_history(asset)\
                for asset in assets}
        
        return assets_data
    
    def calculate_sell_order(self):
        pass

    def calculate_buy_order(self):
        pass

    def set_max_position(self):
        pass

    def set_max_holding_period(self):
        pass

    def set_max_holdings_num(self):
        pass

    def to_confirm_order(self, dict):
        pass

    def round_amount(self, amount):
        pass

    def get_current(self, assets, field):
        pass

    def add_execute_order(orders):
        pass

    def execute_transaction(self, asset, order):
        self.positions_tracker.execute_transaction(asset, order)
        self.add_execute_order(asset, order)
