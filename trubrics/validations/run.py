from typing import Any, Dict, List, Optional

from pydantic import BaseModel, validator
from rich import print as rprint
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
    model_name: str = "new_model"
    model_version: str = "0.0.1"
    metadata: Optional[Dict[str, str]] = None
    tags: List[Optional[str]] = []
    custom_validator: Any = None
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


def generate_new_trubric(run_context: TrubricRun) -> Trubric:
    all_validation_results = run_trubric(tr=run_context)
    validations = []
    for validation_result in all_validation_results:
        validations.append(validation_result)

        message_start = f"{validation_result.validation_type} [{validation_result.severity.upper()}]"
        completed_dots = f"[grey82]{(100 - len(message_start)) * '.'}[grey82]"
        message_end = (
            f"[bold {'green' if validation_result.outcome == 'pass' else 'red'}]{validation_result.outcome.upper()}"
        )
        rprint(message_start + completed_dots + message_end)

    return Trubric(
        name=run_context.trubric.name,
        model_name=run_context.model_name,
        model_version=run_context.model_version,
        data_context_name=run_context.data_context.name,
        data_context_version=run_context.data_context.version,
        metadata=run_context.metadata,
        tags=run_context.tags,
        validations=validations,
    )
