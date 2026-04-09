from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from ray import train, tune, init
from github import Github
from github import Auth
import random
import ray
import numpy as np
import joblib

def fetch_data():
    auth = Auth.Token("YOUR_TOKEN_HERE")
    g = Github(auth=auth)

    # Get the top 1000 repos w.r.t stars and shuffle them
    repositories = g.search_repositories(query='stars:>10000')
    selected_repos = list(repositories)[:999]
    random.shuffle(selected_repos)

    # extract features and store in data/target
    features = [
        [repo.forks_count, repo.size, repo.watchers_count, repo.open_issues_count]
        for repo in selected_repos
    ]
    target = [repo.stargazers_count for repo in selected_repos]

    dataset = {'data': features, 'target': target}
    return dataset

dataset = fetch_data()

def save_model(model, model_name):
    # Save model parameters to pickle file
    joblib.dump(model, 'model.pkl')

def train_model(config, data):
    model = RandomForestRegressor(random_state=42)
    X = data['data']
    y = data['target']
    model.set_params(**config)
    avg_score = np.mean(cross_val_score(model, X, y, scoring='r2', cv=4))

    # Report the accuracy metric
    return {"r2":avg_score}

search_space = {
    "max_depth": tune.grid_search([10]),
    "n_estimators": tune.grid_search([2]),
    "ccp_alpha": tune.grid_search([0.01]),
}

dataset = fetch_data()
dataset = ray.put(dataset)
tuner = tune.Tuner(tune.with_parameters(train_model, data=dataset), param_space=search_space)
result = tuner.fit()
best_trial = result.get_best_result(metric="score", mode="max")
print(best_trial.config)
print(best_trial)