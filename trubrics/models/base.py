from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from trubrics.context import DataContext, ModelContext


class BaseModeller(ABC):
    @abstractmethod
    def __init__(self, data: DataContext, model: ModelContext):
        self.data = data
        self.model = model

    @abstractmethod
    def predict(self, data: Optional[pd.DataFrame] = None) -> pd.Series:
        """Use the estimator to predict on the test data."""

    @abstractmethod
    def explore_test_set_errors(self):
        """Filter the testing data on errors."""

    @abstractmethod
    def compute_performance_on_test_set(self) -> float:
        """Calculate the performance on the test set with the evaluation function."""


class Modeller(BaseModeller):
    def __init__(self, data: DataContext, model: ModelContext):
        self.data = data
        self.model = model

    def predict(self, data: Optional[pd.DataFrame] = None) -> pd.Series:
        """Predict function called on model from model context."""
        try:
            if data is not None:
                return self.model.estimator.predict(data)
            return self.model.estimator.predict(self.data.testing_data[self.data.features])
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def explore_test_set_errors(self):
        """Filter the testing data on errors."""
        raise NotImplementedError()

    def compute_performance_on_test_set(self) -> float:
        """Calculate the performance on the test set with evaluation function."""
        predictions = self.predict()
        actuals = self.data.testing_data[self.data.target_column]
        eval_kwargs = self.model.evaluation_kwargs
        if eval_kwargs:
            return self.model.evaluation_function(predictions, actuals, **eval_kwargs)
        else:
            return self.model.evaluation_function(predictions, actuals)
