PRICE = ['O', 'H', 'C', 'L']
TOR = 'TOR'
V = 'V'

P5MIN_BAR_NUM = 48
P15MIN_BAR_NUM = 16
P30MIN_BAR_NUM = 8
P60MIN_BAR_NUM = 4

DAY_BAR_NUM = {
    "5MIN"  : P5MIN_BAR_NUM,
    "15MIN" : P15MIN_BAR_NUM,
    "30MIN" : P30MIN_BAR_NUM,
    "60MIN" : P60MIN_BAR_NUM,
    "D":1
}

MIN_PERIOD = ['5MIN', '15MIN', '30MIN', '60MIN']
D_PERIOD=['D', 'M', 'W', 'S']

def get_minute(period):
    return int( period.replace('MIN', '') )

def is_inner_period(period1, period2):
    if period1 in MIN_PERIOD and period2 in D_PERIOD:
        return True
    
    if period1 in MIN_PERIOD and period2 in MIN_PERIOD:
        p1 = get_minute(period1)
        p2 = get_minute(period2)

        if p1 <= p2:
            return True

    if period1 in D_PERIOD and period2 in D_PERIOD:
        if D_PERIOD.index(period1) <= D_PERIOD.index(period2):
            return True

    return False

T0 = 'T0'
T1 = 'T1'



    
