from google.cloud import storage
import pandas as pd

def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    # client = storage.Client()
    # data = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}")
    data = pd.read_csv('../raw_data/bitstampUSD.csv')
    # data = pd.read_csv('gs://bitcoin-prediction-01/data/bitstampUSD.csv')
    return data


def preprocessing_data(data, shift_size, h=1):
    data_pp = data[2798176:4727776]
    data_pp['Timestamp'] = pd.to_datetime(data_pp['Timestamp'], unit='s', origin='unix')
    data_pp = data_pp[['Open', 'Timestamp']].set_index("Timestamp").fillna(method='ffill')
    data_pp
    data_pp['diff_Open'] = data_pp['Open'].diff(h)
    data_pp['diff_Open'] = data_pp['diff_Open'].dropna()
    data_pp[f"t+{h}"] = data_pp['diff_Open'].shift(-h)
    for i in range(0, shift_size):
        data_pp[f't-{i}'] = data_pp['Open'].shift(i)
    data_shifted = data_pp.dropna()
    X = data_shifted.drop(columns=['Open', 'diff_Open', f"t+{h}"])
    y = data_shifted[f"t+{h}"]
    y[y > 0] = 1
    y[y <= 0] = 0
    return X, y, data_shifted
