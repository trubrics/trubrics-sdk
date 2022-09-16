```py
from trubrics.context import TrubricContext
trubric_context = TrubricContext(
    name="my_first_trubric",
    model_name=model.name,
    model_version=model.version,
    data_context_name=data_context.name,
    data_context_version=data_context.version,
    validations=validations,  # list of ValidationContexts
)
trubric_context.save_local(path="/data")
```