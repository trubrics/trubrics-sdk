import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

from trubrics.context import DataContext, ModelContext

testing_data = pd.read_csv("examples/data/preprocessed_test.csv")
model = joblib.load("examples/models/rf_model.pkl")

# this config file should output the following three variables:
DATA_CONTEXT = DataContext(testing_data=testing_data, target_column="Survived")
MODEL_CONTEXT = ModelContext(estimator=model, evaluation_function=accuracy_score)
TRUBRIC_PATH = "examples/data/my_first_trubric.json"
