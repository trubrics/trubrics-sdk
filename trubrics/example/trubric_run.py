import json

import pkg_resources  # type: ignore

from trubrics.context import DataContext
from trubrics.example.titanic import get_titanic_data_and_model
from trubrics.validations import Trubric
from trubrics.validations.run import TrubricRun

train_df, test_df, model = get_titanic_data_and_model()

data_context = DataContext(
    name="titanic_dataset",
    testing_data=test_df,
    minimum_functionality_data=test_df.iloc[:5],
    training_data=train_df,
    target="Survived",
)

stream = pkg_resources.resource_stream(__name__, "my_first_trubric.json")
trubric = Trubric.parse_obj(json.load(stream))

RUN_CONTEXT = TrubricRun(
    data_context=data_context, model_name="titanic_model", model=model, tags=["titanic-dev"], trubric=trubric
)
