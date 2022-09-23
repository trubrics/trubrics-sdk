# Out-of-the-box model validations

## Minimum Functionality
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_minimum_functionality()
```
:::trubrics.validations.ModelValidator.validate_minimum_functionality
----
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_minimum_functionality_in_range(
    range_value=0,
    range_inclusive=True
)
```
:::trubrics.validations.ModelValidator.validate_minimum_functionality_in_range
----

## Performance
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_performance_against_threshold(
    metric="recall",
    threshold=0.8
)
```
:::trubrics.validations.ModelValidator.validate_performance_against_threshold
----
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_test_performance_against_dummy(
    metric="accuracy",
    strategy="stratified"
)
```
:::trubrics.validations.ModelValidator.validate_test_performance_against_dummy
----
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_performance_between_train_and_test(
    metric="recall",
    threshold=0.3
)
```
:::trubrics.validations.ModelValidator.validate_performance_between_train_and_test
----
```py
from trubrics.validations import ModelValidator
slicing_functions = {"female": lambda x: x[x["Sex"]=="female"], "male": lambda x: x[x["Sex"]=="male"]}
model_validator = ModelValidator(data=data_context, model=model, slicing_functions=slicing_functions)
model_validator.validate_performance_std_across_slices(
    metric="recall",
    dataset="training_data",
    data_slices=["male", "female"],
    std_threshold=0.05,
    include_global_performance=True
)
```
:::trubrics.validations.ModelValidator.validate_performance_std_across_slices
----

## Inference time
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_inference_time(threshold=0.04, n_executions=100)
```
:::trubrics.validations.ModelValidator.validate_inference_time
----

## Feature Importance
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_feature_in_top_n_important_features(
    dataset="testing_data",
    feature="feature_a",
    top_n_features=2,
)
```
:::trubrics.validations.ModelValidator.validate_feature_in_top_n_important_features

```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
model_validator.validate_feature_importance_between_train_and_test(
    top_n_features=1
)
```
:::trubrics.validations.ModelValidator.validate_feature_importance_between_train_and_test
