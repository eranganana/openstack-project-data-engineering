import os
#os.environ["CUDA_VISIBLE_DEVICES"] = ""

import ray
from ray import tune
from sklearn.model_selection import cross_val_score
import numpy as np
import xgboost as xgb
from github import Github, Auth
import random
from requests.exceptions import RequestException
import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import h5py
import joblib

# Initialize Ray
ray.init(ignore_reinit_error=True)

def fetch_data():
    auth = Auth.Token("YOUR_TOKEN_HERE")
    g = Github(auth=auth)
    repositories = g.search_repositories(query='stars:>10000')

    repo_list = list(repositories)
    if len(repo_list) < 999:
        selected_repos = repo_list  # Use all available repositories if less than 999
    else:
        selected_repos = repo_list[:999]  # Get the first 999 repositories
    random.shuffle(selected_repos)

    dataset = {'data': [], 'target': []}
    for repo in selected_repos:
        forks_count = repo.forks_count
        size = repo.size
        stargazers_count = repo.stargazers_count
        
        # Derive new features
        forks_to_size_ratio = forks_count / size if size != 0 else 0
        stargazers_to_forks_ratio = stargazers_count / forks_count if forks_count != 0 else 0
        
        dataset['data'].append([forks_count, repo.size, repo.watchers_count, repo.open_issues_count])
        dataset['target'].append(stargazers_count)

    return dataset

def train_model(config, data, model_type):
    if model_type == 'xgb':
        model = xgb.XGBRegressor(random_state=42)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    X = data['data']
    y = data['target']
    model.set_params(**config)
    avg_score = np.mean(cross_val_score(model, X, y, scoring='r2', cv=4))
    model.fit(X, y)  # Train the model
    return {"r2": avg_score, "model": model}

def save_model(model, model_name):
    # Save model parameters to pickle file
    joblib.dump(model, 'model.pkl')

def plot_feature_importance(model, feature_names):
    importance = model.feature_importances_
    indices = np.argsort(importance)
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances")
    plt.barh(range(len(indices)), importance[indices], align='center')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel("Relative Importance")
    plt.show()

search_space_xgb = {
    "max_depth": tune.grid_search([10, 20, 30, 50]),
    "n_estimators": tune.grid_search([10, 20, 50, 100, 200]),
    "learning_rate": tune.grid_search([0.01, 0.1, 0.2])
}

dataset = fetch_data()
dataset = ray.put(dataset)

tuner_xgb = tune.Tuner(
    tune.with_parameters(train_model, data=dataset, model_type='xgb'),
    param_space=search_space_xgb,
    tune_config=tune.TuneConfig(metric="r2", mode="max")
)
result_xgb = tuner_xgb.fit()

best_xgb = result_xgb.get_best_result(metric="r2", mode="max")
print("Best XGBoost:", best_xgb.config, "with R2:", best_xgb.metrics["r2"])

# Save the best model
best_model = best_xgb.metrics["model"]
save_model(best_model, "best_xgboost_model")

# Plot feature importance
feature_names = ["forks_count", "size", "forks_to_size_ratio", "stargazers_to_forks_ratio"]
plot_feature_importance(best_model, feature_names)
