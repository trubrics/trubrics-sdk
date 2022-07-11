import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

from examples.custom_validator import CustomValidator
from trubrics.context import DataContext, ModelContext

testing_data = pd.read_csv("examples/data/preprocessed_test.csv")
model = joblib.load("examples/models/rf_model.pkl")

# this config file should output the following three variables:
DATA_CONTEXT = DataContext(testing_data=testing_data, target_column="Survived")
MODEL_CONTEXT = ModelContext(estimator=model, evaluation_function=accuracy_score)
TRUBRIC_PATH = "examples/data/my_first_trubric.json"

# if using a custom validator, this should equally be set here
CUSTOM_VALIDATOR = CustomValidator(
    data=DATA_CONTEXT, model=MODEL_CONTEXT
)  # should be set to 'None' if no custom validator
