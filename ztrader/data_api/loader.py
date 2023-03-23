class NormalLoader():    
    def load_from_csv():
        '''
            option1 : load all stock csv file at once, separate the field, then concat to 
                        new table with stock id as columne, date as rows.

            option2 : just load stock from the list output from stock pool constructor.
        
        '''


        pass


class DLLoader():
    def load_from_csv():
        '''
        write a python code to
            load all stock csv, create field table, then create batch of dimension : 
                case 1: single stock history with given window size as training sample
                        N * W
                case 2: a snapshot of the whole market with a given date and given window
                        size then dim would be N * M * w 
                in all case N for batch size

        From ChatGPT:

        import pandas as pd
        import numpy as np

        # Define function to load all stock CSVs
        def load_stock_csvs(csv_directory):
            """
            Load all CSVs in a directory into a dictionary of Pandas DataFrames.
            """
            stock_data = {}
            for csv_file in csv_directory.glob("*.csv"):
                # Get the stock name from the filename
                stock_name = csv_file.stem
                # Load the CSV into a Pandas DataFrame
                stock_df = pd.read_csv(csv_file)
                # Set the index to be the date
                stock_df.set_index("date", inplace=True)
                # Add the DataFrame to the dictionary
                stock_data[stock_name] = stock_df
            return stock_data

        # Define function to create field table
        def create_field_table(stock_data):
            """
            Create a field table from a dictionary of stock DataFrames.
            """
            # Concatenate all of the stock DataFrames into one DataFrame
            all_data = pd.concat(stock_data.values(), axis=1)
            # Create a multi-level column index
            all_data.columns = pd.MultiIndex.from_product([stock_data.keys(), all_data.columns.levels[1]])
            # Drop any rows with missing data
            all_data.dropna(inplace=True)
            return all_data

        # Define function to create batches for case 1
        def create_case1_batches(data, window_size, batch_size):
            """
            Create batches of data for case 1: single stock history with given window size as training sample.
            """
            # Choose a random stock and start date for each batch
            stock_names = data.columns.levels[0]
            start_dates = data.index[window_size:-1]
            while True:
                # Choose a random batch of stocks and start dates
                stocks = np.random.choice(stock_names, size=batch_size)
                starts = np.random.choice(start_dates, size=batch_size)
                # Create the batch of data
                batch = np.empty((batch_size, window_size))
                for i, (stock, start) in enumerate(zip(stocks, starts)):
                    end = start + pd.Timedelta(days=window_size)
                    batch[i] = data[stock]["close"][start:end].values
                yield batch

        # Define function to create batches for case 2
        def create_case2_batches(data, date, window_size, batch_size):
            """
            Create batches of data for case 2: a snapshot of the whole market with a given date and given window size.
            """
            # Choose a random batch of stocks
            stock_names = data.columns.levels[0]
            stocks = np.random.choice(stock_names, size=batch_size)
            # Create the batch of data
            batch = np.empty((batch_size, len(stock_names), window_size))
            for i, stock in enumerate(stocks):
                start = date - pd.Timedelta(days=window_size-1)
                end = date
                batch[i] = data[stock]["close"][start:end].values
            yield batch

        # Load all stock CSVs
        csv_directory = Path("path/to/csv/directory")
        stock_data = load_stock_csvs(csv_directory)

        # Create field table
        field_table = create_field_table(stock_data)

        # Example usage of create_case1_batches
        case1_batches = create_case1_batches(field_table, window_size=30, batch_size=64)
        batch = next(case1_batches)
        print(batch.shape)  # (64, 30)

        # Example usage of create_case2_batches
        case2_batches = create_case2

        '''

        pass