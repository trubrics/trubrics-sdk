import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

from examples.custom_validator import CustomValidator
from trubrics.context import DataContext, ModelContext
from trubrics.validators.run_context import TrubricRun

testing_data = pd.read_csv("examples/data/preprocessed_test.csv")
model = joblib.load("examples/models/rf_model.pkl")

data_context = DataContext(testing_data=testing_data, target_column="Survived")
model_context = ModelContext(estimator=model, evaluation_function=accuracy_score)

RUN_CONTEXT = TrubricRun(
    data_context=data_context,
    model_context=model_context,
    trubric_path="examples/data/my_first_trubric.json",
    custom_validator=CustomValidator(data=data_context, model=model_context),
)
