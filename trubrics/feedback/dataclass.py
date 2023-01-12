from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

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
    tags: Optional[List[str]] = None
    model_name: str = "my_model"
    model_version: str = "0.1"
    data_context_name: str = "my_data_context"
    data_context_version: str = "0.1"
    open: bool = True
    created_on: Optional[str] = None
    created_by: Optional[str] = None
    closed_on: Optional[str] = None
    closed_by: Optional[str] = None
    discussion: List[Dict[str, str]] = []
    collaborators: List[str] = []
    metadata: Optional[Dict[str, Union[List[Any], float, int, str, dict]]]

    def save_local(self, path: str, file_name: Optional[str] = None):
        if path is None:
            raise TypeError("Specify the local path where you would like to save your Trubric json.")
        if file_name is None:
            file_name = "feedback.json"
        with open(Path(path) / file_name, "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Feedback saved to {Path(path) / file_name}.")

    def save_ui(self):
        trubrics_config = load_trubrics_config()
        auth = get_trubrics_auth_token(
            trubrics_config.firebase_auth_api_url, trubrics_config.email, trubrics_config.password
        )

        if self.metadata:
            self.metadata["timestamp"] = str(datetime.now())
            self.metadata["git_commit"] = Repo(search_parent_directories=True).head.object.hexsha
            if self.tags:
                self.tags.append(str(self.metadata["tags"]))
            self.created_by = trubrics_config.email

        response = add_document_to_project_subcollection(
            auth,
            firestore_api_url=trubrics_config.firestore_api_url,
            project=trubrics_config.project,
            subcollection="feedback",
            document_id=self.title,  # type: ignore
            document_json=self.json(),
        )
        print(response)

        logger.info("Feedback issue saved to the Trubrics Manager.")
