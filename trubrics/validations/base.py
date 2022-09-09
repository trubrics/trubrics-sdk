from typing import Any, Dict, Union

import numpy as np
import pandas as pd

from trubrics.context import DataContext, TrubricsModel
from trubrics.validations.validation_output import (
    validation_output,
    validation_output_type,
)


class Validator:
    def __init__(self, data: DataContext, model: Any, metric: str):
        self.metric = metric
        self.trubrics_model = TrubricsModel(metric=metric, data=data, model=model)
        self.model_type = self.trubrics_model.model_type
        self.score_test = self.trubrics_model.score_test
        self.scorer: Any = self.trubrics_model.scorer

    @validation_output
    def validate_single_edge_case(self, edge_case_data, desired_output):
        """For information, refer to the _validate_single_edge_case method."""
        return self._validate_single_edge_case(edge_case_data, desired_output)

    def _validate_single_edge_case(
        self, edge_case_data: Dict[str, Union[str, int, float]], desired_output: Union[int, float]
    ) -> validation_output_type:
        """Single edge case validation.

        Validate that a combination of features (all features must be defined) input to a model
        result in an exact prediction value. This validation can be used to highlight edge cases
        that a model must respect. It is often used to validate classification models.

        Args:
            edge_case_data: ensemble of all feature values
            desired_output: expected prediction

        Returns:
            True for success, false otherwise. With a results dictionary giving the actual prediction result.

        Example:
            ```py
            model_validator = Validator(data=data_context, model=model_context)
            model_validator.validate_single_edge_case(
                edge_case_data={'feature_a': 1, 'feature_b': 3},
                desired_output=0
            )
            ```
        """
        prediction = self._predict_from_dict(edge_case_data=edge_case_data)
        return prediction == desired_output, {"prediction": prediction}

    # @validation_output
    # def validate_single_edge_case_in_range(self, edge_case_data, lower_output, upper_output):
    #     """For information, refer to the _validate_single_edge_case_in_range method."""
    #     return self._validate_single_edge_case_in_range(edge_case_data, lower_output, upper_output)

    # def _validate_single_edge_case_in_range(
    #     self,
    #     edge_case_data: Dict[str, Union[str, int, float]],
    #     lower_output: Union[int, float],
    #     upper_output: Union[int, float],
    # ) -> validation_output_type:
    #     """Single edge case validation in range.

    #     Validate that a combination of features (all features must be defined) input to a model
    #     result in a range of prediction values. This validation can be used to highlight edge cases
    #     that a model must respect. It is only possible to use on regression models.

    #     Args:
    #         edge_case_data: ensemble of all feature values
    #         lower_output: minimum prediction value to be expected
    #         upper_output: maximum prediction value to be expected

    #     Returns:
    #         True for success, false otherwise. With a results dictionary giving the actual prediction result.

    #     Example:
    #         ```py
    #         model_validator = Validator(data=data_context, model=model_context)
    #         model_validator.validate_single_edge_case_in_range(
    #             edge_case_data={'feature_a': 1, 'feature_b': 3},
    #             lower_output=120,
    #             upper_output=140,
    #         )
    #         ```
    #     """
    #     if lower_output >= upper_output:
    #         raise ValueError("lower_output must be strictly inferior to upper_output.")
    #     if self.trubrics_model_type == "classifier":
    #         raise ClassifierNotSupportedError("Model type 'classifier' not supported for a range output.")
    #     prediction = self._predict_from_dict(edge_case_data=edge_case_data)

    #     return prediction > lower_output and prediction < upper_output, {"prediction": prediction}

    @validation_output
    def validate_performance_against_threshold(self, threshold):
        """For information, refer to the _validate_performance_against_threshold method."""
        return self._validate_performance_against_threshold(threshold)

    def _validate_performance_against_threshold(self, threshold: float) -> validation_output_type:
        """Performance validation versus a fixed threshold value.

        Compares performance of a model on the testing dataset to a hard coded threshold value.

        Args:
            threshold: the performance threshold that the model must attain

        Returns:
            True for success, false otherwise. With a results dictionary giving the actual model performance calculated.

        Example:
            ```py
            model_validator = Validator(data=data_context, model=model_context)
            model_validator.validate_performance_against_threshold(threshold=0.8)
            ```
        """
        return bool(self.score_test < threshold), {"performance": self.score_test}

    @validation_output
    def validate_biased_performance_across_category(self, category, threshold):
        """For information, refer to the _validate_biased_performance_across_category method."""
        return self._validate_biased_performance_across_category(category, threshold)

    def _validate_biased_performance_across_category(self, category: str, threshold: float) -> validation_output_type:
        """Biased performance validation on a category.

        Calculates various performance for all values in a category and validates for
        the maximum difference in performance inferior to the threshold value.

        Args:
            category: categorical feature to split data on
            threshold: maximum difference in performance

        Returns:
            True for success, false otherwise. With a results dictionary giving the maximum performance difference.

        Example:
            ```py
            model_validator = Validator(data=data_context, model=model_context)
            model_validator.validate_biased_performance_across_category(category="feature_a", threshold=0.05)
            ```

        TODO:
            - More complex threshold function
            - Modify cardinality

            To add to output report:

            - Performance across all category values
            - Show distributions of category variables
            - Performance plots of results
        """
        test_data = self.trubrics_model.data.X_test
        cat_values = list(test_data[category].unique())
        if len(cat_values) > 20:
            raise Exception(f"Cardinality of {len(cat_values)} too high for performance test.")
        if len(cat_values) < 1:
            raise Exception(f"Category '{category}' has a single value.")
        if category not in test_data.columns:
            # TODO: check when categorical columns are specified
            raise KeyError(f"Column '{category}' not found in dataset.")
        result: Dict[str, Union[int, float]] = {}
        for value in cat_values:
            if value not in [np.nan, None]:
                if isinstance(value, str):
                    filtered_data = self.trubrics_model.data.testing_data.query(f"`{category}`=='{value}'")
                else:
                    filtered_data = test_data.query(f"`{category}`=={value}")

                result[value] = self.scorer(
                    self.trubrics_model.model,
                    filtered_data.loc[:, self.trubrics_model.data.features],
                    filtered_data[self.trubrics_model.data.target_column],
                )
        max_performance_difference = max(result.values()) - min(result.values())

        return max_performance_difference < threshold, {"max_performance_difference": max_performance_difference}

    @validation_output
    def validate_performance_against_dummy(self, strategy="most_frequent"):
        return self._validate_performance_against_dummy(strategy)

    def _validate_performance_against_dummy(self, strategy: str = "most_frequent") -> validation_output_type:
        """Performance validation versus a dummy baseline model.

        Trains a DummyClassifier / DummyRegressor from sklearn and compares performance against the model.

        Args:
            strategy: see scikit-learns dummy models -\
            https://scikit-learn.org/stable/modules/classes.html?highlight=dummy#module-sklearn.dummy

        Returns:
            True for success, false otherwise. With a results dictionary giving the model's\
            actual performance on the test set and the dummy model's performance.

        Example:
            ```py
            model_validator = Validator(data=data_context, model=model_context)
            model_validator.model_validator.validate_performance_against_dummy(strategy="stratified")
            ```
        """
        if self.trubrics_model.data.training_data is None:
            raise Exception("In order to train dummy classifier, training_data must be set in the DataContext.")

        from sklearn.dummy import DummyClassifier

        dummy_clf = DummyClassifier(strategy=strategy)
        dummy_clf.fit(self.trubrics_model.data.X_train, self.trubrics_model.data.y_train)
        dummy_performance = self.scorer(dummy_clf, self.trubrics_model.data.X_test, self.trubrics_model.data.y_test)

        return self.score_test > dummy_performance, {
            "dummy_performance": dummy_performance,
            "test_performance": self.score_test,
        }

    # @validation_output
    # def validate_feature_in_top_n_important_features(self, feature, feature_importance, top_n_features):
    #     """For information, refer to the _validate_feature_in_top_n_important_features method."""
    #     return self._validate_feature_in_top_n_important_features(feature, feature_importance, top_n_features)

    # @staticmethod
    # def _validate_feature_in_top_n_important_features(
    #     feature: str, feature_importance: Dict[str, float], top_n_features: int
    # ) -> validation_output_type:
    #     """Feature importance validation for top n features.

    #     Verifies that a given feature is in the top n most important features.

    #     Args:
    #         feature: feature to assess
    #         feature_importance: dictionary of feature importance values
    #         top_n_features: the number of important features that the named feature must be in e.g. if
    #                         top_n_features=2, the feature must be within the top two most important features

    #     Returns:
    #         True for success, false otherwise. With a results dictionary giving the actual feature importance ranking.

    #     Example:
    #         ```py
    #         model_validator = Validator(data=data_context, model=model_context)
    #         model_validator.validate_feature_in_top_n_important_features(
    #             feature="feature_a",
    #             feature_importance=feature_importance_dict,
    #             top_n_features=2,
    #         )
    #         ```
    #     """
    #     count = 0
    #     for importance in feature_importance.values():
    #         if importance > feature_importance[feature]:
    #             count += 1

    #     return count < top_n_features, {"feature_importance_ranking": count}

    def _predict_from_dict(self, edge_case_data: Dict[str, Union[str, int, float]]) -> Union[int, float]:
        edge_case_data_df = pd.DataFrame.from_records(
            edge_case_data, index=["0"], columns=self.trubrics_model.data.features
        )
        prediction = self.trubrics_model.model.predict(edge_case_data_df)[0]
        return prediction
