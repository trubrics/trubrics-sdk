from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    model: str
    prompt_template: str = "{prompt}"
    temperature: Optional[str] = None


class Prompt(BaseModel):
    """
    The Prompt object represents all data contained as a prompt / model request from a user.

    Example:
        ```py
        import trubrics

        feedback = trubrics.collect(
        )
        ```

    Attributes:
        model: the model name / version
    """

    id: Optional[str] = None
    model_config: ModelConfig
    prompt: str
    generation: str
    created_on: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    tags: list = []
    metadata: dict = {}
