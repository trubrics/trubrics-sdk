from typing import Dict, Union

import numpy as np
import pandas as pd

from trubrics.context import DataContext, ModelContext
from trubrics.exceptions import ClassifierNotSupportedError, UnknownEstimatorType
from trubrics.modellers.classifier import Classifier
from trubrics.modellers.regressor import Regressor
from trubrics.validators.validation_output import (
    validation_output,
    validation_output_type,
)


class Validator:
    def __init__(self, data: DataContext, model: ModelContext):
        self.trubrics_model: Union[Classifier, Regressor]
        if model.estimator_type == "classifier":
            self.trubrics_model = Classifier(data=data, model=model)
        elif model.estimator_type == "regressor":
            self.trubrics_model = Regressor(data=data, model=model)
        else:
            UnknownEstimatorType(
                f"Estimator type {model.estimator_type} not supported. Please use a 'regressor' or 'classifier'"
                " estimator."
            )
        self.trubrics_model_type = model.estimator_type
        self.trubrics_model_eval_func = model.evaluation_function
        self.test_data = data.testing_data
        self.features = data.features
        self.target = data.target_column

    @validation_output
    def validate_single_edge_case(self, edge_case_data, desired_output):
        return self._validate_single_edge_case(edge_case_data, desired_output)

    def _validate_single_edge_case(
        self, edge_case_data: Dict[str, Union[str, int, float]], desired_output: Union[int, float]
    ) -> validation_output_type:
        """
        Single edge case validation.
        """
        prediction = self._predict_from_dict(edge_case_data=edge_case_data)
        return prediction == desired_output, {"prediction": prediction}

    @validation_output
    def validate_single_edge_case_in_range(self, edge_case_data, lower_output, upper_output):
        return self._validate_single_edge_case_in_range(edge_case_data, lower_output, upper_output)

    def _validate_single_edge_case_in_range(
        self,
        edge_case_data: Dict[str, Union[str, int, float]],
        lower_output: Union[int, float],
        upper_output: Union[int, float],
    ) -> validation_output_type:
        """
        Single edge case validation in range.
        """
        if lower_output >= upper_output:
            raise ValueError("lower_output must be strictly inferior to upper_output.")
        if self.trubrics_model_type == "classifier":
            raise ClassifierNotSupportedError("Model type 'classifier' not supported for a range output.")
        prediction = self._predict_from_dict(edge_case_data=edge_case_data)

        return prediction > lower_output and prediction < upper_output, {"prediction": prediction}

    @validation_output
    def validate_performance_against_threshold(self, threshold):
        return self._validate_performance_against_threshold(threshold)

    def _validate_performance_against_threshold(self, threshold: float) -> validation_output_type:
        """
        Compares performance of a model on a dataset to a hard coded threshold value.
        """
        performance = self.trubrics_model.compute_performance_on_test_set()

        if self.trubrics_model_eval_func.__name__ == "accuracy_score":
            return bool(performance > threshold), {"performance": performance}
        elif self.trubrics_model_eval_func.__name__ == "mean_squared_error":
            return bool(performance < threshold), {"performance": performance}
        else:
            raise NotImplementedError("The evaluation type is not recognized.")

    @validation_output
    def validate_biased_performance_across_category(self, category, threshold):
        return self._validate_biased_performance_across_category(category, threshold)

    def _validate_biased_performance_across_category(self, category: str, threshold: float) -> validation_output_type:
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
        cat_values = list(self.test_data[category].unique())
        if len(cat_values) > 20:
            raise Exception(f"Cardinality of {len(cat_values)} too high for performance test.")
        if len(cat_values) < 1:
            raise Exception(f"Category '{category}' has a single value.")
        if category not in self.test_data.columns:
            # TODO: check when categorical columns are specified
            raise KeyError(f"Column '{category}' not found in dataset.")
        result: Dict[str, Union[int, float]] = {}
        for value in cat_values:
            if value not in [np.nan, None]:
                if isinstance(value, str):
                    filtered_data = self.test_data.query(f"`{category}`=='{value}'")
                else:
                    filtered_data = self.test_data.query(f"`{category}`=={value}")
                predictions = self.trubrics_model.predict(filtered_data.loc[:, self.features])
                result[value] = float(self.trubrics_model_eval_func(filtered_data[self.target], predictions))
        max_performance_difference = max(result.values()) - min(result.values())

        return max_performance_difference < threshold, {"max_performance_difference": max_performance_difference}

    @validation_output
    def validate_feature_in_top_n_important_features(self, feature, feature_importance, top_n_features):
        return self._validate_feature_in_top_n_important_features(feature, feature_importance, top_n_features)

    @staticmethod
    def _validate_feature_in_top_n_important_features(
        feature: str, feature_importance: Dict[str, float], top_n_features: int
    ) -> validation_output_type:
        """
        Verifies that a given feature is in the top n most important features.
        """
        count = 0
        for importance in feature_importance.values():
            if importance > feature_importance[feature]:
                count += 1

        return count < top_n_features, {"feature_importance_ranking": count}

    def _predict_from_dict(self, edge_case_data: Dict[str, Union[str, int, float]]) -> Union[int, float]:
        edge_case_data_df = pd.DataFrame.from_records(edge_case_data, index=["0"], columns=self.features)
        prediction = self.trubrics_model.predict(data=edge_case_data_df)[
            0
        ].item()  # .item() converts numpy to python type, in order to be serialised to json
        return prediction
