import mlflow
from mlflow.tracking import MlflowClient
EXPERIMENT_NAME = "bitcoin_hist_results"

# Indicate mlflow to log to remote server
### mlflow.set_tracking_uri("xxxxx") ### à remplir

client = MlflowClient()

experiment_id = client.create_experiment(EXPERIMENT_NAME)

### buddy_name = "xxx" ### A remplir par le team member faisant un entrainement à retenir

if not yourname:
    print("Please provide your name as a log parameter")

for model in ["linear", "SVM"]:
    run = client.create_run(experiment_id)
    ### client.log_metric(run.info.run_id, "metrics", xxx) ### remplir le nom de la metrics (ex : rmse) et sa valeur (ex : 4.5)
    ### client.log_param(run.info.run_id, "model", xxx) ### remplir le nom du model (ex : linear regression) 
    ### client.log_param(run.info.run_id, "buddy_name", xxx) ### remplir avec votre nom
