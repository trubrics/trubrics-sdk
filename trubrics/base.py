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

        TODO: fix errors due to self.data.target_column and self.data.categorical_columns
        """
        if self.data.business_columns is None:
            raise TypeError("Business columns not set in DataContext.")
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

    def explore_test_set_errors(self, business_columns: bool = False):
        """
        Return the testing dataset errors with a prediction column.
        """
        if business_columns:
            predict_col = f"{self.data.target_column}_predictions"
            assign_kwargs = {predict_col: self.predict()}
            return (
                self.get_renamed_test_data()
                .assign(**assign_kwargs)
                .loc[lambda x: x[self.data.target_column] != x[predict_col], :]
            )
        else:
            raise NotImplementedError("Todo")
