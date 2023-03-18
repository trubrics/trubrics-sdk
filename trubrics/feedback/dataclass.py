from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from git import InvalidGitRepositoryError
from git.repo import Repo
from loguru import logger
from pydantic import BaseModel, validator

from trubrics.ui.auth import get_trubrics_auth_token
from trubrics.ui.firestore import add_document_to_project_subcollection
from trubrics.ui.trubrics_config import load_trubrics_config


class Feedback(BaseModel):
    """
    Dataclass for feedback given by a user from a UI component.

    Attributes:
        type: feedback type ['issue', 'faces', 'thumbs', 'custom']
        title: a title of the feedback
        description: a description of the feedback
        data_context_name: data context name (from DataContext)
        data_context_version: data context version (from DataContext)
        model_name: model name
        model_version: model version
        collaborators: users who have collaborated so far on the issue
        open: whether the feedback item is open or closed
        tags: list of tags for the feedback issue
        git_commit: a git commit hash from the git repo where the app was run to collect feedback
        timestamp: timestamp at which the feedback was recorded
        created_by: who the feedback was run by
        closed_on: timestamp when the feedback was closed
        closed_by: who the feedback was run by
        metadata: free textual metadata field
    """

    type: str
    title: str
    description: str
    data_context_name: Optional[str]
    data_context_version: Optional[str]
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    collaborators: List[Optional[str]] = []
    open: bool = True
    tags: Optional[List[str]] = None
    git_commit: Optional[str] = None
    timestamp: Optional[int] = None
    created_by: Optional[Dict[str, Optional[str]]] = None
    closed_on: Optional[str] = None
    closed_by: Optional[str] = None
    metadata: Optional[Dict[str, Union[List[Any], float, int, str, dict]]] = None

    @validator("type")
    def target_column_must_be_in_data(cls, v):
        if v not in ["issue", "faces", "thumbs", "custom"]:
            raise ValueError("type must be one of ['issue', 'faces', 'thumbs', 'custom'].")
        return v

    def save_local(self, path: Optional[str] = None):
        self._set_fields_on_save()
        if path is None:
            path = f"./{self.timestamp}_feedback.json"
        with open(Path(path).absolute(), "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Feedback saved to {path}.")

    def save_ui(self, email: Optional[str], password: Optional[str]):
        trubrics_config = load_trubrics_config()
        self._set_fields_on_save()

        if email is None and password is None:
            email = trubrics_config.email
            password = trubrics_config.password.get_secret_value()

        auth = get_trubrics_auth_token(trubrics_config.firebase_auth_api_url, email, password)
        if "error" in auth:
            error_msg = f"Error in pushing feedback issue with email '{email}' to the Trubrics UI: {auth['error']}"
            logger.error(error_msg)
            raise Exception(error_msg)
        else:
            self.created_by = {"email": auth["email"], "displayName": auth["displayName"]}
            self.collaborators.append(auth["displayName"])

            res = add_document_to_project_subcollection(
                auth,
                firestore_api_url=trubrics_config.firestore_api_url,
                project=trubrics_config.project,
                subcollection="feedback",
                document_id=self.timestamp,
                document_json=self.json(),
            )
            if "error" in res:
                error_msg = f"Error in pushing feedback issue to the Trubrics UI: {res}"
                logger.error(error_msg)
                raise Exception(error_msg)
            else:
                logger.info("Feedback issue saved to the Trubrics UI.")

    def _set_fields_on_save(self):
        self.timestamp = int(datetime.now().timestamp())
        try:
            self.git_commit = Repo(search_parent_directories=True).head.object.hexsha
        except InvalidGitRepositoryError:
            logger.warning(
                "Current directory is not a git repository. Run `trubrics run` inside a git repository to save the"
                " commit hash."
            )
