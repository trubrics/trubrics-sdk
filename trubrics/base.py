from typing import Callable, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator


class BaseModel:
    """Base class for Models."""

    def __init__(
        self,
        model: BaseEstimator,
        training_data: pd.DataFrame,
        testing_data: pd.DataFrame,
        target_col: str,
        evaluation_function: Callable,
    ):
        self.model = model
        self.training_data = training_data
        self.testing_data = testing_data
        self.target_col = target_col

        # TODO: check on evaluation function
        self.evaluation_function = evaluation_function

    def predict(self, data: Optional[pd.DataFrame] = None) -> np.ndarray:
        if data is None:
            data = self.testing_data
        try:
            return self.model.predict(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def predict_proba(self, data: pd.DataFrame = None) -> np.ndarray:
        if data is None:
            data = self.testing_data
        try:
            return self.model.predict_proba(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict_proba() method.") from error

    def test_single_edge_case(self, edge_case_data: pd.DataFrame, desired_output: Union[int, float]) -> bool:
        """
        Single edge case test that:
            - reads the test config about the schema & data (features and expected output)
            - calls .predict() on the model with the stored data
            - tests the output of that model versus the desired output
        """
        prediction = self.predict(edge_case_data)[0]
        return prediction == desired_output

    def test_performance_against_threshold(self, threshold: float) -> bool:
        """
        Compares performance of a model on a dataset to a hard coded threshold value.
        """
        predictions = self.predict()
        if self.evaluation_function.__name__ == "accuracy_score":
            result = self.evaluation_function(self.testing_data[self.target_col], predictions)
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
        cat_values = self.testing_data[category].unique()
        if len(cat_values) > 20:
            raise Exception(f"Cardinality of {len(cat_values)} too high for performance test.")
        if category not in self.testing_data.columns:
            raise KeyError(f"Column '{category}' not found in dataset.")
        result = {}
        for value in cat_values:
            if value not in [np.nan, None]:
                filtered_data = self.testing_data.query(f"`{category}`=='{value}'")
                predictions = self.predict(filtered_data.loc[:, self.list_model_features(filtered_data)])
                result[value] = self.evaluation_function(filtered_data[self.target_col], predictions)
        max_performance_difference = max(result.values()) - min(result.values())
        return max_performance_difference < threshold

    def test_feature_in_top_n_important_features(
        self, feature: str, feature_importance: dict, top_n_features: int
    ) -> bool:
        """
        Verifies that a given feature is in the top n most important features.
        """
        count = 0
        for importance in feature_importance.values():
            if importance > feature_importance.get(feature):
                count += 1
        return count < top_n_features

    def list_model_features(self, data: pd.DataFrame) -> list:
        """Get features column names excluding the target feature."""
        return [col for col in data.columns if col != self.target_col]
