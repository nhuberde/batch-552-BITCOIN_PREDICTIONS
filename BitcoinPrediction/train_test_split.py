def train_test_split(data, sample_size, shift_size, train_size):
    data_size = data.shape[0]
    sample = data.iloc[(data_size-sample_size):data_size]
    sample_pp = sample[['Open', 'Timestamp']].set_index("Timestamp").fillna(method='backfill')
    for i in range(1, shift_size+1):
        sample_pp[f't - {i}'] = sample_pp['Open'].shift(i)
    sample_shifted = sample_pp.dropna() 
    X = sample_shifted.drop(columns=['Open'])
    y = sample_shifted['Open']
    X_train = X.iloc[0:train_size]
    y_train = y.iloc[0:train_size]
    X_test = X.iloc[(train_size+1):(sample_size-shift_size)]
    y_test = y.iloc[(train_size+1):(sample_size-shift_size)]
    return X_train, X_test, y_train, y_test