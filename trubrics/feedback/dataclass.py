from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from git import InvalidGitRepositoryError
from git.repo import Repo
from loguru import logger
from pydantic import BaseModel

from trubrics.ui.auth import get_trubrics_auth_token
from trubrics.ui.firestore import add_document_to_project_subcollection
from trubrics.ui.trubrics_config import load_trubrics_config


class Feedback(BaseModel):
    """Dataclass for feedback given by a user from a UI component."""

    title: str
    description: str
    model_name: str = "my_model"
    model_version: str = "0.0.1"
    data_context_name: str = "my_data_context"
    data_context_version: str = "0.0.1"
    collaborators: List[Optional[str]] = []
    open: bool = True
    tags: Optional[List[str]] = None
    git_commit: Optional[str] = None
    timestamp: Optional[int] = None
    created_by: Optional[Dict[str, Optional[str]]] = None
    closed_on: Optional[str] = None
    closed_by: Optional[str] = None
    metadata: Optional[Dict[str, Union[List[Any], float, int, str, dict]]] = None

    def save_local(self, path: Optional[str] = None):
        self._set_fields_on_save()
        if path is None:
            path = f"./{self.timestamp}_feedback.json"
        with open(Path(path).absolute(), "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Feedback saved to {path}.")

    def save_ui(self, email: str, password: str):
        trubrics_config = load_trubrics_config()
        self._set_fields_on_save()
        if trubrics_config.firestore_api_url is None or trubrics_config.project is None:
            raise TypeError("Trubrics config not set. Run `trubrics init` to configure.")

        auth = get_trubrics_auth_token(trubrics_config.firebase_auth_api_url, email, password)
        if "error" in auth:
            error_msg = f"Error in pushing feedback issue with email '{email}' to the Trubrics UI: {auth['error']}"
            logger.error(error_msg)
            raise Exception(error_msg)
        else:
            self.created_by = {"email": auth["email"], "displayName": auth["displayName"]}
            self.collaborators.append(auth["email"])

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
