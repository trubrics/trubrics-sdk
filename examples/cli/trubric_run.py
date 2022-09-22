import joblib
import pandas as pd

from examples.cli.custom_scorer import custom_scorers
from examples.cli.custom_validator import CustomValidator
from examples.cli.slicing_functions import slicing_functions
from examples.training import titanic_config
from trubrics.context import DataContext, TrubricContext
from trubrics.validations.run import TrubricRun

testing_data = pd.read_csv(titanic_config.LOCAL_TEST_FILENAME)
training_data = pd.read_csv(titanic_config.LOCAL_TRAIN_FILENAME)
model = joblib.load(titanic_config.LOCAL_MODEL_FILENAME)

data_context = DataContext(
    testing_data=testing_data,
    minimum_functionality_data=testing_data.iloc[:5],
    training_data=training_data,
    target="Survived",
)
trubric_context = TrubricContext.parse_file("examples/data/my_first_trubric.json")

RUN_CONTEXT = TrubricRun(
    data_context=data_context,
    model=model,
    trubric_context=trubric_context,
    custom_validator=CustomValidator,
    custom_scorers=custom_scorers,
    slicing_functions=slicing_functions,
)
