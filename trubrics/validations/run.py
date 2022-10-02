from typing import Any, Dict, Optional

from pydantic import BaseModel, validator
from sklearn.metrics._scorer import _BaseScorer

from trubrics.context import DataContext
from trubrics.exceptions import UnknownValidationError
from trubrics.validations import ModelValidator, Trubric


class TrubricRun(BaseModel):
    """The TrubricRun object to group all necessary code for a run. Load data and models from
    remote locations or locally for validation within a pipeline.

    Attributes:
        data_context: a data context to validate a model on
        model: a model to validate
        trubric: a Trubric object listing all validations to execute
        custom_validator: an optional custom validator
        custom_scorers: an optional dict of custom scorers for computing custom metrics
        slicing_functions: an optional dict of slicing functions
    """

    data_context: DataContext
    model: Any
    trubric: Trubric
    custom_validator: Optional[Any] = None
    custom_scorers: Optional[Dict[str, Any]] = None
    slicing_functions: Optional[Dict[str, Any]] = None

    @validator("custom_validator")
    def custom_validator_inherits_validator(cls, val):
        if issubclass(val, ModelValidator):
            return val
        raise TypeError("Wrong type for 'custom_validator', must be subclass of ModelValidator.")

    @validator("custom_scorers")
    def custom_scorer_is_make_scorer(cls, val):
        for scorer in val:
            if not issubclass(type(val[scorer]), _BaseScorer):
                raise TypeError("Each scorer must be subclass of scikit-learn's _BaseScorer.")
        return val


def run_trubric(tr: TrubricRun):
    if tr.custom_validator is not None:
        model_validator = tr.custom_validator(
            data=tr.data_context,
            model=tr.model,
            custom_scorers=tr.custom_scorers,
            slicing_functions=tr.slicing_functions,
        )
    else:
        model_validator = ModelValidator(
            data=tr.data_context,
            model=tr.model,
            custom_scorers=tr.custom_scorers,
            slicing_functions=tr.slicing_functions,
        )
    for validation in tr.trubric.validations:
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
