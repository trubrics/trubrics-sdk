from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from loguru import logger
from pydantic import BaseModel, validator

from trubrics.exceptions import (
    EstimatorTypeError,
    ModelPredictionError,
    PandasSchemaError,
)
from trubrics.utils.pandas import schema_is_equal
from trubrics.utils.trubrics_manager_connector import make_request


class DataContext(BaseModel):
    """
    The DataContext wraps data into a trubrics friendly format.

    Note:
        The DataContext *must contain* at least a testing_data and a target attribute.
        Default values are set for all other attributes.

    Attributes:
        name: DataContext name. Required for trubrics UI tracking.
        version: DataContext version. Required for trubrics UI tracking.
        testing_data: Dataframe that all validations are executed against. Should contain all features and target
                      values that the model was trained with.
        target: Name of target column.
        training_data: Dataframe of the training data.
        minimum_functionality_data: Dataframe of the minimum functionality of a model. This contains samples that
                                    the model should never fail on.
        categorical_columns: List of categorical names of the train & test datasets.
        business_columns: Mapping between dataset column names and comprehensible column names to be displayed to users.
    """

    name: str = "my_dataset"
    version: float = 0.1
    testing_data: pd.DataFrame
    target: str
    training_data: Optional[pd.DataFrame] = None
    minimum_functionality_data: Optional[pd.DataFrame] = None
    categorical_columns: Optional[List[str]] = None
    business_columns: Optional[Dict[str, str]] = None

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True
        extra = "forbid"

    @property
    def features(self) -> List[str]:
        """Features are here defined as all testing column names excluding the target feature."""
        return [col for col in self.testing_data.columns if col != self.target]

    @property
    def X_test(self) -> pd.DataFrame:
        """Feature testing dataframe."""
        return self.testing_data[self.features]

    @property
    def y_test(self) -> pd.Series:
        """Target testing series."""
        return self.testing_data[self.target]

    @property
    def X_train(self) -> Optional[pd.DataFrame]:
        """Feature training dataframe."""
        return self.training_data[self.features] if self.training_data is not None else None

    @property
    def y_train(self) -> Optional[pd.Series]:
        """Target training series."""
        return self.training_data[self.target] if self.training_data is not None else None

    @property
    def renamed_testing_data(self) -> pd.DataFrame:
        """Renamed testing data with business columns"""
        if self.business_columns is None:
            raise TypeError("Business columns must be set to rename testing features.")
        return self.testing_data.rename(columns=self.business_columns)

    @validator("target")
    def target_column_must_be_in_data(cls, v, values):
        if v not in values["testing_data"].columns:
            raise KeyError("Target column must be in testing_data column names.")
        return v

    @validator("training_data")
    def training_and_testing_must_have_same_schema(cls, v, values):
        if v is not None and not schema_is_equal(values["testing_data"], v):
            raise PandasSchemaError("Training and testing data must have identical schemas.")
        return v

    @validator("minimum_functionality_data")
    def minimum_functionality_and_testing_must_have_same_schema(cls, v, values):
        if v is not None and not schema_is_equal(values["testing_data"], v):
            raise PandasSchemaError("Minimum functionality and testing data must have identical schemas.")
        return v

    @validator("categorical_columns")
    def categorical_columns_must_be_in_data(cls, v, values):
        if not set(v).issubset(values["testing_data"].columns):
            raise KeyError("All categorical columns must be in testing_data column names.")
        return v

    @validator("categorical_columns")
    def target_column_must_not_be_in_categoricals(cls, v, values):
        if v is not None and values["target"] in v:
            raise ValueError(
                "Target column should not feature as a categorical column. Categorical columns only refer to features."
            )
        return v

    @validator("business_columns")
    def business_columns_must_be_in_data(cls, v, values):
        if not set(v.keys()).issubset(values["testing_data"].columns):
            raise KeyError("All business columns must be in testing_data column names.")
        return v


class TrubricsModel(BaseModel):
    """ """

    data: DataContext
    model: Any

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True
        extra = "forbid"

    @validator("model")
    def does_model_predict_train_head(cls, v: Any, values: Any) -> Any:
        """
        Validate that model predicts on the first 5 rows of the training data.
        """
        if values["data"].training_data is not None:
            try:
                v.predict(values["data"].X_train.head())
            except ValueError:
                raise ModelPredictionError("The model specified does not predict on the train data.")
        return v

    @validator("model")
    def does_model_predict_test_head(cls, v: Any, values: Any) -> Any:
        """
        Validate that model predicts on the first 5 rows of the testing data.
        """
        try:
            v.predict(values["data"].X_test.head())
        except ValueError:
            raise ModelPredictionError("The model specified does not predict on the test data.")
        return v

    @property
    def model_type(self) -> Optional[str]:
        if self.model._estimator_type in ["regressor", "classifier"]:
            return self.model._estimator_type
        else:
            raise EstimatorTypeError("_estimator_type must be a 'regressor' or a 'classifier'.")

    @property
    def predictions_train(self) -> Optional[pd.Series]:
        if self.data.training_data is not None:
            logger.debug("Predicting train set.")
            return self.model.predict(self.data.X_train)
        else:
            raise ValueError("Training data not specified in DataContext.")

    @property
    def predictions_minimum_functionality(self) -> Optional[pd.Series]:
        if self.data.minimum_functionality_data is not None:
            logger.debug("Predicting minimum functionality set.")
            return self.model.predict(self.data.minimum_functionality_data[self.data.features])
        else:
            raise ValueError("Minimum functionality data not specified in DataContext.")

    @property
    def predictions_test(self) -> pd.Series:
        logger.debug("Predicting test set.")
        return self.model.predict(self.data.X_test)

    @property
    def probabilities_train(self) -> Optional[Dict[str, pd.Series]]:
        if self.data.training_data is not None:
            logger.debug("Predicting probabilities on train set.")
            probabilities = {}
            for _class, _proba in zip(self.model.classes_, self.model.predict_proba(self.data.X_train).T):
                probabilities[_class] = _proba
            return probabilities
        else:
            raise ValueError("Training data not specified in DataContext.")

    @property
    def probabilities_test(self) -> Dict[str, pd.Series]:
        logger.debug("Predicting probabilities on test set.")
        probabilities = {}
        for _class, _proba in zip(self.model.classes_, self.model.predict_proba(self.data.X_test).T):
            probabilities[_class] = _proba
        return probabilities

    @property
    def testing_data_errors(self):
        return self._filter_errors(self.data.testing_data)

    def _filter_errors(self, df):
        predict_col = f"{self.data.target}_predictions"
        assign_kwargs = {predict_col: self.predictions_test}
        return df.assign(**assign_kwargs).loc[lambda x: x[self.data.target] != x[predict_col], :]


class FeedbackContext(BaseModel):
    """Context for feedback given by a user from a UI component."""

    feedback_type: Optional[str]
    metadata: Dict[str, Union[List[Any], float, int, str, dict]]

    def save_ui(self, url: str):
        make_request(
            f"{url}/api/feedback", headers={"Content-Type": "application/json"}, data=self.json().encode("utf-8")
        )


def _validation_context_example():
    return {
        "example": {
            "validation_type": "validate_performance_against_threshold",
            "validation_kwargs": {"args": [], "kwargs": {"threshold": 0.8}},
            "outcome": "fail",
            "severity": "error",
            "result": {"performance": "0.79"},
        }
    }


class ValidationContext(BaseModel):
    """
    The ValidationContext represents a single validation point.

    Note:
        The ValidationContext is applied to validations with the @validation_output decorator.

    Attributes:
        validation_type: method name of the validation.
        validation_kwargs: all args and kwargs that the validation had run with.
        explanation: docstring explanation of the validation.
        outcome: pass or fail output of the validation.
        severity: severity of the validation, can be one of ["error", "warning", "experiment"], is "error" by default
        result: a dictionary of contextual elements calculated during the validation run
    """

    validation_type: str
    validation_kwargs: Dict[str, Optional[Any]]
    explanation: str
    outcome: str
    severity: str = "error"
    result: Optional[Dict[str, Optional[Any]]]

    class Config:
        extra = "forbid"
        validate_assignment = True
        schema_extra = _validation_context_example()

    @validator("severity")
    def severity_must_be(cls, v: str):
        severity_values = ["error", "warning", "experiment"]
        if v not in severity_values:
            raise KeyError(f"Severity must be set to: {severity_values}.")
        return v

    @validator("outcome")
    def outcome_must_be(cls, v: str):
        outcome_values = ["pass", "fail"]
        if v not in outcome_values:
            raise KeyError(f"Outcome must be set to: {outcome_values}.")
        return v


class TrubricContext(BaseModel):
    """
    Context for a Trubric, or set of validation points.

    Attributes:
        name: Trubric name.
        model_name: model name
        model_version: model version
        data_context_name: data context name (from DataContext)
        data_context_version: data context version (from DataContext)
        metadata: free textual metadata field
        validations: list of validations (defined by ValidationContext)
    """

    trubric_name: str = "my_trubric"
    model_name: str = "my_model"
    model_version: float = 0.1
    data_context_name: str
    data_context_version: float
    metadata: Optional[Dict[str, str]] = None
    validations: List[ValidationContext]

    class Config:
        schema_extra = {
            "example": {
                "name": "my_first_trubric",
                "model_name": "my_model",
                "model_version": 0.1,
                "data_context_name": "my_dataset",
                "data_context_version": 0.1,
                "metadata": {},
                "validations": [_validation_context_example()],
            }
        }

    def save_local(self, path: str, file_name: Optional[str] = None):
        if path is None:
            raise TypeError("Specify the local path where you would like to save your Trubric json.")
        if file_name is None:
            file_name = f"{self.trubric_name}.json"
        with open(Path(path) / file_name, "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Trubric saved to {Path(path) / file_name}.")

    def save_ui(self, url: str, user_id: str):

        if user_id is None:
            raise TypeError("You must specify a 'user_id' to push to the trubrics manager.")
        else:
            make_request(
                f"{url}/api/trubrics/{user_id}",
                headers={"Content-Type": "application/json"},
                data=self.json().encode("utf-8"),
            )
            logger.info("Trubric saved to the trubrics manager.")
