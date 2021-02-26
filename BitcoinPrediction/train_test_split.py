from BitcoinPrediction.data import get_data, preprocessing_data


def input_data(data, sample_size, shift_size, train_size, h=1, w=0):
    
    X, y, data_shifted = preprocessing_data(data, shift_size, h)
    
    data_size = data_shifted.shape[0]
    sample_X = data_shifted.iloc[(data_size-sample_size-w):data_size-w]
    sample_y = data_shifted.iloc[(data_size-sample_size-w):data_size-w]

    X_train = sample_X.iloc[0:train_size]
    y_train = sample_y.iloc[0:train_size] 
    
    X_test = sample_X.iloc[(train_size+h-1):(sample_size-shift_size)]
    y_test = sample_y.iloc[(train_size+h-1):(sample_size-shift_size)] 
    
    
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = input_data()
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)