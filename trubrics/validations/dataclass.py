from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, validator

from trubrics.utils.trubrics_manager_connector import make_request


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


class Validation(BaseModel):
    """
    Dataclass for a single validation point. Must be serialisable to .json, as is fed into Trubric dataclass.

    Note:
        A Validation object constrains the output of validations, with the @validation_output decorator.

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


class Trubric(BaseModel):
    """
    Dataclass for a trubric, or set of validation points. Must be serialisable to .json.

    Attributes:
        name: Trubric name.
        model_name: model name
        model_version: model version
        data_context_name: data context name (from DataContext)
        data_context_version: data context version (from DataContext)
        metadata: free textual metadata field
        validations: list of validations (defined by Validation)
    """

    trubric_name: str = "my_trubric"
    model_name: str = "my_model"
    model_version: float = 0.1
    data_context_name: str
    data_context_version: float
    metadata: Optional[Dict[str, str]] = None
    validations: List[Validation]

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
