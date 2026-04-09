import os
import glob
import json
import joblib
import random
import numpy as np
import xgboost as xgb
import tensorflow as tf

from celery import Celery
from sklearn.metrics import r2_score
from tensorflow.keras.models import model_from_json

data_file = '/app/repos.csv'

def load_data():
   # Search for repositories with stars >= 10000, sorted by stars in descending order
    repositories = np.genfromtxt(data_file, delimiter=',')

    X = repositories[:,:-1]
    y = repositories[:,-1].astype(np.int32)
    return X, y

def load_model():
    model = joblib.load('./model.pkl')
    return model

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task()
def add_nums(a, b):
   return a + b

@celery.task
def get_predictions():
    results ={}
    X, y = load_data()
    loaded_model = load_model()
    
    predictions = np.round(loaded_model.predict(X)).flatten().astype(np.int32)
    results['y'] = y.tolist()
    results['predicted'] = predictions.tolist()
    return results

@celery.task
def get_accuracy():
    X, y = load_data()
    loaded_model = load_model()
    predictions = np.round(loaded_model.predict(X)).flatten().astype(np.int32)    
    score = r2_score(y, predictions)
    return score
