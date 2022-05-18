from dataclasses import dataclass
from typing import Callable

import pandas as pd
from sklearn.base import BaseEstimator


@dataclass
class ModelContext:
    """Context for models."""

    name: str
    version: float
    estimator: BaseEstimator
    evaluation_function: Callable


@dataclass
class DataContext:
    """Context for data."""

    name: str
    training_data: pd.DataFrame
    testing_data: pd.DataFrame
    target_col: str
