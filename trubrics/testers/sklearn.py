from typing import Dict, Union

import numpy as np
import pandas as pd

from trubrics.base import BaseModeller
from trubrics.context import ValidationContext


class SklearnTester(BaseModeller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def test_single_edge_case(
        self, edge_case_data: pd.DataFrame, desired_output: Union[int, float]
    ) -> ValidationContext:
        """
        Single edge case test that:
            - reads the test config about the schema & data (features and expected output)
            - calls .predict() on the model with the stored data
            - tests the output of that model versus the desired output
        """
        prediction = self.predict(edge_case_data)[0]
        outcome = pass_or_fail(prediction == desired_output)

        return ValidationContext(
            validation_type=self.test_single_edge_case.__name__,
            validation_kwargs={"edge_case_data": edge_case_data.to_dict(), "desired_output": desired_output},
            outcome=outcome,
            result=None,
        )

    def test_performance_against_threshold(self, threshold: float) -> ValidationContext:
        """
        Compares performance of a model on a dataset to a hard coded threshold value.
        """
        predictions = self.predict()
        if self.model.evaluation_function.__name__ == "accuracy_score":
            result = self.model.evaluation_function(  # type: ignore
                self.data.testing_data[self.data.target_column], predictions
            )
            outcome = pass_or_fail(result > threshold)

            return ValidationContext(
                validation_type=self.test_performance_against_threshold.__name__,
                validation_kwargs={"threshold": threshold},
                outcome=outcome,
                result={"performance": result},
            )
        else:
            raise NotImplementedError("The evaluation type is not recognized.")

    def test_biased_performance_across_category(self, category: str, threshold: float) -> ValidationContext:
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
                predictions = self.predict(filtered_data.loc[:, self.data.list_features(filtered_data)])
                result[value] = self.model.evaluation_function(  # type: ignore
                    filtered_data[self.data.target_column], predictions
                )
        max_performance_difference = max(result.values()) - min(result.values())
        outcome = pass_or_fail(max_performance_difference < threshold)

        return ValidationContext(
            validation_type=self.test_biased_performance_across_category.__name__,
            validation_kwargs={"category": category, "threshold": threshold},
            outcome=outcome,
            result=None,
        )

    def test_feature_in_top_n_important_features(
        self, feature: str, feature_importance: Dict[str, float], top_n_features: int
    ) -> ValidationContext:
        """
        Verifies that a given feature is in the top n most important features.
        """
        count = 0
        for importance in feature_importance.values():
            if importance > feature_importance[feature]:
                count += 1
        outcome = pass_or_fail(count < top_n_features)

        return ValidationContext(
            validation_type=self.test_feature_in_top_n_important_features.__name__,
            validation_kwargs={
                "feature": feature,
                "feature_importance": feature_importance,
                "top_n_features": top_n_features,
            },
            outcome=outcome,
            result=None,
        )


def pass_or_fail(condition: bool) -> str:
    return "pass" if condition else "fail"
