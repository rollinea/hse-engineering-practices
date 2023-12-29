import sys
from prefect import flow, task
import gdown
import pickle

sys.path.append("~/prefect")
from utils.preprocessing import load_data, feature_engineering, create_dataset
from utils.training import cv
from sklearn.metrics import roc_auc_score, log_loss

@task(log_prints=True)
def get_data(data_path):
    url = "https://drive.google.com/u/0/uc?id=1Em-UZriSKRwCPahc5yLaaPPE3eESaa7S"
    gdown.download(url, data_path + "data.csv", quiet=False)
    print(f"Dataset downloaded to {data_path}!")
    return 

@task(log_prints=True)
def preprocess_data(data_path):
    print("Preprocessing data...")
    interactions = []
    data = load_data(data_path + "data.csv")
    data = feature_engineering(data, interactions)
    data.to_csv(data_path + "data.csv", index=False)
    print("Data preprocessing is done!")
    return data

@task(log_prints=True)
def dataset_creation(data):
    X_train, X_test, y_train, y_test = create_dataset(data)
    return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

@task(log_prints=True)
def train_model_with_cv(split, model_path):
    print("Training model...")
    clf = cv(split["X_train"], split["y_train"])  
    print("Model training is done!")
    with open(model_path + "clf.pkl", "wb") as f:
        pickle.dump(clf, f)
    return clf

@task(log_prints=True)
def test_model(clf, split, results_path):
    print("Testing model...")
    best_estimator = clf.best_estimator_
    y_model = best_estimator.predict_proba(split["X_test"])[:, 1]
    log_loss_res = log_loss(split["y_test"], y_model)
    roc_auc_score_res = roc_auc_score(split["y_test"], y_model)
    results = {"log_loss": log_loss_res,
                "roc_auc": roc_auc_score_res
    }
    print("Model testing is done!")
    print(f"Results:\n{results}")
    with open(results_path + "results.pkl", "wb") as f:
        pickle.dump(results, f)

@flow
def click_prediction():
    data_path = "/home/julia/prefect/data/"
    model_path = "/home/julia/prefect/models/"
    results_path = "/home/julia/prefect/results/"
    get_data(data_path)
    data = preprocess_data(data_path)
    split = dataset_creation(data)
    clf = train_model_with_cv(split, model_path)
    test_model(clf, split, results_path)

if __name__ == "__main__":
    click_prediction.serve(name="pipeline")