from typing import Any, Callable, Dict, List, Optional, Union

import pandas as pd
from jsonschema import SchemaError
from pydantic import BaseModel, validator
from sklearn.base import BaseEstimator

from trubrics.utils.pandas import schema_is_equal


class ModelContext(BaseModel):
    """Context for models."""

    name: Optional[str] = None
    version: Optional[float] = None
    estimator: BaseEstimator
    evaluation_function: Callable[[pd.Series, pd.Series], Union[int, float]]

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True
        extra = "forbid"


class DataContext(BaseModel):
    """Context for data."""

    name: Optional[str] = None
    training_data: Optional[pd.DataFrame] = None
    testing_data: pd.DataFrame
    categorical_columns: Optional[List[str]] = None
    business_columns: Optional[Dict[str, str]] = None
    target_column: str

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True
        extra = "forbid"

    @validator("testing_data")
    def testing_and_training_must_have_same_schema(cls, v: pd.DataFrame, values: List[Any]):
        if values["training_data"] is not None and not schema_is_equal(v, values["training_data"]):  # type: ignore
            raise SchemaError("Testing and training data must have identical schemas.")
        return v

    @validator("target_column")
    def target_column_must_be_in_data(cls, v: str, values: List[Any]):
        if v not in values["testing_data"].columns:  # type: ignore
            raise KeyError("Target column must be in testing_data column names.")
        return v

    @validator("categorical_columns")
    def categorical_columns_must_be_in_data(cls, v: str, values: List[Any]):
        if not set(v).issubset(values["testing_data"].columns):  # type: ignore
            raise KeyError("All categorical columns must be in testing_data column names.")
        return v

    @validator("business_columns")
    def business_columns_must_be_in_data(cls, v: str, values: List[Any]):
        if not set(v.keys()).issubset(values["testing_data"].columns):  # type: ignore
            raise KeyError("All business columns must be in testing_data column names.")
        return v

    @validator("target_column")
    def target_column_must_not_be_in_categoricals(cls, v: str, values: List[Any]):
        if values["categorical_columns"] is not None and v in values["categorical_columns"]:  # type: ignore
            raise Exception(
                "Target column should not feature as a categorical column. Categorical columns only refer to features."
            )
        return v

    def list_features(self, data: Optional[pd.DataFrame] = None) -> List[str]:
        """Get features column names excluding the target feature."""
        if data is None:
            return [col for col in self.testing_data.columns if col != self.target_column]
        return [col for col in data.columns if col != self.target_column]


class TrubricContext(BaseModel):
    """Context for a Trubric set of tests."""

    test_type: Optional[str]
    metadata: Dict[str, Union[List[Any], str, int, float, dict]]
