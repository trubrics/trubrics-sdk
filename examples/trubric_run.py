import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

from examples.custom_validator import CustomValidator
from trubrics.context import DataContext, ModelContext, TrubricContext
from trubrics.validators.run_context import TrubricRun

testing_data = pd.read_csv("examples/data/preprocessed_test.csv")
training_data = pd.read_csv("examples/data/preprocessed_train.csv")
model = joblib.load("examples/models/rf_model.pkl")

data_context = DataContext(testing_data=testing_data, training_data=training_data, target_column="Survived")
model_context = ModelContext(estimator=model, evaluation_function=accuracy_score)
trubric_context = TrubricContext.parse_file("examples/data/my_first_trubric.json")

RUN_CONTEXT = TrubricRun(
    data_context=data_context,
    model_context=model_context,
    trubric_context=trubric_context,
    custom_validator=CustomValidator(data=data_context, model=model_context),
)
