from BitcoinPrediction.data import get_data
from BitcoinPrediction.preprocessing import preprocessing_data, features_target
from BitcoinPrediction.train_test_split import input_data
from BitcoinPrediction.utils import select_date
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from google.cloud import storage
# import joblib
# from termcolor import colored
# import mlflow
# from BitcoinPrediction.transfomers import ### transformerNaN , transformerHours... 
### si on décide de mettre toutes les transformations dans un fichier spécifique, sinon on laisse tout dans data ? ###
# from BitcoinPrediction.utils import xxx
# from memoized_property import memoized_property
# from mlflow.tracking import MlflowClient
# from BitcoinPrediction.params_gcp import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH, MODEL_NAME, MODEL_VERSION 



# MLFLOW_URI = "https://mlflow.lewagon.co/" # Valider qu'on ne doit pas utiliser un autre URI que celui du wagon
# EXPERIMENT_NAME = "bitcoin_hist_results"


# class Trainer(object):
#     def __init__(self, X, y):
#         """
#             X: pandas DataFrame
#             y: pandas Series
#         """
#         self.pipeline = None
#         self.X = X
#         self.y = y
#         # for MLFlow
#         self.experiment_name = EXPERIMENT_NAME

#     def set_experiment_name(self, experiment_name):
#         '''defines the experiment name for MLFlow'''
#         self.experiment_name = experiment_name
    
    #train_test_split
    def input_data(X, y, data_size, sample_size, shift_size, train_size, test_size, h=1, w=0):
        '''creates our train and test samples'''
        self.input_data = input_data

    def set_pipeline(self):
        """defines the pipeline """       
        self.pipeline = Pipeline([
            ('logisitic', LogisticRegression()) ### changer avec logisitic regr, SVC ou autre model ...
        ])

    def run(self):
        self.set_pipeline()
        self.mlflow_log_param("model", "Logistic") ### changer avec SVC ou autre model en fonction...
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on our dataset and return the accuracy"""
        y_pred = self.pipeline.predict(X_test)
        ### accuracy = compute_accuracy(y_pred, y_test) ### besoin du baseline model de Caroline
        self.mlflow_log_metric("accuracy", accuracy)
        return round(accuracy, 2)

    def save_model(self):
        """Saving our model into a .joblib format"""
        joblib.dump(self.pipeline, 'model.joblib')
        print(colored("model.joblib saved locally", "green"))

    def save_model_to_gcp(self):
        """Save our model into a .joblib and upload it on Google Storage /models folder
        HINTS : use sklearn.joblib (or jbolib) libraries and google-cloud-storage"""
        from sklearn.externals import joblib
        
        try:
            local_model_name = 'model.joblib'
            # saving the trained model to disk (which does not really make sense
            # if we are running this code on GCP, because then this file cannot be accessed once the code finished its execution)
            joblib.dump(self.pipeline, local_model_name)
            print("saved model.joblib locally")
            client = storage.Client().bucket(BUCKET_NAME)
            storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
            blob = client.blob(storage_location)
            blob.upload_from_filename(local_model_name)
            print("uploaded model.joblib to gcp cloud storage under \n => {}".format(storage_location))
        


        

    # MLFlow methods
    @memoized_property
    def mlflow_client(self):
        mlflow.set_tracking_uri(MLFLOW_URI)
        return MlflowClient()

    @memoized_property
    def mlflow_experiment_id(self):
        try:
            return self.mlflow_client.create_experiment(self.experiment_name)
        except BaseException:
            return self.mlflow_client.get_experiment_by_name(
                self.experiment_name).experiment_id

    @memoized_property
    def mlflow_run(self):
        return self.mlflow_client.create_run(self.mlflow_experiment_id)

    def mlflow_log_param(self, key, value):
        self.mlflow_client.log_param(self.mlflow_run.info.run_id, key, value)

    def mlflow_log_metric(self, key, value):
        self.mlflow_client.log_metric(self.mlflow_run.info.run_id, key, value)


if __name__ == "__main__":
    # Get and clean data
    df = get_data(nrows=sample_size)
    # ⚠️ alternatively use data from gcp with get_data_from_gcp
    df = clean_data(df)
    y = xxx ### to fill with Amélie's choice
    X = xxx ### to fill with Amélie's choice
    ### X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) ### to fill with Amélie's choice
    # Train and save model, locally and
    trainer = Trainer(X=X_train, y=y_train)
    trainer.set_experiment_name('First_training')
    trainer.run()
    accuracy = trainer.evaluate(X_test, y_test)
    print(f"accuracy: {accuracy}")
    trainer.save_model()
    trainer.save_model_to_gcp()
