import json

import pkg_resources  # type: ignore

from trubrics.context import DataContext
from trubrics.example.titanic import get_titanic_data_and_model
from trubrics.validations import Trubric
from trubrics.validations.run import TrubricRun

train_df, test_df, model = get_titanic_data_and_model()

data_context = DataContext(
    name="titanic_dataset",
    version="0.0.1",
    testing_data=test_df,
    minimum_functionality_data=test_df.iloc[:5],
    training_data=train_df,
    target="Survived",
)

# Note: This method of reading json is only necessary from within python package.
# Call `Trubric.parse_file("your_trubric.json")` to read in a trubric directly.
stream = pkg_resources.resource_stream(__name__, "my_first_trubric.json")
trubric = Trubric.parse_obj(json.load(stream))

RUN_CONTEXT = TrubricRun(
    data_context=data_context,
    model_name="titanic_model",
    model_version="0.0.1",
    model=model,
    tags=["cli-demo"],
    trubric=trubric,
    failing_severity="warning",
)
