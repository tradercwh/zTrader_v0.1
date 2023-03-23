def get_section(df, sids, date_window):
    '''
        select from dataframe with given columne list name and row name list
    
    '''


    pass


def history_rolling(df, window_size):
    '''
        given a dataframe, return a new dataframe, the value is a np array of 
        multiple rows of the old dataframe.
    '''
    pass


def asset_finder(dfs, fields, sid, date_window):
    '''
        create a new dataframe of a given stock id, from table of given field names
    
    '''
    pass


def combine_table(dfs):
    '''

    '''

    pass


def apart_table(dfs):
    '''

    '''

    pass


def disassemble_table(df):
    pass


def sids_indexing_tables(dfs, fields):
    pass


def subperiod_merging(dfs):
    '''
        from tables of different period like day, hour, min, concat the value to np array
        in a single table
    '''
    pass


def index_from_date(date):
    '''
        find the row index give the date name

    '''
    
    
    pass


def calculate_least_date_num(period, candle_num):
    '''
        
        given period in minute, return row number in day talbe that insure there is candle_num
        just no less than the given candle_num

    '''
    
    pass