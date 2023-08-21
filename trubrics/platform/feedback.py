from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Response(BaseModel):
    type: str
    score: Optional[str] = None
    text: Optional[str] = None


class Feedback(BaseModel):
    """
    The Feedback object represents all data contained as a feedback response from a user.

    Example:
        ```py
        import trubrics

        feedback = trubrics.collect(
            component_name="default",
            model="default_model",
            response={
                "type": "thumbs",
                "score": "👎",
                "text": "A comment / textual feedback from the user."
            },
            user_id="user_id",
            tags=["satisfaction"],
            metadata={"prompt": "What is the meaning of user feedback for AI?"}
        )
        ```

    Attributes:
        component_name: the name of the component that the feedback response is saved to
        model: the model name / version
        response: the user response, with a type, score and text
        created_on: datetime of response (in UTC)
        user_id: an optional user id
        tags: optional tags
        metadata: optional metadata, such as model prompts & predictions
    """

    component_name: str
    model: str
    response: Response
    created_on: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    tags: list = []
    metadata: dict = {}
