"""
Something
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, validator
from sklearn.metrics._scorer import _BaseScorer

from trubrics.context import DataContext, TrubricContext
from trubrics.validations import ModelValidator


class TrubricRun(BaseModel):
    """The TrubricRun object to group all necessary contexts in order for a run.
    Attributes:
        data_context: a data context to validate a model on
        model: a model to validate
        trubric_context: a trubric context listing all validations to execute
        custom_validator: an optional custom validator
    """

    data_context: DataContext
    model: Any
    trubric_context: TrubricContext
    custom_validator: Optional[Any] = None
    custom_scorers: Optional[Dict[str, Any]] = None

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
