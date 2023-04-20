from typing import Any, Dict, Iterator, List, Optional

from pydantic import BaseModel, validator
from rich import print as rprint
from sklearn.metrics._scorer import _BaseScorer

from trubrics.context import DataContext
from trubrics.exceptions import UnknownValidationError
from trubrics.validations import ModelValidator, Trubric, Validation


class TrubricRun(BaseModel):
    """The TrubricRun object to group all necessary code for a run. Load data and models from
    remote locations or locally for validation within a pipeline.

    Attributes:
        data_context: a data context to validate a model on
        model: a model to validate
        model_name: the name of the new model
        model_version: the version of the new model
        trubric: a Trubric object listing all validations to execute
        metadata: any new metadata to input to the Trubric
        tags: any new tags for the trubric
        custom_validator: an optional custom validator
        custom_scorers: an optional dict of custom scorers for computing custom metrics
        slicing_functions: an optional dict of slicing functions
    """

    data_context: DataContext
    model: Optional[Any]
    model_name: Optional[str]
    model_version: Optional[str]
    trubric: Trubric
    metadata: Optional[Dict[str, str]] = None
    tags: List[Optional[str]] = []
    custom_validator: Any = None
    custom_scorers: Optional[Dict[str, Any]] = None
    slicing_functions: Optional[Dict[str, Any]] = None
    failing_severity: Optional[str] = None

    @validator("custom_validator")
    def custom_validator_inherits_validator(cls, val):
        if val:
            if issubclass(val, ModelValidator):
                return val
            raise TypeError("Wrong type for 'custom_validator', must be subclass of ModelValidator.")

    @validator("custom_scorers")
    def custom_scorer_is_make_scorer(cls, val):
        if val:
            for scorer in val:
                if not issubclass(type(val[scorer]), _BaseScorer):
                    raise TypeError("Each scorer must be subclass of scikit-learn's _BaseScorer.")
            return val

    def generate_validations_from_trubric(self) -> Iterator[Validation]:
        if self.custom_validator is not None:
            model_validator = self.custom_validator(
                data=self.data_context,
                model=self.model,
                custom_scorers=self.custom_scorers,
                slicing_functions=self.slicing_functions,
            )
        else:
            model_validator = ModelValidator(
                data=self.data_context,
                model=self.model,
                custom_scorers=self.custom_scorers,
                slicing_functions=self.slicing_functions,
            )
        for validation in self.trubric.validations:
            args = validation.validation_kwargs["args"]
            kwargs = validation.validation_kwargs["kwargs"]
            try:
                validation_result = getattr(model_validator, validation.validation_type)(*args, **kwargs)
                new_validation = validation.copy()
                new_validation.passed = validation_result.passed
                new_validation.result = validation_result.result
                yield new_validation
            except AttributeError:
                raise UnknownValidationError(
                    f"The validation '{validation.validation_type}' does not appear to belong to a validator."
                    " Try adding the object that generated the validation to the 'custom_validator' parameter."
                )

    def set_new_trubric(self) -> Trubric:
        all_validation_results = self.generate_validations_from_trubric()
        validations = []
        for validation_result in all_validation_results:
            validations.append(validation_result)

            message_start = f"{validation_result.validation_type} [{validation_result.severity.upper()}]"
            completed_dots = f"[grey82]{(100 - len(message_start)) * '.'}[grey82]"
            message_end = (
                "[bold"
                f" {'green' if validation_result.passed else 'red'}]{'PASS' if validation_result.passed else 'FAIL'}"
            )
            rprint(message_start + completed_dots + message_end)

        return Trubric(
            name=self.trubric.name,
            failing_severity=self.failing_severity or self.trubric.failing_severity,
            model_name=self.model_name,
            model_version=self.model_version,
            data_context_name=self.data_context.name,
            data_context_version=self.data_context.version,
            metadata=self.metadata,
            tags=self.tags,
            validations=validations,
        ).set_dynamic_fields()
