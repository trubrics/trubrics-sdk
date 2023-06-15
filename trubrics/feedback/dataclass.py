from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Response(BaseModel):
    type: str
    score: Optional[str]
    text: Optional[str]


class Feedback(BaseModel):
    component_name: str
    model: str
    response: Response
    created_on: datetime
    user_id: Optional[str] = None
    tags: list = []
    metadata: dict = {}
