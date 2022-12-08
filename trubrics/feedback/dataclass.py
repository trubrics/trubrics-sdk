import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from git.repo import Repo
from loguru import logger
from pydantic import BaseModel

from trubrics.utils.trubrics_manager_connector import make_request


class Feedback(BaseModel):
    """Dataclass for feedback given by a user from a UI component."""

    title: str
    description: str
    tags: Optional[List[str]]
    model_name: str = "my_model"
    model_version: float = 0.1
    data_context_name: str
    data_context_version: float
    open: bool = True
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

    def save_ui(self, trubrics_config_path: str):

        if trubrics_config_path is None:
            raise TypeError("Please specify your trubrics config file path.")
        else:
            config_file = Path(trubrics_config_path) / ".trubrics_config.json"
            with open(config_file) as f:
                config = json.loads(f.read())

            if self.metadata:
                self.metadata.update(config)
                self.metadata["timestamp"] = str(datetime.now())
                self.metadata["git_commit"] = Repo(search_parent_directories=True).head.object.hexsha
                self.collaborators.append(config["display_name"])

            make_request(
                f"{config['api_url']}/api/feedback/{config['user_id']}/{config['project_id']}",
                headers={"Content-Type": "application/json"},
                data=self.json().encode("utf-8"),
                method="POST",
            )
            logger.info("Feedback issue saved to the Trubrics Manager.")
