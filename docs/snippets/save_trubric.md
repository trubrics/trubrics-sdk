```py
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