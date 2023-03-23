from .protocal import *
import pprint


def test_execute_order():
    asset = Asset(
            sid='600288',
            asset_name='fang.zheng.ji.tuan',
            exchange_info='SZ',
            start_date='20130212',
            end_date='20181101',
            entry_date='20160206')

    order1 = ConfirmOrder(
        asset,
        amount=100,
        price=4.34,
        dt = '20181101',
        close = 4.11
    )


    order2 = ConfirmOrder(
        asset,
        amount=100,
        price=4.7,
        dt = '20181111',
        close = 4.2
    )

    order3 = ConfirmOrder(
        asset,
        amount=-200,
        price=5,
        dt = '20181120',
        close = 4.4
    )
    

    order4 = ConfirmOrder(
        asset,
        amount=200,
        price=5.2,
        dt = '20181220',
        close = 4.9
    )

    close_price = {asset : 4.11}

    tracker = PositionTracker(capital_base=10000)


    tracker.execute_transaction(order1)
    print(tracker)
    print(tracker.positions[asset].orders)
    
    tracker.execute_transaction(order2)
    print(tracker)
    print(tracker.positions[asset].orders)

    tracker.execute_transaction(order3)
    print(tracker)
    print(tracker.positions[asset].orders)

    print(tracker.positions.keys())

    tracker.execute_transaction(order4)
    print(tracker)
    print(tracker.positions[asset].orders)

    print(tracker.positions.keys())


def date_range_str(start, end):

    dates = pd.date_range(start=start, end=end)

    str_dates = [str(d).split(' ')[0].replace('-','') for d in dates]

    return str_dates


def geometric_brownian(start, end, show=True):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # Define the parameters of the model
    mu = 0.1
    sigma = 0.2
    S0 = 100

    # Define the start and end dates
    start_date = start
    end_date = end

    # start_date = '1/1/2020'
    # end_date = '31/12/2020'

    # Define the time interval and number of steps
    delta_t = 1/252
    steps = pd.date_range(start=start_date, end=end_date, freq='D').size

    # Generate the random increments
    Z = np.random.normal(0, 1, size=steps)
    delta_S = mu * delta_t * S0 + sigma * np.sqrt(delta_t) * S0 * Z

    # Generate the stock prices
    prices = S0 + np.cumsum(delta_S)

    # Create a pandas dataframe with the dates and prices
    dates = pd.date_range(start=start_date, end=end_date)
    # print(dates[0])
    df = pd.DataFrame({'Date': dates, 'Price': prices})

    # Set the date column as the index
    df.set_index('Date', inplace=True)

    if show:
        # Plot the stock prices over time
        plt.plot(df.index, df['Price'])

        # Set the title and axis labels
        plt.title('Realistic Stock Data')
        plt.xlabel('Date')
        plt.ylabel('Price')

        # Show the plot
        plt.show()

    str_dates = [str(d).split(' ')[0].replace('-','') for d in dates]

    return dict(zip(str_dates, prices))


def test_sequence_order(start='2022-1-1', end='2022-1-30'):
    import random

    close = geometric_brownian(show=True, start=start, end=end)
    date = close.keys()

    asset = Asset(
            sid='600288',
            asset_name='fang.zheng.ji.tuan',
            exchange_info='SZ',
            start_date='20130212',
            end_date='20181101',
            entry_date='20160206')

    tracker = PositionTracker(capital_base=50000)
    trns_stats = TransactionStat()

    for dt in date:
        order_dice = random.randrange(0, 10)
        if order_dice < 3:
            buy_dice = random.randrange(0, 10)
            c = round(close[dt], 2)
            price =  round(c * (1 + random.uniform(-0.1, 0.1)), 2)
            print(price, c)
            if buy_dice < 4:
                order = ConfirmOrder(
                        asset,
                        amount=200,
                        price=price,
                        dt = dt,
                        close =c
                    )
                if tracker.cash_ > 200 *price:

                    print(dt+' buy ')
                    tracker.execute_transaction(order)
                    print(tracker.positions[asset])

            # print(tracker)
            else:
                order = ConfirmOrder(
                        asset,
                        amount=-200,
                        price=price,
                        dt = dt,
                        close =c
                    )
                if tracker.positions[asset].amount >= 200:
                    print(dt+' sell ')
                    tracker.execute_transaction(order)
                    # print(tracker)
                    print(tracker.positions[asset])
            print('\n')

            tracker.update_portfolio(dt)
    # print(tracker.processed_transaction)
    # print(tracker.get_transaction_record(format='ASSET'))
    # pprint.pprint(tracker.get_trading_session())

    stat = trns_stats.position_stat(tracker.get_trading_session()['600288'], close)
    pprint.pprint(tracker.daily_packet)

def tracker_record():
    '''
        on date with order
        {
            'dt':{
                'asset_id':{
                    'amount':,
                    'price':,
                    'close':,
                    }
                }
        }

        all date
        {
            cash:{'dt0':,},
            positions_value:{'dt0':,},
            portfolio_value:{'dt0':,},
            daily_return:{'dt0':,},
            profit:{'dt0':,},
        }

        asset index
        {
            asset_id:{
                'sections':{ '20210202-20210302', ... },
                'order':{
                    'dt1':{},
                    'dt2':{},
                    ...
                }                    
            }
        }
    '''
    pass

def blotter_stat():
    '''
    '''
    pass


if __name__ == '__main__':
    # test_execute_order()
    # close = geometric_brownian(show=False)
    # print(close)
    test_sequence_order(start='2020-1-1', end='2021-3-2')