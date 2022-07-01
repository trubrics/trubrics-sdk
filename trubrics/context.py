from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import requests  # type: ignore
from pydantic import BaseModel, validator

from trubrics.exceptions import PandasSchemaError
from trubrics.utils.pandas import schema_is_equal


class ModelContext(BaseModel):
    """Context for models."""

    name: str = "my_model"
    version: float = 0.1
    estimator: Any
    evaluation_function: Any
    evaluation_kwargs: Optional[Dict[str, Union[bool, str, int, float, None]]] = None

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True
        extra = "forbid"

    @property
    def evaluation_function_name(self) -> str:
        return self.evaluation_function.__name__


class DataContext(BaseModel):
    """Context for data."""

    name: str = "my_dataset"
    version: float = 0.1
    training_data: Optional[pd.DataFrame] = None
    testing_data: pd.DataFrame
    categorical_columns: Optional[List[str]] = None
    business_columns: Optional[Dict[str, str]] = None
    target_column: str

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True
        extra = "forbid"

    @property
    def features(self) -> List[str]:
        """Features defined as all testing column names excluding the target feature."""
        return [col for col in self.testing_data.columns if col != self.target_column]

    @property
    def renamed_testing_data(self) -> pd.DataFrame:
        """Renamed testing data with business columns."""
        if self.business_columns is None:
            raise TypeError("Business columns must be set to rename testing features.")
        return self.testing_data.rename(columns=self.business_columns)

    @validator("testing_data")
    def testing_and_training_must_have_same_schema(cls, v: pd.DataFrame, values: List[Any]):
        if values["training_data"] is not None and not schema_is_equal(v, values["training_data"]):  # type: ignore
            raise PandasSchemaError("Testing and training data must have identical schemas.")
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


class FeedbackContext(BaseModel):
    """Context for feedback given by a user from a UI component."""

    feedback_type: Optional[str]
    metadata: Dict[str, Union[List[Any], str, int, float, dict]]


class ValidationContext(BaseModel):
    """Context for a single validation point of a model."""

    validation_type: str
    validation_kwargs: Dict[str, Optional[Any]]
    outcome: str
    result: Optional[Dict[str, Union[str, int, float]]]

    class Config:
        schema_extra = {
            "example": {
                "validation_type": "validate_performance_against_threshold",
                "validation_kwargs": {"args": [], "kwargs": {"threshold": 0.8}},
                "outcome": "fail",
                "result": {"performance": "0.79"},
            }
        }


class TrubricContext(BaseModel):
    """Context for a Trubric, or set of validation points."""

    name: str = "trubric"
    model_context_name: str
    model_context_version: float
    data_context_name: str
    data_context_version: float
    metadata: Optional[Dict[str, str]] = None
    validations: List[ValidationContext]

    class Config:
        schema_extra = {
            "example": {
                "name": "my_first_trubric",
                "model_context_name": "my_model",
                "model_context_version": 0.1,
                "data_context_name": "my_dataset",
                "data_context_version": 0.1,
                "metadata": {},
                "validations": [
                    {
                        "validation_type": "validate_performance_against_threshold",
                        "validation_kwargs": {"args": [], "kwargs": {"threshold": 0.8}},
                        "outcome": "fail",
                        "result": {"performance": "0.79"},
                    }
                ],
            }
        }

    def save_local(self, path: str):
        if path is None:
            raise Exception("Specify the local path where you would like to save your Trubric json.")
        with open(Path(path) / f"{self.name}.json", "w") as file:
            file.write(self.json())

    def save_ui(self, local_port: int):
        url = f"http://localhost:{local_port}"
        headers = {"Content-type": "application/json"}
        requests.post(
            url + "/api/trubrics/",
            data=self.json(),
            headers=headers,
        )
