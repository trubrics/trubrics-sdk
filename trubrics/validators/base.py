from typing import Dict, Union

import numpy as np
import pandas as pd

from trubrics.base import BaseClassifier
from trubrics.validators.validation_output import (
    validation_output,
    validation_output_type,
)


class Validator(BaseClassifier):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @validation_output
    def validate_single_edge_case(
        self, edge_case_data: Dict[str, str], desired_output: Union[int, float]
    ) -> validation_output_type:
        """
        Single edge case validation.
        """
        edge_case_data = pd.DataFrame.from_records(edge_case_data, index=[0])  # type: ignore
        prediction = self.model.estimator.predict(edge_case_data)[  # type: ignore
            0
        ].item()  # .item() converts numpy to python type, in order to be serialised to json

        return prediction == desired_output, {"prediction": prediction}

    @validation_output
    def validate_performance_against_threshold(self, threshold: float) -> validation_output_type:
        """
        Compares performance of a model on a dataset to a hard coded threshold value.
        """
        predictions = self.predict()
        if self.model.evaluation_function.__name__ == "accuracy_score":
            performance = float(
                self.model.evaluation_function(  # type: ignore
                    self.data.testing_data[self.data.target_column], predictions
                )
            )
            return performance > threshold, {"performance": performance}
        else:
            raise NotImplementedError("The evaluation type is not recognized.")

    @validation_output
    def validate_biased_performance_across_category(self, category: str, threshold: float) -> validation_output_type:
        """
        Calculates various performance for all values in a category and validates for
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
                predictions = self.model.estimator.predict(filtered_data.loc[:, self.data.features])  # type: ignore
                result[value] = float(
                    self.model.evaluation_function(filtered_data[self.data.target_column], predictions)  # type: ignore
                )
        max_performance_difference = max(result.values()) - min(result.values())

        return max_performance_difference < threshold, {"max_performance_difference": max_performance_difference}

    @validation_output
    def validate_feature_in_top_n_important_features(
        self, feature: str, feature_importance: Dict[str, float], top_n_features: int
    ) -> validation_output_type:
        """
        Verifies that a given feature is in the top n most important features.
        """
        count = 0
        for importance in feature_importance.values():
            if importance > feature_importance[feature]:
                count += 1

        return count < top_n_features, {"feature_importance_ranking": count}
