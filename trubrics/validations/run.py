from typing import Optional

from trubrics.context import DataContext, ModelContext, TrubricContext
from trubrics.exceptions import UnknownValidationError
from trubrics.validations.base import Validator


def run_trubric(
    data_context: DataContext,
    model_context: ModelContext,
    trubric: TrubricContext,
    custom_validator: Optional[Validator] = None,
):
    if custom_validator is not None:
        model_validator = custom_validator
    else:
        model_validator = Validator(data=data_context, model=model_context)
    for validation in trubric.validations:
        args = validation.validation_kwargs["args"]
        kwargs = validation.validation_kwargs["kwargs"]
        try:
            validation_result = getattr(model_validator, validation.validation_type)(*args, **kwargs)
            new_validation = validation.copy()
            new_validation.outcome = validation_result.outcome
            new_validation.result = validation_result.result
            yield new_validation
        except AttributeError:
            raise UnknownValidationError(
                f"The validation '{validation.validation_type}' does not appear to belong to a validator."
                " Try adding the object that generated the validation to the 'custom_validator' parameter."
            )
