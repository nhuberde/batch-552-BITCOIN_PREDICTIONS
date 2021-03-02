from BitcoinPrediction.data import get_data
import pandas as pd

# Function to select a specific starting or ending date in the dataframe instead of indexes 

def select_date(data, date_start, date_end):
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s', origin='unix')
    data = data[['Open', 'Timestamp']].set_index("Timestamp").fillna(method='ffill')

    if date_start != None:
        if date_end != None:
            data = data[date_start:date_end].copy()
    else:
        data = data.copy()
        
    return data