```py
from trubrics.validators.base import Validator
model_validator = Validator(data=data_context, model=model_context)
validations = [
    model_validator.validate_performance_against_threshold(threshold=0.8),
    model_validator.validate_biased_performance_across_category(
        category="feature_a", threshold=0.05
    )
]
```
