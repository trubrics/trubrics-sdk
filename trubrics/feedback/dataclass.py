from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Response(BaseModel):
    type: str
    score: Optional[str] = None
    text: Optional[str] = None


class Feedback(BaseModel):
    component_name: str
    model: str
    response: Response
    created_on: datetime = datetime.now()
    user_id: Optional[str] = None
    tags: list = []
    metadata: dict = {}
