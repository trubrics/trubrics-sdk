"""
Something
"""

from typing import Any, Optional

from pydantic import BaseModel, validator

from trubrics.context import DataContext, ModelContext
from trubrics.validators.base import Validator


class TrubricRun(BaseModel):
    """Context for a trubrics run object."""

    data_context: DataContext
    model_context: ModelContext
    trubric_path: str
    custom_validator: Optional[Any]

    @validator("custom_validator")
    def validate_some_foo(cls, val):
        if issubclass(type(val), Validator):
            return val
        raise TypeError("Wrong type for 'custom_validator', must be subclass of Validator.")
