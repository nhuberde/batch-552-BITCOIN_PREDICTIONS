from google.cloud import storage
import pandas as pd

def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    client = storage.Client()
    # data = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}")
    # data = pd.read_csv('../raw_data/bitstampUSD.csv')
    data = pd.read_csv('gs://bitcoin-prediction-01/data/bitstampUSD.csv')
    return data


def clean_data(data, test=False):
    data = data.copy()
    data = data[2798176:4727776]
    data = data.drop(columns=['High', 'Low', 'Close', 'Volume_(BTC)', 'Volume_(Currency)', 'Weighted_Price'])
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s', origin='unix')
    data_test = data_sample[["Timestamp", "Open"]]
    data = data.fillna(method='ffill')
    return data

if __name__ == '__main__':
    data = get_data()
    print(data.shape)
