from BitcoinPrediction.data import get_data
from BitcoinPrediction.utils import select_date


# Function to produce a new dataframe provinding the difference 
# between the current data compared to the shifted data (by our prediction horizon h)

def preprocessing_data(data, shift_size, h):
    
    data_pp = data.copy()
    data_pp['diff_Open'] = data_pp['Open'].diff(h)
    data_pp['diff_Open'] = data_pp['diff_Open'].dropna()
    data_pp[f"t+{h}"] = data_pp['diff_Open'].shift(-h)
    
    for i in range(0, shift_size):
        data_pp[f't-{i}'] = data_pp['Open'].shift(i)
    data_shifted = data_pp.dropna()
    
    return data_shifted


def features_target(data_shifted, h):
    
    X = data_shifted.drop(columns=['Open', 'diff_Open', f"t+{h}"])
    y = data_shifted[f"t+{h}"].copy()
    y[y > 0] = 1
    y[y <= 0] = 0
    
    data_size = data_shifted.shape[0]
    
    return X, y, data_size