import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from git import InvalidGitRepositoryError
from git.repo import Repo
from loguru import logger
from pydantic import BaseModel

from trubrics.ui.auth import (
    expire_after_n_seconds,
    get_trubrics_auth_token,
    get_trubrics_firebase_auth_api_url,
)
from trubrics.ui.firestore import (
    get_trubrics_firestore_api_url,
    list_components_in_organisation,
    record_feedback,
)
from trubrics.ui.trubrics_config import TrubricsDefaults


class Response(BaseModel):
    type: str
    score: Optional[str]
    text: Optional[str]


class Feedback(BaseModel):
    """
    Dataclass for feedback given by a user from a UI component.

    Attributes:
        TODO
    """

    component_name: str
    response: Response
    model: Optional[str] = None
    datasets: List[Optional[str]] = [None]
    model_input: Optional[Any] = None
    model_output: Optional[Any] = None
    tags: Optional[List[str]] = None
    git_commit: Optional[str] = None
    created_by: Optional[Dict[str, Optional[str]]] = None
    created_on: Optional[datetime] = None
    metadata: Optional[Dict[str, Union[List[Any], float, int, str, dict]]] = None

    def save_local(self, path: Optional[str] = None):
        if path is None:
            path = f"./{self.component_name}_feedback.json"
        with open(Path(path).absolute(), "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Feedback saved to {path}.")

    def save_ui(self, firebase_api_key: Optional[str] = None, firebase_project_id: Optional[str] = None):
        """
        1. read trubrics config
        2. check component name exists
        3. record feedback to component
        """
        if firebase_api_key or firebase_project_id:
            if firebase_api_key and firebase_project_id:
                defaults = TrubricsDefaults(firebase_api_key=firebase_api_key, firebase_project_id=firebase_project_id)
            else:
                raise ValueError("Both API key and firebase_project_id are required to change project.")
        else:
            defaults = TrubricsDefaults()

        email = os.environ["TRUBRICS_CONFIG_EMAIL"]
        password = os.environ["TRUBRICS_CONFIG_PASSWORD"]
        firebase_auth_api_url = get_trubrics_firebase_auth_api_url(defaults.firebase_api_key)
        auth = get_trubrics_auth_token(firebase_auth_api_url, email, password, rerun=expire_after_n_seconds())
        if "error" in auth:
            raise Exception(f"Error in login email '{email}' to the Trubrics UI: {auth['error']}")
        else:
            firestore_api_url = get_trubrics_firestore_api_url(auth, defaults.firebase_project_id)

        components = list_components_in_organisation(firestore_api_url=firestore_api_url, auth=auth)
        if self.component_name not in components:
            raise ValueError(
                f"Component '{self.component_name}' not found in organisation '{firestore_api_url.split('/')[-1]}'."
                f" Components currently available: {components}."
            )

        if "error" in auth:
            error_msg = f"Error in pushing feedback issue with email '{email}' to the Trubrics UI: {auth['error']}"
            logger.error(error_msg)
            raise Exception(error_msg)
        else:
            self.created_by = {"email": auth["email"], "name": auth["displayName"]}
            self.created_on = datetime.now()
            try:
                self.git_commit = Repo(search_parent_directories=True).head.object.hexsha
            except InvalidGitRepositoryError:
                logger.warning(
                    "Current directory is not a git repository. Run `trubrics run` inside a git repository to save the"
                    " commit hash."
                )

            res = record_feedback(
                auth,
                firestore_api_url=firestore_api_url,
                component=self.component_name,
                document_json=self.dict(),
            )
            if "error" in res:
                error_msg = f"Error in pushing feedback issue to the Trubrics UI: {res}"
                logger.error(error_msg)
                raise Exception(error_msg)
            else:
                logger.info("Feedback saved to the Trubrics UI.")
