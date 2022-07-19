```py
from trubrics.context import ModelContext
from sklearn.metrics import accuracy_score
model_context = ModelContext(
    estimator=model,  # model to validate
    evaluation_function=accuracy_score  # evaluation function
)
```
