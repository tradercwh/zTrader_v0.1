import pandas as pd

def date_range(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date)

    str_dates = [str(d).split(' ')[0].replace('-','') for d in dates]

    return str_dates