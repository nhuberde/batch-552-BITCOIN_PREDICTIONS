from BitcoinPrediction.data import get_data
from BitcoinPrediction.preprocessing import preprocessing_data, features_target
from BitcoinPrediction.train_test_split import input_data
from BitcoinPrediction.utils import select_date
import numpy as np
# from sklearn.linear_model import LogisticRegression, RidgeClassifier
# from sklearn.ensemble import RandomForestClassifier
import statistics as stats
import math
# from sklearn.svm import SVC
# from sklearn.metrics import accuracy_score


# Function to initiate a Baseline model & predict its score :
def predict_score(model_init, X_train, X_test, y_train, y_test):
    model = model_init
    model = model.fit(X_train, y_train)
    results = model.predict(X_test)
    score = model.score(X_test, y_test) 
    return score, model.coef_

# Cross-val function to predict the average score of our Baseline model :
def cross_val(data, model_init=None,sample_size=1000, train_fraction=0.7, features_size=60, h=1, date_start=None, date_end=None):
    
    data = select_date(data, date_start, date_end)
    data_shifted = preprocessing_data(data, features_size, h)
    X, y, data_size = features_target(data_shifted, h)
    train_size = int(train_fraction*sample_size)
    test_size = sample_size - train_size
    
    
    r = math.floor((data_size-train_size)/test_size)
    intervals = range(0, r)
    reversed_intervals = reversed(intervals)
    results = []
    parameters = []
    
    for i in reversed_intervals:
        X_train, X_test, y_train, y_test = input_data(X, y, sample_size, data_size, train_size, test_size, h, w=i)
        score, params = predict_score(model_init, X_train, X_test, y_train, y_test)
        results.append(score)
        parameters.append(params)

    
    return dict({'mean_score':np.around(np.mean(results), 2),
                 'std':np.around(np.std(results), 2),   
                 'score_min':np.around(np.amin(results), 2),
                 'score_max':np.around(np.amax(results), 2), 
                 'n_fold':r}), np.around(np.mean(parameters, axis=0), 4)

# if __name__ == '__main__':
#     results = run_model(data)
#     print(results)