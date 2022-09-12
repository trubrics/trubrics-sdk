```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(metric="accuracy", data=data_context, model=rf_model)
validations = [
    model_validator.validate_performance_against_threshold(threshold=0.8),
    model_validator.validate_biased_performance_across_category(
        category="feature_a", threshold=0.05
    )
]
```
