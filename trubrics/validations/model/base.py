from typing import Any, Callable, Dict, Optional, Union

import numpy as np
import pandas as pd
import sklearn.metrics
from loguru import logger

from trubrics.context import DataContext, TrubricsModel
from trubrics.exceptions import EstimatorTypeError, SklearnMetricTypeError
from trubrics.validations.validation_output import (
    validation_output,
    validation_output_type,
)


class ModelValidator:
    def __init__(self, data: DataContext, model: Any, custom_scorers: Optional[Dict[str, Any]] = None):
        self.tm = TrubricsModel(data=data, model=model)
        self.model_type = self.tm.model_type
        self.custom_scorers = custom_scorers

    @validation_output
    def validate_minimum_functionality_in_range(self, range_value=0, range_inclusive=True, severity=None):
        return self._validate_minimum_functionality_in_range(range_value, range_inclusive=range_inclusive)

    def _validate_minimum_functionality_in_range(
        self,
        range_value: Union[int, float] = 0,
        range_inclusive: bool = True,
    ) -> validation_output_type:

        if self.model_type == "classifier":
            EstimatorTypeError(
                "Range parameters may only be applied to regressor model types."
                "Try 'validate_minimum_functionality' validation for classifier model types."
            )

        minimum_functionality_df = self.tm.data.minimum_functionality_data
        if minimum_functionality_df is None:
            raise ValueError("Specify minimum_functionality_data attribute in DataContext.")

        def filter_predictions_not_in_range(minimum_functionality_df, range_value, range_inclusive):
            if range_inclusive:
                return minimum_functionality_df.loc[
                    lambda x: (x["predictions"] >= x[self.tm.data.target] + range_value)
                    | (x["predictions"] <= x[self.tm.data.target] - range_value),
                    :,
                ]
            else:
                return minimum_functionality_df.loc[
                    lambda x: (x["predictions"] > x[self.tm.data.target] + range_value)
                    | (x["predictions"] < x[self.tm.data.target] - range_value),
                    :,
                ]

        minimum_functionality_df["predictions"] = self.tm.predictions_minimum_functionality
        errors_df = filter_predictions_not_in_range(minimum_functionality_df, range_value, range_inclusive)
        return len(errors_df) == 0, {"errors_df": errors_df.to_dict()} if len(errors_df) != 0 else {}

    @validation_output
    def validate_minimum_functionality(self, severity=None):
        return self._validate_minimum_functionality()

    def _validate_minimum_functionality(self) -> validation_output_type:
        if self.model_type == "regressor":
            EstimatorTypeError(
                "Validation may only be applied to classifier model types."
                "Try 'validate_minimum_functionality_in_range' validation for regressor model types."
            )
        minimum_functionality_df = self.tm.data.minimum_functionality_data
        if minimum_functionality_df is None:
            raise Exception("Specify minimum_functionality_data attribute in DataContext.")
        minimum_functionality_df["predictions"] = self.tm.predictions_minimum_functionality
        errors_df = minimum_functionality_df.loc[lambda x: x[self.tm.data.target] != x["predictions"], :]
        return len(errors_df) == 0, {"errors_df": errors_df.to_dict()} if len(errors_df) != 0 else {}

    @validation_output
    def validate_performance_against_threshold(self, metric, threshold, severity=None):
        """For information, refer to the _validate_performance_against_threshold method."""
        return self._validate_performance_against_threshold(metric, threshold)

    def _validate_performance_against_threshold(self, metric: str, threshold: float) -> validation_output_type:
        """Performance validation versus a fixed threshold value.

        Compares performance of a model on the testing dataset to a hard coded threshold value.

        Args:
            threshold: the performance threshold that the model must attain

        Returns:
            True for success, false otherwise. With a results dictionary giving the actual model performance calculated.

        Example:
            ```py
            model_validator = ModelValidator(data=data_context, model=model_context)
            model_validator.validate_performance_against_threshold(threshold=0.8)
            ```
        """
        performance = self._testing_data_score(metric)
        return bool(performance > threshold), {"performance": performance}

    @validation_output
    def validate_biased_performance_across_category(self, metric, category, threshold, severity=None):
        """For information, refer to the _validate_biased_performance_across_category method."""
        return self._validate_biased_performance_across_category(metric, category, threshold)

    def _validate_biased_performance_across_category(
        self, metric, category: str, threshold: float
    ) -> validation_output_type:
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
            model_validator = ModelValidator(data=data_context, model=model_context)
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
        scorer = self._scorer(metric)
        test_data = self.tm.data.testing_data
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
                value = f"'{value}'" if isinstance(value, str) else value
                filtered_data = test_data.query(f"`{category}`=={value}")
                result[value] = scorer(
                    self.tm.model,
                    filtered_data.loc[:, self.tm.data.features],
                    filtered_data[self.tm.data.target],
                )
        max_performance_difference = max(result.values()) - min(result.values())

        return max_performance_difference < threshold, {"max_performance_difference": max_performance_difference}

    @validation_output
    def validate_performance_against_dummy(self, metric, strategy="most_frequent", severity=None):
        return self._validate_performance_against_dummy(metric, strategy)

    def _validate_performance_against_dummy(self, metric, strategy: str) -> validation_output_type:
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
            model_validator = ModelValidator(data=data_context, model=model_context)
            model_validator.model_validator.validate_performance_against_dummy(strategy="stratified")
            ```
        """
        test_performance = self._testing_data_score(metric)
        scorer = self._scorer(metric)
        if self.tm.data.training_data is None:
            raise Exception("In order to train dummy classifier, training_data must be set in the DataContext.")

        from sklearn.dummy import DummyClassifier

        dummy_clf = DummyClassifier(strategy=strategy)
        dummy_clf.fit(self.tm.data.X_train, self.tm.data.y_train)
        dummy_performance = scorer(dummy_clf, self.tm.data.X_test, self.tm.data.y_test)

        return test_performance > dummy_performance, {
            "dummy_performance": dummy_performance,
            "test_performance": test_performance,
        }

    @validation_output
    def validate_feature_in_top_n_important_features(self, feature, feature_importance, top_n_features, severity=None):
        """For information, refer to the _validate_feature_in_top_n_important_features method."""
        return self._validate_feature_in_top_n_important_features(feature, feature_importance, top_n_features)

    @staticmethod
    def _validate_feature_in_top_n_important_features(
        feature: str, feature_importance: Dict[str, float], top_n_features: int
    ) -> validation_output_type:
        """Feature importance validation for top n features.

        Verifies that a given feature is in the top n most important features.

        Args:
            feature: feature to assess
            feature_importance: dictionary of feature importance values
            top_n_features: the number of important features that the named feature must be in e.g. if
                            top_n_features=2, the feature must be within the top two most important features

        Returns:
            True for success, false otherwise. With a results dictionary giving the actual feature importance ranking.

        Example:
            ```py
            model_validator = ModelValidator(data=data_context, model=model_context)
            model_validator.validate_feature_in_top_n_important_features(
                feature="feature_a",
                feature_importance=feature_importance_dict,
                top_n_features=2,
            )
            ```
        """
        count = 0
        for importance in feature_importance.values():
            if importance > feature_importance[feature]:
                count += 1

        return count < top_n_features, {"feature_importance_ranking": count}

    def _predict_from_dict(
        self,
        data: Dict[str, Union[str, int, float]],
        proba_class: Optional[Union[int, str]] = None,
    ) -> Union[int, float]:
        data_df = self._single_dict_to_df(data, self.tm.data.features)
        if proba_class is not None:
            return self._predict_probabilities(data_df)[proba_class][0]
        return self.tm.model.predict(data_df)[0]

    def _predict_probabilities(self, data: pd.DataFrame) -> Dict[Union[int, str], pd.Series]:
        probabilities = {}
        for _class, _proba in zip(self.tm.model.classes_, self.tm.model.predict_proba(data).T):
            probabilities[_class] = _proba
        return probabilities

    def _scorer(self, metric: str) -> Callable[[Any, pd.DataFrame, pd.Series], float]:
        if metric in sklearn.metrics.SCORERS:
            scorer = sklearn.metrics.SCORERS[metric]
        else:
            if self.custom_scorers is not None and metric in self.custom_scorers:
                scorer = self.custom_scorers[metric]
            else:
                raise SklearnMetricTypeError(
                    f"The metric '{metric}' is not part of scikit-learns scorers, nor is it defined as a custom scorer"
                    " in the custom_scorers attribute. Run `sklearn.metrics.SCORERS` to list default scorers, or input"
                    " your custom scorer to the ModelValidator."
                )
        return scorer

    def _testing_data_score(self, metric: str) -> float:
        scorer = self._scorer(metric)
        return scorer(self.tm.model, self.tm.data.X_test, self.tm.data.y_test)

    def _is_sample_in_data_context(self, sample: pd.DataFrame):
        """
        Verify if some combination of features is present in either the testing or training data.
        """

        def is_sample_in_df(sample, df):
            return len(pd.concat([sample, df]).drop_duplicates()) == len(df)

        if is_sample_in_df(sample, self.tm.data.X_test):
            logger.warning("Sample data is present in testing data.")

        if self.tm.data.X_train and is_sample_in_df(sample, self.tm.data.X_train):
            logger.warning("Sample data is present in testing data.")

    @staticmethod
    def _single_dict_to_df(_dict, columns):
        if set(_dict) != set(columns):
            raise Exception("Input data and data context have different schemas.")
        return pd.DataFrame.from_records(_dict, index=["0"], columns=columns)
