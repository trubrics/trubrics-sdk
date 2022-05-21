from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

from trubrics.context import DataContext, ModelContext


class BaseTester:
    """Base class for Models."""

    def __init__(self, model: ModelContext, data: DataContext):
        self.model = model
        self.data = data

    def _predict(self, data: Optional[pd.DataFrame] = None) -> pd.Series:
        if data is None:
            data = self.data.testing_data
        try:
            return self.model.estimator.predict(data)  # type: ignore
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def _predict_proba(self, data: Optional[pd.DataFrame] = None) -> pd.Series:
        if data is None:
            data = self.data.testing_data
        try:
            return self.model.estimator.predict_proba(data)  # type: ignore
        except AttributeError as error:
            raise AttributeError("Model has no .predict_proba() method.") from error

    def test_single_edge_case(self, edge_case_data: pd.DataFrame, desired_output: Union[int, float]) -> bool:
        """
        Single edge case test that:
            - reads the test config about the schema & data (features and expected output)
            - calls .predict() on the model with the stored data
            - tests the output of that model versus the desired output
        """
        prediction = self._predict(edge_case_data)[0]
        return prediction == desired_output

    def test_performance_against_threshold(self, threshold: float) -> bool:
        """
        Compares performance of a model on a dataset to a hard coded threshold value.
        """
        predictions = self._predict()
        if self.model.evaluation_function.__name__ == "accuracy_score":
            result = self.model.evaluation_function(  # type: ignore
                self.data.testing_data[self.data.target_column], predictions
            )
            return result > threshold
        else:
            raise NotImplementedError("The evaluation type is not recognized.")

    def test_biased_performance_across_category(self, category: str, threshold: float) -> bool:
        """
        Calculates various performance for all values in a category and tests for
        the maximum difference in performance inferior to the threshold value.

        TODO:
        - More complex threshold function
        - Modify cardinality

        To add to output report:
        - Show distributions of category variables
        - Performance plots of results
        """
        cat_values = list(self.data.testing_data[category].unique())  # type: ignore
        if len(cat_values) > 20:
            raise Exception(f"Cardinality of {len(cat_values)} too high for performance test.")
        if category not in self.data.testing_data.columns:
            raise KeyError(f"Column '{category}' not found in dataset.")
        result: Dict[str, Union[int, float]] = {}
        for value in cat_values:
            if value not in [np.nan, None]:
                filtered_data = self.data.testing_data.query(f"`{category}`=='{value}'")
                predictions = self._predict(filtered_data.loc[:, self.list_model_features(filtered_data)])
                result[value] = self.model.evaluation_function(  # type: ignore
                    filtered_data[self.data.target_column], predictions
                )
        max_performance_difference = max(result.values()) - min(result.values())
        return max_performance_difference < threshold

    @staticmethod
    def test_feature_in_top_n_important_features(
        feature: str, feature_importance: Dict[str, float], top_n_features: int
    ) -> bool:
        """
        Verifies that a given feature is in the top n most important features.
        """
        count = 0
        for importance in feature_importance.values():
            if importance > feature_importance[feature]:
                count += 1
        return count < top_n_features

    def list_model_features(self, data: Optional[pd.DataFrame] = None) -> List[str]:
        """Get features column names excluding the target feature."""
        if data is None:
            return [col for col in self.data.testing_data.columns if col != self.data.target_column]
        return [col for col in data.columns if col != self.data.target_column]
