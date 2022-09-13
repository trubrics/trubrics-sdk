import joblib
import pandas as pd

from examples.cli.custom_validator import CustomValidator
from trubrics.context import DataContext, TrubricContext
from trubrics.validations.run_context import TrubricRun

testing_data = pd.read_csv("examples/data/preprocessed_test.csv")
training_data = pd.read_csv("examples/data/preprocessed_train.csv")
model = joblib.load("examples/models/rf_model.pkl")

data_context = DataContext(testing_data=testing_data, training_data=training_data, target_column="Survived")
trubric_context = TrubricContext.parse_file("examples/data/my_first_trubric.json")

RUN_CONTEXT = TrubricRun(
    data_context=data_context, model=model, trubric_context=trubric_context, custom_validator=CustomValidator
)
