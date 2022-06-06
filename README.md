# Trubrics SDK

Trubrics is a collaborative ML validation platform that allows data scientists and domain experts to define test cases for models. This python SDK allows ML model tests to be explored, developed and saved to the Trubrics UI. There are two main parts to the package:
1. validators: Ready-to-go ML tests to implement on your models, with connection to the Trubrics API
2. components: Plugins to your favorite python web app tool (Streamlit) to collect feedback on your model from domain experts and translate these into tests

## Try it out
### Install trubrics
```
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt && make local-build
```
### Test our example...
Open up `(venv)$ jupyter lab` and run titanic-demo.ipynb.

### ... or try with your own model & data
```
# Instantiate data and model contexts
from trubrics.context import DataContext, ModelContext
data_context = DataContext(
    testing_data=test_df, # the dataframe for all tests
    target_column="Survived"
)
model_context = ModelContext(
    estimator=model, # your saved model
    evaluation_function=accuracy_score # an evaluation function
)

# Test your model
from trubrics.validators.sklearn import SklearnValidator
model_validator = SklearnValidator(data=data_context, model=model_context)

model_validator.validate_performance_against_threshold(threshold=0.75)
```

## Contribute
### Install dev requirements
```
pip install -r requirements-dev.txt
```
### Install the pre-commit hook
```
pre-commit install
make lint
```
