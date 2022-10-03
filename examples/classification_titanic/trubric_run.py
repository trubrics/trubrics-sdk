from examples.classification_titanic.custom_scorer import custom_scorers
from examples.classification_titanic.custom_validator import CustomValidator
from examples.classification_titanic.slicing_functions import slicing_functions
from trubrics.context import DataContext
from trubrics.example.titanic import get_titanic_data_and_model
from trubrics.validations import Trubric
from trubrics.validations.run import TrubricRun

train_df, test_df, model = get_titanic_data_and_model()

data_context = DataContext(
    testing_data=test_df,
    minimum_functionality_data=test_df.iloc[:5],
    training_data=train_df,
    target="Survived",
)
trubric = Trubric.parse_file("examples/classification_titanic/my_first_trubric.json")

RUN_CONTEXT = TrubricRun(
    data_context=data_context,
    model=model,
    trubric=trubric,
    custom_validator=CustomValidator,
    custom_scorers=custom_scorers,
    slicing_functions=slicing_functions,
)
