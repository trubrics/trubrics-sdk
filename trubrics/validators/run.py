from typing import Optional

from trubrics.context import DataContext, ModelContext, TrubricContext
from trubrics.validators.base import Validator


def run_trubric(
    data_context: DataContext,
    model_context: ModelContext,
    trubric_path: str,
    custom_validator: Optional[Validator] = None,
):
    if custom_validator is not None:
        model_validator = custom_validator(data=data_context, model=model_context)  # type: ignore
    else:
        model_validator = Validator(data=data_context, model=model_context)
    trubric = TrubricContext.parse_file(trubric_path)
    for validation in trubric.validations:
        args = validation.validation_kwargs["args"]
        kwargs = validation.validation_kwargs["kwargs"]
        try:
            result = getattr(model_validator, validation.validation_type)(*args, **kwargs)
            yield validation.validation_type, validation.severity, result.outcome
        except AttributeError:
            print(f"Custom validations like '{validation.validation_type}' are not yet supported.")
