# Trubrics SDK

Trubrics is a collaborative ML testing platform that allows data scientists and domain experts to define test cases for models. This python SDK allows ML model tests to be explored, developed and saved to the Trubrics UI. There are two main parts to the package:
1. [testers](./trubrics/testers/): Ready-to-go tests to implement on your models, with connection to the Trubrics API
2. [components](./trubrics/components): Plugins to your favorite python web app tool (Streamlit) to collect feedback on your model from domain experts and translate these into tests

## Try it out:
```
# TODO: publish to PyPI
```

```
from trubrics.context import DataContext, ModelContext
data_context = DataContext(
    name="my_datasource",
    training_data=X_train.assign(Survived=y_train),
    testing_data=X_test.assign(Survived=y_test),
    target_col="Survived"
)
model_context = ModelContext(
    name="my_model",
    version="0.1",
    estimator=rf_model,
    evaluation_function=accuracy_score
)
from trubrics.testers.sklearn import SklearnTester
model_tester = SklearnTester(data=data_context, model=model_context)

# example of performance test
model_tester.test_performance_against_threshold(threshold=0.75)
```

## Contribute
Install dev requirements:
```
pip install -r requirements-dev.txt
```
Then install the pre-commit hook and test it out with:
```
pre-commit install
make lint
```
