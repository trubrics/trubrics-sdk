from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from git import InvalidGitRepositoryError
from git.repo import Repo
from loguru import logger
from pydantic import BaseModel, validator

from trubrics.exceptions import TrubricValidationError
from trubrics.trubrics_platform.auth import (
    expire_after_n_seconds,
    get_trubrics_auth_token,
)
from trubrics.trubrics_platform.firestore import add_document_to_project_subcollection
from trubrics.trubrics_platform.trubrics_config import load_trubrics_config


def _validation_context_example():
    return {
        "example": {
            "validation_type": "validate_performance_against_threshold",
            "validation_kwargs": {"args": [], "kwargs": {"threshold": 0.8}},
            "passed": True,
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
        passed: pass or fail output of the validation.
        severity: severity of the validation, can be one of ["error", "warning", "experiment"], is "error" by default
        result: a dictionary of contextual elements calculated during the validation run
        explanation: docstring explanation of the validation.
    """

    validation_type: str
    validation_kwargs: Dict[str, Optional[Any]]
    passed: bool
    severity: str = "error"
    result: Optional[Dict[str, Optional[Any]]]
    explanation: str

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


class Trubric(BaseModel):
    """
    Dataclass for a trubric, or set of validation points. Must be serialisable to .json.
    A Trubric must contain at least metadata about the DataContext used to create the validations,
    and should contain metadata also about any model that is used.

    Attributes:
        name: trubric name
        passed: has trubric passed all validations (depends on the failing_severity)
        total_passed: number of validations that passed (depends on the failing_severity)
        total_failed: number of validations that failed (depends on the failing_severity)
        failing_severity: minimum severity that the trubric fails on, can be one of ["error", "warning", "experiment"].
        data_context_name: data context name (from DataContext)
        data_context_version: data context version (from DataContext)
        model_name: model name
        model_version: model version
        tags: list of tags for the trubric
        run_by: who the trubric was run by
        git_commit: a git commit hash from the git repo where the trubric was run
        timestamp: timestamp at which the trubric was run
        metadata: free textual metadata field
        validations: list of validations (defined by Validation)
    """

    name: str
    passed: Optional[bool] = None
    total_passed: Optional[int] = None
    total_failed: Optional[int] = None
    failing_severity: str = "error"
    data_context_name: str
    data_context_version: str
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    tags: List[Optional[str]] = []
    run_by: Optional[Dict[str, str]] = None
    git_commit: Optional[str] = None
    timestamp: Optional[int] = None
    metadata: Optional[Dict[str, str]] = None
    validations: List[Validation]

    class Config:
        extra = "forbid"

    @validator("failing_severity")
    def failing_severity_must_be(cls, v: str):
        severity_values = ["error", "warning", "experiment"]
        if v not in severity_values:
            raise KeyError(f"Failing severity must be set to: {severity_values}.")
        return v

    def save_local(self, path: Optional[str] = None, raise_on_failure: bool = False):
        self.set_dynamic_fields()
        if path is None:
            path = f"./{self.name}.json"
        with open(Path(path).absolute(), "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Trubric saved to {path}.")

        if raise_on_failure:
            self.raise_trubric_failure()

    def save_ui(self, raise_on_failure: bool = False):
        trubrics_config = load_trubrics_config()
        auth = get_trubrics_auth_token(
            trubrics_config.firebase_api_key,
            trubrics_config.email,
            trubrics_config.password.get_secret_value(),
            rerun=expire_after_n_seconds(),
        )

        self.run_by = {"email": trubrics_config.email, "displayName": trubrics_config.username}
        self.set_dynamic_fields()

        res = add_document_to_project_subcollection(
            auth,
            firestore_api_url=trubrics_config.firestore_api_url,
            project=trubrics_config.project,
            subcollection="trubrics",
            document_id=self.timestamp,
            document_dict=self.dict(),
        )
        if "error" in res:
            error_msg = f"Error in pushing trubric to the Trubrics UI: {res}"
            logger.error(error_msg)
            raise Exception(error_msg)
        else:
            logger.info("Trubric saved to the Trubrics UI.")

        if raise_on_failure:
            self.raise_trubric_failure()

    def set_dynamic_fields(self):
        if self.failing_severity == "warning":
            failing_severity = ["error", "warning"]
        elif self.failing_severity == "experiment":
            failing_severity = ["error", "warning", "experiment"]
        else:
            failing_severity = ["error"]
        validations = [validation for validation in self.validations if validation.severity in failing_severity]
        self.total_passed = len([a for a in validations if a.passed])
        self.total_failed = len(validations) - self.total_passed
        self.passed = True if self.total_failed == 0 else False
        self.timestamp = int(datetime.now().timestamp())
        try:
            self.git_commit = Repo(search_parent_directories=True).head.object.hexsha
        except InvalidGitRepositoryError:
            self.git_commit = None
            logger.warning(
                "Current directory is not a git repository. Run `trubrics run` inside a git repository to save the"
                " commit hash."
            )
        return self

    def raise_trubric_failure(self):
        if not self.passed and self.total_failed:
            raise TrubricValidationError(
                "Trubric has failed on"
                f" {self.total_failed} {'validations' if self.total_failed > 1 else 'validation'} with minimum"
                f" severity='{self.failing_severity}'."
            )
