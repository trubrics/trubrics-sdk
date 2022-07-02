from typing import Dict, Union

import numpy as np
import pandas as pd

from trubrics.exceptions import ClassifierNotSupportedError
from trubrics.modellers.base import BaseModeller
from trubrics.validators.validation_output import (
    validation_output,
    validation_output_type,
)


class Validator:
    def __init__(self, trubrics_model: BaseModeller):
        self.trubrics_model = trubrics_model

    @validation_output
    def validate_single_edge_case(
        self, edge_case_data: Dict[str, str], desired_output: Union[int, float]
    ) -> validation_output_type:
        """
        Single edge case validation.
        """
        edge_case_data = pd.DataFrame.from_records(edge_case_data, index=[0])  # type: ignore
        prediction = self.trubrics_model.model.estimator.predict(edge_case_data)[
            0
        ].item()  # .item() converts numpy to python type, in order to be serialised to json

        return prediction == desired_output, {"prediction": prediction}

    @validation_output
    def validate_single_edge_case_in_range(
        self, edge_case_data: Dict[str, str], lower_output: Union[int, float], upper_output: Union[int, float]
    ) -> validation_output_type:
        """
        Single edge case validation in range.
        """
        if lower_output >= upper_output:
            raise ValueError("lower_output must be strictly inferior to upper_output.")
        if self.trubrics_model.model_type == "classifier":
            raise ClassifierNotSupportedError("Model type 'classifier' not supported for a range output.")
        edge_case_data = pd.DataFrame.from_records(edge_case_data, index=[0])  # type: ignore
        prediction = self.trubrics_model.model.estimator.predict(edge_case_data)[
            0
        ].item()  # .item() converts numpy to python type, in order to be serialised to json

        return prediction > lower_output and prediction < upper_output, {"prediction": prediction}

    @validation_output
    def validate_performance_against_threshold(self, threshold: float) -> validation_output_type:
        """
        Compares performance of a model on a dataset to a hard coded threshold value.
        """
        performance = bool(self.trubrics_model.compute_performance_on_test_set())
        if self.trubrics_model.model.evaluation_function.__name__ == "accuracy_score":
            return performance > threshold, {"performance": performance}
        elif self.trubrics_model.model.evaluation_function.__name__ == "mean_squared_error":
            return performance < threshold, {"performance": performance}
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
        cat_values = list(self.trubrics_model.data.testing_data[category].unique())
        if len(cat_values) > 20:
            raise Exception(f"Cardinality of {len(cat_values)} too high for performance test.")
        if category not in self.trubrics_model.data.testing_data.columns:
            raise KeyError(f"Column '{category}' not found in dataset.")
        result: Dict[str, Union[int, float]] = {}
        for value in cat_values:
            if value not in [np.nan, None]:
                filtered_data = self.trubrics_model.data.testing_data.query(f"`{category}`=='{value}'")
                predictions = self.trubrics_model.model.estimator.predict(
                    filtered_data.loc[:, self.trubrics_model.data.features]
                )
                result[value] = float(
                    self.trubrics_model.model.evaluation_function(
                        filtered_data[self.trubrics_model.data.target_column], predictions
                    )
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
