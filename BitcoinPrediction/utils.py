from BitcoinPrediction.data import get_data
import pandas as pd

# Function to select a specific starting or ending date in the dataframe instead of indexes

def select_date(data, starting_date, ending_date):
    
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s', origin='unix')
    data = data[['Open', 'Timestamp']].set_index("Timestamp").fillna(method='ffill')
    
    if starting_date != None:
        if ending_date != None:
            data = data[starting_date:ending_date].copy()
    else:
        data = data.copy()
        
    return data 