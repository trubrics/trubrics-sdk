## Install
```console
(venv)$ pip install trubrics
```

## Create a trubric
```python
# instantiate data and model contexts
from trubrics.context import DataContext, ModelContext
from sklearn.metrics import accuracy_score
data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to test against a model
    target_column="target_column_name_in_test_df"
)
model_context = ModelContext(
    estimator=model,  # model to validate
    evaluation_function=accuracy_score  # evaluation function
)

# create a validation point for your model
from trubrics.validators.base import Validator
model_validator = Validator(data=data_context, model=model_context)
validations = [
    model_validator.validate_performance_against_threshold(threshold=0.8)
]

# save trubric as .json
from trubrics.context import TrubricContext
trubric_context = TrubricContext(
    name="my_first_trubric",
    model_context_name=model_context.name,
    model_context_version=model_context.version,
    data_context_name=data_context.name,
    data_context_version=data_context.version,
    validations=validations,
)
trubric_context.save_local(path="/data")
```


--8<-- "docs/snippets/create_trubric.md"
