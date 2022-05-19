from typing import Callable, Optional, Union

import pandas as pd
from pydantic import BaseModel
from sklearn.base import BaseEstimator


class ModelContext(BaseModel):
    """Context for models."""

    name: str
    version: float
    estimator: BaseEstimator
    evaluation_function: Callable[[pd.Series, pd.Series], Union[int, float]]

    class Config:
        allow_mutation = False


class DataContext(BaseModel):
    """Context for data."""

    name: str
    training_data: Optional[pd.DataFrame]
    testing_data: pd.DataFrame
    target_col: str

    class Config:
        allow_mutation = False
