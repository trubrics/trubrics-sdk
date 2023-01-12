from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from git.repo import Repo
from loguru import logger
from pydantic import BaseModel, validator

from trubrics.ui.auth import get_trubrics_auth_token
from trubrics.ui.firestore import add_document_to_project_subcollection
from trubrics.ui.trubrics_config import load_trubrics_config


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
        name: trubric name
        model_name: model name
        model_version: model version
        data_context_name: data context name (from DataContext)
        data_context_version: data context version (from DataContext)
        metadata: free textual metadata field
        validations: list of validations (defined by Validation)
    """

    name: str = "my_trubric"
    model_name: str = "my_model"
    model_version: float = 0.1
    data_context_name: str
    data_context_version: float
    metadata: Optional[Dict[str, str]] = None
    validations: List[Validation]

    class Config:
        extra = "forbid"
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
            file_name = f"{self.name}.json"
        self.metadata = set_metadata(self.validations, self.metadata, None)
        with open(Path(path) / file_name, "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Trubric saved to {Path(path) / file_name}.")

    def save_ui(self):
        trubrics_config = load_trubrics_config()
        auth = get_trubrics_auth_token(
            trubrics_config.firebase_auth_api_url, trubrics_config.email, trubrics_config.password
        )

        self.metadata = set_metadata(self.validations, self.metadata, trubrics_config.email)

        add_document_to_project_subcollection(
            auth,
            firestore_api_url=trubrics_config.firestore_api_url,
            project=trubrics_config.project,
            subcollection="trubrics",
            document_id=self.metadata["timestamp"],  # type: ignore
            document_json=self.json(),
        )
        logger.info("Trubric saved to the Trubrics Manager.")


def set_metadata(validations, metadata, email):
    total_passed = len([a for a in validations if a.outcome == "pass"])
    if metadata:
        metadata["email"] = email
        metadata["timestamp"] = str(datetime.now())
        metadata["git_commit"] = Repo(search_parent_directories=True).head.object.hexsha
        metadata["total_passed"] = str(total_passed)
        metadata["total_passed_percent"] = str(round(100 * total_passed / len(validations), 1))
    return metadata
