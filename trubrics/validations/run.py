from typing import Any

from trubrics.context import DataContext, TrubricContext
from trubrics.exceptions import UnknownValidationError
from trubrics.validations import ModelValidator


def run_trubric(
    data_context: DataContext,
    model: Any,
    trubric: TrubricContext,
    custom_validator=None,
    custom_scorers=None,
):
    if custom_validator is not None:
        model_validator = custom_validator(data=data_context, model=model, custom_scorers=custom_scorers)
    else:
        model_validator = ModelValidator(data=data_context, model=model, custom_scorers=custom_scorers)
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
