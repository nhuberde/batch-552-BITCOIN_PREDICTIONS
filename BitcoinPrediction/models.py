# For the selection of models
from sklearn.linear_model import LogisticRegression
from BitcoinPrediction.train_test_split import input_data
from sklearn.metrics import accuracy_score
from BitcoinPrediction.data import get_data, preprocessing_data

def run_model():
    X_train, X_test, y_train, y_test = input_data(data, sample_size, shift_size, train_size, h=1, w=0)
    model = LogisticRegression()
    model = model.fit(X_train, y_train)
    results = model.score(X_test)
    return results
    print(f"Accuracy:{accuracy_score(y_test, results)}")

# if __name__ == '__main__':
#     results = run_model(data)
#     print(results)