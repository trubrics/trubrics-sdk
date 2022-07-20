# trubrics-sdk

![logo-gradient](./docs/assets/logo-gradient.png)

**Combine data science knowledge with business user feedback to validate machine learning.**

## Install 
```console
(venv)$ pip install trubrics
```

## Getting started
For complete getting started information and tutorials, consult our [trubrics-sdk docs](https://trubrics.github.io/trubrics-sdk/).

### 1. Initialise a trubrics Validator with your data & model
```py
from trubrics.context import DataContext, ModelContext
from trubrics.validators.base import Validator
data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to test against a model
    target_column="target_column_name_in_test_df"
)
model_context = ModelContext(
    estimator=model,  # model to validate
    evaluation_function=accuracy_score  # evaluation function
)

model_validator = Validator(data=data_context, model=model_context)
```

### 2. Run validations with the Validator
```py
validations = [
    model_validator.validate_performance_against_threshold(threshold=0.8),
    model_validator.validate_biased_performance_across_category(
        category="feature_a", threshold=0.05
    )
]
```
