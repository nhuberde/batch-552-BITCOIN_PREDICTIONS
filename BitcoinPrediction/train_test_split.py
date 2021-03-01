from BitcoinPrediction.data import get_data
from BitcoinPrediction.preprocessing import preprocessing_data, features_target


def input_data(X, y, data_size, sample_size, shift_size, train_size, test_size, h=1, w=0):    
 

    sample_X = X.iloc[data_size-(test_size * w + sample_size) : data_size - (test_size * w)]
    sample_y = y.iloc[data_size-(test_size * w + sample_size) : data_size - (test_size * w)]
    
    X_train = sample_X.iloc[0:train_size]
    y_train = sample_y.iloc[0:train_size]
    X_test = sample_X.iloc[(train_size+h-1):(sample_size-shift_size)]
    y_test = sample_y.iloc[(train_size+h-1):(sample_size-shift_size)]
    
    return X_train, X_test, y_train, y_test


# if __name__ == '__main__':
#     X_train, X_test, y_train, y_test = input_data(X, y, data_size, sample_size, shift_size, train_size, test_size, h=1, w=0)
#     print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)