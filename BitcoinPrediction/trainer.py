import joblib
from termcolor import colored
import mlflow
from BitcoinPrediction.data import ### xxx
from BitcoinPrediction.transfomers import ### transformerNaN , transformerHours... 
### si on décide de mettre toutes les transformations dans un fichier spécifique, sinon on laisse tout dans data ? ###
from BitcoinPrediction.utils import ###xxx
from memoized_property import memoized_property
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from google.cloud import storage
from BitcoinPrediction.params_gcp import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH, MODEL_NAME, MODEL_VERSION 
### modifier nom params_gcp en fonction de ce que nico aura créé ###


MLFLOW_URI = "https://mlflow.lewagon.co/" # Valider qu'on ne doit pas utiliser un autre URI que celui du wagon
EXPERIMENT_NAME = "bitcoin_hist_results"


class Trainer(object):
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y
        # for MLFlow
        self.experiment_name = EXPERIMENT_NAME

    def set_experiment_name(self, experiment_name):
        '''defines the experiment name for MLFlow'''
        self.experiment_name = experiment_name

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        preproc_pipe = Pipeline([
            ### ('fill na', transformerNaN()) ###
        ])
        
        self.pipeline = Pipeline([
            ('preproc', preproc_pipe),
            ('linear_model', LinearRegression()) ### changer avec SVM ou autre model en fonction...
        ])

    def run(self):
        self.set_pipeline()
        self.mlflow_log_param("model", "Linear") ### changer avec SVM ou autre model en fonction...
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
    N = xxx ### number of rows we want to try in our first training
    df = get_data(nrows=N)
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
