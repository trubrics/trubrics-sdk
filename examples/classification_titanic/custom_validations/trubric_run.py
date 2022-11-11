from examples.classification_titanic.training_validations.custom_model import (
    ExampleCustomModel,
)
from examples.classification_titanic.training_validations.custom_validator import (
    CustomValidator,
)
from trubrics.context import DataContext
from trubrics.example.titanic import get_titanic_data_and_model
from trubrics.validations import Trubric
from trubrics.validations.run import TrubricRun

train_df, test_df, model = get_titanic_data_and_model()

data_context = DataContext(
    name="my_first_dataset", version=0.1, training_data=train_df, testing_data=test_df, target="Survived"
)
trubric = Trubric.parse_file("./my_first_trubric.json")

RUN_CONTEXT = TrubricRun(
    data_context=data_context,
    model=ExampleCustomModel(model),
    trubric=trubric,
    custom_validator=CustomValidator,
)
