import pandas as pd

from trubrics.context import DataContext, ModelContext
from trubrics.modellers.base import Modeller


class Classifier(Modeller):
    """Classifier class with methods combining data and model contexts."""

    def __init__(self, data: DataContext, model: ModelContext):
        super().__init__(data, model)

    def explore_test_set_errors(self, business_columns: bool = False) -> pd.DataFrame:
        """Filter the testing data on errors.

        Show all errors (with associated features) on the test set, returning a dataframe with
        either the raw column names or the renamed business columns.

        TODO: Fix if target column is renamed.

        Parameters
        ----------
        business_columns
            Set to *false* as a default, this flag allows you to return business column names or
            raw column names.
        """

        def _filter_errors(df):
            predict_col = f"{self.data.target_column}_predictions"
            assign_kwargs = {predict_col: self.predict()}
            return df.assign(**assign_kwargs).loc[lambda x: x[self.data.target_column] != x[predict_col], :]

        if business_columns:
            return _filter_errors(self.data.renamed_testing_data)
        else:
            return _filter_errors(self.data.testing_data)
