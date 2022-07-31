"""
Something
"""

from typing import Any, Optional

from pydantic import BaseModel, validator

from trubrics.context import DataContext, ModelContext, TrubricContext
from trubrics.validators.base import Validator


class TrubricRun(BaseModel):
    """The TrubricRun object to group all necessary contexts in order for a run.
    Attributes:
        data_context: a data context to validate a model on
        model_context: a model context with the model to validate
        trubric_context: a trubric context listing all validations to execute
        custom_validator: an optional custom validator
    """

    data_context: DataContext
    model_context: ModelContext
    trubric_context: TrubricContext
    custom_validator: Optional[Any] = None

    @validator("custom_validator")
    def validate_some_foo(cls, val):
        if issubclass(type(val), Validator):
            return val
        raise TypeError("Wrong type for 'custom_validator', must be subclass of Validator.")
