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
### Test our example on the titanic dataset...
1. Run `make train-titanic` to train a model on the titanic dataset.
2. Then open up `(venv)$ jupyter lab` and run the cells in the titanic-demo.ipynb.
3. Finally, run `make streamlit-demo` to collect user feedback on your model.

### ... or try with your own model & data
```
# Instantiate data and model contexts
from trubrics.context import DataContext, ModelContext
from sklearn.metrics import accuracy_score
from trubrics.context import DataContext, ModelContext
data_context = DataContext(
    name="my_dataset",
    testing_data=test_df,
    target_column="Survived"
)
model_context = ModelContext(
    name="my_model",
    version="0.1",
    estimator=model,
    evaluation_function=accuracy_score
)

# Test your model
from trubrics.validators.base import Validator
model_validator = Validator(data=data_context, model=model_context)
my_first_validation = model_validator.validate_performance_against_threshold(threshold=0.8)
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
