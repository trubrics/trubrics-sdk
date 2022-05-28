from typing import Optional

import pandas as pd

from trubrics.context import DataContext, ModelContext


class BaseModeller:
    """Base class with methods combining data and model contexts."""

    def __init__(self, model: ModelContext, data: DataContext):
        self.model = model
        self.data = data

    def get_renamed_test_data(self):
        """
        Get test DataFrame with renamed business columns.
        """
        return self.data.testing_data.rename(columns=self.data.business_columns)

    def predict(self, data: Optional[pd.DataFrame] = None) -> pd.Series:
        if data is None:
            data = self.data.testing_data
        try:
            return self.model.estimator.predict(data)  # type: ignore
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def predict_proba(self, data: Optional[pd.DataFrame] = None) -> pd.Series:
        if data is None:
            data = self.data.testing_data
        try:
            return self.model.estimator.predict_proba(data)  # type: ignore
        except AttributeError as error:
            raise AttributeError("Model has no .predict_proba() method.") from error
