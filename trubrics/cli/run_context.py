from typing import Any, Optional

from pydantic import BaseModel

from trubrics.context import DataContext, ModelContext


class TrubricRun(BaseModel):
    data_context: DataContext
    model_context: ModelContext
    trubric_path: str
    custom_validator: Optional[Any]
