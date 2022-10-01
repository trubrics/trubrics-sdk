from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from trubrics.utils.trubrics_manager_connector import make_request


class Feedback(BaseModel):
    """Dataclass for feedback given by a user from a UI component."""

    feedback_type: Optional[str]
    metadata: Dict[str, Union[List[Any], float, int, str, dict]]

    def save_ui(self, url: str):
        make_request(
            f"{url}/api/feedback", headers={"Content-Type": "application/json"}, data=self.json().encode("utf-8")
        )
