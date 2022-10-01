from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from loguru import logger
from pydantic import BaseModel


class Feedback(BaseModel):
    """Dataclass for feedback given by a user from a UI component."""

    feedback_type: Optional[str]
    metadata: Dict[str, Union[List[Any], float, int, str, dict]]

    def save_local(self, path: str, file_name: Optional[str] = None):
        if path is None:
            raise TypeError("Specify the local path where you would like to save your Trubric json.")
        if file_name is None:
            file_name = f"{self.feedback_type}.json"
        with open(Path(path) / file_name, "w") as file:
            file.write(self.json(indent=4))
            logger.info(f"Trubric saved to {Path(path) / file_name}.")
